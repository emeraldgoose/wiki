---
title: "장기 기억을 위한 지속 학습 메커니즘의 구성"
published: 2026-09-07
arxiv_id: "2609.06986"
url: "https://arxiv.org/abs/2609.06986"
authors: ["Zheyuan Zhang", "Alvin Zhang", "Daniel Khashabi", "Tianmin Shu"]
---

# 장기 기억을 위한 지속 학습 메커니즘의 구성

[EN version](../en/sources/papers/Continual_Learning_Mechanisms_Compose_for_Long-Horizon_Memorization.md)

## 초록

언어 모델은 시간이 지남에 따라 들어오는 정보를 내재화하고 이후 수많은 업데이트를 거쳐도 유지해야 할 수 있다. 저자들은 **장기 기억(long-horizon memorization)** 설정을 제안한다: 모델이 이전 학습 예제를 보관하지 않고 추론 시 과제 식별자도 받지 않은 채 지속적 지도 미세조정(SFT)으로 100개의 질의-응답 과제를 학습한다. 순차 업데이트는 치명적 망각을 일으키며, 평가한 단일 지속 학습 메커니즘 중 어느 것도 이 지평에서 강한 유지를 보여주지 못한다. 가설은 망각의 서로 다른 원인을 다루는 메커니즘들이 단독보다 **구성(compose)**될 때 더 효과적이라는 것이다. 구성은 두 설계 축으로 정리된다 — **앵커**(각 업데이트가 보존해야 할 과거 정보: 데이터·함수·가중치)와 **저랭크 할당 규칙**(LoRA 어댑터에 연속 업데이트를 어디에 유지할지). 새로 구축한 3종의 100-과제 기억 데이터셋에서 과제 단위 successive halving으로 조합 공간을 탐색하고 요인 실험(factorial experiment)으로 개별·상호작용 효과를 측정한 결과, 최적 방법(3개 앵커 전부 + merged LoRA)이 모든 데이터셋에서 3위 안에 들고 평균 최종 유지율(final retention)이 순수 순차 미세조정 **1.2%**에서 **34.9%**로 — 28배 개선됐다. 데이터 앵커와 merged LoRA가 가장 큰 평균 이득을 제공하고 세 데이터셋 모두에서 초가산적(super-additive) 상호작용을 보인다.

## 배경 및 문제 설정

프롬프팅과 검색은 새 정보를 파라미터 밖에 둔다 — 매번 다시 공급해야 한다. 이 논문은 반복된 파라미터 업데이트가 모델 내부에 durable한 기억을 구축할 수 있는지 묻는다. 설정은 도메인 점증형 지속 SFT다: 동일 QA 인터페이스·어휘로 100개 과제를 순차 학습, 과거 원시 예제 보관 없음, 테스트 시 과제 ID 없음. 지표는 이후 모든 과제를 거친 뒤 학습 질의의 회상률(최종 유지율)과 기억 반감기(유지율이 절반이 될 때까지의 과제 수)다. 이는 기존 지속 언어학습 벤치마크(TRACE, TemporalWiki, CITB)의 전이·중 downstream 성능 측정이나 순차 모델 편집(GRACE 등, 반복 편집이 이전 편집을 약화시킨다는 후속 연구)의 표적 편집 지표와 구별되는, 연상 유지(associative retention)의 분리 측정이다. 적은 고전적 치명적 망각(McCloskey & Cohen, French, EWC, SI)이 적이다: 새 과제의 그래디언트 스텝이 이전 연상을 덮어쓴다.

## 방법론

**설계 공간.** 앵커는 업데이트가 보존해야 할 과거 과제의 증거 형태를, 저랭크 할당은 각 과제가 쓰는 LoRA 용량과 업데이트 영속 방식을 규정한다:

- **데이터 앵커 — 무조건 생성적 리플레이**: 마지막 과제까지 학습된 모델이 과거 데이터의 의사 샘플을 무조건 생성 (저장 예제 전달 없음; Shin et al., LAMOL 계열). 과제 수에 대해 상수 메모리.
- **함수 앵커 — 이전 상태 자기 증류**: 과제 t−1 종료 시점의 고정 모델을 교사로 삼아 현재 과제 입력에 대한 출력 분포(KL)를 일치시킨다 (Learning without Forgetting 계열). 상수 메모리.
- **가중치 앵커 — 중요도 정규화**: Synaptic Intelligence (SI)와 online EWC가 이전 과제에 중요한 파라미터의 이동에 페널티 (학습 가능 텐서당 기준값 + 대각 중요도/Fisher 텐서 1개씩, 과제마다 폐기). 상수 메모리.
- **Shared LoRA**: 모든 과제가 하나의 rank-r 어댑터 재사용 (바닐라 베이스라인 할당).
- **Merged LoRA** (ReLoRA 계열): 과제별 업데이트를 dense 가중치에 폴드한 뒤 새 rank-r 어댑터 초기화 — 누적 변화가 사실상 higher-rank가 된다. 상수 메모리.
- **O-LoRA / 순차 OSRM**: 과제별 부분공간 + 중첩 페널티 또는 특징 기반 초기화 (선형 저장 비용, 비교용 포함).

