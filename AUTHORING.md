# 문서 작성 가이드 (Authoring Guide)

`content/`에 새 문서를 추가하는 절차. 모든 문서는 마크다운으로 작성되며,
빌드(`scripts/wiki_builder.py` + `scripts/make_index.py`)가 HTML로 변환한다.

## 1. 파일 위치와 이름

```
content/<lang>/<kind>/<분야>/.../<파일명>.md
```

- `<lang>`: `ko` 또는 `en`. 양쪽에 **같은 상대 경로**로 두면 상단 Language 메뉴가
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
  상단 Language 메뉴가 상대 문서를 자동으로 가리킨다. 단독 버전 링크행은
  빌드가 제거한다.
- 이미지는 별도 파이프라인이 없으므로 외부 URL을 쓴다.
  `![설명](https://…)` 형식, `alt` 설명은 필수다 (캡션으로 렌더링된다).
  단독 문단의 이미지는 가운데 정렬 figure가 되고, 본문 중 이미지는
  lazy loading으로 읽힌다.   단독 이미지는 클릭하면 전체화면 라이트박스로
  확대된다 (내용이 빽빽한 아키텍처 그림용. 썸네일 위치에서 펼쳐지는
  Medium식 애니메이션, `scripts/zoom.js`. JS 없으면 즉시 열림으로 폴백.
  확대 중 스크롤하면 자동으로 줌아웃된다 (닫기는 스크롤·클릭·`Esc`).
  이미 외부 링크가 걸린 이미지는
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

아티클·논문 모두 **같은 4단계를 순서대로** 거친다. 단계를 건너뛰지 않는다
(흔한 실패: 수집 후 승격 없이 방치, 초안 채우기 생략):

1. **수집** (§5.1) — inventory JSON + 양 언어 stub 생성. 본문을 쓰지 않는다.
2. **초안 채우기** (§5.2) — `fetch_drafts.py`로 원문을 읽어 스켈레톤 본문 생성.
3. **승격** (§5.3) — stub마다 본문 완성 + frontmatter 확정 (`en` 먼저, §5.3 체크리스트).
4. **번역 + 검증** (§5.3) — `ko` 작성 후 §4 빌드로 확인.

**상태 판정 (공통).** 파일 앞부분에 `status: pending` 또는 `[Content pending]` 중
하나라도 있으면 미완성이다. 빌드는 이런 파일을 메인 목록에서 빼고
`pending.html`로 분리한다 (빌드 끝의 `NOTE: N article(s) are still stubs`가
남은 분량). 관련 스크립트 모두 앞 2000~4000자만 보고 판정하므로 전문 파싱 없이
고른다. `--full` 출력도 `status: pending`을 유지하므로 같은 기준으로 계속
걸리고, 마커를 지우는 순간 정식 문서로 취급되니 요약 완료 전까지 유지한다:

```bash
grep -rl "status: pending" content/en/sources/articles/ content/en/sources/papers/ \
  content/ko/sources/articles/ content/ko/sources/papers/
python3 scripts/fetch_drafts.py --kind all --dry-run --limit 5   # 처리 대상 목록
```

### 5.1 수집 — stub 만들기 (종류별 명령. 이 단계에서 본문을 쓰지 않는다)

공통 규칙: `--stubs`는 미작성 건만 양 언어에 만든다
(이미 있으면 0건이 정상). `source_url`은 중복 판정·출처 기준이니
지우거나 바꾸지 않는다.

**아티클 (RSS/Atom).**

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
- stub 상태에서는 빌드가 페이지를 렌더링하되 메인 포털 목록에는 넣지 않고
  `pending.html`로 분리한다.
- 새 피드를 추가하려면 세 곳을 함께 고친다:
  `collect_articles.py`의 `FEEDS` + `BLOG_SLUG`,
  `make_index.py`의 `BLOG_LABEL`. 폴더명(`content/<lang>/sources/articles/<slug>/`)은
  세 곳에서 동일해야 한다.

**논문 (HF Daily Papers).** `concepts/`, `guides/`는 수집 대상이 아니다
(수동 작성, §1 양식 준수).

```bash
python3 scripts/collect_articles.py --kind papers --date $(date -u +%F) --stubs
```

- `--date`를 생략하면 오늘(UTC) 기준이다.
- 기대 출력: `Total N items -> .index-backup/collected_papers.json` +
  `en: K new stub(s)`, `ko: K new stub(s)`.
- 생성물: `content/<lang>/sources/papers/<arxiv_id-대시형>.md`
  (예: `2609.04199` → `2609-04199.md`). 제목 슬러그형 파일명 금지.
- stub frontmatter는 `title`, `source_url`(arXiv abs URL), `blog: huggingface`,
  `arxiv_id`, `authors`, `published_date`, `locale`, `status: pending`만 담고,
  본문은 `[Content pending]` 한 줄이다.
- 선택 기준: 수집된 전건을 대상으로 한다. 주제·추천수로 자의 제외 금지.
  이미 쓴 논문은 `source_url` 기준 자동 제외된다.
- HF API 실패 (`fetch failed`) → `--date`가 `YYYY-MM-DD` 형식인지, 미래 날짜가
  아닌지 확인 후 재시도.

### 5.2 초안 채우기 — `fetch_drafts.py` (아티클·논문 공통, `--kind`만 다름)

수집이 끝나면 같은 단계로 초안을 채운다. 반드시 dry-run으로 대상을 먼저 확인한다.

```bash
# 아티클
python3 scripts/fetch_drafts.py --kind articles --dry-run --limit 5
python3 scripts/fetch_drafts.py --kind articles --limit 5 --write
# 논문
python3 scripts/fetch_drafts.py --kind papers --dry-run --limit 5
python3 scripts/fetch_drafts.py --kind papers --limit 5 --write
```

- 기대 출력: `Pending stubs in scope (<lang>/<kind>): N` 헤더 +
  건별 `robots(...)` / `fetch(...)` 경과 행 + `extract: N blocks` →
  `wrote draft summary -> ...`.
  dry-run은 `(cached, no file change)`로 끝나며 파일을 바꾸지 않는다.
- 읽는 원문: 아티클은 stub의 `source_url` HTML 그대로.
  논문은 arXiv HTML (`arxiv.org/html/<id>`, 실패시 `ar5iv.org/html/<id>`).
  PDF 파싱 금지.
- `--write` 후 파일 상태 (반드시 확인): `status: pending` 삭제됨(= pending 탈출),
  `description`·`tags`·`published` 자동 기입, 본문은 요약 스켈레톤.
  자동 `tags`는 `[source, <blog>, <lang>]`
  (논문은 `[source, paper, huggingface, <lang>]`) — 주제 태그는 §5.3에서 직접
  추가한다. 스켈레톤을 그대로 두지 말고 §5.3으로 간다.
- `--full`은 전문 초안으로 `status: pending`을 유지한다 (여전히 pending에 머무름).
  요약이 끝난 뒤 `status`를 지우고 §5.3을 적용한다.
- 실패시 행동 (공통): `extract: too few blocks` → stub 유지, 수동 작성 대상으로 보고.
  논문에서 arXiv HTML·ar5iv 둘 다 실패 → stub 그대로 두고 다음 stub으로.
  robots 차단 URL은 재시도하지 않는다.

### 5.3 승격 — 정식 문서로 만들기 (아티클·논문 공통. 매 stub마다 수행)

§5.2 출력물(또는 손으로 쓴 stub)을 아래 순서대로 처리한다.
`en`을 먼저 완성하고, 그 다음 같은 상대 경로에 `ko`를 만든다.
**이 절을 생략하면 글이 pending에 영원히 남는다.**

1. **본문 작성.** 스켈레톤을 완성형으로 확장한다 (§1·§3 양식).
   `--full` 출력이면 먼저 요약하고 `status: pending`을 지운다.
2. **`tags`에 주제 태그 추가.** fetch가 넣어준 뼈대
   (`[source, <blog>, en]` / `[source, paper, huggingface, en]`)에 주제 태그를
   끼운다 (`[source, paper, machine-learning, en]`). 끝 언어 태그는 유지한다 (§2).
3. **날짜 키 확인.** `published`(fetch 출력) 또는 `published_date`(stub/`--full` 출력)
   중 하나가 `YYYY-MM-DD` 형식이면 된다. 둘 다 넣지 않는다.
4. **종류별 보존 키 (삭제·변경 금지).**

   | 종류 | 유지해야 할 키 |
   |---|---|
   | 아티클 | `source_url`, `blog` |
   | 논문 | `source_url`(arXiv abs URL), `blog: huggingface`, `arxiv_id`, `authors` |

   HF 페이지 URL은 본문 References에만 적는다.
5. **`ko` 작성.** 같은 상대 경로 (`content/ko/...` ↔ `content/en/...`, §1).
   본문은 `en` 완성본을 한국어로 번역·요약(원문 복붙 금지),
   `title`·`description` 한국어 작성, `tags` 끝을 `ko`로, `locale: ko`,
   나머지 키(`source_url`·`blog`·`arxiv_id`·`authors`·날짜)는 `en`과 동일.
6. **빌드 검증** (§4): `Build verified` + 포털 Recent·Navigator 노출 +
   언어 버튼 상호 이동 확인. `en` 단독 완성 금지
   (`ko` 없으면 언어 버튼이 포털로 폴백).

예시 완성형 (아티클, `ko`):

  ```yaml
  ---
  title: "Iceberg 머티리얼라이즈드 뷰로 Spark 쿼리 가속하기"
  description: "한 줄 요약."
  tags: [source, aws-big-data, spark, iceberg, ko]
  locale: ko
  source_url: "https://aws.amazon.com/blogs/big-data/..."
  blog: aws-big-data
  published: "2026-09-10"
  ---
  ```

예시 완성형 (논문, `ko`):

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

**금지 / 필수 체크리스트.**

- 금지: PDF 파싱, `source_url` 변경·삭제, 논문의 제목 슬러그형 파일명,
  수집건의 주제 자의 제외, 스켈레톤 그대로 방치, §5.3 생략.
- 필수: 양 언어 동일 상대 경로, 깨진 수식·표·그림은 PDF와 대조 수정
  (논문만), 매 stub마다 §5.3 1→6 완주.

### 5.4 개념 — sources로 보강·신설 (`concepts/`)

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
| Language 메뉴가 포털로 간다 | 반대 언어 쪽에 같은 경로 파일이 없음 |
| 링크가 404다 | `.md`가 아닌 `.html`로 직접 연결했거나, 이동·개명한 경로를 가리킴 |
| 목차(TOC)가 비었다 | `##` 섹션이 없음. TOC는 h2에서 자동 생성 |
| 수집한 글이 포털에 안 보인다 | `status: pending` stub은 정상적으로 `pending.html`로만 간다. §5.3 승격 후 `status` 제거 확인 |
| 아티클 stub이 pending에만 있다 | `fetch_drafts.py --kind articles --write` 미실행 또는 `--write` 누락. §5.2→§5.3 순서 준수 |
| 논문 stub이 pending에만 있다 | `fetch_drafts.py --kind papers --write` 미실행 또는 `--write` 누락 |
| fetch 후에도 Recent에 안 보인다 | `--full`로 써서 `status` 유지 중. 요약 후 `status` 제거 (§5.3.1) |
| 같은 논문이 중복 수집된다 | `source_url`을 abs가 아닌 html/ar5iv URL로 바꿈 |
| 오늘 날짜 수집이 비어 있다 | 미래 날짜 지정 또는 API 장애. `--date` 확인 후 재시도 |
