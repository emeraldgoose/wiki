---
title: Iceberg REST 엔드포인트로 EMR Trino에서 S3 Tables 쿼리하기
description: EMR 7.11+ Trino와 관리형 S3 Tables Iceberg 스토리지의 REST 카탈로그 연동 — CloudFormation 배포, 카탈로그 설정, ACID 대화형 분석.
date: 2026-09-02
tags: [aws, data-engineering, lakehouse, apache-iceberg, trino, emr, s3-tables, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/query-amazon-s3-tables-from-amazon-emr-trino-using-the-iceberg-rest-endpoint/"
blog: aws
---

# Iceberg REST 엔드포인트로 EMR Trino에서 S3 Tables 쿼리하기

**저자**: Shubham Purwar, Anirudh Chawla, Nitin Kumar, Prashanthi Chinthala · **발행**: 2026-09-02 · **출처**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/query-amazon-s3-tables-from-amazon-emr-trino-using-the-iceberg-rest-endpoint/)

## 문제

S3 기반 Iceberg 데이터 레이크는 개방형 분석을 제공하지만, 직접 운영하면 파일 압축(compaction), 스냅샷 만료, 고아 파일 정리, 메타데이터 추적이라는 비차별적 운영 부담이 남는다. 동시에 대용량에 대한 빠른 대화형 SQL도 필요하다.

## 해법: 관리형 Iceberg 스토리지 + 분산 SQL

- **Amazon S3 Tables** — 네이티브 Iceberg 지원 S3 기능. 압축·스냅샷 만료·메타데이터 관리를 자동화하고, SigV4 인증 Iceberg REST 카탈로그 엔드포인트를 노출.
- **EMR 위 Trino**(v475+, EMR 7.11+) — 대규모 데이터셋에 대한 저지연 분산 ANSI-SQL 엔진.
- **Iceberg REST 카탈로그 표준** — 엔진과 스토리지 사이 표준 인터페이스라 여기서 만든 테이블을 Spark·Flink·Dremio에서도 읽을 수 있음(벤더 종속 없음).

데이터 흐름: Trino CLI/JDBC → Iceberg 커넥터가 REST 엔드포인트에서 메타데이터 조회 → 파티션 프루닝·푸시다운으로 S3의 Parquet/ORC를 직접 읽기. 쓰기는 REST 엔드포인트 경유 원자적 커밋.

## 구현

1. **CloudFormation 배포**(`emr-trino-s3tables.yaml`, 약 15분): VPC·프라이빗 서브넷, S3 Tables용 VPC 엔드포인트, Trino 탑재 EMR 클러스터, S3 Tables 버킷, 범용 S3 버킷, IAM 역할, 보안 그룹. Trino 카탈로그 파일과 부트스트랩 스크립트를 자동 생성.
2. **Trino 카탈로그**(`/etc/trino/conf/catalog/s3tables_irc.properties`): `connector.name=iceberg`, `catalog.type=rest`, S3 Tables REST URI·웨어하우스 ARN, `sigv4-enabled=true`, `signing-name=s3tables`, `view-endpoints-enabled=false`, `fs.native-s3.enabled=true` + `fs.hadoop.enabled=false`, 리전·IAM 역할. 버킷당 카탈로그 하나.
3. **EMR 서비스 역할 신뢰 관계**: EMR 서비스와 EC2 인스턴스 프로파일이 역할을 Assume하도록 설정.
4. **사용**: Session Manager로 프라이머리 노드 접속 → `trino-cli --catalog s3tables_irc` → `CREATE SCHEMA`·`CREATE TABLE ... WITH (format='PARQUET', ...)`·`INSERT INTO ... SELECT`·분석 쿼리. 타임 트래블(`FOR VERSION AS OF`), 스냅샷 조회(`"table$snapshots"`), 스키마 진화(`ADD/RENAME COLUMN`)가 그대로 동작.

## 의의

- **운영 단순화**: 압축 스케줄·스냅샷 수명 정책 관리 불필요.
- **독립적 확장**: 컴퓨트(EMR)와 스토리지(S3) 분리.
- **ACID + 거버넌스**: Iceberg 트랜잭션의 원자적 동시 읽기/쓰기, IAM + Lake Formation의 테이블·컬럼·로우 수준 접근 제어.
- **이식성**: 개방형 포맷 + REST 카탈로그로 엔진 선택지 유지.

## 세미나 시사점

- 관리형 카탈로그 + 개방형 포맷의 조합이 "유연성 대 운영 부담"의 오랜 딜레마를 해소한다.
- 정확해야 하는 카탈로그 속성(sigv4, signing-name, view-endpoints, native-S3 fs)이 연동의 핵심 함정 — 암기할 가치 있음.

## 관련 개념

- `concepts/data-engineering/apache-iceberg.md`, `concepts/data-engineering/lakehouse.md`, `concepts/data-engineering/stream-processing.md`
