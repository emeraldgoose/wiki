#!/usr/bin/env python3
"""Generate static/en/index.html and static/ko/index.html from content/<lang>/**.

Stdlib only. Reads every markdown file's frontmatter, then emits a
Medium-style portal index:

  - "Recent" table over ALL documents, not just the curated 10, with a
    Type/Category column and client-side filtering.
  - A navigator sidebar that indexes every concept, guide and source, so
    documents not linked from the curated sections are still reachable.
  - Category / blog / tag facets, each rendering a linked filterable table.
  - A top-level static/index.html language-choice landing (en/ko cards).

Rewrites only static/<lang>/index.html (+ static/index.html landing).
Run scripts/wiki_builder.py first (it owns assets/style.css and every
other page).

Usage:
    python3 scripts/make_index.py [--limit N] [--dry-run]
"""

import argparse
import html
import json
import os
import re
import sys
from collections import Counter, defaultdict
from urllib.parse import quote

CWD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(CWD, "content")
PUBLIC = {"en": os.path.join(CWD, "static", "en"), "ko": os.path.join(CWD, "static", "ko")}
STATIC_ROOT = os.path.join(CWD, "static")
ASSETS = os.path.join(CWD, "static", "en", "assets")

SKIP_NAMES = {"index.md"}

I18N = {
    "en": {
        "lang": "en",
        "title": "Wiki Portal",
        "tagline": "Papers, concepts and guides, verified against original sources.",
        "intro": "A reading-first index of everything in this wiki. Filter by type, "
                 "category or source, or search. The full navigator on the left reaches "
                 "every document, including ones not listed below.",
        "recent": "Recent",
        "recent_sub": "Every document, newest first.",
        "all": "All",
        "papers": "Papers",
        "concepts": "Concepts",
        "guides": "Guides",
        "articles": "Articles",
        "browse": "Browse",
        "by_category": "By category",
        "by_source": "By source",
        "by_tag": "By tag",
        "navigate": "Navigator",
        "search_ph": "Search 519 documents…",
        "col_title": "Title",
        "col_type": "Type",
        "col_category": "Category",
        "col_date": "Date",
        "col_source": "Source",
        "read": "Read",
        "empty": "No documents match.",
        "count": "documents",
        "footer": "Built from content/ by scripts/make_index.py.",
        "no_date": "—",
        "uncategorized": "Uncategorized",
        "pending_title": "Pending",
        "pending_intro": "Collected from the source feeds but not yet written. These are placeholders, not readable articles.",
        "no_pending": "Nothing pending.",
        "other_lang": "한국어",
    },
    "ko": {
        "lang": "ko",
        "title": "위키 포털",
        "tagline": "논문, 개념, 가이드. 원문 대조 검증 완료.",
        "intro": "이 위키의 모든 문서를 읽기 순서로 정리한 색인입니다. 유형, 카테고리, "
                 "출처로 걸러내거나 검색하세요. 왼쪽 내비게이터에서 목록에 없는 문서도 "
                 "모두 찾을 수 있습니다.",
        "recent": "최근 글",
        "recent_sub": "전체 문서, 최신순.",
        "all": "전체",
        "papers": "논문",
        "concepts": "개념",
        "guides": "가이드",
        "articles": "아티클",
        "browse": "탐색",
        "by_category": "카테고리별",
        "by_source": "출처별",
        "by_tag": "태그별",
        "navigate": "내비게이터",
        "search_ph": "519개 문서 검색…",
        "col_title": "제목",
        "col_type": "유형",
        "col_category": "카테고리",
        "col_date": "날짜",
        "col_source": "출처",
        "read": "읽기",
        "empty": "문서가 없습니다.",
        "count": "개 문서",
        "footer": "scripts/make_index.py가 content/에서 생성.",
        "no_date": "—",
        "uncategorized": "미분류",
        "pending_title": "작성 대기",
        "pending_intro": "원본 피드에서 수집했으나 아직 본문을 작성하지 않은 항목입니다. 읽을 수 있는 글이 아닌 자리표시자입니다.",
        "no_pending": "대기 중인 항목이 없습니다.",
        "other_lang": "English",
    },
}

BLOG_LABEL = {
    "AWS Big Data": "AWS Big Data", "aws": "AWS", "airbnb": "Airbnb",
    "netflix": "Netflix", "twitter": "Twitter", "linkedin": "LinkedIn",
    "spotify": "Spotify", "uber": "Uber",
}

