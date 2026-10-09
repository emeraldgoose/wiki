---
title: 고카디널리티 비롤업 지표의 정확한 COUNT(DISTINCT) 스케일링
description: 해시 상위 비트로 Roaring 비트맵을 청크 분할해 JVM 2GB 한계를 극복한 수십억 규모 정확 distinct count 전략
tags: [source, uber, data-engineering, count-distinct, spark, hive, bitmap, ko]
locale: ko
source_url: "https://www.uber.com/us/en/blog/scaling-exact-count/"
blog: uber
published_date: 2026-07-30
---

# 고카디널리티 비롤업 지표의 정확한 COUNT(DISTINCT) 스케일링

**저자**: Prakhar Agarwal, Avinash Varma Sagi, Abhay Singh Chauhan
**출처**: [Uber Blog](https://www.uber.com/us/en/blog/scaling-exact-count/)
**날짜**: 2026-07-30

## 문제

비롤업(non-rollup) 지표(MAU, 분기 리텐션, 교차 기간 인게이지먼트)는粗粒度 사전 집계로부터 도출할 수 없다 — 일별/월별 카운트의 어떤 조합으로도 분기 결과가 맞지 않는다. 분기 규모에서 36억 UUID에 대한 정확한 distinct count가 필요했고, RoaringBitmap은 약 1.79억 고유값에서 JVM 2GB 단일 배열 한계에 부딪혔다.

## 실패한 접근

- **Bitmap-32 + 전역 사전**: 단일 장애점, 순차 백필.
- **Bitmap-64 단일 버퍼**: 2GB JVM 배열 한계 — 튜닝으로 해결 불가한 구조적 한계.
- **HyperLogLog**: 1–5% 오차는 재무 보고에 허용 불가.

## 해결: 청크드 집계 버퍼 전략

xxHash64 상위 16비트로 비트맵 집계 버퍼를 분할한다 (`Map<Integer, Roaring64Bitmap>`):

```
chunkId = (int)(hash >>> 48)   // 65,536 청크
```

- 36억 규모에서 청크당 평균 ~55K 값; Chernoff bound로 OOM 확률 ≈ 0 확인.
- 16비트가 sweet spot: 8비트는 headroom 부족, 24비트는 맵 오버헤드/GC 압박.
- 청크별 독립 직렬화 → 피크 메모리는 최대 청크에 종속, 2GB 제약 완전 제거.
- 자가 기술적 부분 결과 (0xDEADBEEF 매직 넘버), 스트리밍 직렬화 (단일 `byte[]` 없음).
- UDAF가 수 KB 비트맵 대신 그룹 키당 8바이트 long 반환 → 셔플·HDFS/네트워크 I/O 감소.

## 배포 결과

- Mobility·Delivery·Platform 75개 지표 패밀리, 배포 후 OOM 제로.
- 2년 백필 시간 평균 −65% (최고 카디널리티는 최대 −94%).
- 일별 파이프라인 실행 −23%, 월별 데이터 준비 −43%.

## 향후 방향 (원문)

- 비롤업 지표의 풍부한 분석: 차원 슬라이싱, 코호트 비교, 트렌드 분석.
- uMetric의 셀프서비스 기본형으로 노출: 커스텀 UDAF·OOM 걱정 없이 고카디널리티 지표 정의.
- UUID 너머 64비트 해시 도메인(기기 ID, 세션 토큰, geohash)으로 일반화.

## 세미나 시사점

- 롤업/비롤업 구분이 집계 아키텍처 전체를 결정하므로 초기에 구분하라.
- 구조적 한계(JVM 배열 크기)는 구조적 해법(값 공간 분할)으로만 넘는다.
- 해시 상위 비트 분할은 청크를 서로소·균등·독립 직렬화 가능하게 만든다.
- 규모에서도 정확성을 포기할 필요가 없다.

## 관련 개념

- `concepts/data-engineering/apache-spark.md`
- `concepts/data-engineering/stream-processing.md`
