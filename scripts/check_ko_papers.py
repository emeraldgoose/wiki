#!/usr/bin/env python3
"""ko 논문 문서 정책 검사 (AUTHORING.md §2·§3·§5.3).

content/ko/sources/papers 만 검사한다. 실패 시 exit 1.

검사 항목:
  1. 필수 frontmatter 키(title, description, tags, locale, source_url,
     arxiv_id, authors, blog, published/published_date)
  2. title·description 의 "(한국어 번역)", "(한국어 요약)" 같은 잔여 표시
  3. title 에 한국어가 없는 경우(영문 제목 방치)
  4. 본문 H1 이 frontmatter title 과 다른 경우
  5. tags 중복, tags 끝이 ko 가 아닌 경우
  6. 본문이 영어 원문인 경우(한글 50자 미만) 또는 300자 미만
  7. 같은 경로 en 본문과 90% 이상 동일한 경우(복붙)
  8. 파일명이 arXiv ID 형식이 아닌 경우(경고만)
"""
import difflib
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPERS = os.path.join(ROOT, "content", "ko", "sources", "papers")
REQUIRED = ["title", "description", "tags", "locale", "source_url",
            "arxiv_id", "authors", "blog"]
MARKER = re.compile(r"\(한국어\s*(?:번역|요약)\)")


def split_doc(text):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    return (m.group(1), m.group(2)) if m else ("", text)


def fm_value(fm, key):
    m = re.search(r"^%s:\s*(.*)$" % re.escape(key), fm, re.M)
    return m.group(1).strip() if m else ""


def unquote(value):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        return value[1:-1].replace('\\"', '"')
    return value


def main():
    errors = []
    warnings = []
    for path in sorted(glob.glob(os.path.join(PAPERS, "*.md"))):
        name = os.path.basename(path)
        text = open(path, encoding="utf-8").read()
        fm, body = split_doc(text)
        add = lambda kind, why: errors.append((name, kind, why))

        keys = {m.group(1) for m in re.finditer(r"^([A-Za-z_]+):", fm, re.M)}
        for key in REQUIRED:
            if key not in keys:
                add("missing-key", key)
        if "published" not in keys and "published_date" not in keys:
            add("missing-key", "published/published_date")

        title = unquote(fm_value(fm, "title"))
        desc = unquote(fm_value(fm, "description"))
        if MARKER.search(title) or MARKER.search(desc):
            add("marker", "한국어 번역/요약 표시 잔존")
        if title and not re.search(r"[\uac00-\ud7a3]", title):
            add("title-en", "제목에 한국어 없음")
        if desc.startswith("en/sources/") or "번역 요약" in desc:
            add("desc-placeholder", desc[:60])

        h1 = re.search(r"^#\s+(.*)$", body, re.M)
        if not h1:
            add("h1", "본문 H1 없음")
        elif h1.group(1).strip() != title:
            add("h1", "H1 != title: %s" % h1.group(1).strip()[:60])

        tags = fm_value(fm, "tags").strip("[]")
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        if len(tag_list) != len(set(tag_list)):
            add("tags", "중복 태그: %s" % tag_list)
        if not tag_list or tag_list[-1] != "ko":
            add("tags", "tags 끝이 ko 아님: %s" % tag_list)

        hangul = len(re.findall(r"[\uac00-\ud7a3]", body))
        if hangul < 50:
            add("body-en", "본문 한글 %d자 (영어 원문 의심)" % hangul)
        if len(body.strip()) < 300:
            add("body-short", "본문 %d자 (<300)" % len(body.strip()))

        en_path = path.replace(os.sep + "ko" + os.sep, os.sep + "en" + os.sep)
        if os.path.exists(en_path):
            en_body = split_doc(open(en_path, encoding="utf-8").read())[1]
            en_hangul = len(re.findall(r"[\uac00-\ud7a3]", en_body))
            en_latin = len(re.findall(r"[A-Za-z]", en_body))
            # en 쪽이 실제로 영어일 때만 복붙 비교(한국어로 잘못 채워진 en 은 제외)
            if (en_latin > en_hangul and len(en_body.strip()) > 300
                    and len(body.strip()) > 300):
                ratio = difflib.SequenceMatcher(
                    None, en_body[:4000], body[:4000]).ratio()
                if ratio > 0.9:
                    add("copy", "en 본문 복붙 의심 (%.2f)" % ratio)

        if not re.fullmatch(r"\d{4}-\d{4,5}\.md", name):
            warnings.append((name, "filename", "arXiv ID 형식 아님"))

    for name, kind, why in errors:
        print("FAIL %-14s %s -- %s" % (kind, name, why))
    for name, kind, why in warnings:
        print("WARN %-14s %s -- %s" % (kind, name, why))
    print("\nko papers: %d, errors: %d, warnings: %d" %
          (len(glob.glob(os.path.join(PAPERS, "*.md"))), len(errors), len(warnings)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
