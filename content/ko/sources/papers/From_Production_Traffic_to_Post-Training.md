---
title: "From Production Traffic to Post-Training: Building a Self-Hosted LLM That Covers the Corporate Request Mix (번역 요약)"
description: en/sources/papers/From_Production_Traffic_to_Post-Training.md 한국어 번역 요약
tags: [source, paper, huggingface, ko]
locale: ko
arxiv_id: 2609.01572
---

# From Production Traffic to Post-Training: Building a Self-Hosted LLM That Covers the Corporate Request Mix — 요약

**arXiv**: 2609.01572 | **게시일**: 2026-09-01 | **기관**: T-Tech

**저자**: Olga Tsymboi, Dmitrii Stoianov, Ramil Latypov, Danil Taranets, Daniil Dryabin, Mikhail Gashkov, Viktor Zelenkovskiy, Aleksandr Fida, Gleb Alektorov, Nikita Gulyakov, Arthur Babkin, Aleksandr Medvedev, Pavel Gein, Anatolii Potapov

## 핵심 기여

- 200개 이상 내부 애플리케이션을 단일 셀프호스팅 LLM으로 통합
- 3축 품질 분석: 지시 이행, 함수 호출, 내부 태스크 분포
- 축별 실패 모드 해소를 위한 축별 GRPO 전문가 학습
- 2단계 SLERP 병합으로 전문가들의 상호 보완 강점 결합
- 사내 Arena에서 약 7배 작은 모델이 대형 베이스라인과 대등
- 플랫폼 트래픽의 50%(월 1.16억 요청)를 일부 서빙 비용으로 흡수

## 방법론

200개 이상 내부 앱의 운영 오류 분석을 3축으로 수행. 축별(지시 이행, 함수 호출, 태스크 분포) GRPO 전문가 개별 학습. 2단계 SLERP 전문가 병합. 결정적 검증기와 보정된 LLM 저지자를 쓰는 오프라인 벤치마크. 운영 트래픽 분포로 층화한 품질 추적.

## 결과

약 7배 작은 모델이 사내 Arena에서 대형 베이스라인과 대등(69.6 vs 65.8). 지시 이행 0.85 vs 0.83, 함수 호출 0.79 vs 0.77 개선. 일반 대화 벤치마크도 상승. 플랫폼 트래픽 50% 흡수(월 1.16억 요청)를 일부 서빙 비용으로 달성.

## SW 엔지니어를 위한 시사점

SW 엔지니어 관점에서 다수 LLM 서빙 엔드포인트를 단일 모델로 통합하는 실용 접근. 축별 GRPO 전문가 학습과 SLERP 병합 기법은 비용 비례 증가 없이 모델 역량을 키우는 프레임워크. 동등 성능의 7배 축소는 GPU 제약 환경에 직접 적용 가능. 3축 품질 프레임워크(지시 이행, 함수 호출, 태스크 분포)는 점진적 모델 개선의 실용 방법론. 월 1.16억 요청을 저비용으로 처리한 사례는 대규모 배포 시나리오에 바로 적용 가능.

## 관련 개념

- `concepts/ai-engineering/agent.md`
- `concepts/ai-engineering/llm-training.md`
- `concepts/machine-learning/transformer.md`

## 참고

- 원문: en/sources/papers/From_Production_Traffic_to_Post-Training.md
- arXiv: https://arxiv.org/abs/2609.01572
