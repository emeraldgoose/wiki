# 문서 작성 가이드 (Authoring Guide)

`content/`에 새 문서를 추가하는 절차. 모든 문서는 마크다운으로 작성되며,
빌드(`scripts/wiki_builder.py` + `scripts/make_index.py`)가 HTML로 변환한다.

> **에이전트 필독.** 이 문서는 설명문이 아니라 **실행 계약**이다.
> `content/`를 만지는 에이전트는 §0 → §7 순서로 읽고, §7의 런북을 그대로 따른다.
> 같은 저장소 상태에서는 어떤 에이전트가 실행해도 **같은 파일, 같은 순서, 같은 결과**가
> 나와야 한다.

## 0. 에이전트 실행 계약 (필독)

### 0.1 작업 유형 판별

사용자 요청을 아래 표의 **위에서부터 첫 번째로 해당하는 유형**으로 분류한다.
애매하면 임의로 해석하지 말고 **B(기존 backlog)** 로 간주한다.

| 유형 | 요청 예시 | 시작 지점 |
|---|---|---|
| **A. 새 수집 배치** | "오늘 논문/아티클 수집해줘", 날짜 지정 | §7.1 |
| **B. 기존 backlog** | "남은 것 마저", "전체 정리", "stub 처리" | §7.2 |
| **C. 개념/가이드** | "개념 문서 써줘", "가이드 추가" | §7.3 |
| **D. 지정 문서 1건** | 파일 경로/제목을 직접 지정 | §7.4 |

### 0.2 고정 규칙

1. **한 번에 문서 쌍 1건만 승격한다.** `fetch_drafts.py`는 최대 5건까지 초안을
   만들 수 있지만, 본문 작성·번역은 반드시 1건씩 끝낸다.
2. **순서는 게이트가 정한다.** `--next`가 출력한 `NEXT:` 경로를 그대로 처리한다.
   파일을 임의로 고르거나 정렬을 바꾸지 않는다. 게이트의 고정 우선순위
   (`stub` → `draft` → 본문/제목 → 짝 → 메타데이터)와 경로명 순서를 따른다.
3. **stub과 draft는 산출물이 아니다.** `status: pending`, `[Content pending]`,
   `Draft summary auto-extracted`, `RAW DRAFT`가 남아 있으면 미완성이다.
4. **en 먼저, ko는 그다음.** ko를 `fetch_drafts.py`로 채우지 않는다.
   완성된 en을 읽고 한국어로 번역·요약한다.
5. **`source_url`은 불변.** 수집·중복 판정의 기준이므로 바꾸거나 지우지 않는다.
6. **논문 파일명은 arXiv ID** (`2610.18868` → `2610-18868.md`). 제목 슬러그 금지.
7. **커밋 전 `--staged`, 푸시 전 hook.** `--no-verify`로 우회하지 않는다.
8. **실패를 숨기지 않는다.** 처리 못 한 경로와 이유를 `BLOCKED`로 남기고,
   완료라고 보고하지 않는다.
9. **`static/`은 직접 수정하지 않는다.** 소스는 `content/`와 `scripts/`뿐이다.

### 0.3 상태 머신

```text
stub ──fetch --write──▶ draft ──en 재작성──▶ en 완성 ──ko 번역──▶ 짝 완성 ──gate──▶ done
```

- `stub`: `status: pending` 또는 `[Content pending]`
- `draft`: `Draft summary auto-extracted` 또는 `RAW DRAFT`
- `done`: 게이트가 `Gate: OK`라고 판정한 상태 **만** 해당

### 0.4 30초 시작

```bash
# 이번에 만진 파일이 있으면 이것부터
python3 scripts/gate_promote_check.py --next --worktree

# 할 일이 없고 저장소 backlog를 봐야 하면
python3 scripts/gate_promote_check.py --next
```