**데이터셋 (3종 × 100과제)**: 임의 기호 연상(순수 기억 스트레스 테스트), LLM 생성 가상 팩트(LLM-QA), 공개 QA 선별 자연 질문(Real-QA: TriviaQA, SQuAD, ARC, OpenBookQA, MedMCQA 출처). 학습은 질문+답변 토큰 전체 시퀀스를 커버 (배포 시 질문 프리픽스가 없다는 가정과 일치, 리플레이 시드는 마스킹).

**탐색·분석**: 과제 단위 successive halving (하이퍼파라미터 탐색에서 차용)으로 큰 조합 공간을 저비용으로 가지치기해 예비 증거 확보, 이후 요인 실험으로 주효과·상호작용을 엄밀 정량화.

## 결과

- **구성이 모든 데이터셋에서 최단일 메커니즘을 이긴다** (Figure 1 기억 수명 곡선, 3-시드 평균): 순수 순차 SFT 최종 유지율 평균 1.2%, 최단일 메커니즘 8.1%에 그친다.
- **최적 방법 — 3개 앵커 전부 + merged LoRA** — 요인 실험 구성 중 유일하게 전 데이터셋 3위권, 평균 최종 유지율 34.9% (순수 대비 28배).
- **요인 분석**: 데이터 앵커와 merged LoRA가 가장 큰 개별 기여, 둘의 상호작용은 세 데이터셋 모두에서 **초가산적** — 생성 리플레이 의사 데이터와 과제별 fresh 용량이 서로 강화한다.
- **할당 규칙 ablation**에서 merged LoRA가 shared LoRA를 앞서고, O-LoRA/OSRM 변형은 경쟁적이나 선형 저장 비용을 치른다.
- **코드/데이터**: compose-cl.github.io, github.com/cozheyuanzhangde/compose-cl, Hub 데이터셋 cozzyde/long-horizon-memorization.

## 한계 및 향후 과제

- **일반화가 아닌 기억**: 평가는 학습 질의를 그대로 회상한다. 연상을 유지해도 바꿔 말한 질의에는 실패할 수 있으며, 새 formulation으로의 일반화 주장은 없다.
- **일반 능력은 여전히 저하**: 부록 E.9에서 보듯 최적 방법도 100과제 후 held-out 일반 벤치마크(MATH/MMLU 계열) 정확도가 크게 하락 — 연상을 쌓으면서 광범위 능력을 지키는 것은 미해결 과제.
- **100과제 지평과 QA 전용 인터페이스**: 더 긴 지평, 혼합 과제 형식, 사전학습 스케일 업데이트와의 interleaving은 미검증이며, 분포 이동 하에서 중요도 추정치(SI/Fisher)가 빗나갈 수 있다.

## 소프트웨어 엔지니어에의 시사점

배포 모델을 계속 미세조정하는 팀(신제품을 흡수하는 지원 봇, 새 API를 따라가는 코딩 어시스턴트)에게 교훈은 아키텍처적이다: **망각 방지 트릭 하나를 고르지 말고 리플레이 신호와 용량 정책을 구성하라**. 구체적으로 무조건 생성적 리플레이는 예제 저장이 필요 없고(프라이버시 친화적), merged-LoRA 폴딩은 학습 루프 두 줄 변경에 상수 메모리 — 본 연구에서 초가산으로 작용한 쌍이다. 최신 과제 정확도가 아니라 과제 스위트가 늘어남에 따른 최종 유지율과 기억 반감기를 추적하고, 일반 능력 회귀는 별도 완화(사전학습 데이터 혼합, 주기적 병합)가 필요하다고 예상하라. `concepts/ai-engineering/llm-training.md`와 `concepts/machine-learning/knowledge-distillation.md`의 확장이다.

## 참고 자료

- 논문: https://arxiv.org/abs/2609.06986 (HTML: https://arxiv.org/html/2609.06986)
- 프로젝트: https://compose-cl.github.io/ — 코드: https://github.com/cozheyuanzhangde/compose-cl — 데이터: https://huggingface.co/datasets/cozzyde/long-horizon-memorization
- LoRA (Hu et al. 2022); ReLoRA (Lialin et al. 2024); O-LoRA (Wang et al. 2023); EWC (Kirkpatrick et al. 2017); SI (Zenke et al. 2017); LwF (Li & Hoiem 2017); DER (Buzzega et al. 2020)
