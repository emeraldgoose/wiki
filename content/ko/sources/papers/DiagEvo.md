---
title: "DiagEvo: Diagnosis-Guided Self-Evolution via Hierarchical Error Memory"
description: '실패 기록 기반 자가진화 — 9 벤치 전부 최고, Qwen3-8B 수학 72.3%'
tags: [source, paper, huggingface, ko]
locale: ko
source_url: "https://arxiv.org/abs/2609.00768"
arxiv_id: 2609.00768
---

# DiagEvo: Diagnosis-Guided Self-Evolution via Hierarchical Error Memory

**arXiv**: 2609.00768 | **게시일**: 2026-09-01 | **기관**: LongCat

**저자**: Xincheng Wei, Yifan Ding, Yoshua Li, Dongsheng Ma, Rongxiang Weng, Xunliang Cai, Wenjian Ding, Yao Zhang

## 핵심 기여

- **실패 기록에서 구한 방향**: 난이도·학습가능성·다양성 신호나 외부 태스크 자원이 아니라, 진단기(diagnostician)가 솔버 자신의 실패 기록에서 반복 오류 원인을 뽑아 계층 오류-원인 메모리에 저장 (스킬 노드, Active/Mastered 상태 추적)
- **챌린저**: 메모리 상태·재발 횟수로 원인-표적 생성과 자유 탐색을 균형
- **이중 확신 필터링**: 최다 솔버 답이 명확한 표차일 때만 중간 난이도 문항 유지

## 방법론

기본 4B 진단기의 셀프플레이 루프: 진단→계층 메모리→표적+탐색 문항 생성→필터링 풀이→메모리 갱신. 외부 태스크 자원 없음. 3종 솔버(Qwen3-4B·8B, OctoThinker-8B) × 9 벤치 평가.

## 결과

| 발견 | 수치 |
|---|---|
| 9 벤치 평균 × 3 솔버 전부 | 전 베이스라인 최고 |
| Qwen3-8B, 수학 5 벤치 | **72.3%** (R-Zero 대비 +4.5점) |
| Qwen3-8B, 9 벤치 전체 | **57.4%** (DARC 대비 +1.1점) |
| 절제 | 계층 메모리·이중 확신 필터링 모두 기여 |

## SW 엔지니어를 위한 시사점

자가 개선 LM 파이프라인에는 난이도 점수가 아니라 실패 로그를 캐세요. 오류 원인을 상태 메모리(active/mastered)로 관리하고, 답 일치 마진으로 훈련 문항을 거르세요. 정체된 셀프플레이 루프(코딩·도구 사용 포함)에 그대로 이식됩니다.

## 관련 개념

- [LLM 훈련](../../concepts/ai-engineering/llm-training.md)
- [트랜스포머](../../concepts/machine-learning/transformer.md)

## 참고

- 원문: https://arxiv.org/abs/2609.00768
- HF Daily Papers: https://huggingface.co/papers/2609.00768
- 범위: 초록 기반. 벤치별 표는 전문에서 확인
