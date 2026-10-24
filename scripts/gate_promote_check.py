#!/usr/bin/env python3
"""Authoring loop gate (AUTHORING.md §5).

A source document is finished only when all of these hold:
  * it is not a `status: pending` / `[Content pending]` stub,
  * it is not an unexpanded `fetch_drafts.py` skeleton,
  * the same relative path exists in both en and ko and both are finished,
  * (for new files and for promotions out of stub/draft) frontmatter, body,
    tags and links pass the §5.3 checks.

This is the single "am I done?" command for the authoring loop. A stub or a
`--write` draft is step 1 or 2 of 4, never a deliverable.

Usage:
  python3 scripts/gate_promote_check.py              # full audit
  python3 scripts/gate_promote_check.py --next       # print the next 1 item
  python3 scripts/gate_promote_check.py --next --worktree  # next touched file
  python3 scripts/gate_promote_check.py --worktree   # current edits (agent loop)
  python3 scripts/gate_promote_check.py --staged     # pre-commit hook
  python3 scripts/gate_promote_check.py --changed    # pre-push / CI
  python3 scripts/gate_promote_check.py --strict     # legacy warnings -> errors
  python3 scripts/gate_promote_check.py --json       # machine-readable

Exit codes:
  0  no blocking issue
  1  blocking issue remains
  2  usage / git error
"""
from __future__ import annotations

import argparse
import difflib
import glob
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
LANGS = ("en", "ko")
STUB_MARK = "[Content pending]"
DRAFT_MARKS = (
    "Draft summary auto-extracted",
    "RAW DRAFT",
    "Summary pending human review.",
)
DATE_KEYS = ("published_date", "published")
PRIORITY = {
    "stub": 0,
    "draft": 1,
    "body-short": 2,
    "h1-missing": 3,
    "pair-incomplete": 4,
    "ko-missing": 5,
    "en-missing": 5,
    "missing-key": 6,
    "missing-date": 6,
    "bad-locale": 7,
    "bad-tags": 7,
    "duplicate-tags": 8,
    "bad-source-url": 8,
    "placeholder-description": 8,
    "h1-mismatch": 9,
    "paper-filename": 9,
    "ko-body-en": 9,
    "ko-copy": 9,
    "en-body-ko": 10,
}


@dataclass
class Issue:
    severity: str  # "error" | "warn"
    code: str
    rel: str
    message: str
    state: str = ""

    def as_dict(self) -> dict:
        return {
            "severity": self.severity,
            "code": self.code,
            "path": self.rel,
            "message": self.message,
            "state": self.state,
        }


@dataclass
class Doc:
    path: str
    rel: str
    lang: str
    kind: str
    text: str
    fm: str
    body: str
    state: str
    issues: list[Issue] = field(default_factory=list)


def split_doc(text: str) -> tuple[str, str]:
    if text.startswith("---"):
        m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?(.*)$", text, re.S)
        if m:
            return m.group(1), m.group(2)
    return "", text


def fm_value(fm: str, key: str) -> str:
    m = re.search(r"^%s:\s*(.*)$" % re.escape(key), fm, re.M)
    return unquote(m.group(1).strip()) if m else ""


def unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        return value[1:-1].replace('\\"', '"')
    return value


def tag_list(fm: str) -> list[str]:
    raw = fm_value(fm, "tags").strip()
    if raw.startswith("[") and raw.endswith("]"):
        raw = raw[1:-1]
    return [t.strip().strip("'\"") for t in raw.split(",") if t.strip()]


def detect_state(text: str, fm: str) -> str:
    head = text[:4000]
    if re.search(r"^status:\s*pending\s*$", fm, re.M) or STUB_MARK in head:
        return "stub"
    if any(mark in text for mark in DRAFT_MARKS):
        return "draft"
    return "ok"


def make_doc(path: str, text: str) -> Doc:
    fm, body = split_doc(text)
    rel = os.path.relpath(path, CONTENT)
    parts = rel.split(os.sep)
    lang = parts[0] if len(parts) > 1 else ""
    kind = parts[2] if len(parts) > 3 and parts[1] == "sources" else "sources"
    return Doc(path, rel, lang, kind, text, fm, body, detect_state(text, fm))


def load_doc(path: str) -> Doc:
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    return make_doc(path, text)


