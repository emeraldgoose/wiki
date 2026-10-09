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
  인용(`>`), 코드펜스, 구분선.
- 문서 간 링크는 **상대경로 `.md`** 로 건다. 빌드가 `/<lang>/....html`로
  바꿔준다. 예: `[RAG 가이드](../ai-engineering/build-rag.md)`
- 바깥 링크(`http…`)는 자동으로 새 탭으로 열린다.
- **"English version" / "한국어 버전" 같은 본문 링크를 넣지 않는다.**
  상단 언어 버튼이 상대 문서를 자동으로 가리킨다. 단독 버전 링크행은
  빌드가 제거한다.
- 이미지는 별도 파이프라인이 없으므로 외부 URL을 쓴다.

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

## 5. 흔한 실수

| 증상 | 원인 |
|---|---|
| 포털에 글이 안 보인다 | `index.md`로 저장했거나, `tags`가 비어 카테고리 추론 실패 |
| 언어 버튼이 포털로 간다 | 반대 언어 쪽에 같은 경로 파일이 없음 |
| 링크가 404다 | `.md`가 아닌 `.html`로 직접 연결했거나, 이동·개명한 경로를 가리킴 |
| 목차(TOC)가 비었다 | `##` 섹션이 없음. TOC는 h2에서 자동 생성 |
