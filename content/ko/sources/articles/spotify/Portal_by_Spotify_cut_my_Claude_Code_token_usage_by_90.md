---
title: "Portal by Spotify가 Claude Code 토큰 사용량을 90% 줄여준 이야기"
description: Portal AiKA 모드와 shunt 플러그인으로 Claude Code의 대량 읽기·정형 코드 생성을 저가 모델에 위임 — 대량 읽기에서 평균 90% 토큰 절감 (한국어 번역)
tags: [source, spotify, ai-coding, agents, cost-optimization, ko, ko]
locale: ko
source_url: "https://engineering.atspotify.com/2026/9/portal-by-spotify-cut-my-claude-code-token-usage-by-90"
blog: spotify
published_date: 2026-09-03
---

# Portal by Spotify가 Claude Code 토큰 사용량을 90% 줄여준 이야기

**저자**: Dimitri Mazmanov, Principal Product Manager
**출처**: [Spotify Engineering](https://engineering.atspotify.com/2026/9/portal-by-spotify-cut-my-claude-code-token-usage-by-90)
**날짜**: 2026-09-03

## 개요

코딩 에이전트의 토큰 소모 대부분은 추론이 아니라 I/O다. 하나의 질문에 답하려고 파일 다섯 개를 읽고, 옆의 스무 개 테스트와 똑같은 테스트 파일을 찍어낸다. 개발자 1인당 월 수백~수천 달러의 토큰 비용이 드는 상황에서, 저자는 단순한 해법을 제시한다. Portal AiKA 모드 두 개에 잡무를 위임하고 shunt라는 Claude Code 플러그인으로 강제하는 것이다. Java 모노레포 측정에서 대량 읽기의 평균 절감률은 약 90%였다.

## 두 개의 AiKA 모드

모드는 임시 런타임(Lambda식)에서 도는 선언적 에이전트다. 지침·모델·파라미터·MCP 도구를 정의하면 Portal CLI나 API로 호출하고, 공개·비공개로 공유한다. 저자가 만든 두 모드는 모두 Gemini 2.5 Flash를 작업 모델로 쓴다.

- **bulk-reader** — 전달된 파일들을 읽고 질문에 구조화된 불릿으로만 답한다. "큰 파일 N개를 읽고 한 가지만 답하기" 패턴을 대신 맡는다.
- **code-writer** — 스펙과 참조 파일을 받아 기존 패턴 그대로 코드만 출력한다(마크다운 펜스·설명 금지 — Claude가 다시 파싱해야 하므로).

설계 원칙은 역할 분리다. 위임 시점은 플러그인이, 응답 방식은 모드가 정하므로 모델·프롬프트 교체가 플러그인에 영향을 주지 않는다.

## shunt 플러그인: 훅·스크립트·스킬

초기의 `CLAUDE.md` 라우팅 규칙은 권고에 불과하고 프로젝트별 복사본이 필요해 실패했다. shunt는 세 겹으로 강제한다.

- **훅** — `check-file-size`가 행 수 임계값(기본 350줄, `SHUNT_MIN_LINES`로 조정) 초과 읽기를 차단하고 bulk-reader 스킬로 돌린다. `check-bash-read`는 큰 파일 대상 `cat`·`head`·`tail`·`less`·`more`를 잡되 파이프로 거르는 표적 읽기는 통과시킨다.
- **스크립트** — `bulk-read`는 파일을 XML 경계로 감싸 일회성·무상태 호출로 보내고(서버에 저장 없음), `code-write`는 스펙과 필수 참조 파일을 보내 디스크에 직접 쓴다. Claude는 생성 토큰을 보지 않는다.
- **스킬** — 훅이 읽기를 차단했을 때 호출법을 알려주는 마크다운 파일. 스킬을 안 읽어도 훅이 비싼 읽기를 막으므로 점진적으로 성능이 저하될 뿐이다.

## 결과와 한계

Java 모노레포 4개 시나리오에서 대량 읽기 평균 절감률은 90% 안팎이었다. 코드 생성은 출력 토큰이 Claude를 우회하므로 정량화가 어렵다. 안 되는 것도 분명하다. 편집 위임(작업 모델 요약엔 믿을 만한 줄 번호가 없으므로 offset/limit 표적 읽기는 Claude 몫), 추론 위임(미묘한 스레드 안전성 버그를 작업 모델이 놓치고 Claude가 잡아냄), 작은 작업(10~30초 위임 지연이 절감보다 크므로 임계값 이하에서는 직접 읽기)이다. 더 큰 의미는 이것이다. AiKA 모드는 모델 라우팅을 시스템 공학 문제에서 설정 문제로 바꾼다. 같은 모드는 프로젝트·도구를 가리지 않고 재사용·공유·조합(doc-writer, reviewer, translator 등)할 수 있다.

## 참고 자료

- [Portal by Spotify cut my Claude Code token usage — 원문](https://engineering.atspotify.com/2026/9/portal-by-spotify-cut-my-claude-code-token-usage-by-90)
- [AiKA 모드 문서](https://backstage.spotify.com/docs/portal/core-features-and-plugins/aika/modes) (원문에서 인용)
- [spotify/portal-ai-plugins 마켓플레이스](https://github.com/spotify/portal-ai-plugins) (원문에서 인용)