def all_docs() -> dict[str, Doc]:
    docs: dict[str, Doc] = {}
    for lang in LANGS:
        pattern = os.path.join(CONTENT, lang, "sources", "**", "*.md")
        for path in sorted(glob.glob(pattern, recursive=True)):
            doc = load_doc(path)
            docs[doc.rel] = doc
    return docs


def _batch_read(specs: list[str]) -> list[str | None]:
    """Read many blobs in one `git cat-file --batch` call."""
    if not specs:
        return []
    proc = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=ROOT,
        input=("\n".join(specs) + "\n").encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    data = proc.stdout
    out: list[str | None] = []
    pos = 0
    for _spec in specs:
        nl = data.find(b"\n", pos)
        if nl < 0:
            out.append(None)
            break
        header = data[pos:nl].decode("utf-8", "replace")
        parts = header.split()
        if len(parts) < 3 or parts[-1] == "missing":
            out.append(None)
            pos = nl + 1
            continue
        size = int(parts[2])
        blob = data[nl + 1:nl + 1 + size]
        out.append(blob.decode("utf-8", "replace"))
        pos = nl + 1 + size + 1
    while len(out) < len(specs):
        out.append(None)
    return out


def docs_from_git(rev: str) -> dict[str, Doc]:
    """Documents exactly as they exist in the index (`:`) or a commit."""
    if rev == ":":
        ok, out = _git(["ls-files", "-z", "--", "content"])
    else:
        ok, out = _git(["ls-tree", "-r", "-z", "--name-only", rev, "--", "content"])
    if not ok:
        return {}
    paths = [p for p in out.split("\0")
             if p.endswith(".md") and "/sources/" in p]
    specs = [(":" if rev == ":" else rev + ":") + p for p in paths]
    blobs = _batch_read(specs)
    docs: dict[str, Doc] = {}
    for path, text in zip(paths, blobs):
        if text is None:
            continue
        doc = make_doc(os.path.join(ROOT, path), text)
        docs[doc.rel] = doc
    return docs


def counterpart(docs: dict[str, Doc], doc: Doc) -> tuple[str, Doc | None]:
    other_lang = "ko" if doc.lang == "en" else "en"
    rel = os.path.join(other_lang, *doc.rel.split(os.sep)[1:])
    return rel, docs.get(rel)


def _issue(severity: str, code: str, doc: Doc, message: str) -> Issue:
    return Issue(severity, code, doc.rel, message, doc.state)


