---
title: "Databricks AI Runtime으로 더 안전하고 유용한 개방형 모델을 만든 Flo Health"
description: "Flo Health는 임상 검증 AI 저지와 프라이버시 우선 합성 데이터를 Databricks AI Runtime 위 post-training 파이프라인으로 전환해 파인튜닝된 개방형 모델의 의료 안전성을 34%에서 61%로, 유용성을 42%에서 76%로 끌어올렸다." (한국어 번역)
tags: [source, databricks, llm-post-training, ai-judges, supervised-fine-tuning, preference-optimization, ko, ko]
locale: ko
source_url: "https://www.databricks.com/blog/how-flo-health-built-safer-more-useful-open-models-databricks-ai-runtime"
blog: databricks
published: "2026-10-12"
---

# Databricks AI Runtime으로 더 안전하고 유용한 개방형 모델을 만든 Flo Health

**Source**: Databricks Blog, 2026-10-12

**핵심**: 월 8,100만 사용자가 쓰는 여성 건강 앱 Flo Health에게 AI 답변은 의학적으로 안전하면서도 실질적으로 유용해야 한다. Flo는 단일 범용 모델 의존 대신, 임상의 전문성을 훈련 신호로 바꾸는 저지 기반 post-training 파이프라인을 Databricks AI Runtime 위에 구축했다. 결과: 의료 안전성 34%→약 61%, 유용성 42%→76%, 복합 점수 16%→47%.

## 배경

Flo가 전통적 ML에서 생성형 AI 기반 개인화 인사이트로 이동하면서 단일 프론티어 모델의 한계가 드러났다: 8,100만 사용자 규모의 추론 비용, 모델 제공자 라이프사이클 종속, Flo 고유 도메인 지식 인코딩의 어려움. Flo의 장기 비전은 작업마다 적합한 모델을 쓰면서 일관된 안전 기준을 유지하는 복합 AI 시스템이다. 이를 위해 개방형 모델 파인튜닝과 "좋음"을 정의·측정하는 재사용 가능한 방법이 필요했고, Flo는 훈련이 아니라 평가부터 시작했다.

## 전문가 판단을 확장 가능한 훈련 신호로

Flo의 의료·프로덕트·엔지니어링 팀은 의료 리스크를 테스트 가능한 루브릭으로 분해했다 — 예컨대 증상 질문 답변에 양성 원인과 중대한 원인을 균형 있게 다루도록 요구하는 "balanced causes" 규칙 — 그리고 각 루브릭을 정의·채점 지침·학습 케이스를 갖춘 AI 저지로 인코딩했다. 저지는 합성 케이스와 익명화된 실제 사용자 케이스로 검증했고, 불일치는 블라인드 임상 검토로 ground truth를 확정했다.

최종 프레임워크는 3개 그룹 26개 저지를 사용한다:

- **12개 의료 안전성 저지**: 하드 제약 조건.
- **6개 "마이크로" 저지**: 어조, 근거 기반, 프레이밍, 세부 안전성 등 뉘앙스 행동.
- **8개 유용성 기준**: 완전성, 관련성, 일관성, 어조 등.

임상의는 개별 훈련 쌍 라벨링이 아니라 이 평가 시스템의 설계·교정에 시간을 집중했고, 시스템이 대규모로 훈련 후보를 채점한다 — 사례별 인간 라벨이 필요 없다.

## AI 저지와 선호 최적화로 파인튜닝

Flo는 프라이버시 우선 원칙으로 15,000개 이상의 합성 질문을 생성했고(사용자 자유 텍스트가 아닌 모델 생성·익명 집계 신호에서 파생), Reinforcement Fine-Tuning 루프를 채택했다:

1. 프라이버시 보존 질문 합성.
2. 복수 후보 답변 생성.
3. 안전성·유용성·행동 기준으로 채점.
4. 상위 답변으로 선호 쌍 구성.
5. 지도 파인튜닝 + Direct Preference Optimization(DPO) 훈련 후 저지로 재검증.

초기 버전은 유용성은 올랐지만 안전성이 정체됐다 — 선호 쌍이 의료 품질의 정도를 구분하지 못했기 때문이다. Flo는 등급형 안전성 점수로 해결했다: 이진 안전 게이트를 통과한 답변을 의료 기준 충족 정밀도로 재정렬해 안전성 대비가 선명한 선호 쌍을 만들었다.

## Databricks AI Runtime으로 post-training 확장

생성-채점-선택-훈련 루프는 Databricks AI Runtime 위에서 돌았고, 분산 훈련은 LLM Foundry, 선호 최적화는 Compose-RL, 추적·체크포인트는 MLflow가 맡았다. 파인튜닝 실행은 PyTorch + Fully Sharded Data Parallel(FSDP)로 32개 NVIDIA H100 GPU를 사용, SFT 후 DPO 순서 — 실험마다 GPU 클러스터를 직접 세팅하지 않는 서버리스 GPU 컴퓨트다. Flo 추산으로 맞춤형 파인튜닝 모델은 프론티어 API 대비 추론 비용을 한 자릿수 배율로 낮추면서 행동·라이프사이클 통제권을 준다.

## 결과

| 지표 | 이전 | 이후 |
|--------|--------|-------|
| 의료 안전성 | 34% | ~61% |
| 유용성 | 42% | 76% |
| 복합(두 기준 동시 충족) | 16% | 47% |

복합 점수가 약 3배가 됐다. Flo가 강조하듯 숫자보다 durable한 자산은 재사용 가능한 평가-훈련 시스템 자체다: 훈련 환경을 재구축하지 않고도 새 개방형 가중치 모델(Gemma, Qwen, Kimi)에 그대로 적용된다.

## 소프트웨어 엔지니어를 위한 시사점

- **평가 우선 post-training**: 전문가 시간을 교정된 저지에 한 번 투자하면 보상 신호이자 회귀 스위트로 재사용된다 — 정확성 제약이 있는 모든 도메인(의료, 금융, 법률)에 적용 가능한 패턴.
- **이진보다 등급형 선호**: DPO가 스타일은 개선해도 정확성이 안 오르면, 통과 답변을 품질 깊이로 재정렬해 옵티마이저가 필요로 하는 대비를 복원한다.
- **프라이버시 보존 합성 데이터**: 훈련 입력을 모델 생성·집계 신호에서 파생시켜 전문가는 기준 검증에만 참여시킨다.
- **비용 엔지니어링**: 높은 QPS에서는 작은 파인튜닝 모델이 프론티어 API보다 ~10배 저렴하면서 통제 가능성도 높다.

## 참고문헌

- 원문: [https://www.databricks.com/blog/how-flo-health-built-safer-more-useful-open-models-databricks-ai-runtime](https://www.databricks.com/blog/how-flo-health-built-safer-more-useful-open-models-databricks-ai-runtime)
