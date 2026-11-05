"""Audit content quality for emeraldgoose/wiki.

Usage:
  python3 scripts/audit_content_quality.py --scope all
  python3 scripts/audit_content_quality.py --scope worktree
  python3 scripts/audit_content_quality.py --scope worktree --json

Scopes:
  all       audit every source document in content/{en,ko}/sources
  worktree  audit only files touched in the worktree (staged+unstaged+untracked)
"""
import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)
import gate_promote_check as g  # noqa: E402

DATE_KEYS = ("published_date", "published")


def tag_list(fm):
    raw = g.fm_value(fm, "tags").strip()
    if raw.startswith("[") and raw.endswith("]"):
        raw = raw[1:-1]
    return [t.strip().strip("\"'") for t in raw.split(",") if t.strip()]


def audit_doc(doc, all_docs):
    out = []
    body = doc.body
    # state issues
    if doc.state == "stub":
        out.append(g.Issue("error", "stub", doc.rel, "status: pending / [Content pending] remains"))
    if doc.state == "draft":
        out.append(g.Issue("error", "draft", doc.rel, "fetch_drafts skeleton not expanded"))
    # structural gate quality (html, placeholders, english runs, bullets, etc.)
    out.extend(g.quality_issues(doc, "warn"))
    # h1 mismatch
    title = g.fm_value(doc.fm, "title")
    h1 = re.search(r"^#\s+(.*)$", body, re.M)
    if h1 and title and h1.group(1).strip() != title:
        out.append(g.Issue("error", "h1-mismatch", doc.rel, "H1 != title"))
    # tags
    tags = tag_list(doc.fm)
    if not tags:
        out.append(g.Issue("error", "bad-tags", doc.rel, "tags is empty"))
    else:
        if tags[-1] != doc.lang:
            out.append(g.Issue("error", "bad-tags", doc.rel, "last tag must be " + doc.lang))
        if len(tags) != len(set(tags)):
            out.append(g.Issue("error", "duplicate-tags", doc.rel, "duplicate tags: " + str(tags)))
    # source_url
    su = g.fm_value(doc.fm, "source_url")
    if not su:
        out.append(g.Issue("error", "missing-source-url", doc.rel, "source_url is empty"))
    elif not su.startswith(("http://", "https://")):
        out.append(g.Issue("error", "bad-source-url", doc.rel, su[:80]))
    # duplicate published keys
    present = [k for k in DATE_KEYS if re.search(r"^" + re.escape(k) + r":", doc.fm, re.M)]
    if len(present) > 1:
        out.append(g.Issue("error", "duplicate-published", doc.rel, "both " + " and ".join(present)))
    # paper/article keys
    if doc.kind == "papers":
        for key in ("arxiv_id", "authors", "blog"):
            if not g.fm_value(doc.fm, key):
                out.append(g.Issue("error", "missing-key", doc.rel, "paper missing frontmatter: " + key))
    elif doc.kind == "articles":
        if not g.fm_value(doc.fm, "blog"):
            out.append(g.Issue("error", "missing-key", doc.rel, "article missing frontmatter: blog"))
    # ko-copy / english-run copy
    hangul = len(re.findall(r"[\uac00-\ud7a3]", body))
    latin = len(re.findall(r"[A-Za-z]", body))
    if doc.lang == "ko" and hangul < 50:
        out.append(g.Issue("error", "ko-body-en", doc.rel, "Korean body has only " + str(hangul) + " Hangul chars"))
    if doc.lang == "en" and hangul > 100 and hangul > latin:
        out.append(g.Issue("warn", "en-body-ko", doc.rel, "English doc looks Korean"))
    if doc.lang == "ko":
        other_rel, other = g.counterpart(all_docs, doc)
        if other is not None:
            en_body = other.body.strip()
            if len(en_body) > 300 and len(body.strip()) > 300:
                ratio = __import__("difflib").SequenceMatcher(None, en_body[:4000], body.strip()[:4000]).ratio()
                if ratio > 0.9:
                    out.append(g.Issue("error", "ko-copy", doc.rel, "Korean body copies English (" + format(ratio, ".2f") + ")"))
    return out


def target_rels(scope):
    if scope == "all":
        return set(g.all_docs().keys())
    changes = g.changes_worktree()
    out = set()
    for status, rel in changes:
        if status == "D":
            continue
        if rel.endswith(".md"):
            out.add(rel)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--scope", choices=("all", "worktree"), default="all")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--max-samples", type=int, default=8)
    args = ap.parse_args()

    all_docs = g.all_docs()
    rels = target_rels(args.scope)
    selected = [d for rel, d in all_docs.items() if rel in rels]

    by_code = defaultdict(list)
    sev_counts = Counter()
    total_issues = 0
    for doc in selected:
        for issue in audit_doc(doc, all_docs):
            by_code[issue.code].append(issue.rel)
            sev_counts[issue.severity] += 1
            total_issues += 1

    if args.json:
        payload = {
            "scope": args.scope,
            "docs_scanned": len(selected),
            "issues": total_issues,
            "severity": dict(sev_counts),
            "by_code": {k: len(v) for k, v in sorted(by_code.items())},
            "samples": {k: v[:args.max_samples] for k, v in sorted(by_code.items())},
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    print("Audit scope: " + args.scope)
    print("Docs scanned: " + str(len(selected)))
    print("Issues: " + str(total_issues) + " (" + ", ".join(f"{k}={v}" for k,v in sorted(sev_counts.items())) + ")")
    if not by_code:
        print("No issues found.")
        return
    print("")
    for code in sorted(by_code):
        paths = by_code[code]
        print(f"{code}: {len(paths)}")
        for p in paths[:args.max_samples]:
            print("  " + p)
        if len(paths) > args.max_samples:
            print("  ... and " + str(len(paths)-args.max_samples) + " more")


if __name__ == "__main__":
    main()
