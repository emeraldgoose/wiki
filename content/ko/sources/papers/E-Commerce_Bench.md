---
title: "E-Commerce Bench: Evaluating LLM Agents on Long-Horizon Autonomous Business Operation"
description: '365일 상점 운영 벤치 — GPT-5.6 Sol 143만, 오픈 최고 Qwen3.8-Max'
tags: [source, paper, huggingface, ko]
locale: ko
source_url: "https://arxiv.org/abs/2608.30730"
arxiv_id: 2608.30730
---

# E-Commerce Bench: Evaluating LLM Agents on Long-Horizon Autonomous Business Operation

**arXiv**: 2608.30730 | **게시일**: 2026-08-31 | **기관**: Qwen

**저자**: Wei Fan, Xinjie Shen, Xudong Guo, Jianhong Tu, Yang Su, Yinger Zhang, Lianghao Deng, Fengyu Wang, Baohua Dong, Yangqiu Song, Dayiheng Liu

## 핵심 기여

- **협상+동적 이벤트를 넣은 최초 오픈소스 장기 벤치마크**: 365일 1년, 복수 온라인 상점 동시 운영(시장 조사·공급 협상·판매 전략·주문 이행·반품·현금흐름)으로 연말 총자산 최대화
- **현실적이면서 재현 가능**: 실제 커머스 플랫폼의 상품·공급 데이터, 1년 프로모션·재해·공급충격 캘린더, 결정적 수요 모델+협상 커널 (LLM은 발화만)
- **18 프런티어 모델 × 7 차원**, 단일 지배 모델 없음

## 방법론

10만 시드로 365일 시뮬레이션, 결정적 고객·협상 동역학. 연말 자산 + 사기 회피·효율 등 6개 운영 차원으로 채점.

## 결과

| 발견 | 수치 |
|---|---|
| 최고 수익 | GPT-5.6 Sol: 10만 → **1,431,425** — 단 사기 회피 18위 중 16위 |
| 최고 오픈 가중치 | Qwen3.8-Max-Preview **416,252** (GLM 5.2 high 대비 +38%) |
| 지평 학습 | 반복 주문에서 가격을 점진 인하 협상 |
| 결론 | 7 차원 전부 지배 모델 없음 |

## SW 엔지니어를 위한 시사점

장기 비즈니스 에이전트에는 상대방 행동 메모리(협상 레버리지 복리)와 강건성 트레이드오프(최고 수익≈최저 사기 회피)가 필요합니다. 운영 에이전트 벤치는 자산 *과* 안전·효율을 분리 채점하세요. 코드: https://github.com/QwenLM/E-CommerceBench

## 관련 개념

- [에이전트](../../concepts/ai-engineering/agent.md)
- [에이전트 평가](../../concepts/ai-engineering/agent-evaluation.md)

## 참고

- 원문: https://arxiv.org/abs/2608.30730
- HF Daily Papers: https://huggingface.co/papers/2608.30730
- 범위: 초록 기반. 모델별 차원 표는 전문에서 확인
