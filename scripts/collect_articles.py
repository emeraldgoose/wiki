#!/usr/bin/env python3
"""Collect recent engineering-blog posts from RSS/Atom feeds, and
HuggingFace Daily Papers from the HF API.

Stdlib only. Article mode fetches each feed, keeps items published in the
current year or later, and writes a normalised JSON inventory for the
writing stage. Paper mode fetches one HF Daily Papers date and normalises
it into the same record shape (arxiv abs URL as source_url).

Neither stage writes bodies — they only resolve titles, URLs, dates and
publisher, so the (expensive, model-driven) summarisation step runs
against a known list.

Usage:
    python3 scripts/collect_articles.py [--year 2026] [--out .index-backup/collected.json]
    python3 scripts/collect_articles.py --kind papers --date 2026-10-12 [--stubs]
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

CWD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FEEDS = {
    "netflix": "https://netflixtechblog.com/feed",
    "airbnb": "https://airbnb.tech/feed/",
    "spotify": "https://engineering.atspotify.com/feed/",
    "aws-big-data": "https://aws.amazon.com/blogs/big-data/feed/",
    "databricks": "https://www.databricks.com/feed",
}

# Folder slug per publisher. Must match the on-disk layout in
# content/<lang>/sources/articles/<slug>/ and make_index.py's BLOG_LABEL.
BLOG_SLUG = {
    "netflix": "netflix",
    "airbnb": "airbnb",
    "spotify": "spotify",
    "aws-big-data": "aws-big-data",
    "databricks": "databricks",
}

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "dc": "http://purl.org/dc/elements/1.1/",
    "content": "http://purl.org/rss/1.0/modules/content/",
}


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "application/rss+xml, application/atom+xml, application/xml;q=0.9, */*;q=0.8",
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def text_of(node, *paths):
    for p in paths:
        found = node.find(p, NS)
        if found is not None and found.text:
            return found.text.strip()
        # some feeds carry a default namespace instead
        alt = p.replace("atom:", "").replace("content:", "").replace("dc:", "")
        for child in node:
            if child.tag.split("}")[-1] == alt and child.text:
                return child.text.strip()
    return ""


def parse_date(raw):
    if not raw:
        return ""
    raw = raw.strip()
    for fmt in (
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S %Z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d",
    ):
        try:
            dt = datetime.strptime(raw, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc).date().isoformat()
        except ValueError:
            continue
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", raw)
    return m.group(0) if m else ""


def summary_of(item):
    for p in ("content:encoded", "atom:summary", "description", "atom:content"):
        val = text_of(item, p)
        if val:
            val = re.sub(r"<[^>]+>", " ", val)
            val = re.sub(r"\s+", " ", val).strip()
            if val:
                return val[:600]
    return ""


def normalize_url(url):
    """Strip tracking query strings and fragments.

    Feeds append params like ?source=rss----<token> that never appear in the
    canonical article URL. Without this, dedupe against the wiki's
    source_url never matches and already-written articles get re-written.
    """
    url = url.split("#", 1)[0]
    if "?" in url:
        url = url.split("?", 1)[0]
    return url.rstrip("/")


def collect(min_year):
    collected, per_feed = [], {}
    for blog, url in FEEDS.items():
        try:
            raw = fetch(url)
        except (urllib.error.URLError, OSError, ET.ParseError) as exc:
            print(f"  {blog:14s} FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
            per_feed[blog] = {"status": "error", "error": str(exc)[:120]}
            continue

        try:
            root = ET.fromstring(raw)
        except ET.ParseError as exc:
            print(f"  {blog:14s} PARSE ERROR: {exc}", file=sys.stderr)
            per_feed[blog] = {"status": "parse_error", "error": str(exc)[:120]}
            continue

        items = root.findall(".//item") or root.findall(".//atom:entry", NS)
        kept = []
        for item in items:
            title = text_of(item, "title", "atom:title")
            link = text_of(item, "link", "atom:link")
            if not link:
                el = item.find("atom:link", NS)
                if el is not None:
                    link = el.get("href", "")
            published = parse_date(
                text_of(item, "pubDate", "atom:published", "atom:updated", "dc:date")
            )
            if not title or not link:
                continue
            if published and published < f"{min_year}-01-01":
                continue
            if not published:
                continue  # undated items can't satisfy a year filter
            rec = {
                "blog": blog,
                "title": title,
                "url": link,
                "url_normalized": normalize_url(link),
                "published": published,
                "summary": summary_of(item),
            }
            kept.append(rec)
            collected.append(rec)

        kept.sort(key=lambda r: r["published"], reverse=True)
        per_feed[blog] = {"status": "ok", "kept": len(kept), "total_items": len(items)}
        print(f"  {blog:14s} {len(kept):3d} kept / {len(items):3d} items")

    collected.sort(key=lambda r: r["published"], reverse=True)
    return collected, per_feed


def slugify(text, limit=80):
    """Filesystem-safe slug. Keeps the publisher's own wording so the
    filename stays recognisable next to the source article."""
    s = re.sub(r"[^A-Za-z0-9]+", "_", str(text)).strip("_")
    return s[:limit].rstrip("_") or "untitled"


def pending_path(item, lang="en"):
    """Where this article's markdown will live once written."""
    folder = BLOG_SLUG.get(item["blog"], item["blog"])
    name = slugify(item["title"])
    return os.path.join(CWD, "content", lang, "sources", "articles", folder, name + ".md")


