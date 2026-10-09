---
title: Uber 규모에서 소프트웨어 팩토리를 효율적으로 운영하기
description: Uber의 AI 에이전트 코딩 비용 방정식과 최적화 레버 — 모델 선택, 토큰 효율, 매니지드 에이전트 경제성
tags: [source, uber, ai-engineering, agent, cost-optimization, software-factory, ko]
locale: ko
source_url: "https://www.uber.com/us/en/blog/efficient-software-factory/"
blog: uber
published_date: 2026-08-27
---

# Uber 규모에서 소프트웨어 팩토리를 효율적으로 운영하기

**저자**: Uday Kiran Medisetty (Distinguished Engineer)
**출처**: [Uber Blog](https://www.uber.com/us/en/blog/efficient-software-factory/)
**날짜**: 2026-08-27

## 배경

Uber PR의 70% 이상이 AI 에이전트 기여이며, 3,600개 이상의 에이전트 스킬과 하루 30K건 이상의 에이전트 실행이 이루어진다. 2026년 2~7월 주간 활성 사용자는 7배, 에이전트 요청은 9.4배 증가했지만 최적화로 총 AI खर्च는 안정화되었다. 모델 요청 1K건당 비용은 피크 대비 ~34%↓, 세션당 비용은 6월 피크 대비 52%↓.

## 비용 방정식

```
Total Spend = Users × Sessions/User × Turns/Session × Requests/Turn × Tokens/Request × Price/Token
```

각 항은 독립적으로 측정·최적화 가능하다.

## 에이전트 활용 4계층

특수 → 범용 순으로, 상위 계층일수록 비용·품질·모델 선택 제어권이 크다:

1. 전문화된 매니지드 에이전트 (예: uReview 코드 리뷰)
2. 태스크 범위 코딩 에이전트
3. 범용 코딩 어시스턴트
4. 개방형 에이전트 세션

## 계층별 지표

| 계층 | 지표 | 답하는 질문 |
|------|------|--------------|
| 포트폴리오 | 총비용, 고유 사용자, 도구별 비용 | 돈이 어디로 가는가 |
| 단위 경제성 | 사용자당 비용, 요청/사용자, 1K 요청당 비용, 요청당 토큰, 1M 토큰당 비용, 세션당 비용 | 도구가 싸지고 있는가 |
| 모델 경제성 | 모델별 비용, 1K 요청당 비용, 1M 토큰당 비용 | 모델 릴리스가 요금에 영향을 주는가 |
| 동인 분해 | 도입률, 참여도, 입출력 워크로드 | 숫자가 왜 움직였는가 |
| 매니지드 에이전트 성과 | 병합 PR당 비용, 리뷰당 비용, 알림당 비용, 품질 (revert율, F1, MTTR) | 가치 단위당 싸지는가 |

## 최적화 레버

- **Price/Token**: 벤치마크 기반 파레토 최적 모델 선택, 모델 기본값
- **Tokens/Request**: 400K 컨텍스트 캡, Medium 추론, 프롬프트 캐싱, Tool search/CLI 해결 MCP, 코드 모드 배칭, 게이트웨이 라우팅 SaaS MCP
- **Requests/Turn**: 그래프 기반 컨텍스트, 지속적 스킬 최적화
- **가시성·교육**: 상태 표시줄 실시간 비용 카운터, 지출 티어, 세션 분석 대시보드

## 벤치마크 기반 모델 선택 (4단계)

1. 실제 업무로 벤치마크 구성 (알려진 버그가 있는 실제 PR, 난이도 분류)
2. 정밀도/재현율/F1 + PR당 비용, 지연시간, 타임아웃, 노이즈 측정
3. 비용-품질 파레토 프론티어 도출
4. 파레토 최적 설정 배포 — 프론티어는 수 주마다 이동하므로 지속 추적

**uReview 사례**: 모델 전환으로 F1은 올리고 PR당 비용은 대폭 절감.

## 세미나 시사점

- AI खर्च는 곱셈 형태로 분해해야 각 항에 대응하는 레버가 보인다.
- 실제 업무 기반 벤치마크 + 파레토 프론티어 선택이 핵심이다.
- 컨텍스트 캡과 캐싱이 규모에서 가장 통제 가능한 항이다.
- 매니지드 에이전트는 토큰 खर्च보다 병합 PR당 비용·품질 지표로 평가해야 한다.

## 관련 개념

- `concepts/ai-engineering/agent.md`
- `concepts/ai-engineering/model-selection.md`
