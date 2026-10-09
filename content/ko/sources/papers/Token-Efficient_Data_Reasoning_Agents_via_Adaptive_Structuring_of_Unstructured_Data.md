---
title: Token-Efficient Data Reasoning Agents via Adaptive Structuring of Unstructured Data (번역 요약)
description: en/sources/papers/Token-Efficient_Data_Reasoning_Agents_via_Adaptive_Structuring_of_Unstructured_Data.md 한국어 번역 요약
tags: [source, paper, huggingface, ko]
locale: ko
arxiv_id: 2608.31082
---

# Token-Efficient Data Reasoning Agents via Adaptive Structuring of Unstructured Data — 요약

**arXiv**: 2608.31082 | **게시일**: 2026-08-31 | **기관**: Harvard University

**저자**: Milad Rezaei Hajidehi, Qitong Wang, Stratos Idreos

## 핵심 기여

- 추론 중 비정형 데이터의 적응적/투기적 구조화를 위한 에이전틱 데이터 크래킹 제안
- 구조화는 적응적: 관측된 쿼리가 언제·무엇을 구조화할지 결정
- 구조화는 투기적: 현재 질문을 넘어 관련 미래 쿼리까지 대비
- 로드된 컨텍스트에서 한계 비용으로 분기하는 크래킹 서브에이전트
- FanOutQA에서 테스트 질문당 관련 질문 1개 기준 정확도 유지하며 비용 53% 절감
- 차세대 데이터 인프라 프레임워크: 모델 아래 공유 기층

## 방법론

에이전틱 데이터 크래킹: 에이전트가 문서를 열면 크래킹 서브에이전트가 로드된 컨텍스트에서 한계 비용으로 분기해 그라운딩된 구조를 추출. 구조화는 적응적(쿼리가 시기/대상 결정)이고 투기적(현재 질문 초과). 시간이 지날수록 구조화 데이터가 쿼리의 더 큰 비중을 커버해 문서 열람 없이 답변. FanOutQA 벤치마크로 비용/정확도 트레이드오프 평가.

## 결과

FanOutQA에서 테스트 질문당 관련 질문 1개 기준 정확도 유지하며 비용 53% 절감. 질문 수 확대 시 사전 구조화 저장소 대비 격차가 수십 배로 확대(이상적 조건 28배 저렴). RAG 수준 비용으로 에이전틱 정확도 유지.

## SW 엔지니어를 위한 시사점

SW 엔지니어 관점에서 LLM 에이전트가 거대 비정형 문서를 반복 열람하는 비용 문제를 해결. 적응적/투기적 구조화는 필요할 때만, 미래 쿼리까지 대비해 구조를 만들어 RAG 수준 비용으로 사전 구조화 DB급 효율에 접근. 한계 비용 크래킹 서브에이전트 모델은 효율적 데이터 인프라 구축 패턴. 비정형 사내 데이터(Confluence, SharePoint, S3 문서 등) 위에서 추론하는 에이전틱 시스템 전반에 해당. 관련 질문 1개당 53% 절감은 구체적이고 측정 가능한 개선.

## 관련 개념

- `concepts/ai-engineering/agent.md`
- `concepts/ai-engineering/llm-training.md`
- `concepts/machine-learning/transformer.md`

## 참고

- 원문: en/sources/papers/Token-Efficient_Data_Reasoning_Agents_via_Adaptive_Structuring_of_Unstructured_Data.md
- arXiv: https://arxiv.org/abs/2608.31082
