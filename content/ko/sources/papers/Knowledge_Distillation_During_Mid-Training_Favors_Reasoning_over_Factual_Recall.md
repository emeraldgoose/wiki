---
title: Knowledge Distillation During Mid-Training Favors Reasoning over Factual Recall
description: '중간학습 Switch 증류 — 추론 1.6배, 사실 회상 96.7% 보존'
tags: [source, paper, huggingface, machine-learning, ko]
locale: ko
source_url: "https://arxiv.org/abs/2609.01532"
arxiv_id: 2609.01532
---

# Knowledge Distillation During Mid-Training Favors Reasoning over Factual Recall

**arXiv**: 2609.01532 | **게시일**: 2026-09-01 | **기관**: Meta

**저자**: Jacqueline He, Howard Yen, Shuyue Stella Li, Margaret Li, Hanqing Zeng, Yinglong Xia, Benyu Zhang, Zhuokai Zhao, Qiang Zhang, Pang Wei Koh, Luke Zettlemoyer, Wen-tau Yih

## 핵심 기여

- **단계 의존성 발견**: forward-KL 증류는 사전학습에서 NTP 대비 추론·사실 회상 둘 다 올리지만, 중간학습(mid-training)에서는 추론 이득 지속 + 사실 회상 습득 *지연*
- **메커니즘**: 도메인별 교사 확신 비대칭(절차 데이터 확신 > 지식 집약 확신) × 학생 상태(저엔트로피 사실 먼저 학습)의 충돌
- **Switch Distillation**: 교사 확신 토큰만 증류(예측 엔트로피 라우팅), 나머지는 CE. 교사 크기 전반에서 기존 KD 목적함수 능가

## 방법론

사전/중간학습에서 forward KD vs 표준 NTP 통제 실험으로 확신×지식상태 상호작용을 추적한 뒤, 엔트로피 라우팅 Switch 증류를 사후학습까지 검증.

## 결과

| 발견 | 수치 |
|---|---|
| Switch vs NTP: 추론 | **1.61~1.71배** |
| Switch vs NTP: 지식·상식 | **1.13~1.19배** |
| 사실 회상 보존 | **96.7~96.8%** |
| 사후학습 후 | 격차 해소, 추론 **1.25~1.32배**·지식 **1.13~1.20배** 유지 |

## SW 엔지니어를 위한 시사점

소형 LM 중간학습 증류는 무작정 하지 마세요 — 교사 엔트로피로 라우팅하지 않으면 사실 회상에 세금이 붙습니다. Switch 증류는 2줄 변경(엔트로피 게이트+CE 폴백)에 1.6배급 추론 이득, 사후학습까지 생존합니다.

## 관련 개념

- [지식 증류](../../concepts/machine-learning/knowledge-distillation.md)
- [LLM 훈련](../../concepts/ai-engineering/llm-training.md)
- [트랜스포머](../../concepts/machine-learning/transformer.md)

## 참고

- 원문: https://arxiv.org/abs/2609.01532
- HF Daily Papers: https://huggingface.co/papers/2609.01532
- 범위: 초록 기반. 교사 크기별 결과는 전문에서 확인
