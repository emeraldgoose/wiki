# 문서 작성 가이드 (Authoring Guide)

`content/`에 새 문서를 추가하는 절차. 모든 문서는 마크다운으로 작성되며,
빌드(`scripts/wiki_builder.py` + `scripts/make_index.py`)가 HTML로 변환한다.

## 1. 파일 위치와 이름

```
content/<lang>/<kind>/<분야>/.../<파일명>.md
```

- `<lang>`: `ko` 또는 `en`. 양쪽에 **같은 상대 경로**로 두면 상단 언어 버튼이
  두 문서를 서로 오간다.
- `<kind>`: 문서 종류. 첫 경로가 곧 포털 분류가 된다.
  - `concepts/` → 개념, `guides/` → 가이드
  - `sources/papers/` → 논문, `sources/articles/` → 아티클
- 파일명은 kebab-case 영문 (`build-rag.md`). 한글 파일명·공백 금지.
- `index.md`라는 이름은 쓰지 않는다 (포털 인덱스와 충돌하므로 빌드가 건너뛴다).

## 2. Frontmatter

파일 맨 앞 `---` 블록에 메타데이터를 적는다. 필수 4종 + 선택:

```yaml
---
title: "문서 제목"
description: "한 줄 요약. 포털 목록과 검색에 쓰인다."
tags: [guide, ai-engineering, rag, ko]
locale: ko
published: 2026-10-09
---
```

- `tags`: 첫 태그는 종류 태그(`guide`, `concept`, `paper`, `source` 등),
  그 뒤에 주제 태그. 주제 태그(`ai-engineering`, `data-engineering` 등)가
  포털의 카테고리 열을 만든다. 언어 태그(`ko`/`en`)를 끝에 붙인다.
- 선택 키: `source_url` (원문 링크), `blog` (출처명), `authors`,
  `arxiv_id`, `published_date`.
- 원문 기반 정리글은 `source_url`을 반드시 남긴다.

## 3. 본문 규칙

- 본문은 `# 문서 제목`으로 시작한다 (frontmatter `title`과 동일하게 —
  빌드가 중복을 제거한다).
- 섹션은 `##`, 하위는 `###`부터. `#`은 제목 한 번에만 쓴다.
- 지원하는 문법: 굵게/기울임/인라인 코드, 순서·비순서 목록, 표,
  인용(`>`), 코드펜스, 구분선, 이미지(`![alt](url)`), 수식(`$…$`, `$$…$$`).
- 문서 간 링크는 **상대경로 `.md`** 로 건다. 빌드가 `/<lang>/....html`로
  바꿔준다. 예: `[RAG 가이드](../ai-engineering/build-rag.md)`
- 바깥 링크(`http…`)는 자동으로 새 탭으로 열린다.
- **"English version" / "한국어 버전" 같은 본문 링크를 넣지 않는다.**
  상단 언어 버튼이 상대 문서를 자동으로 가리킨다. 단독 버전 링크행은
  빌드가 제거한다.
- 이미지는 별도 파이프라인이 없으므로 외부 URL을 쓴다.
  `![설명](https://…)` 형식, `alt` 설명은 필수다 (캡션으로 렌더링된다).
  단독 문단의 이미지는 가운데 정렬 figure가 되고, 본문 중 이미지는
  lazy loading으로 읽힌다. 단독 이미지는 클릭하면 전체화면 라이트박스로
  확대된다 (내용이 빽빽한 아키텍처 그림용. 이미 외부 링크가 걸린 이미지는
  기존 링크 유지). 빌드가 리사이즈하지 않으므로 원본은 적정
  크기로 고르고, 브라우저가 본문 폭(`--measure`)에 맞춰 축소한다.
  화면별 대응은 CSS가 담당한다 (`max-width: 100%; height: auto`).