`NEXT:`가 나오면 §7.5로 간다. `DONE`이면 §7.7 형식으로 보고한다.

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
python3 scripts/check_ko_papers.py   # ko 논문 정책 검사
python3 scripts/wiki_builder.py      # content/ → static/en, static/ko
python3 scripts/make_index.py        # 포털 인덱스, 랜딩, _redirects 생성
python3 scripts/serve_wiki.py 8900   # 로컬 확인 (http://localhost:8900/)
```

- `check_ko_papers.py`는 `errors: 0`이어야 한다.
- 빌드 끝의 `wrote N pages`와 `Build verified`를 확인한다.
- `NOTE: N article(s) are still stubs`는 **저장소 전체**에 남은 stub 수다.
  이번 배치 완료는 `gate_promote_check.py --worktree`의 `Gate: OK`로,
  저장소 전체 완료는 `--next`(플래그 없이)의 `Gate: DONE`으로 판정한다.
  이번에 새로 만든 stub이 남아 있으면 물론 미완성이다.
- 새 글이 포털 Recent와 Navigator에 들어갔는지, 상대 언어 문서가 있으면
  언어 버튼이 그 문서를 가리키는지 본다.
- `static/`은 빌드 산출물이라 git에 올리지 않는다 (`.gitignore`).

## 5. 외부 문서 가져오기 (수집 파이프라인)

아티클·논문 모두 **같은 4단계를 순서대로** 거친다. 단계를 건너뛰지 않는다
(흔한 실패: 수집 후 승격 없이 방치, 초안 채우기 생략):

1. **수집** (§5.1) — inventory JSON + 양 언어 stub 생성. 본문을 쓰지 않는다.
   **이 단계는 완료가 아니다.**
2. **초안 채우기** (§5.2) — `fetch_drafts.py`로 원문을 읽어 스켈레톤 본문 생성.
   **스켈레톤도 완료가 아니다.**
3. **승격** (§5.3) — stub마다 본문 완성 + frontmatter 확정 (`en` 먼저, §5.3 체크리스트).
4. **번역 + 검증** (§5.3) — `ko` 작성 후 §4 빌드로 확인.

### 5.0 강제 게이트 — 루프의 종료 조건

stub 생성이나 `fetch_drafts.py --write` 직후에는 절대 멈추지 않는다. 아래
게이트가 `Gate: OK`가 될 때까지 §5.1→§5.3을 반복한다.

```bash
python3 scripts/gate_promote_check.py --next --worktree  # 이번 배치의 다음 1건
python3 scripts/gate_promote_check.py --worktree         # 이번 배치 검사
python3 scripts/gate_promote_check.py --staged           # git add 후, 커밋 전 (hook 자동)
python3 scripts/gate_promote_check.py                    # 저장소 전체 감사
python3 scripts/gate_promote_check.py --changed --base origin/main  # push/CI
```

- `stub`(`status: pending` / `[Content pending]`)과 `draft`
  (`Draft summary auto-extracted` / `RAW DRAFT`)는 **둘 다 실패**다.
  파일이 존재한다고 완료가 아니다.
- en/ko 짝이 없거나, 짝이 아직 stub/draft면 실패다.
- 새로 추가하거나 승격하는 문서는 frontmatter·태그·H1·본문 언어 검사를 통과해야 한다.
- `--next --worktree`가 항목을 출력하는 동안은 작업이 남아 있다는 뜻이다.
  그 1건을 §5.3까지 처리하고 다시 실행한다.
  `Gate: DONE — no blocking work in this batch`가 **이번 배치**의 종료 조건이다.
  같은 명령이 이번 세션에서 만진 파일만 보므로, 레거시 backlog에 발목 잡히지 않고
  방금 만든 stub부터 끝낼 수 있다.
- 전체 backlog는 `--next`(플래그 없이)로 본다. 저장소 전체 완료는
  `gate_promote_check.py`의 `Gate: OK`다.
- `.githooks/pre-commit`·`pre-push`가 같은 검사를 실행한다. 우회하지 않는다
  (`git commit --no-verify` 금지). 새 clone은 `git config core.hooksPath .githooks`.

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
python3 scripts/gate_promote_check.py --next                     # 초안/짝 누락까지 포함
```

게이트는 `status: pending`뿐 아니라 `Draft summary auto-extracted`/`RAW DRAFT`
스켈레톤과 en/ko 짝 누락도 미완성으로 판정한다.

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
- `--write`가 만든 `Draft summary auto-extracted` 본문은 **초안일 뿐**이다.
  게이트는 이 마커를 미완성으로 판정한다. 출력 후 §5.3으로 바로 간다.
