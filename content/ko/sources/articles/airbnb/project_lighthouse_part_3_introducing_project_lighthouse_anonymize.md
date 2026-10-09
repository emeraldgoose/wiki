---
title: "Project Lighthouse — Part 3: project-lighthouse-anonymize 소개"
description: 차별 측정용 프라이버시 보호 익명화 라이브러리 오픈소스 공개; Core Mondrian 알고리즘과 데이터 품질 프레임워크
tags: [source, airbnb, privacy, anonymization, open-source, data-engineering, ko]
locale: ko
source_url: "https://medium.com/airbnb-engineering/project-lighthouse-part-3-introducing-project-lighthouse-anonymize-74f8b26653fb"
blog: airbnb
date: 2026-08-25
---

# Project Lighthouse — Part 3: project-lighthouse-anonymize 소개

**출처**: Airbnb Engineering (Medium) · **발행**: 2026-08-25 · **저자**: Adam Bloomston

## 배경: Project Lighthouse의 목적

2020년 Airbnb는 시민권·프라이버시 단체와 함께 플랫폼 내 **경험 격차(차별 가능성) 측정**을 위한 Project Lighthouse를 시작했다. 설계 원칙:

- 인지된 인종(perceived race) 데이터는 **개인 계정과 절대 연결하지 않음**.
- 데이터는 격차 측정 **전용**이며, 사용자는 개인정보 설정에서 옵트아웃 가능.
- 2024년 업데이트에서 측정 결과를 공개.

2020년 기초 논문이 **p-sensitive k-익명성**을 기술적 프라이버시 모델로 확립했고(Part 1·2 참조), 이번 글은 익명화 파이프라인의 Python 라이브러리 **`project-lighthouse-anonymize`** 오픈소스 공개(PyPI·GitHub)와 이를 뒷받침하는 **신규 arXiv 논문 2편**(확장 가능한 구현 + 품질 검증)을 발표한다.

## Core Mondrian: 확장 가능한 분할 기반 익명화

논문 *Core Mondrian: Basic Mondrian beyond k-anonymity* (2025). 고전 Mondrian 알고리즘의 확장:

1. **확장 가능한 아키텍처** — Strategy 패턴으로 k-익명성 우선 지원, 향후 프라이버시 모델 확장 가능.
2. **병렬 처리** — 하이브리드 재귀-큐 실행(작은 파티션은 즉시 재귀, 큰 파티션은 큐 기반 병렬).
3. **NaN 패턴 사전 분할** — 결측값을 버리지 않고 원칙적으로 처리.
4. **동적 억제 예산 관리** — k를 만족시키기 위한 레코드 억제량 제어.

대규모 실제 데이터셋을 통계 분석에 쓸 수 있는 수준으로 익명화할 수 있게 된다.

## 익명화 하의 데이터 품질 측정

논문 *Measuring Data Quality for Project Lighthouse* (2025). 핵심 질문: 익명화된 데이터가 분석에 "충분히 좋은지" 어떻게 아는가?

**세 가지 핵심 지표**:

| 지표 | 의미 |
|------|------|
| Pearson 상관계수 | 원본–익명값 간 선형 관계 보존 |
| RILM | 데이터의 기하학적 "형태"/크기 보존 (높을수록 왜곡 적음) |
| NMIv1 | 엔트로피(정보량) 보존 |

**검증 방법론**: 품질 평가를 ML 분류 문제로 재구성 — 합성 데이터셋으로 지표+임계값이 "통계적으로 유효한 결과를 낼 조건"을 예측함을 검증. Airbnb가 실제 사용하는 **기본 임계값**을 논문·라이브러리에 함께 제공하므로, 익명화 전문가가 아닌 분석가도 `check_dq_meets_minimum_thresholds` 게이트로 결과를 신뢰할 수 있다.

## 사용법

```python
p, k = 2, 5
anon_df, dq_metrics, disclosure_metrics = k_anonymize(logger, input_df, qids, k, {}, "row_id")
sensitized_df, _, _ = p_sensitize(logger, anon_df, qids, "race", p, k, sens_attr_value_to_prob)
minimum_dq_met, reasons = check_dq_meets_minimum_thresholds(dq_metrics)
assert minimum_dq_met, str(reasons)
```

입문 가이드는 UCI Adult 데이터셋으로 실행 가능한 예제를 제공한다.

## 엔지니어 관점 시사점

- **2단계 프라이버시**: k-익명성 후 p-민감화(摂動) — 조합이 민감 속성 노출을 막는다.
- **품질 게이트를 파이프라인에 내장**: 익명화 → 측정 → 임계값 assert → 분석.
- **병렬 Mondrian + NaN 사전 분할**이 실제 대규모 지저분한 테이블에 적용 가능케 하는 핵심이다.

## 참고

- https://github.com/airbnb/project-lighthouse-anonymize · https://arxiv.org/abs/2510.09661 · https://arxiv.org/abs/2510.06121