- 수식은 TeX로 쓴다. 인라인 `$…$`, 디스플레이 `$$…$$`
  (`\(…\)`, `\[…\]`도 가능). 빌드가 MathJax(CDN)를 해당 페이지만에
  붙여 렌더링하므로 `$` 앞뒤로 공백을 두지 않는다 (`$100` 같은 금액은
  TeX 문자(`\`, `^`, `_`, `{`, `=`)가 없어 수식으로 오인되지 않는다).
  오프라인에서는 TeX 원문이 그대로 보인다.

## 4. 빌드와 확인

```bash
python3 scripts/wiki_builder.py   # content/ → static/en, static/ko
python3 scripts/make_index.py     # 포털 인덱스, 랜딩, _redirects 생성
python3 scripts/serve_wiki.py 8900  # 로컬 확인 (http://localhost:8900/)
```

- 빌드 끝의 `wrote N pages`와 `Build verified`를 확인한다.
- 새 글이 포털 Recent와 Navigator에 들어갔는지, 상대 언어 문서가 있으면
  언어 버튼이 그 문서를 가리키는지 본다.
- `static/`은 빌드 산출물이라 git에 올리지 않는다 (`.gitignore`).

## 5. 외부 문서 가져오기 (수집 파이프라인)

### 5.1 아티클 — RSS 자동 수집

아티클(`sources/articles/`)은 RSS/Atom 피드에서 자동 수집한다.

```bash
python3 scripts/collect_articles.py --year 2026
python3 scripts/collect_articles.py --year 2026 --stubs   # stub까지 생성
```

- 수집 대상(`scripts/collect_articles.py` 상단 `FEEDS`):
  `netflix`, `airbnb`, `spotify`, `aws-big-data`, `databricks`.
- 동작: 각 피드를 읽어 올해(`--year`) 이후 발행글만 남기고,
  `.index-backup/collected.json`에 제목·URL·날짜·출처 목록을 쓴다.
  이 단계에서는 본문을 쓰지 않는다.
- `--stubs`를 붙이면 미작성 글마다 양 언어에 자리표시자를 만든다:
  `content/<lang>/sources/articles/<slug>/<제목슬러그>.md`
  (`<slug>`은 `BLOG_SLUG` 매핑. 파일명은 제목에서 뽑은
  `slugify` 결과이므로 발행처 원제와 대략 일치한다).
- stub frontmatter는 `title`, `source_url`, `blog`,
  `published_date`, `locale`, `status: pending`만 담고, 본문은
  `[Content pending]` 한 줄이다.
- 중복 판정은 `source_url` 기준이다. 피드 URL의 추적 쿼리(`?...`)와
  프래그먼트(`#...`)를 떼고 정규화한 뒤 양 언어 기존 파일과 비교하므로,
  이미 쓴 글은 다시 수집되지 않는다. `source_url`을 지우거나 바꾸면
  중복 검사가 깨지니 유지한다.
- stub을 정식 문서로 바꾸는 법: `status: pending` 줄을 지우고,
  `description`, `tags` (§2 규칙), `published`를 채운 뒤 본문을 작성한다.
  수집·초안 스크립트는 `en`만 만든다. `en` 정식 문서가 완성되면 에이전트가
  이를 기반으로 `ko` 문서를 만든다: 같은 상대 경로
  (`content/ko/...` ↔ `content/en/...`, §1), 본문은 `en` 완성본을 한국어로
  번역·요약(원문 복붙 금지), frontmatter는 `title`·`description` 한국어 작성,
  `tags` 끝을 `ko`로, `locale: ko`, `source_url`·`blog`·`published`는 `en`과
  동일하게 유지한다. `ko` 대응이 없으면 언어 버튼이 포털로 폴백되므로
  `en` 단독 완성 상태로 두지 않는다.
  예시 완성형:

  ```yaml
  ---
  title: "Accelerating Spark queries with Iceberg materialized views"
  description: "한 줄 요약."
  tags: [source, aws-big-data, spark, iceberg, ko]
  locale: ko
  source_url: "https://aws.amazon.com/blogs/big-data/..."
  blog: aws-big-data
  published: "2026-09-10"
  ---
  ```

- stub 상태에서는 빌드가 페이지를 렌더링하되 메인 포털 목록에는 넣지 않고
  `pending.html`로 분리한다. 빌드 끝의
  `NOTE: N article(s) are still stubs`가 남은 분량이다.
- 초안 판정 (본문을 끝까지 읽지 않고 고르는 법): 파일 앞부분(head) 마커만 본다.
  `status: pending` 또는 `[Content pending]` 중 하나라도 있으면 초안이다.
  `wiki_builder.py`·`make_index.py`·`fetch_drafts.py` 모두 앞 2000~4000자만 읽고
  판정하므로 전문 파싱이 필요 없다. `--full` 원문 초안도 `status: pending`을
  유지하므로 같은 기준으로 계속 골라지고, 마커를 지우는 순간 정식 문서로
  취급되니 요약 완료 전까지 유지한다. 고르는 명령:

  ```bash
  grep -rl "status: pending" content/en/sources/articles/ content/ko/sources/articles/
  python3 scripts/make_index.py --dry-run | grep pending   # 개수만 확인
  python3 scripts/fetch_drafts.py --dry-run --limit 5      # 처리 대상 목록
  ```
- 새 피드를 추가하려면 세 곳을 함께 고친다:
  `collect_articles.py`의 `FEEDS` + `BLOG_SLUG`,
  `make_index.py`의 `BLOG_LABEL`. 폴더명(`content/<lang>/sources/articles/<slug>/`)은
  세 곳에서 동일해야 한다.

### 5.2 논문 — 수동 수집 (HF Daily Papers + arXiv HTML)

논문(`sources/papers/`)은 자동 수집 스크립트가 없으므로 수동으로 가져온다.
`concepts/`, `guides/`도 마찬가지다 (§1 양식 준수).

1. 고르기: [HuggingFace Daily Papers](https://huggingface.co/papers)에서
   고른다. 날짜별(`?date=YYYY-MM-DD`)·주별 보기가 있고,
   개별 페이지(`https://huggingface.co/papers/<arxiv_id>`)에 요약·코드 링크·추천수가 있다.
2. 읽기: arXiv PDF를 직접 파싱하지 말고 HTML 버전을 쓴다.
   - 공식 HTML: `https://arxiv.org/html/<arxiv_id>`
     (예: `abs/2609.04199` → `html/2609.04199`. abs 페이지의 PDF 링크 밑 "HTML" 버튼.
     2023-12 이후 TeX 제출분부터 제공되는 실험 기능이라 최신 논문은 대부분 된다)
   - 구버전·변환 실패분은 미러: `https://ar5iv.org/html/<arxiv_id>`
     (arxiv의 `x`를 `5`로 바꾸면 된다)
3. 저장: `content/<lang>/sources/papers/`에 파일을 만든다.
   파일명은 arXiv ID형(`2609-04199.md`) 또는 제목 슬러그형(`JIT-Agent.md`) 중 하나.
   양 언어에 **같은 상대 경로**로 두면 언어 버튼이 서로 오간다.
   frontmatter 완성형:

  ```yaml
  ---
  title: "논문 제목"
  description: "한 줄 요약. 포털 목록과 검색에 쓰인다."
  tags: [source, paper, machine-learning, ko]
  locale: ko
  source_url: "https://arxiv.org/abs/xxxx.xxxxx"
  arxiv_id: "xxxx.xxxxx"
  published_date: 2026-08-30
  authors: ["홍길동", "김철수"]
  ---
  ```

- `source_url`은 반드시 arXiv abs URL로 남긴다 (중복 판정·출처 표기의 기준).
  HF 페이지 URL은 본문 References에 따로 적는다.
- HTML 변환이 깨지는 수식·표·그림은 PDF와 대조해서 고치고,
  포털 footer의 "원문 대조 검증 완료" 기준을 맞춘다.

### 5.3 개념 — sources로 보강·신설 (`concepts/`)

개념 문서는 여러 원전(source)을 종합하는 문서다. 단일 원문 복사가 아니다.
`sources/`에 글을 쓸 때마다 관련 개념을 확인한다:

- 기존 개념이 있으면 보강한다:
  1. 본문 맨 앞 `**원전**: ...` 줄에 새 원전을 덧붙인다.
  2. 새 내용이 들어갈 섹션을 추가·수정한다. 어느 원전에서 왔는지
     소제목·문장에 명시한다 (`(StepGuard에서 차용)` 방식).
  3. 맨 끝 `## 관련 원전`에 상대경로 `.md` 링크를 추가한다 (§3 규칙).
- 새 개념이 등장하면 문서를 만든다:
  `content/<lang>/concepts/<분야>/<kebab-case>.md`
  (예: `content/ko/concepts/ai-engineering/harness.md`).
  양 언어에 **같은 상대 경로**로 둔다. frontmatter:

  ```yaml
  ---
  title: "개념명 (English Name)"
  description: "한 줄 요약."
  tags: [concept, ai-engineering, harness, ko]
  locale: ko
  ---
  ```

  본문 최소 구조: `# 제목` → `**원전**: ...` → 핵심 섹션(`##`) →
  `## 관련 원전` → `## 관련 가이드` (있으면).
- `## 관련 원전`에는 개념을 뒷받침하는 `sources/papers/...`,
  `sources/articles/...` 링크를, `## 관련 가이드`에는 이를 쓰는
  `guides/...` 링크를 건다. 링크가 없으면 섹션을 생략한다.

## 6. 흔한 실수

| 증상 | 원인 |
|---|---|
| 포털에 글이 안 보인다 | `index.md`로 저장했거나, `tags`가 비어 카테고리 추론 실패 |
| 언어 버튼이 포털로 간다 | 반대 언어 쪽에 같은 경로 파일이 없음 |
| 링크가 404다 | `.md`가 아닌 `.html`로 직접 연결했거나, 이동·개명한 경로를 가리킴 |
| 목차(TOC)가 비었다 | `##` 섹션이 없음. TOC는 h2에서 자동 생성 |
| 수집한 글이 포털에 안 보인다 | `status: pending` stub은 정상적으로 `pending.html`로만 간다. 본문 작성 후 `status` 제거 |
