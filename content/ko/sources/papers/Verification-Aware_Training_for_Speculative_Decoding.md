---
title: Verification-Aware Training for Speculative Decoding
description: '검증 인식 드래프트 학습 — 수락 길이 +11.4%, 벽시계 +8.7%'
tags: [source, paper, huggingface, ko]
locale: ko
source_url: "https://arxiv.org/abs/2608.30135"
arxiv_id: 2608.30135
---

# Verification-Aware Training for Speculative Decoding

**arXiv**: 2608.30135 | **게시일**: 2026-08-31 | **기관**: NAVER AI Lab

**저자**: Geonmo Gu, Byeongho Heo, HeeJae Jun, Yoohoon Kang, Sangmin Lee, Sangdoo Yun, Dongyoon Han

## 핵심 기여

- **문제**: 순차 검증은 첫 기각부터 뒤를 전부 버리는데, 드래프트 학습은 이를 반영 못하는 고정 위치별 모방 가중치 사용
- **VAT(검증 인식 학습)**: 매 스텝 검증을 시뮬해 수락·기각 패턴을 supervision으로 — (i) 검증 헤드(각 위치의 순차 검증 생존 여부 이진 분류기, 공동 학습), (ii) 검증 적응 가중(표본별 첫 기각까지 전 가중, 감쇠를 거기서 재시작)
- **호환성**: 학습 목적함수만 변경. 드래프트 구조·타깃·추론 절차 불변, 기존 기법 위에 얹힘

## 방법론

Qwen3-4B·8B, LLaMA-3.1-8B에서 EAGLE-3·DFlash에 적용. 수학·코드·대화 벤치로 수락 길이·벽시계 가속 측정.

## 결과

| 발견 | 수치 |
|---|---|
| 평균 수락 길이 | 최대 **+11.4%** |
| 벽시계 가속 | 최대 **+8.7%** |
| 일반성 | 수학·코드·대화 일관 이득 |

## SW 엔지니어를 위한 시사점

스페큘러티브 디코딩 서빙 중이라면 VAT는 공짜 업그레이드 — 추론 변경 없이 드래프트 헤드만 검증 시뮬레이션으로 재학습. 위치가 아니라 생존으로 가중하세요. 코드 공개 예정: https://github.com/naver-ai/vat

## 관련 개념

- [스페큘러티브 디코딩](../../concepts/ai-engineering/speculative-decoding.md)
- [LLM 훈련](../../concepts/ai-engineering/llm-training.md)
- [트랜스포머](../../concepts/machine-learning/transformer.md)

## 참고

- 원문: https://arxiv.org/abs/2608.30135
- HF Daily Papers: https://huggingface.co/papers/2608.30135
- 범위: 초록 기반. 모델·벤치별 표는 전문에서 확인
