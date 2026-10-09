---
title: "LLaDA-Image: 완전 공개 학습 레시피로 강한 이미지 생성기 만들기"
description: "HuggingFace Daily Papers — 2026-09-03 — 이미지-전용 사전학습과 TwinFlow 증류의 6B 통합 이미지 생성기"
tags: [source, paper, huggingface]
locale: ko
arxiv_id: 2609.03796
published: 2026-09-03
---

# LLaDA-Image: 완전 공개 학습 레시피로 강한 이미지 생성기 만들기



**arXiv**: [2609.03796](https://arxiv.org/abs/2609.03796) | **HuggingFace**: [papers/2609.03796](https://huggingface.co/papers/2609.03796) | **Published**: 2026-09-03 | **제출**: Haoxing Chen (Inclusion AI) | **Paper of the day #3 (2026-09-04)**

**저자**: Chuyan Chen, Haoxing Chen, Kun Chen, Zhenglin Cheng, Long Cui, Ruishan Fang, Zhangxuan Gu, Zhicheng Huang, Zhenzhong Lan, Yuanting Lei, Haoquan Li, Jianguo Li, Rongchuan Li, Sidu Li, Tao Lin, Deyuan Liu, Jiacheng Liu, Lin Liu, Yuxuan Lou, Zhisheng Lu, Yuxin Ma, Shuheng Shen 외 (AGI Research Center, Inclusion AI)

## 초록

LLaDA-Image는 **처음부터 학습한 6B Diffusion Transformer(DiT)** 와 LLaDA2.0-Mini 확산 언어모델 백본 위의 **고정(frozen) 비전-언어 이해 모듈**을 결합한 통합 프레임워크이다. 처음부터 이미지–텍스트 쌍 데이터에 크게 의존하는 대신 **이미지-전용 사전학습과 중간학습**으로 강한 시각 생성 prior를 먼저 만든다. 전체 생성 파이프라인은 약 **220M 샘플(98% 실제 이미지)** 을 처리하며, 이미지-전용 학습이 전체의 90% 이상을 차지한다. 최적화는 DiT 전반의 **무파라미터 RMSNorm과 Muon 옵티마이저**로 대규모 안정성을 확보한다. 통합 모델은 사실적인 이미지를 만들면서 세밀한 편집 지시를 따르고, **LLaDA-Image-Turbo**로 증류되어 **2~4 스텝** 추론을 지원한다. Qwen-Image-Bench에서 **영어 53.53, 중국어 53.38**으로 영어·중국어 트랙 모두 오픈소스 SOTA를 세웠다. 가중치·학습 코드·상세 레시피를 전부 공개한다(Base, Turbo, 각각의 FP8 변형 포함).

## 배경: 문제 설정 (WHY)

이미지 시스템은 단일 목적 T2I 모델에서 범용 시각 창작 시스템으로 이동 중이다. 복잡한 다국어 지시를 이해하고, 사실적 콘텐츠를 합성하며, 편집 중 reference 정보를 보존하고, 텍스트를 정확히 렌더링하면서도 실용적인 추론 예산 안에 들어야 한다. proprietary 시스템이 앞서지만 데이터·모델·레시피가 닫혀 있다. 따라서 오픈 모델의 목표는 품질만이 아니다. 달성 가능한 데이터 예산, 안정적인 대규모 학습, 효율적 배포가 함께 와야 한다.

주류 패러다임은 시각 prior 학습과 언어 정렬을 첫 스텝부터 묶어, 가장 계산량이 큰 단계에 쌍 캡션을 요구한다. 그러나 캡션은 비싸고 손실적이다(낮은 학습 해상도에서는 캡션의 세부사항이 다운샘플링 뒤 사라질 수 있다). 합성 이미지–텍스트 쌍은 초기 수렴을 가속하지만 아티팩트를 전파하고 장기 사실성에 상한을 둔다. 여기에 두 문제가 더 얽힌다. reference 이미지 증거를 보존하면서 다중모달 이해를 생성에 연결하는 것, 그리고 긴 확산 궤적을 배포용으로 압축하는 것이다. LLaDA-Image는 데이터·아키텍처·배포를 함께 설계해 셋을 한 번에 겨냥한다.

## 방법론 (HOW)

### 아키텍처: 세 요소, 하나의 체크포인트

- **dLLM 기반 VLM (고정).** LLaDA2.0-Mini 백본 + SigLIP-VQ 비전 인코더 위의 이해 모듈이다. 정적 텍스트 인코더와 달리 텍스트·시각 맥락·구조화된 추론 흔적을 함께 추론한다. 핵심적으로, 편집 시 **reference 이미지는 VLM을 완전히 우회**하여 DiT에 직접 주입된다. VLM은 편집 지시만 본다.
- **이해→생성 커넥터.** 표현 간극을 메우는 생성 전용 모듈 두 개: **Residual Query Adapter(RQA)** — 학습 가능한 쿼리가 다중모달 입력에 cross-attend한 뒤 입력에 덧붙어, 고정 VLM에 단일 prefill 패스로 생성에 유용한 맥락을 끌어내게 한다 — 와 VLM hidden state를 DiT 조건 공간에 투영하는 얕은 **Transformer 커넥터**이다.
- **단일 스트림 DiT (6B).** 이미지 토큰과 조건 토큰을 하나의 공유 시퀀스에 임베드해 같은 블록 스택으로 함께 처리하므로, 모든 블록이 joint self-attention으로 조건↔시각 상호작용을 모델링한다(분리 스트림 없음). flow-matching velocity를 예측한다. **레시피 #1: 모든 정규화층을 무파라미터 RMSNorm으로 교체**했고, 저자들은 이것이 장기 학습 안정성의 공신이라 밝힌다.

### 학습 파이프라인: 시각 prior 먼저, 언어는 나중에

1. **CoT SFT**로 고정 이해 백본을 준비한다.
2. **이미지-전용 사전학습 (256²).** 고정 dLLM-VLM이 DiT가 생성할 바로 그 이미지 영역에서 조건을 도출한다. 조건–타깃 정합을 외부 캡션 없이 확보하므로 고해상도 이미지의 정보성 crop을 가볍게 리사이즈해 바로 쓸 수 있다.
3. **이미지-전용 중간학습 (512², 종횡비 버킷).**
4. **지도 미세조정 (512² → 1024²)** — T2I 학습 뒤 **생성–편집 공동** 학습(T2I + I2I), 텍스트 밀집·인물 데이터 정제와 체크포인트 병합 포함. **SFT 전 기간 실제 이미지 비중이 70%를 넘는다**. 합성 위주 레시피보다 초기 벤치마크 상승은 느리지만 수렴 시 사실성이 강하고 장기 상한이 높다.
5. **TwinFlow 퓨-스텝 증류.** 분포 매칭 증류(DMD)와 자기적대 flow 학습 기반: 하나의 공유 DiT 백본이 **부호 시간**으로 두 역할을 수행한다. 양의 +t는 생성자 업데이트, 음의 −t는 fake-score 추정기 학습(별도 score 네트워크 없음). "one-input, dual-output"로 출력 헤드 두 개(fake-score 헤드, DMD 헤드)를 달고, 추론 때는 DMD 헤드만 남기고 fake-score 헤드는 버린다. 결과: **2~4 샘플링 스텝의 LLaDA-Image-Turbo**.

## 결과

- **Qwen-Image-Bench.** 전체 영어 53.53, 중국어 53.38 — **양 트랙 오픈소스 SOTA**. 논문의 정성 그리드는 Qwen-Image, GPT-Image 2, Gemini Flash Image 등과 비교한다(사실적 인물, 서예 포함 중국 산수화, 한영 텍스트 렌더링).
- **범위.** 태스크별 백본 없이 단일 체크포인트로 경쟁력 있는 지시 기반 편집(스타일 변환, 텍스트 교체, 객체 제거·추가, 배경 교체, 제스처 편집)과 LongText-Bench, CVTG-2K 성적.
- **배포 프로파일.** Base(다중 스텝, 품질)와 Turbo(2~4 스텝, 비용). 공개 체크포인트 총 4개(Base, Turbo, 각각 FP8)에 학습·추론 코드와 데이터 구축 레시피 포함.
- **정성적 장치.** 보고서는 독자 챌린지로 시작한다. 진짜 사진처럼 보이는 격자를 보여주고 진짜를 고르게 한 뒤, **전부 생성 이미지**였음을 밝힌다(T2I 합성과 한영 텍스트 렌더링). 통제된 지각 연구가 아닌 시연임을 명시한다.

## 한계 / 열린 질문

- **명시적 범위 선언.** 각 요소의 보편 최적성을 주장하지 않으며 아키텍처·데이터 혼합의 exhaustive 비교도 시도하지 않았다. 기여는 들여다볼 수 있고 재사용 가능한 레시피이다.
- **실제 데이터는 인내가 필요.** 실제 데이터 위주 혼합은 초기 벤치마크 상승이 느리다. 빠른 리더보드 상승이 목표면 사실성 상한이 낮아도 합성 위주 레시피가 유혹적일 수 있다.
- **단일 모델 편집의 경계.** reference 보존 편집은 설계상 VLM을 우회한다. 세밀한 정체성 보존과 복합 다중 지시 편집 실패가 실용적 프런티어로 남는다.
- **6B 동작점.** 레시피는 단일 규모에서 입증되었다. 6B 너머에서 이미지-전용 prior 접근의 스케일링 법칙은 미검증이다.

## 소프트웨어 엔지니어와의 관련성

- **prior와 정렬을 분리하라.** 이미지-전용 자기조건화 트릭(생성 타깃 자체 영역에서 조건 도출, 캡션 불필요)은 쌍 데이터가 병목인 곳이면 어디든 이식 가능하다. 값비싼 캡션 예산을 쓰기 전에 저렴한 unlabeled 이미지로 prior를 태우는 방법이다.
- **복사할 만한 안정성 레시피.** 전역 무파라미터 RMSNorm + Muon 옵티마이저는 장기 생성 학습 불안정에 대한 작고 구체적인 개입이다.
- **부호 시간 패턴으로 증류하라.** 하나의 백본, 두 개의 헤드, 타임스텝 부호로 역할 구분 — 별도 fake-score 네트워크가 필요 없다. 서빙용으로 압축해야 하는 flow-matching 모델에 그대로 적용된다.
- **하나의 계보에서 두 프로파일을 출고하라.** 품질용 Base, 비용용 Turbo, 메모리용 FP8 변형 — 생성 모델 서빙 경로의 출시 행렬로 복사할 만하다.
- **쓰지 말아야 할 곳.** 자체 평가 하네스 없이 모션·비디오나 상용 렌더링 파이프라인의 텍스트 렌더링 정확도를 기대하지 마라. 자신의 프롬프트 분포에서 Qwen-Image-Bench/LongText-Bench류 검사를 먼저 돌려라.

## 관련 개념

- `concepts/machine-learning/transformer.md`
- `concepts/ai-engineering/llm-training.md`

## 참고문헌

- arXiv: https://arxiv.org/abs/2609.03796
- HuggingFace: https://huggingface.co/papers/2609.03796
- 코드 + 가중치: https://github.com/inclusionAI/LLaDA-Image 및 https://huggingface.co/collections/inclusionAI/llada-image
