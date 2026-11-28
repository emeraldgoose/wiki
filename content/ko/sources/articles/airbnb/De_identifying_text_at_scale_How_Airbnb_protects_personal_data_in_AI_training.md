---
title: "데이터 스케일링 시 개인 정보 보호: Airbnb가 ML 훈련용 PII 제거 방법"
description: "Airbnb는 메시지, 리뷰, 고객 지원 채팅과 같은 거래 정보를 ML 훈련용으로 사용할 때, 이름, 위치, 결제 정보 등 PII를 Presidio 라이브러리 기반으로 제거하고 현실적인 가짜 값으로 대체한다. 이 과정에서 검출, 정제, 가짜 생성, 일관성 유지가 핵심이다."
tags: [source, airbnb, privacy, machine-learning, nlp, ko]
locale: ko
source_url: "https://airbnb.tech/infrastructure/de-identifying-text-at-scale-how-airbnb-protects-personal-data-in-ai-training"
blog: airbnb
published_date: 2026-11-28
---

# 데이터 스케일링 시 개인 정보 보호: Airbnb가 ML 훈련용 PII 제거 방법

**원문**: [Airbnb Engineering & Data Science](https://airbnb.tech/infrastructure/de-identifying-text-at-scale-how-airbnb-protects-personal-data-in-ai-training) · **게시일**: 2026-11-18

## 개요

Airbnb는 메시지, 리뷰, 고객 지원 채팅과 같은 거래 정보를 머신러닝 모델에 전달하기 전에 PII(개인식별 정보) — 이름, 주소, 위치, 결제 정보 등 — 를 제거하고 현실적인 가짜 값으로 대체한다. 이 작업은 모델이 학습하는 데이터의 복사 수를 줄이고 모델을 통한 데이터 누출을 방지하기 위함이다. 프라이버시 정책은 Airbnb 프라이버시 아키텍처 팀이 법무, 정책, 공학 팀과 협의해 결정하고, 공학 팀이 이를 코드로 구현한다.

## 핵심 내용

- 두 단계 파이프라인: Presidio Analyzer 가 PII 후보 span 을 찾고 entity type 와 confidence 를 부여한다. Anonymizer 는 겹치는 span 을 해결하고 redact, mask, realistic replacement 와 같은 연산자를 적용한다.
- 세 가지 인식자 유형: pattern-based (regex + context words), NER-based (model-driven), list/context-based. 겹치는 claim 은 Analyzer 에서 해결되지 않고 Anonymizer 의 재구성 단계에 맡긴다.
- Airbnb 전용 entity types: LISTING_ID, AIRBNB_GIFT_CARD 등은 PatternRecognizers 로 구현한다. context word 를 통해 shape-identical digit runs 를 구분한다.
- phrase-context layer: 단일 토큰 매칭은 \"gift card\" 를 놓치고 \"card\" 를 찾는다. Airbnb 는 multi-word phrase 를 먼저 매칭하고, 그 결과가 더 높은 스코어로 선택한다.
- NER backend: spaCy 를 기본으로 사용하지만 PERSON 과 LOCATION 은 GLiNER (zero-shot NER) 로 교체해 정밀도를 높인다. GLiNER2 는 benchmark 가 개선할 경우만 사용된다.
- 언어 감지는 필수: recognizers 와 model 은 언어별로 동작하므로, short spans like names 은 언어 단서가 부족하다. 전체 레코드 또는 locale metadata 로 감지하고, 확신이 없으면 보수적인 설정을 사용한다.
- Anonymizer: 모든 entity type 은 faker-based realistic value 를 사용한다. placeholder token 은 learnable pattern 이므로 실제 값과 매핑되지 않는다. 각 fake 값은 per-run secret 에서 시드된 실제 값 + 시드이다.
- Structured columns: identifier 는 caller-supplied salt 로 해시, coordinates 는 Privacy precision 로 절단, 64-bit internal ID 는 format-preserving encryption 이다.
- Evaluation: recall, precision, throughput 이 세 차원으로 평가되며, recall 을 우선시한다. metrics 은 entity type 와 language 별, labeled-instance count 와 span-claim confusion table 로 보고한다.
- 미래 계획: 더 많은 언어 지원, LLM 기반 recognizer, 텍스트 외 매체 de-identification 이다.

## 세부 사항

- Detection thresholds 와 entity scope 는 recognizer 와 consumer 에 따라 구성된다. training 텍스트 를 위한 낮은 threshold 와 false positive 허용, reviewed data 를 위한 높은 recall 과 제한적인 redaction 을 허용한다.
- Operator choice: faker-based replacement for training, masking for review. structured columns 은 salted hashing, coordinate truncation, format-preserving encryption 으로 처리한다.
- Benchmark 은 release 전 side-by-side evaluation, regression 없이 모든 언어와 entity type 에 대해 검증한다.
- 미래 계획: LLM-based recognizer, 텍스트 외 매체 de-identification 이다.

## References

- Airbnb Engineering & Data Science, [De-identifying text at scale: How Airbnb protects personal data in AI training](https://airbnb.tech/infrastructure/de-identifying-text-at-scale-how-airbnb-protects-personal-data-in-ai-training) (2026-11-18)
- Presidio: [microsoft/presidio](https://github.com/microsoft/presidio)
---