- 실패시 행동 (공통): `extract: too few blocks` → stub을 유지하고 **수동 작성 대상**으로
  기록한다. 논문에서 arXiv HTML·ar5iv 둘 다 실패 → stub을 지우지 말고 `BLOCKED`로
  기록한다. robots 차단 URL은 재시도하지 않는다.
  **건너뛴 것을 숨기지 않는다.** 새로 만든 stub이 남아 있으면 그 배치는 커밋할 수 없다
  (pre-commit이 차단). 실패 경로와 이유를 §7.6 형식으로 보고한다.

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
   **새로 쓰는 문서는 `published_date`로 통일한다.** 수집일이 아니라 원문 게시일을 쓴다.
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
7. **게이트 통과** (§5.0):
   `python3 scripts/gate_promote_check.py --worktree`가 `Gate: OK`여야
   그 문서 쌍의 승격이 끝난 것이다. `--next --worktree`로 다음 1건을 꺼내
   1→7을 반복한다. 전체 backlog를 처리 중이면 `--next`(플래그 없이)를 쓴다.

예시 완성형 (아티클, `ko`):

  ```yaml
  ---
  title: "Iceberg 머티리얼라이즈드 뷰로 Spark 쿼리 가속하기"
  description: "한 줄 요약."
  tags: [source, aws-big-data, spark, iceberg, ko]
  locale: ko
  source_url: "https://aws.amazon.com/blogs/big-data/..."
  blog: aws-big-data
  published_date: 2026-09-10
  ---
  ```

예시 완성형 (논문, `ko`):

  ```yaml
  ---
  title: "논문 제목"
  description: "한 줄 요약. 포털 목록과 검색에 쓰인다."
  tags: [source, paper, huggingface, machine-learning, ko]
  locale: ko
  source_url: "https://arxiv.org/abs/xxxx.xxxxx"
  arxiv_id: "xxxx.xxxxx"
  blog: huggingface
  published_date: 2026-08-30
  authors: ["홍길동", "김철수"]
  ---
  ```

**금지 / 필수 체크리스트.**

- 금지: PDF 파싱, `source_url` 변경·삭제, 논문의 제목 슬러그형 파일명,
  수집건의 주제 자의 제외, 스켈레톤 그대로 방치, §5.3 생략.
- 필수: 양 언어 동일 상대 경로, 깨진 수식·표·그림은 PDF와 대조 수정
  (논문만), 매 stub마다 §5.3 1→7 완주.

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
| stub만 만들고 작업이 끝난 것처럼 보인다 | §5.0 게이트를 실행하지 않음. `gate_promote_check.py --next`가 남은 1건을 알려준다 |
| `--write` 초안에서 작업이 멈춘다 | `Draft summary auto-extracted` 본문을 완성본으로 착각함. §5.3.1로 다시 쓴다 |
| 커밋이 `BLOCKED stub`으로 거부된다 | 정상 동작. 해당 문서를 §5.3까지 승격한 뒤 다시 커밋한다 |

## 7. 에이전트 실행 런북 (복붙용)

이 절은 **아무것도 모르는 에이전트가 그대로 실행하는 순서**다. 모든 명령은
저장소 루트(`wiki/`)에서 실행한다. 명령·인자·순서를 임의로 바꾸지 않는다.
같은 상태에서 시작하면 항상 같은 `NEXT` 파일이 나온다.

### 7.1 A. 새 수집 배치

**1) 종류 선택**

- 아티클(RSS/Atom)이면 아래 명령에서 `articles`를 쓴다.
- 논문(HF Daily Papers)이면 아래 명령에서 `papers`를 쓴다.

**2) 수집 (stub 생성, 아직 완료 아님)**

```bash
# 아티클
python3 scripts/collect_articles.py --year 2026 --stubs

# 논문
python3 scripts/collect_articles.py --kind papers --date $(date -u +%F) --stubs
```

기대 출력: `en: K new stub(s)`, `ko: K new stub(s)`.
`en`/`ko` 양쪽에 stub이 생긴다. **이 단계에서 본문을 쓰지 않는다.**

**3) en 초안 채우기 (dry-run 먼저)**