TAG_LABEL = {
    "computer-science": "Computer Science", "data-engineering": "Data Engineering",
    "ai-engineering": "AI Engineering", "machine-learning": "Machine Learning",
    "infrastructure": "Infrastructure",
    "논문": "논문", "개념": "개념", "concept": "Concept", "paper": "Paper",
    "source": "Source", "rss": "RSS", "blog": "Blog", "블로그": "블로그",
    "daily-update": "Daily Update", "일일 업데이트": "일일 업데이트",
    "huggingface": "HuggingFace", "ko": "한국어", "en": "English",
}

# Tags that describe document structure or provenance, not a subject domain.
# These should NOT produce a Category label — otherwise the Category column
# just duplicates the Type column (e.g. Category="Paper" next to Type="Paper").
# Only genuine subject tags (ai-engineering, data-engineering, etc.) should.
STRUCTURAL_TAGS = {
    "논문", "개념", "concept", "paper",
    "source", "rss", "blog", "블로그",
    "daily-update", "일일 업데이트",
    "huggingface", "ko", "en",
}

# Tags that describe provenance/pipeline, not subject matter. Used for the
# category facet only; they are too noisy to be useful as navigation.
CATEGORY_TAGS = [
    "computer-science", "data-engineering", "ai-engineering",
    "machine-learning", "infrastructure",
]

# Many articles carry only provenance tags (source/rss/blog) plus a
# publisher, with no explicit category tag — that left ~51 documents per
# language rendering as "—" in the Category column and invisible to the
# category facet. These keyword sets let the index infer a category from the
# subject tags and title that are already present, without editing content.
#
# First match wins, so order is most-specific first. Deliberately does NOT
# invent a category it has no signal for: unmatched rows still show "—".
CATEGORY_KEYWORDS = [
    ("ai-engineering", {
        "ai-agents", "agents", "agent", "agent-harness", "llm", "llms",
        "rag", "retrieval", "embedding", "embeddings", "vector-search",
        "fine-tuning", "model-training", "inference", "mcp", "prompt",
        "vllm", "evaldriven", "evaluation", "sagemaker", "machine-learning",
    }),
    ("data-engineering", {
        "kafka", "flink", "spark", "iceberg", "delta-lake", "hudi", "dbt",
        "airflow", "dagster", "etl", "elt", "warehouse", "lakehouse",
        "data-lake", "data-modeling", "cdc", "stream-processing",
        "batch-processing", "glue", "redshift", "athena", "emr", "kinesis",
        "trino", "presto", "materialized-view", "schema-registry",
        "data-quality", "bigquery", "data-science", "analytics",
    }),
    ("infrastructure", {
        "kubernetes", "k8s", "docker", "terraform", "service-mesh",
        "observability", "sre", "reliability", "incident", "post-mortem",
        "platform-engineering", "developer-experience", "networking",
        "storage", "compute", "performance", "cost-optimization",
    }),
    ("machine-learning", {
        "transformer", "attention", "diffusion", "reinforcement-learning",
        "fine-tuning", "training", "multimodal", "ranking", "recommendation",
        "recommender", "personalization", "forecasting",
    }),
    ("computer-science", {
        "concurrency", "parallelism", "distributed-systems", "consensus",
        "algorithms", "data-structures", "caching", "indexing", "compilers",
        "operating-systems", "complexity", "graph", "memory", "virtual-memory",
    }),
]


def infer_category(tags, title, summary=""):
    """Best-effort category from a document's existing tags and title.

    Returns "" when there is no clear signal, so a row is never given a
    category it does not support.

    Structural tags (paper, concept, source, rss, etc.) are ignored so they
    never populate the Category column — that would just duplicate the Type
    column. Only genuine subject tags (ai-engineering, data-engineering, etc.)
    produce a category label.
    """
    # Only subject tags should map to a Category. Structural tags describe
    # provenance or document type, not a subject domain.
    explicit = next(
        (TAG_LABEL.get(t, t) for t in tags
         if t in CATEGORY_TAGS and t not in STRUCTURAL_TAGS),
        "",
    )
    if explicit:
        return explicit

    haystack = {t.lower() for t in tags if t.lower() not in {s.lower() for s in STRUCTURAL_TAGS}}
    haystack |= set(re.findall(r"[a-z][a-z0-9\-]{2,}", (title or "").lower()))
    haystack |= set(re.findall(r"[a-z][a-z0-9\-]{2,}", (summary or "").lower()))

    for category, keys in CATEGORY_KEYWORDS:
        if haystack & keys:
            return TAG_LABEL.get(category, category)
    return ""


