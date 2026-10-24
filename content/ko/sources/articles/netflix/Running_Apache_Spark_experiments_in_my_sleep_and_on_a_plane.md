---
title: "잠자는 동안, 비행기에서 Apache Spark 실험 돌리기"
description: "Netflix member-sessionizer의 Spark 성능 실험을 자동화해 한 번에 여러 테스트를 돌리고 결과를 추적한 방법입니다."
tags: [source, netflix, data-engineering, spark, performance, ko]
locale: ko
source_url: "https://netflixtechblog.com/running-apache-spark-experiments-in-my-sleep-and-on-a-plane-588816b6b5f8"
blog: netflix
published_date: 2026-10-14
---

# 잠자는 동안, 비행기에서 Apache Spark 실험 돌리기

**원문**: [netflix](https://netflixtechblog.com/running-apache-spark-experiments-in-my-sleep-and-on-a-plane-588816b6b5f8) · **게시일**: 2026-10-14

## 개요

Netflix의 대표적인 대규모 데이터 파이프라인 중 하나인 member-sessionizer는 매시간 수십억 건의 클라이언트 이벤트를 모아 프로필별 시청 세션으로 정리합니다. 원래 2주 정도로 예상한 튜닝 작업이 두 달로 늘어났는데, 표준적인 접근이 벽에 부딪혔기 때문입니다. 실패가 프로덕션 규모에서만 발생해 테스트 한 번에 몇 시간이 걸렸고, 하루에 서너 번밖에 시도할 수 없었습니다.

전환점은 목표를 바꾼 것이었습니다. 한 번의 실행을 빠르게 만드는 대신, 여러 테스트를 동시에 실행하고 모든 결과를 추적하는 방법을 만들었습니다.

## 핵심 내용

- 필드 타입과 Option 박싱: 세션 ID가 8바이트 Long에서 UUID 문자열로 바뀌고, Option 래퍼가 JVM 객체 역직렬화를 유발해 오버헤드가 커졌습니다.
- 비대한 문자열 속성: referrer URL, 테스트 할당 같은 저가치 필드가 이벤트당 수백 바이트를 추가했습니다.
- 박싱 제거: non-nullable 필드에서 Option을 없애 피크 실행 메모리를 112%에서 58%로 줄이고 디스크 스필을 없앴습니다.
- 이벤트 백 슬림화: 사용하지 않는 속성을 제거하고 세션 불변 메타데이터를 세션 헤더로 올렸습니다.
- 행을 좁히면 Spark의 자동 브로드캐스트 임계값 아래로 내려가 쿼리 플래너가 달라질 수 있습니다.

## 참고 자료

- 원문: https://netflixtechblog.com/running-apache-spark-experiments-in-my-sleep-and-on-a-plane-588816b6b5f8
