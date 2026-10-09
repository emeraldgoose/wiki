---
title: Apache Iceberg
description: ACID 트랜잭션, 타임 트래블, 스키마 진화를 지원하는 대용량 분석 데이터셋용 오픈 테이블 포맷
tags: [concept, data-engineering, lakehouse, iceberg, table-format, ko]
locale: ko
---

# Apache Iceberg

**Apache Iceberg**는 대용량 분석 데이터셋을 위한 오픈 테이블 포맷입니다. 데이터 레이크에 데이터베이스 수준의 신뢰성과 단순성을 제공하면서 다중 컴퓨트 엔진(Spark, Trino, Flink, Athena 등)을 지원합니다.

## 핵심 기능

### ACID 트랜잭션
- 테이블 연산에 대한 완전한 ACID 준수
- 리더용 스냅샷 격리, 라이터용 직렬화 가능 격리
- 부분 쓰기나 손상된 상태 없음

### 타임 트래블 & 롤백
- 타임스탬프나 스냅샷 ID로 과거 스냅샷 쿼리 가능
- 이전 상태로 즉시 롤백 (메타데이터 연산만으로)
- 재현 가능한 실험과 컴플라이언스 감사 지원

### 스키마 진화
- **컬럼 추가/제거/이름 변경** 시 데이터 재작성 불필요
- **타입 승격** (예: int → long, float → double) 안전하게 수행
- **컬럼 재정렬** 시 데이터 이동 없음
- **파티션 진화** — 데이터 재작성 없이 파티션 스펙 변경

### 파티션 레이아웃 진화
- 파티션 전략 변경(예: 일별 → 시간별) 시 전체 테이블 재작성 불필요
- 숨겨진 파티셔닝 — 파티션 값이 데이터 컬럼에서 자동 유도
- 매니페스트 파일을 통한 쿼리 타임 파티션 프루닝

### 숨겨진 파티셔닝
- 파티션 변환: `year(ts)`, `month(ts)`, `day(ts)`, `hour(ts)`, `bucket(N, col)`, `truncate(L, col)`
- 데이터에 명시적 파티션 컬럼 불필요
- 엔진이 쓰기 시 파티션 값 계산

## 아키텍처

### 메타데이터 계층
```
카탈로그 (REST/Hive/Glue/Nessie)
    ↓
메타데이터 파일 (테이블 메타데이터, 스키마, 파티션 스펙, 스냅샷)
    ↓
매니페스트 리스트 (스냅샷 → 매니페스트 파일 목록 + 파티션 통계)
    ↓
매니페스트 파일 (데이터 파일 목록 + 파티션 튜플 + 통계: min/max/count/nulls)
    ↓
데이터 파일 (Parquet/Avro/ORC)
```

### 주요 컴포넌트
- **카탈로그**: 현재 메타데이터 포인터 추적 (REST 카탈로그, Hive Metastore, AWS Glue, Project Nessie)
- **메타데이터 파일**: 불변; 각 커밋마다 새 버전 생성
- **매니페스트 리스트**: 스냅샷별 매니페스트 파일 인덱스 + 파티션 경계
- **매니페스트 파일**: 파티션 값과 컬럼 레벨 통계로 데이터 파일 추적
- **데이터 파일**: Parquet(기본), Avro, ORC 형태의 실제 데이터

## 컴퓨트 엔진 지원

| 엔진 | 읽기 | 쓰기 | 비고 |
|--------|------|-------|-------|
| Apache Spark | ✅ | ✅ | `spark.sql.catalog`로 네이티브 지원 |
| Apache Flink | ✅ | ✅ | 스트리밍 읽기/쓰기; 다이나믹 싱크 |
| Trino/Presto | ✅ | ✅ | Iceberg 커넥터; 프레디케이트 푸시다운 |
| Amazon Athena | ✅ | ✅ | 서버리스 SQL; CTAS/INSERT |
| AWS Glue | ✅ | ✅ | ETL 작업; 구체화 뷰 (5.1+) |
| Dremio | ✅ | ✅ | 리플렉션 가속 |
| Snowflake | ✅ | ✅ | Iceberg 테이블 (외부) |

## Iceberg REST 카탈로그

카탈로그 연산을 위한 표준화된 HTTP API (v1 스펙):
- **테이블**: CRUD, 메타데이터, 스냅샷
- **네임스페이스**: 계층적 구성
- **뷰**: 논리적 뷰 지원
- **인증**: OAuth2, AWS SigV4, 커스텀

엔진에 구애받지 않는 테이블 관리 가능; S3 Tables, Polaris, Unity Catalog, Gravitino에서 채택.

## Iceberg로 스트리밍

### Flink 다이나믹 싱크 (Iceberg 1.5+)
- **스키마 진화**: 새 컬럼 자동 처리 (과거 파일에 null)
- **새 이벤트 타입**: 이벤트 타입별 자동 테이블 생성
- **정확히 한 번**: 체크포인트된 쓰기 + 트랜잭션 조정
- **포맷 버전**: v2 (광범위한 호환성) 또는 v3 (로우 레벨 삭제, 더 나은 압축)

### CDC 통합
- Debezium → Kafka → Flink → Iceberg (동등 삭제 + 삽입으로 업서트)
- 네이티브 MoR(merge-on-read)로 고처리량 CDC 지원

## 성능 최적화

### 컴팩션
- **자동** (S3 Tables, Athena) 또는 **수동** (Spark `rewriteDataFiles`)
- 작은 파일 병합; 파티션 정렬을 위한 재작성
- 스냅샷 만료 + 고아 파일 정리

### 매니페스트 병합
- 작은 매니페스트 파일 결합으로 계획 속도 향상
- 자동 트리거 또는 `rewriteManifests`로 수동 실행

### 스캔 계획
- 매니페스트 리스트 파티션 경계로 파티션 프루닝
- 컬럼 통계(min/max/nulls)로 프레디케이트 푸시다운
- 데이터 파일 열지 않고 파일 레벨 프루닝

## 운영 패턴

### 브랜칭 & 태깅 (Nessie/카탈로그)
- **브랜치**: 격리된 개발; 카탈로그를 통해 병합
- **태그**: 릴리스/감사용 불변 스냅샷
- **멀티 테이블 트랜잭션**: Nessie로 크로스 테이블 ACID

### 멀티 엔진 접근
- 데이터 단일 복사본; Spark로 ETL, Trino로 대화형, Flink로 스트리밍
- 데이터 중복 없음; 컴퓨트 독립적 확장

### 거버넌스
- **행/컬럼 레벨 보안**: 카탈로그 통해 (Lake Formation, Polaris, Unity)
- **감사 로깅**: 카탈로그가 모든 메타데이터 변경 추적
- **데이터 계약**: 쓰기 시 스키마 검증

## 주요 참고 자료
- [Iceberg Spec](https://iceberg.apache.org/spec/)
- [Iceberg REST Catalog Spec](https://github.com/apache/iceberg/tree/master/rest-catalog)
- [Flink Iceberg Integration](https://nightlies.apache.org/flink/flink-docs-master/docs/connectors/table/iceberg/)
- [AWS S3 Tables](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables.html)
- [Project Nessie](https://projectnessie.org/) — Iceberg를 위한 Git 스타일 버저닝

## 관련 개념
- `concepts/data-engineering/stream-processing.md`
- `concepts/data-engineering/delta-lake.md`
- `concepts/data-engineering/apache-spark.md`
- `concepts/infrastructure/kubernetes.md` (Flink on K8s)