def parse_frontmatter(text):
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    meta = {}
    for line in text[3:end].split("\n"):
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, val = line.partition(":")
        meta[key.strip()] = val.strip().strip("'\"")
    return meta, text[end + 4:].lstrip("\n")


def e(text):
    return html.escape(str(text), quote=False)


def eattr(text):
    return html.escape(str(text), quote=True)


ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}")


def resolve_date(meta):
    """Return an ISO date string, or '' when the value is unusable.

    Some RSS-derived files carry a truncated junk value like `date: 2`
    (day-of-month only, or a column offset). Those are dropped rather than
    guessed at, so they never get a fabricated timestamp.
    """
    for key in ("date", "published_date", "published", "pubDate", "created"):
        val = meta.get(key, "").strip()
        if ISO_DATE.match(val):
            return val[:10]
    return ""


def collect(lang):
    root = os.path.join(CONTENT, lang)
    records = []
    pending = []
    for dirpath, _dirs, files in os.walk(root):
        for name in sorted(files):
            if not name.endswith(".md") or name in SKIP_NAMES:
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, root).replace(os.sep, "/")
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                raw = fh.read()
            meta, _body = parse_frontmatter(raw)

            # Unwritten stubs are placeholders, not articles. Listing them in
            # the index alongside real writing makes the wiki look far more
            # complete than it is, so they are held back for a dedicated
            # "pending" view until a body is written.
            if "status: pending" in raw or "[Content pending]" in raw:
                pending.append({
                    "rel": rel,
                    "title": meta.get("title") or rel.rsplit("/", 1)[-1].replace("_", " "),
                    "blog": meta.get("blog", ""),
                    "date": meta.get("published_date", ""),
                    "url": meta.get("source_url", ""),
                })
                continue

            parts = rel.split("/")
            kind = parts[0] if len(parts) > 1 else "root"
            if kind == "sources" and len(parts) > 2:
                kind = "articles" if parts[1] == "articles" else "papers"
            elif kind == "root":
                kind = "other"

            tags = [t.strip() for t in meta.get("tags", "").strip("[]").split(",") if t.strip()]
            title = meta.get("title") or rel.rsplit("/", 1)[-1].replace("_", " ")
            category = infer_category(tags, title, meta.get("description", ""))
            blog = BLOG_LABEL.get(meta.get("blog", "").strip(),
                                  meta.get("blog", "").strip())

            records.append({
                "rel": rel,
                "href": url_path("/wiki/%s/%s.html" % (lang, rel[:-3])),
                "title": title,
                "desc": meta.get("description", ""),
                "date": resolve_date(meta),
                "kind": kind,
                "category": category,
                "blog": blog,
                "tags": tags,
            })
    return records, pending


def _sort_date(d):
    """Parse an ISO-ish date string into a tuple for descending sort.

    Returns a zero-padded comparable tuple (YEAR, MONTH, DAY, HOUR, MIN).
    Missing components default to 0, so partial dates stay sortable.
    Unparseable values sort as empty (bottom)."""
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})(?:[ T](\d{2})(?::(\d{2}))?)?", d)
    if not m:
        return (0, 0, 0, 0, 0)
    return tuple(int(x) if x else 0 for x in m.groups())  # type: ignore


def sort_key(rec):
    # Dated documents first, newest first; undated ones keep a stable,
    # alphabetical tail so the table never reshuffles between builds.
    d = rec["date"]
    if d:
        sd = _sort_date(d)
        # Negate for descending order within the dated group.
        return (0, (-sd[0], -sd[1], -sd[2], -sd[3], -sd[4]), rec["title"])
    return (1, (0, 0, 0, 0, 0), rec["title"])


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")


def url_path(path):
    """Percent-encode a site path for use in an href.

    Some source filenames contain non-ASCII text (Korean titles, accented
    Latin), so hrefs must be encoded or the server 404s on the raw path.
    """
    return quote(path, safe="/")