```bash
# 아티클
python3 scripts/fetch_drafts.py --kind articles --lang en --dry-run --limit 5
python3 scripts/fetch_drafts.py --kind articles --lang en --limit 5 --write

# 논문
python3 scripts/fetch_drafts.py --kind papers --lang en --dry-run --limit 5
python3 scripts/fetch_drafts.py --kind papers --lang en --limit 5 --write
```

- `--lang en`을 명시한다. **ko를 fetch하지 않는다.**
- `--write` 출력의 `Draft summary auto-extracted`는 초안이다.
- `extract: too few blocks` 또는 fetch 실패는 §7.6으로 간다.

**4) 게이트가 시키는 순서대로 1건씩 승격**

```bash
python3 scripts/gate_promote_check.py --next --worktree
```

`NEXT:` 경로를 §7.5로 처리하고, 다시 같은 명령을 실행한다.
`Gate: DONE`이 될 때까지 반복한다.

**5) 배치 마감**

```bash
git status --short                         # 의도하지 않은 파일 확인
git add -A
python3 scripts/gate_promote_check.py --worktree
python3 scripts/gate_promote_check.py --staged
python3 scripts/check_ko_papers.py
python3 scripts/wiki_builder.py
python3 scripts/make_index.py
```

모두 통과하면 커밋·푸시한다. `--staged`는 반드시 `git add -A` 뒤에 실행한다.
실패하면 스테이징을 유지한 채 해당 파일을 고치고 다시 `git add -A`부터 실행한다.

### 7.2 B. 기존 backlog

새로 수집하지 않는다. 저장소 전체에서 게이트가 고른 첫 항목을 처리한다.

```bash
python3 scripts/gate_promote_check.py --next
```

출력된 `NEXT:` 경로 1건만 §7.5로 끝낸다. 그다음 다시 `--next`를 실행한다.
전체 backlog가 0이 될 때까지 반복한다. 1건을 끝낼 때마다
`--next --worktree`가 `Gate: DONE`인지 확인하고, 배치를 마감할 때는 §7.1 5)를
그대로 실행한다. 중간에 새로 만진 파일이 있으면 `--next --worktree`로 범위를
좁혀도 된다.

### 7.3 C. 개념/가이드

`concepts/`, `guides/`는 수집·fetch 대상이 아니다. **양 언어를 직접 작성한다.**

```text
content/en/concepts/<분야>/<kebab-case>.md
content/ko/concepts/<분야>/<kebab-case>.md
content/en/guides/<분야>/<kebab-case>.md
content/ko/guides/<분야>/<kebab-case>.md
```

- frontmatter: `title`, `description`, `tags`, `locale`
- `tags` 끝은 `en`/`ko`
- 본문: `# 제목` → `**원전**: ...` → `##` 섹션 → `## 관련 원전` → `## 관련 가이드`
- 문서 간 링크는 상대경로 `.md`
- en/ko 제목·본문을 서로 복붙하지 않는다

게이트는 현재 `sources/`만 검사하므로 concepts/guides는 빌드와 수동 확인으로
검증한다. 양쪽 파일 존재, `locale`, 태그 끝 언어, H1, 링크 404 여부를 확인한다.

### 7.4 D. 지정 문서 1건

경로를 직접 받았으면 그 파일만 처리한다. URL만 받았고 기존 파일이 없으면
§7.5.1 템플릿으로 새 파일을 만들고 원문을 직접 읽어 본문을 쓴다
(수집 스크립트는 임의 URL을 받지 않는다).

1. 파일을 읽고 상태를 판정한다.
   - `status: pending`/`[Content pending]` → stub
   - `Draft summary auto-extracted`/`RAW DRAFT` → draft
   - 둘 다 없고 en/ko 짝이 있으면 complete
2. stub이면 frontmatter와 `source_url`을 확인한다.
   - 있으면 `fetch_drafts.py --kind ... --only 'content/en/...' --limit 1 --write`
   - frontmatter 구분자(`---`)가 없으면 기존 `title:`/`source_url:`/`blog:`/
     `published_date:` 줄을 `---`로 감싼다. 값은 그대로 유지한다.
   - 메타데이터 자체가 없으면 §7.5.1 템플릿으로 frontmatter를 먼저 만든다