def already_written(item, subdir="articles", lang=None):
    """True if the item already has a file with this source_url.

    With lang set, only that language tree is checked (used when creating
    per-language stubs: an en-only item must still get a ko stub).
    Without lang, both languages are checked (used for pending counts).
    """
    pattern = re.escape(item["url_normalized"])
    langs = (lang,) if lang else ("en", "ko")
    for lg in langs:
        root = os.path.join(CWD, "content", lg, "sources", subdir)
        if not os.path.isdir(root):
            continue
        for dirpath, _dirs, files in os.walk(root):
            for fname in files:
                if not fname.endswith(".md"):
                    continue
                try:
                    with open(os.path.join(dirpath, fname), encoding="utf-8", errors="replace") as fh:
                        head = fh.read(2000)
                except OSError:
                    continue
                if re.search(r"^source_url:\s*\"?[^\"\n]*" + pattern, head, re.M | re.I):
                    return True
    return False


def write_stubs(items, lang="en"):
    """Create a marked placeholder for each unwritten article.

    The placeholder carries the source URL and an explicit TODO, so the
    article is discoverable and the next run does not re-collect it, but it
    can never be mistaken for finished content.
    """
    written = []
    for item in items:
        if already_written(item, lang=lang):
            continue
        path = pending_path(item, lang)
        if os.path.exists(path):
            continue
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(
                "---\n"
                f'title: "{item["title"]}"\n'
                f'source_url: "{item["url_normalized"]}"\n'
                f"blog: {item['blog']}\n"
                f"published_date: {item['published']}\n"
                f"locale: {lang}\n"
                "status: pending\n"
                "---\n\n"
                "[Content pending] This stub was created by scripts/collect_articles.py.\n"
                f"Source: {item['url_normalized']}\n"
            )
        written.append(os.path.relpath(path, CWD))
    return written


HF_DAILY_PAPERS_API = "https://huggingface.co/api/daily_papers?date={date}"


def collect_papers(date_str):
    """Fetch one day of HuggingFace Daily Papers, normalised to article-rec shape.

    source_url is always the arXiv abs URL (dedupe + provenance key per
    AUTHORING.md §5.2). Raises on network/parse failure so main() refuses
    to write an empty inventory.
    """
    raw = fetch(HF_DAILY_PAPERS_API.format(date=date_str))
    try:
        data = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as exc:
        raise SystemExit(f"HF Daily Papers returned unparsable JSON: {exc}")
    items = []
    for entry in data:
        p = entry.get("paper", {}) if isinstance(entry, dict) else {}
        pid = str(p.get("id", "")).strip()
        title = str(p.get("title", "")).strip()
        if not pid or not title:
            continue
        published = str(p.get("publishedAt", "") or "")[:10] or date_str
        authors = [str(a.get("name", "")).strip()
                   for a in p.get("authors", []) or []
                   if isinstance(a, dict) and a.get("name")]
        summary = re.sub(r"\s+", " ", str(p.get("summary", "") or "")).strip()[:600]
        url = f"https://arxiv.org/abs/{pid}"
        items.append({
            "blog": "huggingface",
            "title": title,
            "url": url,
            "url_normalized": url,
            "published": published,
            "summary": summary,
            "arxiv_id": pid,
            "authors": authors,
        })
    items.sort(key=lambda r: r["published"], reverse=True)
    print(f"  huggingface/papers {len(items):3d} kept for {date_str}")
    return items


def paper_pending_path(item, lang="en"):
    """Where this paper's markdown will live once written.

    Flat layout per AUTHORING.md §5.2: content/<lang>/sources/papers/<id-dash>.md
    (e.g. 2609.04199 -> 2609-04199.md).
    """
    name = item["arxiv_id"].replace(".", "-")
    return os.path.join(CWD, "content", lang, "sources", "papers", name + ".md")