def table_html(records, t, show_type=True, id_prefix=""):
    """Render one records table. Rows carry data-* for client-side filtering."""
    kind_label = {
        "papers": t["papers"], "concepts": t["concepts"],
        "guides": t["guides"], "articles": t["articles"],
    }

    has_cat = any(r["category"] for r in records)
    has_date = any(r["date"] for r in records)
    has_src = any(r["blog"] for r in records)

    cols = [t["col_title"]]
    if show_type:
        cols.append(t["col_type"])
    if has_cat:
        cols.append(t["col_category"])
    if has_date:
        cols.append(t["col_date"])
    if has_src:
        cols.append(t["col_source"])

    out = ['<table class="doc-table">', "<thead><tr>"]
    out += [f"<th>{e(c)}</th>" for c in cols]
    out.append("</tr></thead><tbody>")

    for rec in records:
        search = " ".join([rec["title"], rec["desc"], rec["category"], rec["blog"]]).lower()
        tags = " ".join(rec["tags"])
        out.append(
            f'<tr data-kind="{eattr(rec["kind"])}" '
            f'data-category="{eattr(rec["category"])}" '
            f'data-blog="{eattr(rec["blog"])}" '
            f'data-date="{eattr(rec["date"])}" '
            f'data-tags="{eattr(tags)}" '
            f'data-search="{eattr(search)}">'
        )
        out.append(
            f'<td class="t-title"><a href="{eattr(rec["href"])}">{e(rec["title"])}</a></td>'
        )
        if show_type:
            label = kind_label.get(rec["kind"], rec["kind"])
            out.append(f'<td class="t-type"><span class="pill pill-{eattr(rec["kind"])}">{e(label)}</span></td>')
        if has_cat:
            out.append(f'<td class="t-cat">{e(rec["category"] or "")}</td>')
        if has_date:
            out.append(f'<td class="t-date">{e(rec["date"] or "")}</td>')
        if has_src:
            out.append(f'<td class="t-src">{e(rec["blog"] or "")}</td>')
        out.append("</tr>")

    out.append("</tbody></table>")
    return "\n".join(out)


def facet_groups(records, key, t, id_prefix):
    groups = defaultdict(list)
    for rec in records:
        if rec[key]:
            groups[rec[key]].append(rec)
    # Documents with no subject signal still need to be reachable, so collect
    # them under an explicit group rather than dropping them from the facet.
    if key == "category":
        leftover = [r for r in records if not r[key]]
        if leftover:
            label = t.get("uncategorized", "Uncategorized")
            groups[label] = leftover
    if not groups:
        return ""
    blocks = ['<div class="facets" id="facet-%s">' % id_prefix]
    for name in sorted(groups, key=lambda n: (-len(groups[n]), n)):
        items = sorted(groups[name], key=sort_key)
        sid = f"{id_prefix}-{slugify(name)}"
        blocks.append(
            f'<details class="facet" id="{eattr(sid)}" data-facet="{eattr(id_prefix)}" '
            f'data-value="{eattr(name)}">'
            f'<summary><span class="facet-name">{e(name)}</span>'
            f'<span class="facet-count">{len(items)}</span></summary>'
            f"{table_html(items, t, show_type=True)}"
            f"</details>"
        )
    blocks.append("</div>")
    return "\n".join(blocks)


def nav_tree(records, t):
    """Full navigator: every document, grouped by kind then category."""
    sections = []
    order = ["papers", "articles", "concepts", "guides", "other"]
    label = {
        "papers": t["papers"], "articles": t["articles"],
        "concepts": t["concepts"], "guides": t["guides"],
    }
    for kind in order:
        subset = [r for r in records if r["kind"] == kind]
        if not subset:
            continue
        groups = defaultdict(list)
        for rec in subset:
            groups[rec["category"] or rec["blog"] or "—"].append(rec)

        items = [
            f'<details class="nav-group"><summary>{e(label.get(kind, kind))}'
            f'<span class="facet-count">{len(subset)}</span></summary><ul>'
        ]
        for name in sorted(groups, key=lambda n: (-len(groups[n]), n)):
            items.append(
                f'<li class="nav-sub"><span class="nav-subname">{e(name)}'
                f' <em>({len(groups[name])})</em></span><ul>'
            )
            for rec in sorted(groups[name], key=sort_key):
                items.append(
                    f'<li><a href="{eattr(rec["href"])}">{e(rec["title"])}</a></li>'
                )
            items.append("</ul></li>")
        items.append("</ul></details>")
        sections.append("".join(items))
    return "\n".join(sections)