3. draft면 fetch를 다시 돌리지 말고 §7.5.2로 바로 간다.
4. ko가 없으면 §7.5.3으로 번역한다.
5. `gate_promote_check.py --worktree`로 확인한다.
6. 1건만 처리해도 §7.1 5)의 검사·스테이징·보고를 수행한다.

### 7.5 한 문서 쌍 승격 절차 (정확히 이 순서)

1. `--next`가 지정한 `NEXT:` 경로를 연다.
2. `NEXT:`가 `content/ko/...`이면 같은 상대 경로의 `content/en/...`을 먼저 연다.
   en 파일의 상태를 확인한다 (stub / draft / complete).
3. en이 stub이면 해당 파일만 fetch한다.

   ```bash
   python3 scripts/fetch_drafts.py --kind <articles|papers> --lang en \
     --only 'content/en/sources/<kind>/<파일>.md' --limit 1 --write
   ```
4. en 본문을 실제 요약으로 다시 쓴다. `Draft summary auto-extracted`,
   `[Content pending]`, `status: pending`을 모두 제거한다.
5. frontmatter를 §7.5.1 템플릿으로 확정한다.
6. 같은 상대 경로의 ko 파일을 §7.5.3 규칙으로 작성한다.
7. `python3 scripts/gate_promote_check.py --next --worktree`를 다시 실행한다.
   `NEXT:`가 나오면 그 파일 하나만 고친다.
8. `--worktree`가 `Gate: OK`가 되면 §7.1 5)의 검사·스테이징을 수행하고
   §7.7 형식으로 보고한다.

#### 7.5.1 Frontmatter 템플릿

**논문 en:**

```yaml
---
title: "Actual Paper Title"
description: "One-line summary."
tags: [source, paper, huggingface, agents, en]
locale: en
source_url: "https://arxiv.org/abs/2610.18868"
arxiv_id: "2610.18868"
authors: ["Author One", "Author Two"]
blog: huggingface
published_date: 2026-10-13
---
```

**논문 ko:**

```yaml
---
title: "논문 제목의 한국어 번역"
description: "한 줄 한국어 요약."
tags: [source, paper, huggingface, agents, ko]
locale: ko
source_url: "https://arxiv.org/abs/2610.18868"
arxiv_id: "2610.18868"
authors: ["Author One", "Author Two"]
blog: huggingface
published_date: 2026-10-13
---
```

**아티클 en:**

```yaml
---
title: "Original Article Title"
description: "One-line summary."
tags: [source, aws-big-data, data-engineering, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/..."
blog: aws-big-data
published_date: 2026-09-10
---
```

**아티클 ko:**

```yaml
---
title: "원문 제목의 한국어 번역"
description: "한 줄 한국어 요약."
tags: [source, aws-big-data, data-engineering, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/..."
blog: aws-big-data
published_date: 2026-09-10
---
```

규칙:

- en의 `title`·`description`은 영어, ko는 한국어로 쓴다.
- 날짜는 `published_date` 하나만. `published`와 동시에 넣지 않는다.
- `tags`는 `source`로 시작하고 언어 태그로 끝난다. 중복 태그 금지.
- 논문은 `arxiv_id`, `authors`, `blog: huggingface`를 반드시 유지한다.
- 아티클은 `source_url`, `blog`를 반드시 유지한다.
- `source_url`은 수집 당시 값을 바꾸지 않는다.

#### 7.5.2 본문 템플릿

**en:**

```markdown
# Actual Paper Title

**Source**: [arXiv:2610.18868](https://arxiv.org/abs/2610.18868) · **Published**: 2026-10-13
**Authors**: Author One, Author Two

## Overview

Explain the problem and the proposed approach in 2-4 paragraphs.

## Key points

- Contribution 1
- Contribution 2
- Contribution 3

## Details

Method, data, setup, and results. Do not add facts absent from the source.

## References

- Paper: [arXiv:2610.18868](https://arxiv.org/abs/2610.18868)
```

**ko:**

