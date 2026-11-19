---
title: "Databricks AI Runtime의 테이블형 파운데이션 모델(Tabular Foundation Models)"
description: "TFM이 동작하는 원리 — 어텐션 기반 in-context learning, 합성 데이터 사전학습, TabICLv2/TabFM/TabPFNv3.5 비교 — 그리고 Databricks AI Runtime이 관리형 GPU·MLflow·Unity Catalog로 TFM 실험과 파인튜닝을 지원하는 방법."
tags: [source, databricks, ko]
locale: ko
source_url: "https://www.databricks.com/blog/tabular-foundation-models-databricks-ai-runtime"
blog: databricks
published_date: "2026-11-19"
---

# Databricks AI Runtime의 테이블형 파운데이션 모델(Tabular Foundation Models)

**출처**: [databricks](https://www.databricks.com/blog/tabular-foundation-models-databricks-ai-runtime) · **게시일**: 2026-11-16

## 개요

가장 가치 있는 예측 ML 애플리케이션 상당수는 테이블형 데이터를 다룬다 — 신용 리스크, 고객 이탈, 수요 예측, 예지 정비. 이런 사용 사례는 전통적으로 예측 작업마다 모델을 개발·학습·유지해야 했다. 테이블형 파운데이션 모델(TFM)은 다른 접근을 제시한다: 작업별 학습 없이 새 데이터셋에 예측을 수행하는 사전학습 모델이다.

공개 벤치마크의 강한 결과에도 불구하고 TFM은 아직 엔터프라이즈 AI 주류에 들어오지 못했다 — 분야가 초기인 탓도 있고, 컴퓨팅 인프라 요구사항 탓도 있다. 이 글은 TFM의 동작 원리, 최신 모델 비교, 그리고 Databricks AI Runtime이 관리형 GPU 인프라, 통합 개발 도구, 모델 거버넌스로 TFM 실험과 파인튜닝을 어떻게 지원하는지 설명한다.

## 핵심 내용

- **In-context learning(ICL)**: TFM은 수백만 개의 다양한 합성 데이터셋으로 사전학습된다. 예측 시점에 라벨이 있는 행들을 컨텍스트로 넣으면 어텐션이 새 행을 그 예시들과 연결한다 — 예측은 단일 forward pass로 나오며 작업별 학습이 필요 없다.
- **제로샷 기준선, 파인튜닝 가능**: ICL이 강력한 즉시 사용 기준선을 제공하고, 특정 데이터셋으로 사전학습 가중치를 갱신하면 핵심 사용 사례에서 정확도를 더 끌어올릴 수 있다.
- **전용 토크나이저**가 혼합 타입 입력(수치·범주·불리언)을 모든 셀을 공유 잠재 표현으로 매핑해 해결했다. TabPFNv2는 행 내 어텐션 후 열 간 어텐션을 순차 적용해 파운데이션 모델 규모에서 이를 처음 실현했다.
- **확장성 해법 — 행 압축**: TabICLv1은 각 행을 단 4개의 토큰으로 표현하는 전용 인코더를 써서 샘플 간 어텐션 비용을 크게 낮추면서도 경쟁력 있는 성능을 유지한다. TabPFNv3, TabFM, KumoTabular는 이 계열을 채택·확장했으며 TabArena 같은 벤치마크 상위권에 있다.
- **합성 데이터 사전학습**: 제작자는 누락값·이상치·관측되지 않은 특성 같은 엔터프라이즈 데이터 품질 문제를 담은 대규모 다양한 데이터를 시뮬레이션한다. Structural Causal Models가 표준 샘플링 프레임워크를 제공하지만 구체적 파이프라인은 TFM마다 다르다.
- **최신 모델**: TabICLv2(2026-02, ~28M 파라미터, BSD 3-Clause, 상업적 허용), TabFM(2026-06, ~400M, 비상업 라이선스), TabPFNv3.5(2026-09, ~220M, 비상업 라이선스) — 규모와 라이선스가 실무 배포의 두 필터다.
- **프로덕션 마찰**: 작업별 맞춤 모델이 여전히 지배적이다. 사용 사례별 실험, 드리프트·성능 저하 모니터링, 길고 예측 불가능한 GPU 프로비저닝과 상시 예약의 높은 TCO가 과제다.
- **Databricks AI Runtime**은 관리형 GPU, MLflow 추적, Unity Catalog 통합을 제공해 TFM 실험과 파인튜닝, 그리고 산출 모델의 거버넌스를 지원한다.

## 세부 내용

TFM은 맞춤형 모델의 학습·유지 부담을 사실상 없앤다. 트랜스포머의 핵심 난제는 이질적인 테이블 입력 처리였고, 커뮤니티는 범주형·수치형 피처를 공통 잠재 공간에 임베딩하는 토크나이저로 해결했다. TabPFNv2는 행 내/열 간 어텐션을 번갈아 적용해 파운데이션 규모의 접근을 입증했지만, 조밀한 어텐션은 행과 피처가 늘수록 비용이 급증했다. 행 압축 아키텍처(TabICLv1 계열)는 각 행을 ~4 토큰으로 압축해 비용을 극적으로 낮추면서 경쟁력을 유지하는데, 현재 TabArena 상위 모델들이 이 계열이다.

합성 데이터 사전학습이 또 다른 기둥이다. TFM의 제로샷 성공 여부는 합성 사전학습 분포가 실제 엔터프라이즈 데이터와 그 실패 양상을 얼마나 충실히 포괄하는지에 달려 있다. Structural Causal Models가 샘플링을 표준화하지만, 각 TFM의 파이프라인은 제각각 튜닝된다.

엔터프라이즈의 실무 평가 틀은 규모와 라이선스다: TabICLv2는 작고 상업적으로 허용되며, TabFM과 TabPFNv3.5는 더 크지만 비상업 라이선스다. Databricks AI Runtime은 운영 측면을 해결한다 — 상시 예약 TCO 없는 관리형 GPU, 실험 추적용 MLflow, 리니지·거버넌스용 Unity Catalog — 팀이 도입 전에 정확도·추론 지연·GPU 메모리·비용 면에서 TFM을 기존 기준선과 비교 평가할 수 있게 한다.

## 참고 자료

- 원문: [Tabular foundation models on Databricks AI Runtime](https://www.databricks.com/blog/tabular-foundation-models-databricks-ai-runtime)