def render(records, t, lang, other_lang_code):
    total = len(records)
    recent = sorted(records, key=sort_key)
    kinds = Counter(r["kind"] for r in records)
    other = I18N[other_lang_code]

    counts = {k: kinds.get(k, 0) for k in ("papers", "articles", "concepts", "guides")}
    filter_buttons = [f'<button class="chip is-active" data-filter-kind="">{e(t["all"])} ({total})</button>']
    for kind in ("papers", "articles", "concepts", "guides"):
        if counts[kind]:
            label = {"papers": t["papers"], "articles": t["articles"],
                     "concepts": t["concepts"], "guides": t["guides"]}[kind]
            filter_buttons.append(
                f'<button class="chip" data-filter-kind="{kind}">{e(label)} ({counts[kind]})</button>'
            )

    cats = sorted({r["category"] for r in records if r["category"]})
    cat_options = "".join(
        f'<option value="{eattr(c)}">{e(c)} ({sum(1 for r in records if r["category"] == c)})</option>'
        for c in cats
    )
    srcs = sorted({r["blog"] for r in records if r["blog"]})
    src_options = "".join(
        f'<option value="{eattr(s)}">{e(s)} ({sum(1 for r in records if r["blog"] == s)})</option>'
        for s in srcs
    )

    latest = [r for r in recent if r["date"]][:3]
    hero_cards = "\n".join(
        f'<a class="hero-card" href="{eattr(r["href"])}">'
        f'<span class="hero-date">{e(r["date"])}</span>'
        f'<span class="hero-title">{e(r["title"])}</span>'
        f'<span class="hero-kind">{e({"papers": t["papers"], "articles": t["articles"], "concepts": t["concepts"], "guides": t["guides"]}.get(r["kind"], ""))}</span>'
        f"</a>"
        for r in latest
    )

    return f"""<!DOCTYPE html>
<html lang="{t['lang']}" dir="ltr">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<meta name="description" content="{eattr(t['tagline'])}"/>
<meta property="og:title" content="{eattr(t['title'])}"/>
<meta property="og:type" content="website"/>
<title>{e(t['title'])}</title>
<link rel="stylesheet" href="assets/style.css"/>
</head>
<body class="portal">
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="/wiki/{lang}/">{e(t['title'])}</a>
    <nav class="header-nav">
      <a href="#recent">{e(t['recent'])}</a>
      <a href="#categories">{e(t['by_category'])}</a>
      <a href="#sources">{e(t['by_source'])}</a>
      <a href="#tags">{e(t['by_tag'])}</a>
      <a href="pending.html">{e(t['pending_title'])}</a>
    </nav>
    <a class="lang-switch" href="/wiki/{other_lang_code}/">{e(other['other_lang'])}</a>
  </div>
</header>

<div class="wrap layout">
  <aside class="sidebar" id="navigator">
    <p class="sidebar-title">{e(t['navigate'])}</p>
    <input type="search" id="nav-search" class="search" placeholder="{eattr(t['search_ph'])}" autocomplete="off"/>
    <div class="nav-tree" id="nav-tree">
{nav_tree(records, t)}
    </div>
  </aside>

  <main class="content">
    <section class="hero">
      <p class="intro">{e(t['intro'])}</p>
      <div class="hero-cards">
{hero_cards}
      </div>
    </section>

    <section id="recent" class="block">
      <h2>{e(t['recent'])}</h2>
      <p class="block-sub">{e(t['recent_sub'])}</p>
      <div class="controls">
        <div class="chips" id="kind-filter">{''.join(filter_buttons)}</div>
        <div class="selects">
          <select id="cat-filter"><option value="">{e(t['by_category'])}: {e(t['all'])}</option>{cat_options}</select>
          <select id="src-filter"><option value="">{e(t['by_source'])}: {e(t['all'])}</option>{src_options}</select>
        </div>
      </div>
      <p class="result-count" id="result-count"></p>
      {table_html(recent, t, show_type=True)}
      <p class="empty" id="empty-msg" hidden>{e(t['empty'])}</p>
    </section>

    <section id="categories" class="block">
      <h2>{e(t['by_category'])}</h2>
      {facet_groups(records, 'category', t, 'cat') or '<p class="empty">—</p>'}
    </section>

    <section id="sources" class="block">
      <h2>{e(t['by_source'])}</h2>
      {facet_groups(records, 'blog', t, 'src') or '<p class="empty">—</p>'}
    </section>

    <section id="tags" class="block">
      <h2>{e(t['by_tag'])}</h2>
      <div class="tag-cloud" id="tag-cloud">
{tag_cloud(records, t)}
      </div>
    </section>
  </main>
</div>

<footer class="site-footer">
  <div class="wrap">
    <p>{e(t['footer'])} · {total} {e(t['count'])}</p>
  </div>
</footer>
<script src="assets/portal.js"></script>
</body>
</html>
"""


