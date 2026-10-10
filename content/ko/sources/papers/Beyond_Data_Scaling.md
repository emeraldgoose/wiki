---
title: "데이터 스케일을 넘어서 — 비전-언어-액션 모델의 표현 중심 지속 사전학습"
description: "HuggingFace Daily Papers — 2026-08-26 — VLAct: 표현 중심 지속 사전학습으로 데이터 효율적인 VLA"
tags: [source, paper, huggingface, ai-engineering]
locale: ko
arxiv_id: 2608.27550
published: 2026-08-26
---

# 데이터 스케일을 넘어서 — 비전-언어-액션 모델의 표현 중심 지속 사전학습



**arXiv**: [2608.27550](https://arxiv.org/abs/2608.27550) | **HuggingFace**: [papers/2608.27550](https://huggingface.co/papers/2608.27550) | **Published**: 2026-08-26 | **조직**: StarVLA | **프로젝트**: https://starvla.github.io/VLAct | **백본**: VLAct · Qwen3-VL-4B (`StarVLA/VLAct_Qwen3_Pretrain`)

**저자**: Senqiao Yang, Chengyao Wang, Yuxin Chen, Zixuan Wang, Longxiang Tang, Haokun Gui, Jinhui Ye, Changsheng Lu, Xiaoyang Wu, Mingkang Zhu, Pengguang Chen, Shu Liu, Zhuotao Tian, Hengshuang Zhao, Bei Yu, Jiaya Jia

## 초록

비전-언어-액션(VLA) 모델은 보통 로봇 궤적 데이터를 늘려 개선하지만, 로봇 데이터는 희귀하고 수집 비용이 크다. 고정된 로봇 데이터 예산에서는 지속 사전학습(continued pre-training)이 제한된 궤적을 단순히 행동에 fitting하는 것이 아니라 전이 가능한 시각-행동 지식으로 바꿔야 하며, 이때 표현 품질이 핵심 병목이 된다. 본 논문은 태스크별 미세조정 이전에 광범위하고 이질적이며 다중 embodiment인 로봇 데이터로 학습한 VLA 지향 VLM 백본 VLAct를 제안한다. VLAct는 VLM prior 보존, 다중 헤드 연속 행동 공동 supervision, 부분 통합 다중 embodiment 행동 배치로 넓은 VLM prior를 유지하고 embodiment를 가로지르는 공유 행동 의미를 유도하면서, 미세조정 시 태스크별 행동 헤드를 허용한다. 완전 오픈소스 데이터와 16-GPU 학습 설정만으로 얻은 결과는, 표현 중심 지속 사전학습이 적당한 계산 예산에서 매우 경쟁력 있는 성능을 내며 데이터 스케일을 넘어선 VLA 발전의 독립적 축임을 보여준다.

## 핵심 기여

- VLA 발전을 데이터양이 아닌 표현 품질의 문제로 framing — 데이터 스케일을 넘어선 독립적 축
- VLAct: 광범위·이질적·다중 embodiment 로봇 데이터로 지속 사전학습한 VLA 지향 VLM 백본(Qwen3-VL-4B 기반)
- 지속 사전학습 세 원칙: VLM prior 유지, embodiment 간 행동 의미 공유, 미세조정 시 버려지는 사전학습 헤드의 스캐폴딩
- 부분 통합 다중 embodiment 행동 배치: 로봇이 동일하다고 가장하지 않고 공유할 의미는 공유한다(embodiment별 차원은 유지)
- 공개 레시피: 완전 오픈소스 데이터, 16-GPU 설정, 공개 가중치(`StarVLA/VLAct_Qwen3_Pretrain`), 학습 파이프라인과 데이터셋 준비 스크립트

## 방법론

지속 사전학습은 베이스 VLM과 하류 태스크 미세조정 사이에 위치한다. 하류 미세조정에서는 전체 모델을 다시 unfrozen하며, 지속 사전학습의 행동 헤드는 스캐폴딩으로 쓰고 새로 초기화된 태스크별 헤드로 교체한다.

1. **VLM-prior 보존** — VLM이 이미 아는 것을 지킨다. 캡션 supervision이 지속 사전학습 중 넓은 시각·의미 지식을 고정시켜 로봇-행동 학습이 범용 비전-언어 prior를 씻어내지 않게 한다. 비전-언어 데이터 혼합 ablation에서 prior 보존 항이 load-bearing임이 확인된다.
2. **다중 헤드 연속 행동 공동 supervision** — embodiment들을 가로지르는 연속 행동 헤드들의 공동 supervision이 단일 로봇의 행동 분포에 과적합되는 대신 공유되고 전이 가능한 행동 의미를 유도한다.
3. **부분 통합 다중 embodiment 행동 배치** — 세 배치를 비교한다. embodiment별 분리 헤드, 순진한 완전 통합(모든 로봇을 하나의 공간에 강제), 부분 통합(공유 의미 부분공간 + embodiment별 차원). 부분 배치가 승리한다. 전이되는 것은 공유하고 다른 것은 남긴다.

학습 데이터는 광범위하고 이질적인 다중 embodiment 오픈소스 로봇 데이터이며, 데이터셋 준비 스크립트와 실행 스크립트는 VLAct 저장소에 공개되어 있다.

## 결과

- **미관측 embodiment 일반화**: 미관측 휴머노이드 embodiment인 RoboCasa-GR1에서, VLAct 기반 VLA가 하류 궤적의 **20%만으로 전체 데이터 GR00T-N1.6 베이스라인을 능가** — 대표적 데이터 효율 결과이다.
- **넓은 경쟁력**: 적당한 16-GPU 예산에도 시뮬레이션과 관측 embodiment 전반에서 강한 성적.
- **Ablation**: 캡션 혼합 ablation이 VLM-prior 보존의 중요성을 확인하고, 행동 공간 비교는 분리·순진 통합 헤드보다 부분 통합 배치를 지지한다.
- **효율 주장**: 독점 데이터 규모 없이 경쟁력 있는 성능 — 표현 작업이 원시 궤적 물량을 대체한다.

## 한계 / 열린 질문

- 지속 사전학습에도 여전히 다양한 다중 embodiment 데이터 큐레이션이 필요하다. 레시피는 데이터 의존을 줄이지만 없애지는 못한다.
- 부분 통합 배치는 embodiment별 설계 판단(어느 차원을 공유할지)을 요구한다. 완전 자동이 아니다.
- 평가는 조작·휴머노이드 벤치마크(RoboCasa류) 중심이다. 매우 장기 horizon과 접촉 밀집 태스크는 열린 문제로 남는다.

## 소프트웨어 엔지니어와의 관련성

로봇 스택을 만드는 실무자에게: 새 로봇·데이터셋·행동 헤드의 기본 적응 베이스로 raw VLM 미세조정 대신 지속 사전학습 백본(`StarVLA/VLAct_Qwen3_Pretrain`)에서 시작하라. 지속 사전학습 혼합에 캡션/prior 보존 데이터를 유지하고, 다중 embodiment 서빙에는 부분 통합 행동 배치를 쓰며, 사전학습 행동 헤드는 일회용 스캐폴딩으로 취급하라. 실용적 보상은 데이터 효율이다. 적당한 GPU 예산으로 하류 궤적의 일부만으로 전체 데이터 베이스라인과 동등 이상을 맞춘다.

## 관련 개념

- `concepts/ai-engineering/agent.md` (embodied 에이전트 아키텍처)
- `concepts/machine-learning/transformer.md` (VLM 백본 표현)
- `concepts/ai-engineering/llm-training.md` (지속 사전학습 레시피)
- `guides/ai-engineering/build-agent.md` (로봇 에이전트 배포)

## 참고문헌

- arXiv: https://arxiv.org/abs/2608.27550
- HuggingFace: https://huggingface.co/papers/2608.27550
- 프로젝트 페이지: https://starvla.github.io/VLAct
- 가중치: https://huggingface.co/StarVLA/VLAct_Qwen3_Pretrain
