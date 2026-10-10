---
title: "Learning Where Outcomes Change:Credit-Addressable Reasoning for Multimodal Geometry"
description: en/sources/papers/Learning_Where_Outcomes_Change.md 한국어 번역 요약
tags: [source, paper, huggingface, ko]
locale: ko
source_url: "https://arxiv.org/abs/2608.30457"
arxiv_id: 2608.30457
---

# Learning Where Outcomes Change:Credit-Addressable Reasoning for Multimodal Geometry

**arXiv**: 2608.30457 | **게시일**: 2026-08-31 | **기관**: Tsinghua IIGroup

**저자**: Jiani Guo, Junjie Wang, Jie Wu, Pengxiang Zhao, Dongdong Zhang, Shaohan Huang, Yujiu Yang, Furu Wei

## 핵심 기여

- 크레딧 할당 가능 추론(credit-addressable reasoning): 추론에 드러난 의미 단위(타입 이벤트)가 곧 학습이 대안을 비교하고 크레딧을 매기는 위치 — 궤적 단위 RL의 표현 격차·크레딧 격차를 함께 해소
- Code-CoT: 다이어그램을 유지한 채 시각 관계를 줄 단위 실행 가능 Matplotlib 코드로 표현하고, 추론을 타입 이벤트(`reference`·`auxiliary`·`coordinate`·`think`)로 조직. 각 이벤트는 검증·분기 가능
- CE-GRPO: 구조 사전분포+타입 정규화 엔트로피로 후보 이벤트 경계를 고르고, 공유 접두사에서 완결 후속들을 끝까지 샘플해 종단 결과 차이로 국소 어드밴티지를 계산 (공유 접두사는 손실 제외, 전원 동일 보상은 업데이트 없음)
- 근거: 9개 기하 벤치 평균 76.04, Qwen3-VL-8B 대비 +8.09, 궤적 단위 GRPO 대비 +3.43. 중간 이벤트가 1개 늘수록 격차가 3.77점 벌어짐

## 방법론

18,302개 정제 트레이스로 Code-CoT SFT(시각 인코더 고정) 후 CE-GRPO. 일반 그룹과 공유-접두사 그룹을 1:1로 섞고, 프로그램 검증 보상(정답+행동 유효−반복/답누설 패널티)으로 같은 GRPO 목적함수 최적화. 이미지·질문·접두사를 고정한 채 분기하므로 업데이트는 재생성 이벤트와 그 하류에만 적용.

## 결과

| 비교 | 결과 |
|---|---|
| CE-GRPO 평균 (9 벤치) | **76.04** |
| Qwen3-VL-8B 백본 대비 | **+8.09** (9개 전부 개선) |
| 궤적 단위 GRPO 대비 | **+3.43** (완결 응답만 +3.91) |
| Code-CoT SFT 대비 | +6.49 |
| 의존사슬 긴 분할 | GeoLaux-mini **+15.16**, MM-Math **+9.44** |
| 이벤트 스케일링 | 이벤트 1개당 격차 **+3.77점** (r=0.866) |
| 셀렉터 절제 | 구조+엔트로피 최고 (76.04, 미종결 4.73%) |

MathVerse 텍스트-지배→시각-전용 격차도 30.07→14.09로 축소. 벤치별 표는 원문 HTML 대조 완료. 프로토콜 준수는 비어 있지 않은 `<answer>` 블록 종결이 필수.

## SW 엔지니어를 위한 시사점

SW 엔지니어 관점에서 멀티모달 모델 디버깅(운영 AI 시스템의 흔한 난제)에 필요한 프레임워크 제공. 결과를 특정 시각·텍스트 요소에 귀속시키는 능력은 모델 감사, 편향 탐지, 예기치 못한 출력 디버깅에 유용. 문서 이해, VQA, 멀티미디어 분석 등 멀티모달 입력을 쓰는 모든 시스템에 해당. 기하 태스크를 넘어 해석 가능성이 중요한 광범위한 멀티모달 도메인으로 확장 가능.

## 관련 개념

- [LLM 훈련](../../concepts/ai-engineering/llm-training.md)
- [트랜스포머](../../concepts/machine-learning/transformer.md)
- [어텐션](../../concepts/machine-learning/attention.md)

## 참고

- 원문: https://arxiv.org/abs/2608.30457
- arXiv HTML (대조 완료): https://arxiv.org/html/2608.30457
- en 대응: en/sources/papers/Learning_Where_Outcomes_Change.md