def tag_cloud(records, t):
    counter = Counter()
    for rec in records:
        for tag in rec["tags"]:
            counter[tag] += 1
    parts = []
    for tag, n in counter.most_common(60):
        label = TAG_LABEL.get(tag, tag)
        parts.append(
            f'<a class="tag-chip" href="#" data-tag="{eattr(tag)}" '
            f'data-count="{n}">{e(label)} <em>{n}</em></a>'
        )
    return "\n".join(parts)


def render_pending(pending, t, lang, other):
    """A single page listing every collected-but-unwritten article.

    Kept out of the main index so the portal reflects what is actually
    readable, with one obvious place to see the backlog.
    """
    rows = []
    for item in sorted(pending, key=lambda r: (r["date"] or "", r["title"]), reverse=True):
        blog = BLOG_LABEL.get(item["blog"], item["blog"])
        link = (
            f'<a href="{eattr(item["url"])}" target="_blank" rel="noopener">{e(blog)}</a>'
            if item["url"] else e(blog or "—")
        )
        rows.append(
            "<tr>"
            f'<td class="t-title">{e(item["title"])}</td>'
            f'<td class="t-src">{link}</td>'
            f'<td class="t-date">{e(item["date"] or t["no_date"])}</td>'
            "</tr>"
        )
    body = "\n".join(rows) or f'<p class="empty">{e(t["no_pending"])}</p>'
    return f"""<!DOCTYPE html>
<html lang="{t['lang']}" dir="ltr">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<meta name="robots" content="noindex"/>
<title>{e(t['pending_title'])} — {e(t['title'])}</title>
<link rel="stylesheet" href="assets/style.css"/>
</head>
<body class="portal">
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="index.html">{e(t['title'])}</a>
    <nav class="header-nav"><a href="index.html">{e(t['recent'])}</a></nav>
    <a class="lang-switch" href="/wiki/{other}/pending.html">{other.upper()}</a>
  </div>
</header>
<div class="wrap layout">
  <aside class="sidebar">
    <p class="sidebar-title">{e(t['pending_title'])}</p>
    <p class="intro" style="font-size:0.9rem">{e(t['pending_intro'])}</p>
  </aside>
  <main class="content">
    <section class="hero">
      <p class="intro">{e(t['pending_intro'])}</p>
    </section>
    <section class="block">
      <h2>{e(t['pending_title'])} <span class="facet-count">{len(pending)}</span></h2>
      <table class="doc-table">
        <thead><tr><th>{e(t['col_title'])}</th><th>{e(t['col_source'])}</th><th>{e(t['col_date'])}</th></tr></thead>
        <tbody>
{body}
        </tbody>
      </table>
    </section>
  </main>
</div>
<footer class="site-footer"><div class="wrap"><p>{e(t['footer'])}</p></div></footer>
</body>
</html>
"""


