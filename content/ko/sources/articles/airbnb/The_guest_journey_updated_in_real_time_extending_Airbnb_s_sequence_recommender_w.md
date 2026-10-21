---
title: "실시간으로 갱신되는 게스트 여정: Chronon으로 확장한 Airbnb 시퀀스 추천"
description: "Chronon의 Push Mode와 실시간 모델 변환으로 게스트 임베딩 지연을 2일에서 수십 초로 줄인 Airbnb 사례."
tags: [source, airbnb, ml, recommendation, chronon, streaming, ko, ko]
locale: ko
source_url: "https://airbnb.tech/ai-ml/the-guest-journey-updated-in-real-time-extending-airbnbs-sequence-recommender-with-chronon"
blog: airbnb
published: "2026-09-23"
---

# 실시간으로 갱신되는 게스트 여정: Chronon으로 확장한 Airbnb 시퀀스 추천

## 개요

Airbnb의 Transformer 기반 시퀀스 인코더는 게스트의 예약·리뷰·브라우징 이력으로 검색 랭킹을 개인화하지만, 야간 배치로 돌아 임베딩이 실제 행동보다 최대 2일 가까이 뒤처졌다. 팀은 오픈소스 피처 플랫폼 Chronon에 두 가지 범용 기능을 추가해 격차를 메웠다. 스트리밍 피처 갱신 시 이벤트로 알리는 Push Mode와, 스트리밍 파이프라인 안에서 배포된 모델을 직접 실행하는 실시간 모델 변환(NRT Model Transform)이다.

## 배치가 부족했던 이유

지연은 두 원인에서 왔다. 하루 한 번 스케줄과 잡 자체의 처리 지연이다. 실행 빈도를 높이는 것만으로는 부족했고, 활동 발생 시점에 반응하는 파이프라인이 필요했다. 인코더도 하루치 스냅샷용으로 설계되어 건별 호출 구조가 아니었고, 페이지뷰·검색 같은 게스트 신호는 독립 스트림으로 도착하므로 장기 프로필 상태와 병합해 배치 출력과 비교 가능한 임베딩을 유지해야 했다.

## Push Mode와 실시간 모델 변환

Push Mode는 Chronon 스트리밍 잡이 새 피처 값을 커밋하자마자 가벼운 알림을 발행해, 폴링 단계를 이벤트 주도 트리거로 바꾼다. 실시간 모델 변환은 애플리케이션 코드에 모델을 박거나 오프라인 배치를 기다리는 대신, Chronon이 이미 배포된 모델(여기서는 기존 Transformer 인코더)을 스트리밍 흐름 안에서 호출해 결과를 즉시 서빙 가능한 피처 값으로 기록한다. 둘을 합치면 게스트의 페이지뷰·검색이 기존 시퀀스 상태와 병합되고 인코더가 실행되어, 배치 잡과 랭킹 모델이 이미 쓰던 저지연 저장소에 새 임베딩이 기록된다. 두 기능 모두 특정 유스케이스가 아닌 플랫폼에 속하고 오픈소스로 공개되어 다른 팀의 실시간 모델링에도 재사용된다.

## 결과

임베딩 신선도가 약 2일에서 보통 10~30초 수준으로 개선되어, 몇 분 전 본 리스팅이 바로 다음 검색에 반영된다. 오프라인 랭킹 품질은 배치 대비 NDCG +1.67% 향상으로, 10년 이상 다듬어진 시스템에서는 큰 폭이다. 온라인 A/B 테스트에서도 미취소 예약이 약 +0.33% 증가해, 신선도 자체가 랭킹 품질의 의미 있는 원천임이 확인됐다.

## References

- 원문: https://airbnb.tech/ai-ml/the-guest-journey-updated-in-real-time-extending-airbnbs-sequence-recommender-with-chronon
- Chronon: https://github.com/airbnb/chronon