def _yaml_quote(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def write_paper_stubs(items, lang="en"):
    """Create a marked placeholder for each uncollected paper.

    Same contract as write_stubs: source_url + status: pending so the next
    run does not re-collect it, but it renders only as a placeholder until
    fetch_drafts.py fills the body and a human promotes it.
    """
    written = []
    for item in items:
        if already_written(item, subdir="papers", lang=lang):
            continue
        path = paper_pending_path(item, lang)
        if os.path.exists(path):
            continue
        os.makedirs(os.path.dirname(path), exist_ok=True)
        authors = ", ".join(_yaml_quote(a) for a in item.get("authors", []))
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(
                "---\n"
                f"title: {_yaml_quote(item['title'])}\n"
                f"source_url: {_yaml_quote(item['url_normalized'])}\n"
                "blog: huggingface\n"
                f"arxiv_id: {_yaml_quote(item['arxiv_id'])}\n"
                f"authors: [{authors}]\n"
                f"published_date: {item['published']}\n"
                f"locale: {lang}\n"
                "status: pending\n"
                "---\n\n"
                "[Content pending] This stub was created by scripts/collect_articles.py --kind papers.\n"
                f"Source: {item['url_normalized']}\n"
            )
        written.append(os.path.relpath(path, CWD))
    return written


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", choices=("articles", "papers"), default="articles",
                    help="articles: RSS feeds by year; papers: HF Daily Papers by date")
    ap.add_argument("--year", type=int, default=datetime.now(timezone.utc).year,
                    help="only keep articles published in this year or later")
    ap.add_argument("--date", default="",
                    help="HF Daily Papers date YYYY-MM-DD (papers kind; default: today UTC)")
    ap.add_argument("--out", default="",
                    help="inventory path (default: .index-backup/collected.json "
                         "for articles, .index-backup/collected_papers.json for papers)")
    ap.add_argument("--stubs", action="store_true",
                    help="create marked [Content pending] placeholders for new items")
    args = ap.parse_args()

    if args.kind == "papers":
        date_str = args.date or datetime.now(timezone.utc).date().isoformat()
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_str):
            raise SystemExit("--date must be YYYY-MM-DD")
        out = args.out or os.path.join(CWD, ".index-backup", "collected_papers.json")
        print(f"Collecting HF Daily Papers for {date_str}")
        try:
            items = collect_papers(date_str)
        except (urllib.error.URLError, OSError) as exc:
            raise SystemExit(f"HF Daily Papers fetch failed: {type(exc).__name__}: {exc}")
        if not items:
            raise SystemExit("no papers collected — refusing to write an empty inventory")

        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as fh:
            json.dump({"kind": "papers", "date": date_str, "items": items},
                      fh, ensure_ascii=False, indent=1)
        print(f"\nTotal {len(items)} items -> {os.path.relpath(out, CWD)}")

        if args.stubs:
            for lang in ("en", "ko"):
                made = write_paper_stubs(items, lang)
                print(f"  {lang}: {len(made)} new stub(s) under content/{lang}/sources/papers/")
            unwritten = sum(1 for it in items if not already_written(it, subdir="papers"))
            print(f"\nPending papers needing a written body: {unwritten}")
        return

    out = args.out or os.path.join(CWD, ".index-backup", "collected.json")
    print(f"Collecting engineering-blog posts published {args.year} or later")
    items, per_feed = collect(args.year)
    if not items:
        raise SystemExit("no items collected — refusing to write an empty inventory")

    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"min_year": args.year, "feeds": per_feed, "items": items},
                  fh, ensure_ascii=False, indent=1)

    blogs = {}
    for it in items:
        blogs[it["blog"]] = blogs.get(it["blog"], 0) + 1
    print(f"\nTotal {len(items)} items -> {os.path.relpath(out, CWD)}")
    print("By blog:", json.dumps(blogs, ensure_ascii=False))
    failed = [b for b, s in per_feed.items() if s["status"] != "ok"]
    if failed:
        print(f"Unreachable feeds: {', '.join(failed)}")

    if args.stubs:
        for lang in ("en", "ko"):
            made = write_stubs(items, lang)
            print(f"  {lang}: {len(made)} new stub(s) under content/{lang}/sources/articles/")
        unwritten = sum(1 for it in items if not already_written(it))
        print(f"\nPending articles needing a written body: {unwritten}")


if __name__ == "__main__":
    main()