---
title: "AgentJudgeBench: A Multi-Difficulty Benchmark for Evaluating LLM Judges on Agentic Tool-Calling"
description: '에이전틱 도구 호출 심판의 첫 벤치마크 — 3,808 인스턴스, 난이도별 77~82% 상한, 정답 과잉 앵커링'
tags: [source, paper, huggingface, ko]
locale: ko
source_url: "https://arxiv.org/abs/2608.26623"
arxiv_id: 2608.26623
---

# AgentJudgeBench: A Multi-Difficulty Benchmark for Evaluating LLM Judges on Agentic Tool-Calling

**arXiv**: 2608.26623 | **게시일**: 2026-08-27 | **기관**: ServiceNow-AI

**저자**: Abhigya Verma, Amit Kumar Saha, Seganrasan Subramanian, Sai Harshitha Aluru

## 핵심 기여

- 에이전틱 도구 호출용 LLM-as-a-judge의 첫 체계적 벤치마크 — 6종 DAG 위상 × 3단계 난이도, 3,808 인스턴스. 개방형 텍스트 평가와 분리해 심판 신뢰도를 측정
- 정답 유무 paired 조건: 5종 생성기(3B~70B 오픈 + GPT-5.4) × 6종 심판(20B~프런티어)
- 구조적 상한 발견: 난이도가 오르면 정렬도 단조 감소, 정답 없을 때 1.5배 가속. 어려운 질의+정답 없음에서는 6종 심판 모두 규모 무관하게 77~82%에 수렴
- 과잉 앵커링: 정답 노출이 GPT-5.4 −1.5점, Gemini-2.5-Pro −3.9점 하락

## 방법론

3단계 난이도 워크플로 DAG에 정답 유무 조건을 짝지어 평가. 프로그램 기준 정답 + 인간 검증 연구로 심판-생성기 행렬을 측정. 완화책(CoT·온도·구조화 루브릭)을 비교.

## 결과

| 발견 | 수치 |
|---|---|
| 정답 없을 때 난이도 열화 | 정답 있을 때의 1.5배 속도 |
| 어려운 질의·정답 없음 (6종 심판) | 규모 무관 77~82% 구간 |
| 정답 과잉 앵커링 | GPT-5.4 −1.5점, Gemini-2.5-Pro −3.9점 |
| CoT 추론·온도 | 효과 미미 |
| 구조화 루브릭 | 최대 +6.5점, 쌍별 편차 있음 |
| 정답 조건 최고 | QwQ-32B (프로그램 일치), 인간 일치 최고는 GPT-OSS-120B |

## SW 엔지니어를 위한 시사점

어려운 다단계 도구 호출에서 정답 없는 LLM 심판을 믿지 마세요 — 규모로 상한이 안 깨집니다. 구조화 루브릭(+6.5점, 전이 확인 필요)과 정답 유무 paired 평가를 예산에 넣고, 정답을 보여줄 때 과잉 앵커링을 경계하세요. 기준점은 QwQ-32B와 GPT-OSS-120B.

## 관련 개념

- [에이전트 평가](../../concepts/ai-engineering/agent-evaluation.md)
- [에이전트](../../concepts/ai-engineering/agent.md)
- [LLM 훈련](../../concepts/ai-engineering/llm-training.md)

## 참고

- 원문: https://arxiv.org/abs/2608.26623
- HF Daily Papers: https://huggingface.co/papers/2608.26623
- 범위: 초록 기반. DAG별 표는 전문에서 확인
