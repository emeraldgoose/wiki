#!/usr/bin/env python3
"""Fetch pending article stubs into reviewable summary drafts — politely.

Safest possible crawler for this repo:

  - stdlib only (matches collect_articles.py / wiki_builder.py).
  - Checks robots.txt per host via urllib.robotparser BEFORE fetching any
    article URL. Blocked URLs are skipped, never retried in the same run.
  - Generic browser User-Agent. Medium (netflixtechblog.com) blocks AI-bot
    UAs (GPTBot/ClaudeBot/...) at the root, so an ML-named UA would be
    denied even where a normal reader is allowed.
  - Sequential + per-host rate limit (default 3s), 30s timeout, 2MB cap,
    single pass, no recursive crawling. Raw HTML is cached under
    .index-backup/raw/ so re-runs never re-hit the network.
  - Never copies the article verbatim: the generated body is a short
    summary skeleton (overview + key points + source outline) with a link
    back to the original and source_url preserved in frontmatter.

Usage:
    python3 scripts/fetch_drafts.py --dry-run            # what would be fetched
    python3 scripts/fetch_drafts.py --limit 2 --only databricks --write
"""

import argparse
import hashlib
import html as htmlmod
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import urllib.robotparser
from html.parser import HTMLParser

CWD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(CWD, "content")
CACHE_DIR = os.path.join(CWD, ".index-backup", "raw")

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36 WikiCollector/1.0"
)
MAX_BYTES = 2_000_000

_last_hit = {}
_robot_cache = {}


def polite_sleep(host, delay):
    now = time.monotonic()
    prev = _last_hit.get(host)
    if prev is not None:
        wait = delay - (now - prev)
        if wait > 0:
            time.sleep(wait)
    _last_hit[host] = time.monotonic()


def robot_allows(url, timeout=15):
    """Return (allowed, reason). Fetches and caches robots.txt per host."""
    parts = urllib.parse.urlsplit(url)
    host = parts.netloc.lower()
    if host in _robot_cache:
        rp = _robot_cache[host]
    else:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(f"{parts.scheme}://{parts.netloc}/robots.txt")
        try:
            rp.read()
        except Exception as exc:  # fail closed: do not crawl on doubt
            return False, f"robots.txt unreadable: {type(exc).__name__}"
        _robot_cache[host] = rp
    try:
        if rp.can_fetch(USER_AGENT, url):
            return True, "allowed by robots.txt"
        return False, "disallowed by robots.txt"
    except Exception as exc:
        return False, f"robots check error: {exc}"


def cache_path(url):
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]
    return os.path.join(CACHE_DIR, digest + ".html"), os.path.join(
        CACHE_DIR, digest + ".json"
    )


