---
title: "Amazon Redshift에서 Apache Iceberg 테이블의 동시 쓰기 충돌 해결"
description: "Amazon Redshift가 이제 작업, 파티션, 파일 세 가지 세분성에서 커밋을 리베이스해 Apache Iceberg 테이블로의 비중첩 동시 쓰기를 자동 해결—스트리밍 삽입 대 컴플라이언스 삭제 같은 독립적 쓰기의 재시도 루프 제거."
tags: [source, aws-big-data, apache-iceberg, amazon-redshift, concurrency-control, data-lake, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/resolving-concurrent-write-conflicts-for-apache-iceberg-tables-in-amazon-redshift"
blog: aws-big-data
published: "2026-10-13"
---

# Amazon Redshift에서 Apache Iceberg 테이블의 동시 쓰기 충돌 해결

**Source**: AWS Big Data Blog, 2026-10-13

**핵심**: Apache Iceberg는 테이블 버전 수준에서 낙관적 동시성 제어(OCC) 사용—동시 커밋 시 버전 체크 실패로 전체 쓰기 버려짐, 실제로는 완전히 분리된 데이터를 건드리는 경우에도. Amazon Redshift가 이제 세 가지 세분성 수준(작업 → 파티션 → 파일)에서 비충돌 쓰기를 자동 리베이스해, 이전에 재시도해야 했던 작업을 보존.

## 문제: 테이블 버전 수준의 둔탁한 OCC

Iceberg의 OCC는 현재 테이블 버전 대비 각 쓰기자가 커밋하도록 요구해 스냅샷 격리 보장. 다른 쓰기자가 먼저 커밋하면 조건 실패로 **전체 쓰기 버려짐**—두 쓰기가 실제 같은 데이터를 건드렸는지와 무관하게.

예시: 소매 `customer_orders` Iceberg 테이블. 스트리밍 파이프라인이 새 주문 지속 삽입(분당 수백 건). 야간 컴플라이언스 작업이 7년 이상 레코드 삭제(약 1시간 소요). 두 쓰기는 **절대 같은 데이터 건드리지 않음**—스트림은 최근 주문 추가, 컴플라이언스는 오래된 것 삭제. 하지만 기본 OCC에서 스트리밍 삽입이 컴플라이언스 작업 윈도우 중 커밋하면, 컴플라이언스 작업이 경주에서 패배, 1시간 작업 버려짐, 테라바이트 재스캔 필요.

전통적 우회책은 모두 수동적이고 비용 큼:
- 쓰기자 직렬화(동시성 포기)
- 여러 물리 테이블로 분할(데이터 모델 단편화)
- 애플리케이션 측 재시도 루프(실제 충돌 없는 작업 재실행 비용 흡수)

## Redshift 해결책: 리베이스 통한 자동 충돌 해결

커밋이 경주에서 패배하면 Redshift가 이제 묻는다: **앞서 커밋한 쓰기자들이 실제로 같은 파티션/파일/행을 변경했는가?** 아니면, 최신 테이블 버전 위로 변경사항 리베이스 후 커밋—재스캔, 재실행, 애플리케이션 재시도 없음.

소매 예시에서: 컴플라이언스 삭제가 스트리밍 삽입이 윈도우 내 커밋 시 이전엔 실패. 이제 Redshift는 삽입이 데이터 파일만 *추가*하고 삭제는 다른 파일만 *제거*함을 봄—증명 가능한 독립성. 삭제를 업데이트된 버전 위로 리베이스; 둘 다 성공.

두 가지 지배 원칙:
1. **충돌은 세분성의 문제** — 실패한 경주가 자동으로 충돌 아님. 작업 수준에서 먼저 체크(가장 저렴), 그 다음 파티션, 그 다음 파일. 더 세밀한 체크가 더 비싸지만 더 많은 경우 해결.
2. **동시성보다 정확성 우선** — 해결은 테이블 메타데이터만 사용, 데이터 재스캔 안 함. 독립성 증명 못 하면 해결 거부하고 쓰기 재시도(안전한 결과).

## 3단계 에스컬레이션

| 수준 | 체크 | 해결 대상 |
|-------|-------|----------|
| **작업** | 최소 한 쓰기만 추가(`INSERT`) | 모든 쓰기 대 삽입; 삽입 대 컴팩션 포함 모든 쓰기 |
| **파티션** | 둘 다 데이터 제거했으나 분리된 파티션 | 다른 날짜 배치 작업; 리전별 파이프라인 |
| **파일** | 같은 파티션, 다른 파일 | 같은 날짜 파티션에서 다른 행 삭제하는 두 작업 |

둘 다 **같은 파일** 수정 시 충돌 표면화, 문장 재실행(올바른 동작).

## 결과

**마이크로벤치마크** (1 비파티션 테이블, 삽입만, 1-16 동시 쓰기자, 60초):
- 기본 OCC: 16 쓰기자 처리량 = 단일 쓰기자의 **0.17배** (94% 실패율)
- 자동 해결: 단일 쓰기자의 **2배** 처리량, 모든 수준에서 **0 충돌**

**플릿 데이터**: 해결 전, 동시 쓰기 충돌이 Iceberg 쓰기 실패의 1위 원인(주당 약 5개 중 1개 실패). 작업 수준 체크 롤아웃 후(2026년 9월 초), 충돌 오류가 **거의 0**으로 감소하며 Iceberg 쓰기 볼륨이 **2배 이상 증가**.

## 관측 가능성

모든 커밋 시도가 `stl_iceberg_commit` 시스템 테이블에 기록: 결과, 시도 횟수, 리베이스된 동시 작업, 리베이스 시간.

## 소프트웨어 엔지니어를 위한 시사점

**Iceberg 테이블에서 동시 파이프라인 실행**하는 팀에게(스트리밍 + 배치, 다중 ETL 작업, CDC + 컴팩션): Redshift의 자동 해결이 쓰기자 수동 조정이나 재시도 로직 구축 필요성 제거. 엔진이 일반적인 경우(추가 대 모든 것, 분리된 파티션/파일) 투명하게 처리.

Redshift 패치 203+에서 사용 가능. `write.*.isolation-level = serializable`인 테이블은 엄격한 OCC 유지(해결 안 함).

## 참고문헌

- 원문: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/resolving-concurrent-write-conflicts-for-apache-iceberg-tables-in-amazon-redshift)
- Iceberg OCC 문서: [iceberg.apache.org/docs/1.6.0/reliability/#concurrent-write-operations](https://iceberg.apache.org/docs/1.6.0/reliability/#concurrent-write-operations)