def evaluate(doc: Doc, docs: dict[str, Doc], status: str | None, strict: bool,
             prev_state: str | None = None) -> list[Issue]:
    """status: "A" added, "M" modified, "D" deleted, None = full audit.

    Frontmatter policy is enforced for new files and for files that were a
    stub/draft in the previous revision (a promotion), not for every legacy
    file that merely gets a typo fix. `--strict` audits everything.
    """
    out: list[Issue] = []
    promotion = prev_state in ("stub", "draft")
    policy = strict or status == "A" or promotion
    pair_strict = status == "A" or promotion or strict

    if doc.state == "stub":
        out.append(_issue("error", "stub", doc,
                          "status: pending / [Content pending] remains"))
        return out
    if doc.state == "draft":
        out.append(_issue("error", "draft", doc,
                          "fetch_drafts skeleton not expanded "
                          "(Draft summary auto-extracted / RAW DRAFT)"))
        return out

    body = doc.body.strip()
    if len(body) < 300:
        out.append(_issue("error", "body-short", doc,
                          f"body is {len(body)} chars (<300)"))
    if not re.search(r"^#\s+", doc.body, re.M):
        out.append(_issue("error", "h1-missing", doc, "body has no H1"))

    # en/ko pair ---------------------------------------------------------
    other_rel, other = counterpart(docs, doc)
    if other is None:
        if doc.lang == "en":
            out.append(_issue("error" if pair_strict else "warn", "ko-missing", doc,
                              f"no translated pair: content/{other_rel}"))
        else:
            out.append(_issue("error" if pair_strict else "warn", "en-missing", doc,
                              f"no English pair: content/{other_rel}"))
    elif doc.state == "ok" and other.state != "ok":
        out.append(_issue("error" if pair_strict else "warn",
                          "pair-incomplete", doc,
                          f"pair is still {other.state}: content/{other_rel}"))

    if not policy:
        return out

    # frontmatter / body policy (blocking for new files and promotions) ----
    for key in ("title", "description", "tags", "locale", "source_url"):
        if not fm_value(doc.fm, key):
            out.append(_issue("error", "missing-key", doc, f"missing frontmatter: {key}"))
    if not any(fm_value(doc.fm, key) for key in DATE_KEYS):
        out.append(_issue("error", "missing-date", doc,
                          "need published or published_date (YYYY-MM-DD)"))
    elif len(fm_value(doc.fm, "published_date") or fm_value(doc.fm, "published")) < 8:
        out.append(_issue("error", "missing-date", doc,
                          "date is not YYYY-MM-DD"))

    locale = fm_value(doc.fm, "locale")
    if locale != doc.lang:
        out.append(_issue("error", "bad-locale", doc,
                          f"locale: {locale or '(missing)'} (expected {doc.lang})"))

    tags = tag_list(doc.fm)
    if not tags:
        out.append(_issue("error", "bad-tags", doc, "tags is empty"))
    else:
        if tags[-1] != doc.lang:
            out.append(_issue("error", "bad-tags", doc,
                              f"last tag must be {doc.lang}: {tags}"))
        if len(tags) != len(set(tags)):
            out.append(_issue("error", "duplicate-tags", doc, f"duplicate tags: {tags}"))

    source_url = fm_value(doc.fm, "source_url")
    if source_url and not source_url.startswith(("http://", "https://")):
        out.append(_issue("error", "bad-source-url", doc, source_url[:80]))

    desc = fm_value(doc.fm, "description")
    if desc.startswith("[Content pending]") or desc.startswith("en/sources/"):
        out.append(_issue("error", "placeholder-description", doc, desc[:80]))

    title = fm_value(doc.fm, "title")
    h1 = re.search(r"^#\s+(.*)$", doc.body, re.M)
    if h1 and title and h1.group(1).strip() != title:
        out.append(_issue("error", "h1-mismatch", doc,
                          f"H1 != title ({h1.group(1).strip()[:50]!r})"))

    if doc.kind == "papers":
        for key in ("arxiv_id", "authors", "blog"):
            if not fm_value(doc.fm, key):
                out.append(_issue("error", "missing-key", doc,
                                  f"paper missing frontmatter: {key}"))
        name = os.path.basename(doc.path)
        if not re.fullmatch(r"\d{4}-\d{4,5}\.md", name):
            out.append(_issue("error", "paper-filename", doc,
                              f"paper filename is not an arXiv id: {name}"))
    elif doc.kind == "articles":
        if not fm_value(doc.fm, "blog"):
            out.append(_issue("error", "missing-key", doc,
                              "article missing frontmatter: blog"))

    hangul = len(re.findall(r"[\uac00-\ud7a3]", doc.body))
    latin = len(re.findall(r"[A-Za-z]", doc.body))
    if doc.lang == "ko" and hangul < 50:
        out.append(_issue("error", "ko-body-en", doc,
                          f"Korean body has only {hangul} Hangul chars"))
    if doc.lang == "en" and hangul > 100 and hangul > latin:
        out.append(_issue("warn", "en-body-ko", doc,
                          f"English doc looks Korean ({hangul} Hangul > {latin} Latin)"))

    if doc.lang == "ko" and other is not None:
        en_body = other.body.strip()
        if len(en_body) > 300 and len(body) > 300:
            ratio = difflib.SequenceMatcher(None, en_body[:4000], body[:4000]).ratio()
            if ratio > 0.9:
                out.append(_issue("error", "ko-copy", doc,
                                  f"Korean body copies English ({ratio:.2f})"))
    return out