def render_landing(counts):
    """Top-level landing: static/index.html.

    Auto-redirects by browser locale (navigator.language): ko* -> ko/,
    anything else (including absent) -> en/. Uses location.replace so the
    landing never stays in history. The en/ko cards remain as a fallback
    for no-JS / direct-file use. Relative targets work both as a file and
    when static/ is served at /wiki/.
    """
    en_n = counts.get("en", 0)
    ko_n = counts.get("ko", 0)
    return f"""<!DOCTYPE html>
<html lang="ko" dir="ltr">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Wiki — English / 한국어</title>
<link rel="stylesheet" href="en/assets/style.css"/>
<script>
(function () {{
  try {{
    var l = (navigator.language || navigator.userLanguage || "en") + "";
    location.replace(/^ko/i.test(l) ? "ko/" : "en/");
  }} catch (e) {{
    location.replace("en/");
  }}
}})();
</script>
<style>
.lang-landing {{ max-width: 760px; margin: 12vh auto; padding: 0 24px; text-align: center; }}
.lang-landing h1 {{ font-family: Georgia, "Times New Roman", serif; font-size: 2rem; margin: 0 0 8px; }}
.lang-landing .sub {{ color: #757575; margin: 0 0 32px; }}
.lang-cards {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
@media (max-width: 560px) {{ .lang-cards {{ grid-template-columns: 1fr; }} }}
.lang-card {{ display: block; border: 1px solid #e6e6e6; border-radius: 12px; padding: 28px 20px; }}
.lang-card:hover {{ border-color: #191919; }}
.lang-card .big {{ font-size: 1.25rem; font-weight: 700; display: block; margin-bottom: 6px; }}
.lang-card .small {{ color: #757575; font-size: 0.9rem; }}
</style>
</head>
<body class="portal">
<div class="lang-landing">
  <h1>Wiki</h1>
  <p class="sub">Redirecting… / 이동 중…</p>
  <noscript><p class="sub">Choose a language / 언어를 선택하세요</p></noscript>
  <div class="lang-cards">
    <a class="lang-card" href="en/">
      <span class="big">English</span>
      <span class="small">Wiki Portal · {en_n} documents</span>
    </a>
    <a class="lang-card" href="ko/">
      <span class="big">한국어</span>
      <span class="small">위키 포털 · {ko_n}개 문서</span>
    </a>
  </div>
</div>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="report only, write nothing")
    args = ap.parse_args()

    print("Generate portal index from content/")
    counts = {}
    for lang, other in (("en", "ko"), ("ko", "en")):
        records, pending = collect(lang)
        if not records:
            raise SystemExit(f"no records found under content/{lang}")
        records.sort(key=sort_key)
        counts[lang] = len(records)
        out = render(records, I18N[lang], lang, other)
        path = os.path.join(PUBLIC[lang], "index.html")
        if args.dry_run:
            print(f"  [dry-run] static/{lang}/index.html would be {len(out):,}B "
                  f"from {len(records)} records")
        else:
            os.makedirs(PUBLIC[lang], exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(out)
            print(f"  wrote static/{lang}/index.html ({len(out):,}B, {len(records)} records)")

        pend_path = os.path.join(PUBLIC[lang], "pending.html")
        pend = render_pending(pending, I18N[lang], lang, other)
        if args.dry_run:
            print(f"  [dry-run] static/{lang}/pending.html would be {len(pend):,}B "
                  f"from {len(pending)} pending")
        else:
            with open(pend_path, "w", encoding="utf-8") as fh:
                fh.write(pend)
            print(f"  wrote static/{lang}/pending.html ({len(pending)} pending)")
    landing = render_landing(counts)
    redirects = (
        "# Cloudflare Pages: serve the /wiki/<lang>/ URL namespace from the\n"
        "# static/en|ko output dirs. 200 keeps the /wiki/... URL in the bar\n"
        "# (matches serve_wiki.py locally), so every absolute /wiki/... link\n"
        "# in the built pages resolves without moving files.\n"
        "/wiki/* /:splat 200\n"
    )
    if args.dry_run:
        print(f"  [dry-run] static/index.html would be {len(landing):,}B")
        print(f"  [dry-run] static/_redirects would be {len(redirects):,}B")
    else:
        os.makedirs(STATIC_ROOT, exist_ok=True)
        with open(os.path.join(STATIC_ROOT, "index.html"), "w", encoding="utf-8") as fh:
            fh.write(landing)
        print(f"  wrote static/index.html (en={counts.get('en', 0)}, ko={counts.get('ko', 0)})")
        with open(os.path.join(STATIC_ROOT, "_redirects"), "w", encoding="utf-8") as fh:
            fh.write(redirects)
        print("  wrote static/_redirects (/wiki/* -> /:splat 200)")
    print("Index generation complete")


if __name__ == "__main__":
    main()