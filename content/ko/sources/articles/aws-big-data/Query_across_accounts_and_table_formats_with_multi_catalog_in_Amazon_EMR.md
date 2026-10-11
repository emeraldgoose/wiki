---
title: "Amazon EMR 멀티카탈로그로 계정·테이블 포맷 넘나들며 조회하기"
description: "EMR 8.1의 RedirectingSessionCatalog으로 Iceberg, Delta, Hudi, Hive 테이블을 단일 Spark 카탈로그에서 조회하고 쿼리 시점에 원격 카탈로그 자동 탐색."
published: "2026-10-06"
source_url: "https://aws.amazon.com/blogs/big-data/query-across-accounts-and-table-formats-with-multi-catalog-in-amazon-emr"
blog: aws-big-data
locale: ko
tags: [source, aws-big-data, emr, glue, ko]
---

# Amazon EMR 멀티카탈로그로 계정·테이블 포맷 넘나들며 조회하기

## 개요

Spark 기본 카탈로그는 한 번에 하나의 포맷 확장만 받고, V1 메타스토어는 단일 계정의 Glue 카탈로그에 묶인다. 그래서 혼합 포맷 레이크와 교차 계정 메시는 포맷별 카탈로그와 Lake Formation·RAM·리소스 링크 우회책이 필요했다. EMR 8.1의 옵트인 `RedirectingSessionCatalog`(RSC)은 두 제약을 함께 푼다. Spark 기본값으로 두면 Glue 메타데이터에서 테이블 포맷을 감지해 맞는 핸들러로 라우팅하고, 다른 계정의 Glue 카탈로그와 조인해도 데이터를 복사하지 않으며, 원격 카탈로그를 쿼리 시점에 자동 탐색한다.

## 세 가지 기능

멀티포맷 지원은 포맷별 카탈로그 설정을 속성 하나로 접어, 접두사 없는 `db.table` 참조와 포맷 간 조인을 한 문장으로 수행한다. 멀티카탈로그 접근은 원격 계정 Glue 카탈로그 ID를 가리키는 이름付き RSC 카탈로그를 선언해 로컬·원격 테이블을 직접 조인한다. 각 이름付き 인스턴스가 자체 메타스토어 위임을 가져 V1 싱글턴 한계가 사라진다. 자동 연결(auto-wiring)은 한 걸음 더 나아가 포맷 핸들러를 자동 등록하고, 옵트인 `GlueCatalogResolver`가 미선언 카탈로그 첫 참조 시 Glue GetCatalog API로 등록한다. 교차 계정 Glue 카탈로그, S3 Tables, Redshift Managed Storage를 지원한다.

## 실습과 설정 선택

aws-emr-utilities 저장소의 실습은 포맷별 테이블을 같은 카탈로그에 만들고 4방향 교차 포맷 조인을 실행한 뒤, 소비자·프로듀서 부트스트랩 스크립트로 교차 계정 조인까지 확장한다. 선택 기준은 단순하다. 혼합 포맷 레이크면 기본값을 RSC로(Delta·Hudi는 세션 확장 필요), 데이터가 다른 계정이면 이름付き 카탈로그, 여러 계정을 사전 설정 없이 쓰려면 리졸버 활성화다. 셋은 조합된다. 교차 계정 읽기의 Lake Formation 승인, Glue 리소스 정책, S3 버킷 정책, KMS 키 정책은 여전히 필요하다.

## 참고 자료

- [원문: Query across accounts and table formats with multi-catalog in Amazon EMR](https://aws.amazon.com/blogs/big-data/query-across-accounts-and-table-formats-with-multi-catalog-in-amazon-emr)
- [실습 코드: aws-emr-utilities](https://github.com/aws-samples/aws-emr-utilities)
