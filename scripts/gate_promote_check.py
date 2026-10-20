#!/usr/bin/env python3
"""승격 전 필수 게이트 (authoring.md §5.3).

검증 범위: content/<lang>/sources/** (papers, articles) — concepts/guides 는
수동 작성이라 게이트 대상이 아니다.

검사 항목 (실패하면 exit 1 = 푸시 차단):
  1. en 파일에 'status: pending' 또는 '[Content pending]' 없음
  2. 같은 상대 경로의 ko 파일 존재
  3. ko 본문 300자 이상 (스켈레톤/빈 본문 차단)
  4. ko frontmatter: locale: ko, tags 마지막이 ko
  5. ko 본문 en 복붙 방지 (en 본문과 90% 이상 동일하면 차단)

사용:
  python3 scripts/gate_promote_check.py            # 요약 출력
  python3 scripts/gate_promote_check.py --quiet    # 실패 목록만
"""
import glob, os, re, sys, difflib

ROOT = "/opt/data/workspace/wiki/content"
QUIET = "--quiet" in sys.argv


def read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def split_doc(text):
    """frontmatter / body 분리"""
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        try:
            end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
            return "\n".join(lines[1:end]), "\n".join(lines[end + 1:])
        except StopIteration:
            pass
    return "", text


def fm_get(fm, key):
    m = re.search(r"^%s:\s*(.+)$" % re.escape(key), fm, re.M)
    return m.group(1).strip() if m else ""


def is_stub(text):
    return "status: pending" in text[:4000] or "[Content pending]" in text[:4000]


def body_of(text):
    return split_doc(text)[1].strip()


def main():
    problems = []
    en_files = sorted(glob.glob(ROOT + "/en/sources/**/*.md", recursive=True))
    for en_path in en_files:
        rel = en_path.replace(ROOT + "/en/", "")
        ko_path = en_path.replace("/en/", "/ko/")
        en_text = read(en_path)

        if is_stub(en_text):
            problems.append(("en-stub", rel, "status: pending 또는 [Content pending] 잔존"))
            continue
        if not os.path.exists(ko_path):
            problems.append(("ko-missing", rel, "ko 파일 없음"))
            continue

        ko_text = read(ko_path)
        ko_fm, ko_body = split_doc(ko_text)
        en_body = body_of(en_text)

        if is_stub(ko_text):
            problems.append(("ko-stub", rel, "ko 파일이 아직 stub"))
        if len(ko_body) < 300:
            problems.append(("ko-short", rel, "ko 본문 %d자 (<300)" % len(ko_body)))
        if fm_get(ko_fm, "locale") != "ko":
            problems.append(("ko-locale", rel, "locale: ko 아님"))
        tags = fm_get(ko_fm, "tags").strip("[]").strip()
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        if not tag_list or tag_list[-1] != "ko":
            problems.append(("ko-tags", rel, "tags 끝이 ko 아님: %s" % tag_list))
        # en 복붙 방지
        if len(en_body) > 300 and len(ko_body) > 300:
            ratio = difflib.SequenceMatcher(None, en_body[:4000], ko_body[:4000]).ratio()
            if ratio > 0.9:
                problems.append(("ko-copy", rel, "en 원문 복붙 의심 (유사도 %.2f)" % ratio))

    if problems:
        for kind, rel, why in problems:
            print("BLOCKED %-11s %s -- %s" % (kind, rel, why))
        print("\nTotal BLOCKED: %d" % len(problems))
        return 1
    print("GATE OK: %d en source docs, ko 짝/본문/tags 모두 정상" % len(en_files))
    return 0


if __name__ == "__main__":
    sys.exit(main())