def _git(args: list[str]) -> tuple[bool, str]:
    proc = subprocess.run(["git", *args], cwd=ROOT, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode == 0, proc.stdout if proc.returncode == 0 else proc.stderr


def _content_md(path: str) -> bool:
    path = path.replace("\\", "/")
    return path.startswith("content/") and path.endswith(".md")


def _norm_git_path(path: str) -> str:
    """git prints paths relative to the repo root: content/en/..."""
    return os.path.relpath(os.path.join(ROOT, path), CONTENT)


def changes_staged() -> list[tuple[str, str]]:
    """(status, content-relative path) for the staged index vs HEAD."""
    entries: list[tuple[str, str]] = []
    ok, out = _git(["diff", "--cached", "--name-status", "--find-renames", "--no-ext-diff"])
    if not ok:
        return entries
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        status = parts[0][0]
        if status == "R" and len(parts) >= 3:
            if _content_md(parts[1]):
                entries.append(("D", _norm_git_path(parts[1])))
            if _content_md(parts[2]):
                entries.append(("A", _norm_git_path(parts[2])))
        elif _content_md(parts[-1]):
            entries.append((status, _norm_git_path(parts[-1])))
    return entries


def untracked_paths() -> list[str]:
    ok, out = _git(["ls-files", "--others", "--exclude-standard", "--", "content"])
    if not ok:
        return []
    return [_norm_git_path(p) for p in out.splitlines()
            if _content_md(p) and "/sources/" in p]


def changes_worktree() -> list[tuple[str, str]]:
    """(status, content-relative path) for everything touched in the worktree.

    Includes staged, unstaged, and untracked files. Used by `--next --worktree`
    so an agent sees the batch it just created, not the legacy backlog.
    """
    ok, out = _git(["status", "--porcelain=v1", "-z",
                    "--untracked-files=all", "--", "content"])
    if not ok:
        return []
    fields = out.split("\0")
    entries: list[tuple[str, str]] = []
    i = 0
    while i < len(fields):
        entry = fields[i]
        i += 1
        if not entry or len(entry) < 4:
            continue
        xy, path = entry[:2], entry[3:]
        if "R" in xy or "C" in xy:
            old = fields[i] if i < len(fields) else ""
            i += 1
            if old and _content_md(old):
                entries.append(("D", _norm_git_path(old)))
        if not _content_md(path):
            continue
        if "D" in xy:
            status = "D"
        elif xy == "??" or "A" in xy or "R" in xy or "C" in xy:
            status = "A"
        else:
            status = "M"
        entries.append((status, _norm_git_path(path)))
    return entries


def changes_since(base: str) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    ok, out = _git(["diff", "--name-status", "--find-renames",
                    f"{base}...HEAD", "--no-ext-diff"])
    if not ok:
        # Unknown base (fresh clone, first push): fall back to the last commit.
        ok, out = _git(["diff-tree", "--no-commit-id", "--name-status",
                        "-r", "--find-renames", "HEAD"])
    if ok:
        for line in out.splitlines():
            parts = line.split("\t")
            if len(parts) < 2:
                continue
            status = parts[0][0]
            if status == "R" and len(parts) >= 3:
                if _content_md(parts[1]):
                    entries.append(("D", _norm_git_path(parts[1])))
                if _content_md(parts[2]):
                    entries.append(("A", _norm_git_path(parts[2])))
            elif _content_md(parts[-1]):
                entries.append((status, _norm_git_path(parts[-1])))
    return entries


def previous_states(changes: list[tuple[str, str]], rev: str | None) -> dict[str, str]:
    states: dict[str, str] = {}
    if not rev:
        return states
    for status, rel in changes:
        if status == "D":
            continue
        ok, out = _git(["show", f"{rev}:content/{rel}"])
        if ok:
            fm, _body = split_doc(out)
            states[rel] = detect_state(out, fm)
    return states


def audit(docs: dict[str, Doc], changes: list[tuple[str, str]] | None,
          strict: bool, prev: dict[str, str] | None = None) -> list[Issue]:
    issues: list[Issue] = []
    if changes is None:
        for doc in docs.values():
            issues.extend(evaluate(doc, docs, None, strict))
        return issues

    prev = prev or {}
    seen: set[tuple[str, str]] = set()
    for status, rel in changes:
        key = (status, rel)
        if key in seen:
            continue
        seen.add(key)
        if status == "D":
            other_lang = "ko" if rel.startswith("en" + os.sep) else "en"
            other_rel = os.path.join(other_lang, *rel.split(os.sep)[1:])
            if other_rel in docs:
                issues.append(Issue("error", "pair-incomplete", rel,
                                    f"{other_lang} pair remains after deletion"))
            continue
        doc = docs.get(rel)
        if doc is None:
            continue
        issues.extend(evaluate(doc, docs, status, strict, prev.get(rel)))
    return issues


def sort_issues(issues: list[Issue]) -> list[Issue]:
    return sorted(issues, key=lambda i: (PRIORITY.get(i.code, 99), i.rel))


def summarize(docs: dict[str, Doc], issues: list[Issue]) -> dict:
    blocking = [i for i in issues if i.severity == "error"]
    warnings = [i for i in issues if i.severity == "warn"]
    by_code: dict[str, int] = {}
    for issue in blocking:
        by_code[issue.code] = by_code.get(issue.code, 0) + 1
    return {
        "docs": len(docs),
        "blocking": len(blocking),
        "warnings": len(warnings),
        "by_code": by_code,
        "states": {
            "stub": sum(1 for d in docs.values() if d.state == "stub"),
            "draft": sum(1 for d in docs.values() if d.state == "draft"),
            "ok": sum(1 for d in docs.values() if d.state == "ok"),
        },
    }


def source_of(doc: Doc | None) -> str:
    if doc is None:
        return ""
    url = fm_value(doc.fm, "source_url")
    if url:
        return url
    m = re.search(r"https?://[^\s)>\"']+", doc.body)
    return m.group(0) if m else ""


def next_item(docs: dict[str, Doc], issues: list[Issue]) -> dict | None:
    for issue in sort_issues(issues):
        if issue.severity != "error" and issue.code not in ("ko-missing", "en-missing"):
            continue
        doc = docs.get(issue.rel)
        if doc is None:
            continue
        item = {
            "path": os.path.join("content", doc.rel),
            "state": doc.state,
            "code": issue.code,
            "message": issue.message,
            "source_url": source_of(doc),
            "kind": doc.kind,
            "lang": doc.lang,
        }
        steps: list[str] = []
        if issue.code == "stub":
            if doc.lang == "ko":
                steps.append(
                    "write the en pair first (AUTHORING.md §5.3), then translate "
                    "it into %s; do not fetch a ko stub" % item["path"])
            elif doc.fm:
                steps.append(
                    "python3 scripts/fetch_drafts.py --kind %s --lang en "
                    "--only 'content/%s' --limit 1 --write" % (doc.kind, doc.rel))
            else:
                steps.append(
                    "manual: this stub has no frontmatter; create the frontmatter "
                    "from AUTHORING.md §2, then write the body")
            if doc.lang == "en":
                steps.append(
                    "expand the draft, add topic tags, then translate it into the "
                    "ko pair (AUTHORING.md §5.3)")
        elif issue.code == "draft":
            if doc.lang == "en":
                steps.append(
                    "open %s and replace the auto-extracted skeleton with a real "
                    "summary (AUTHORING.md §5.3.1)" % item["path"])
                steps.append(
                    "then translate it into content/ko/%s" %
                    os.path.join(*doc.rel.split(os.sep)[1:]))
            else:
                steps.append(
                    "finish the en pair first: content/en/%s" %
                    os.path.join(*doc.rel.split(os.sep)[1:]))
                steps.append(
                    "then rewrite %s in Korean from that finished en doc" %
                    item["path"])
        elif issue.code == "ko-missing":
            steps.append(
                "translate the finished en doc into content/ko/%s "
                "(same frontmatter, tags end with ko)" %
                os.path.join(*doc.rel.split(os.sep)[1:]))
        elif issue.code == "en-missing":
            steps.append(
                "write the English pair at content/en/%s" %
                os.path.join(*doc.rel.split(os.sep)[1:]))
        elif issue.code == "pair-incomplete":
            other = "ko" if doc.lang == "en" else "en"
            steps.append(
                "finish the %s pair of %s (it is still a stub/draft)" %
                (other, item["path"]))
        else:
            steps.append("fix %s in %s" % (issue.message, item["path"]))
        if issue.code != "ko-missing":
            steps.append(
                "re-run: python3 scripts/gate_promote_check.py --next")
        item["steps"] = steps
        return item
    return None


def print_issue(issue: Issue) -> None:
    label = "BLOCKED" if issue.severity == "error" else "WARN   "
    print("%s %-16s %s -- %s" % (label, issue.code, issue.rel, issue.message))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--staged", action="store_true",
                      help="check the index only (pre-commit)")
    mode.add_argument("--changed", action="store_true",
                      help="check the committed tree since --base (pre-push/CI)")
    mode.add_argument("--worktree", action="store_true",
                      help="check staged + unstaged + untracked edits (agent loop)")
    ap.add_argument("--next", action="store_true",
                    help="print the next single item to work on (combine with "
                         "--worktree for the current batch)")
    ap.add_argument("--base", default="origin/main",
                    help="base rev for --changed (default: origin/main)")
    ap.add_argument("--strict", action="store_true",
                    help="treat legacy warnings as blocking")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--quiet", action="store_true",
                    help="print blocking lines only")
    args = ap.parse_args()

    docs = all_docs()
    changes: list[tuple[str, str]] | None = None
    untracked: list[str] = []
    prev: dict[str, str] = {}

    if args.staged:
        # Audit the index, not the worktree: an untracked ko file must not
        # make a staged en-only commit look complete.
        docs = docs_from_git(":")
        changes = changes_staged()
        untracked = untracked_paths()
        if changes:
            prev = previous_states(changes, "HEAD")
        if not changes and not untracked and not args.next:
            if args.json:
                print(json.dumps({"mode": "staged", "blocking": 0,
                                  "warnings": 0, "issues": []}, ensure_ascii=False))
            elif not args.quiet:
                print("Gate: OK — no source changes staged")
            return 0
    elif args.changed:
        # Audit the committed tree that is about to be pushed.
        docs = docs_from_git("HEAD")
        changes = changes_since(args.base)
        rev = args.base if _git(["rev-parse", "--verify", "--quiet", args.base])[0] else None
        if rev is None and _git(["rev-parse", "--verify", "--quiet", "HEAD~1"])[0]:
            rev = "HEAD~1"
        prev = previous_states(changes, rev)
    elif args.worktree:
        # The agent loop: whatever was touched in this session, staged or not.
        docs = all_docs()
        changes = changes_worktree()
        prev = previous_states(changes, "HEAD")

    if not docs:
        print("gate: no source documents found under content/*/sources/",
              file=sys.stderr)
        return 2

    issues = audit(docs, changes, args.strict, prev)
    # Untracked files cannot be committed, but leaving one behind is the
    # "created a stub and stopped" failure mode. Check each against the index.
    for rel in untracked:
        path = os.path.join(CONTENT, rel)
        if os.path.exists(path):
            issues.extend(evaluate(load_doc(path), docs, "A", args.strict))
    stats = summarize(docs, issues)
    blocking = [i for i in issues if i.severity == "error"]

    if args.next:
        nxt = next_item(docs, issues)
        if args.json:
            print(json.dumps({"done": nxt is None, "next": nxt, **stats},
                             ensure_ascii=False, indent=1))
        elif nxt is None:
            scope = ("this batch" if args.staged or args.changed or args.worktree
                     else "the repository")
            print("Gate: DONE — no blocking work in %s "
                  "(%d docs, %d warning(s))" %
                  (scope, stats["docs"], stats["warnings"]))
            if scope == "this batch":
                print("  full backlog: python3 scripts/gate_promote_check.py --next")
        else:
            print("NEXT: %s" % nxt["path"])
            print("  state: %s" % nxt["state"])
            print("  issue: %s — %s" % (nxt["code"], nxt["message"]))
            if nxt["source_url"]:
                print("  source: %s" % nxt["source_url"])
            print("  do:")
            for step in nxt["steps"]:
                print("    - %s" % step)
            print("\nBlocking items left: %d" % stats["blocking"])
        return 0

    if args.json:
        mode_name = ("staged" if args.staged else
                     "changed" if args.changed else
                     "worktree" if args.worktree else "full")
        print(json.dumps({"mode": mode_name, **stats,
                          "issues": [i.as_dict() for i in issues]},
                         ensure_ascii=False, indent=1))
    elif not args.quiet:
        for issue in sort_issues(issues):
            if issue.severity == "error":
                print_issue(issue)
        warn_shown = 0
        for issue in sort_issues(issues):
            if issue.severity == "warn":
                if warn_shown >= 12:
                    remaining = sum(1 for i in issues if i.severity == "warn") - 12
                    print("WARN    ... and %d more warning(s)" % remaining)
                    break
                print_issue(issue)
                warn_shown += 1
        print()
        print("Summary: %d blocking (%s), %d warning(s); "
              "repo stubs=%d drafts=%d complete=%d" % (
                  stats["blocking"],
                  ", ".join("%s=%d" % kv for kv in sorted(stats["by_code"].items()))
                  or "none",
                  stats["warnings"],
                  stats["states"]["stub"], stats["states"]["draft"],
                  stats["states"]["ok"]))
        if stats["blocking"]:
            print("Gate: FAIL — a stub/draft is not a deliverable; "
                  "run `python3 scripts/gate_promote_check.py --next`")
        else:
            print("Gate: OK")
    else:
        for issue in blocking:
            print_issue(issue)

    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