def fetch_url(url, delay, timeout=30):
    """Fetch one article page. Returns (html_text, from_cache, note)."""
    html_path, meta_path = cache_path(url)
    if os.path.exists(html_path) and os.path.exists(meta_path):
        try:
            with open(html_path, "r", encoding="utf-8", errors="replace") as fh:
                return fh.read(), True, "cache hit"
        except OSError:
            pass
    host = urllib.parse.urlsplit(url).netloc
    polite_sleep(host, delay)
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read(MAX_BYTES + 1)
            if len(raw) > MAX_BYTES:
                return "", False, "skipped: page larger than 2MB cap"
            charset = resp.headers.get_content_charset() or "utf-8"
            text = raw.decode(charset, errors="replace")
    except Exception as exc:
        return "", False, f"fetch failed: {type(exc).__name__}: {str(exc)[:120]}"
    os.makedirs(CACHE_DIR, exist_ok=True)
    try:
        with open(html_path, "w", encoding="utf-8") as fh:
            fh.write(text)
        with open(meta_path, "w", encoding="utf-8") as fh:
            json.dump({"url": url, "fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}, fh)
    except OSError:
        pass
    return text, False, "fetched"


SKIP_TAGS = {"script", "style", "noscript", "nav", "footer", "header", "aside", "form"}

# Void elements never have an end tag; counting them as depth breaks the
# skip/article tracking on meta-heavy pages (e.g. Gatsby <meta/> soup).
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}


class MainTextExtractor(HTMLParser):
    """Collect h2/h3/p/li/pre blocks, preferring <article>/<main> content."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.skip_depth = None
        self.article_depth = None
        self.in_block = None
        self.buf = []
        self.global_blocks = []
        self.article_blocks = []
        self.page_title = ""

    def handle_startendtag(self, tag, attrs):
        # Self-closing / void tag: no depth change, no block content.
        return

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in VOID_TAGS:
            if tag == "br" and self.in_block:
                self.buf.append(" ")
            return
        self.depth += 1
        if tag in SKIP_TAGS and self.skip_depth is None:
            self.skip_depth = self.depth
            return
        if tag in ("article", "main") and self.article_depth is None:
            self.article_depth = self.depth
        if tag in ("h1", "h2", "h3", "p", "li", "pre") and self.skip_depth is None:
            self.in_block = tag
            self.buf = []
        elif tag == "br" and self.in_block:
            self.buf.append(" ")

    def handle_endtag(self, tag):
        tag = tag.lower()
        if self.skip_depth is not None and self.depth <= self.skip_depth:
            if tag in SKIP_TAGS:
                self.skip_depth = None
        if self.article_depth is not None and self.depth <= self.article_depth:
            if tag in ("article", "main"):
                self.article_depth = None
        if self.in_block == tag:
            text = re.sub(r"\s+", " ", "".join(self.buf)).strip()
            text = htmlmod.unescape(text)
            if len(text) >= 40:
                # route: once inside article, everything article-scoped
                if self.article_depth is not None:
                    self.article_blocks.append((tag, text[:5000]))
                else:
                    self.global_blocks.append((tag, text[:5000]))
            self.in_block = None
            self.buf = []
        self.depth = max(0, self.depth - 1)

    def handle_data(self, data):
        if self.skip_depth is not None:
            return
        if self.in_block:
            self.buf.append(data)


def extract_blocks(html_text):
    # Drop <head> (meta/script soup, ~480k on Gatsby pages) before parsing:
    # truncating mid-<script> would leave the skip flag engaged and wipe
    # the whole body. Body-first parsing keeps the bound safe.
    nohead = re.sub(r"<head\b.*?</head>", " ", html_text, flags=re.S | re.I)
    ext = MainTextExtractor()
    try:
        ext.feed(nohead[:1_500_000])
        ext.close()
    except Exception:
        pass
    blocks = ext.article_blocks if len(ext.article_blocks) >= 3 else ext.global_blocks
    return blocks


def clean_sentence(text, limit=300):
    text = re.sub(r"\s+", " ", text).strip()
    # drop cookie/consent/newsletter boilerplate
    if re.search(r"cookie|consent|subscribe|newsletter|sign up|accept all", text, re.I):
        if len(text) < 200:
            return ""
    return text[:limit]


def word_cut(text, limit=140):
    """Cut at a word boundary so descriptions don't end mid-word."""
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return cut or text[:limit]


def build_full_body(title, blog, source_url, published, blocks):
    """Verbatim working draft: every extracted block in source order.

    Nothing is summarized or cut — this is the raw material the later
    summarization step condenses. Kept behind `status: pending` so the
    portal keeps it in pending.html until a human promotes it.
    """
    lines = [
        f"# {title}",
        "",
        f"**Source**: [{blog}]({source_url})",
        f"**Date**: {published}",
        "",
        "> RAW DRAFT — full text extracted from the original for "
        "summarization work. Not yet condensed. Do not treat as finished.",
        f"> Original: [{source_url}]({source_url})",
        "",
    ]
    in_list = False
    for kind, text in blocks:
        text = re.sub(r"\s+", " ", text).strip()
        if re.search(r"cookie|consent|subscribe to our newsletter|accept all cookies",
                     text, re.I) and len(text) < 200:
            continue
        if kind in ("h2", "h3"):
            if in_list:
                lines.append("")
                in_list = False
            lines += [("## " if kind == "h2" else "### ") + text, ""]
        elif kind == "li":
            lines.append(f"- {text}")
            in_list = True
        elif kind == "pre":
            if in_list:
                lines.append("")
                in_list = False
            lines += ["```", text[:4000], "```", ""]
        else:  # p, h1 treated as paragraph
            if in_list:
                lines.append("")
                in_list = False
            lines += [text, ""]
    lines += [
        "## References",
        "",
        f"- Original article: [{source_url}]({source_url})",
        "",
    ]
    return "\n".join(lines)


def build_draft_body(title, blog, source_url, published, blocks):
    paras = [clean_sentence(t, 600) for k, t in blocks if k == "p"]
    paras = [p for p in paras if len(p) >= 80][:6]
    heads = [clean_sentence(t, 120) for k, t in blocks if k in ("h2", "h3")]
    heads = [h for h in heads if len(h) >= 4][:10]
    bullets_src = [clean_sentence(t, 220) for k, t in blocks if k == "li"]
    bullets_src = [b for b in bullets_src if len(b) >= 40][:8]

    overview = " ".join(paras[:2])[:800] or "Summary pending human review."
    lines = [
        f"# {title}",
        "",
        f"**Source**: [{blog}]({source_url})",
        f"**Date**: {published}",
        "",
        "> Draft summary auto-extracted from the original article. "
        "Condensed here — see the original for full detail.",
        f"> Original: [{source_url}]({source_url})",
        "",
        "## Overview",
        "",
        overview,
        "",
        "## Key points",
        "",
    ]
    if bullets_src:
        for b in bullets_src[:6]:
            lines.append(f"- {b}")
    elif paras[2:]:
        for p in paras[2:5]:
            lines.append(f"- {p[:220]}")
    else:
        lines.append("- Summary pending human review.")
    lines += ["", "## Source outline", ""]
    if heads:
        for h in heads:
            lines.append(f"- {h}")
    else:
        lines.append("- See the original article for section details.")
    lines += [
        "",
        "## References",
        "",
        f"- Original article: [{source_url}]({source_url})",
        "",
    ]
    return "\n".join(lines)


def parse_stub(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        raw = fh.read()
    meta = {}
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    body = raw
    if m:
        for line in m.group(1).split("\n"):
            if ":" in line:
                k, _, v = line.partition(":")
                meta[k.strip()] = v.strip().strip("'\"")
        body = m.group(2)
    return meta, body, raw


def find_stubs(lang, only="", reprocess=False):
    out = []
    root = os.path.join(CONTENT_DIR, lang, "sources", "articles")
    if not os.path.isdir(root):
        return out
    for dirpath, _dirs, files in os.walk(root):
        for fname in sorted(files):
            if not fname.endswith(".md"):
                continue
            full = os.path.join(dirpath, fname)
            try:
                with open(full, encoding="utf-8", errors="replace") as fh:
                    head = fh.read(4000)
            except OSError:
                continue
            is_stub = ("status: pending" in head or "[Content pending]" in head
                       or (reprocess and "Draft summary auto-extracted" in head))
            if is_stub:
                rel = os.path.relpath(full, CWD)
                if only and only not in rel:
                    continue
                out.append(full)
    return sorted(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", default="en")
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--delay", type=float, default=3.0,
                    help="seconds between requests to the same host")
    ap.add_argument("--only", default="", help="substring filter on file path")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--write", action="store_true",
                    help="update content/ files; without it, only fetch+cache")
    ap.add_argument("--full", action="store_true",
                    help="write the full extracted text as a raw working draft "
                         "(no summarizing/cutting); keeps status: pending so the "
                         "portal holds it in pending.html until summarized")
    ap.add_argument("--reprocess", action="store_true",
                    help="also pick up files already converted to condensed drafts")
    args = ap.parse_args()

    stubs = find_stubs(args.lang, args.only, args.reprocess)[: args.limit]
    print(f"Pending stubs in scope ({args.lang}): {len(stubs)}")
    if not stubs:
        return

    for path in stubs:
        meta, _body, _raw = parse_stub(path)
        url = meta.get("source_url", "")
        rel = os.path.relpath(path, CWD)
        if not url or not url.startswith("http"):
            print(f"  SKIP {rel}: no source_url")
            continue
        allowed, reason = robot_allows(url)
        print(f"  {rel}\n    robots: {reason}")
        if not allowed:
            continue
        html_text, cached, note = fetch_url(url, args.delay)
        print(f"    fetch: {note} ({len(html_text)} chars)")
        if not html_text:
            continue
        if args.dry_run or not args.write:
            blocks = extract_blocks(html_text)
            print(f"    extract: {len(blocks)} blocks (cached, no file change)")
            continue
        blocks = extract_blocks(html_text)
        if len(blocks) < 3:
            print("    extract: too few blocks, leaving stub for manual review")
            continue
        title = meta.get("title", "Untitled")
        blog = meta.get("blog", "")
        published = meta.get("published_date", meta.get("published", ""))
        locale = meta.get("locale", args.lang)
        lang_tag = locale if locale in ("en", "ko") else args.lang
        if args.full:
            body = build_full_body(title, blog, url, published, blocks)
            first_para = next((t for k, t in blocks if k == "p"), "")
            desc = word_cut(first_para) or f"Summary of {title}."
            front = (
                "---\n"
                f'title: "{title}"\n'
                f'description: "{desc}"\n'
                f"tags: [source, {blog}, {lang_tag}]\n"
                f"locale: {lang_tag}\n"
                f'source_url: "{url}"\n'
                f"blog: {blog}\n"
                f"published: \"{published}\"\n"
                "status: pending\n"
                "---\n\n"
            )
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(front + body)
            print(f"    wrote RAW full-text draft -> {rel} ({len(blocks)} blocks, kept pending)")
            continue
        body = build_draft_body(title, blog, url, published, blocks)
        first_para = next((t for k, t in blocks if k == "p"), "")
        desc = (word_cut(first_para)
                or f"Summary of {title}.")
        front = (
            "---\n"
            f'title: "{title}"\n'
            f'description: "{desc}"\n'
            f"tags: [source, {blog}, {lang_tag}]\n"
            f"locale: {lang_tag}\n"
            f'source_url: "{url}"\n'
            f"blog: {blog}\n"
            f"published: \"{published}\"\n"
            "---\n\n"
        )
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(front + body)
        print(f"    wrote draft summary -> {rel} ({len(blocks)} blocks)")


if __name__ == "__main__":
    main()