```markdown
# 논문 제목의 한국어 번역

**원문**: [arXiv:2610.18868](https://arxiv.org/abs/2610.18868) · **게시일**: 2026-10-13
**저자**: Author One, Author Two

## 개요

무엇을 문제로 삼고, 무엇을 제안했는지 2~4문단.

## 핵심 내용

- 핵심 기여 1
- 핵심 기여 2
- 핵심 기여 3

## 상세

방법, 데이터, 실험 설정, 결과. 원문에 없는 내용은 쓰지 않는다.

## 참고 자료

- 논문: [arXiv:2610.18868](https://arxiv.org/abs/2610.18868)
```

- 아티클은 `**Authors**` 줄을 빼고 `**Source**: [블로그 제목](URL)`만 쓴다.
  ko는 `**원문**: [블로그 제목](URL)`으로 쓴다.
- H1은 frontmatter `title`과 **글자 단위로 동일**해야 한다.
- 본문은 300자 이상. ko는 한글 50자 이상.
- en 본문을 ko에 그대로 복붙하지 않는다.

#### 7.5.3 ko 작성 규칙

- en 완성본을 읽고 한국어로 **번역·요약**한다.
- `title`, `description`은 한국어.
- `locale: ko`, `tags` 끝은 `ko`.
- `source_url`, `blog`, `arxiv_id`, `authors`, `published_date`는 en과 동일.
- 제목은 자연스러운 한국어로 옮기되, 고유명사(모델명·시스템명)는 유지한다.
- 영어 문장을 그대로 남기지 않는다. 코드·수식·고유명사만 허용.

### 7.6 실패 처리 (같은 상황이면 같은 행동)

| 상황 | 판정 | 반드시 할 일 |
|---|---|---|
| `robots` 차단 | BLOCKED | 재시도 금지. stub 유지, 경로+이유 기록 |
| `fetch failed` | BLOCKED | 같은 명령 1회만 재시도. 실패 시 stub 유지, 기록 |
| `extract: too few blocks` | BLOCKED | 원문을 직접 읽고 수동 작성. 불가능하면 stub 유지 |
| arXiv HTML·ar5iv 둘 다 실패 | BLOCKED | PDF 파싱 금지. stub 유지, 기록 |
| `source_url` 없음 | BLOCKED | URL을 추측하지 않는다. 경로+이유 기록 |
| frontmatter `---` 없음 | 수정 | 기존 key 줄을 `---`로 감싼다. 값은 유지 |
| `tags` 언어 태그 중복 | 수정 | 중복 제거 후 주제 태그 추가 |
| 제목이 arXiv ID | 수정 | arXiv abs 페이지에서 실제 제목 확인 후 frontmatter/H1 수정 |
| 날짜가 비어 있음 | 수정 | 원문 게시일 사용. 오늘 날짜로 채우지 않는다 |
| ko가 아직 stub | 수정 | ko fetch 금지. 완성된 en을 번역 |
| `gate`가 metadata BLOCKED | 수정 | 지적된 필드만 고친다. 게이트 우회 금지 |
| hook이 커밋 거부 | 정상 | 미완성 파일을 끝내거나, 새로 만든 미완성 stub을 제거하고 보고 |
| 같은 `source_url` 존재 | 중복 | 새로 만들지 않는다. 기존 경로를 보고 |

**커밋 금지 조건:** 새로 만든 stub/draft가 작업 트리에 남아 있으면 커밋하지 않는다.
`git commit --no-verify`, `git push --no-verify`는 금지한다.

### 7.7 완료 보고 형식 (매번 동일)

성공 시:

```text
## 처리 결과
- 문서: content/en/... ↔ content/ko/...
- 상태: complete
- gate: Gate: OK (--worktree, --staged)
- checks: ko papers N, errors 0; Build verified (N pages); Index generation complete
- commit: <hash>
- backlog: stubs N, drafts N (전체 감사 기준)
- blocked: none
```

실패/중단 시:

```text
## 처리 결과
- 문서: content/en/... (미완성)
- 상태: BLOCKED
- 이유: <robots | fetch failed | too few blocks | source_url 없음 | ...>
- gate: FAIL — <BLOCKED 항목>
- commit: none
- 다음 행동: <수동 작성 | URL 확인 | 사용자 확인>
```

보고에는 실제 실행한 명령과 실제 출력의 핵심 줄을 포함한다. 추측으로 "완료"라고
쓰지 않는다.
