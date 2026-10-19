---
title: "Amazon Redshift의 Apache Iceberg 쓰기 지원 시작하기 – 3부"
description: "Redshift에서 메타데이터 전용 ALTER로 Iceberg 스키마·파티션을 진화시키고 Lake Formation으로 교차 엔진 공유합니다." (한국어 번역)
tags: [source, aws-big-data, redshift, iceberg, ko, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/getting-started-with-apache-iceberg-write-support-in-amazon-redshift-part-3"
blog: aws-big-data
published_date: 2026-09-28
---

# Amazon Redshift의 Apache Iceberg 쓰기 지원 시작하기 – 3부

## 개요

운영 테이블은 끊임없이 변합니다. 컬럼이 생기고 없어지고, 타입이 정밀도를 초과하고, 파티션 배치가 쿼리 패턴과 어긋납니다. 시리즈 3부에서는 Redshift의 ALTER 문으로 Iceberg 스키마와 파티션을 메타데이터 전용 연산으로 진화시킵니다. 데이터 재작성도 파이프라인 재구축도 없습니다. Lake Formation 리소스 링크로 S3 Tables를 다른 엔진과 하나의 권한 모델로 공유하는 방법도 다룹니다. 1부에서 Iceberg 테이블 생성·삽입을, 2부에서 DELETE·UPDATE·MERGE를 다뤘다고 가정합니다.

## ALTER TABLE 스키마 진화

모든 연산이 메타데이터만 갱신합니다. 기존 파일은 그대로 두고 모든 리더가 즉시 새 스키마를 봅니다.

- **컬럼 추가:** 새 컬럼은 고유 Iceberg 필드 ID와 함께 들어오고 기존 행은 NULL로 읽힙니다. `customer`에 `loyalty_tier`를 추가하고 주문 합계로 채우는 예로 시연합니다.
- **컬럼 삭제:** 현재 스키마에서 빠지고 기존 파일 데이터는 쿼리에서 보이지 않게 됩니다(해당 컬럼을 쓰는 파티션 필드를 먼저 삭제·교체).
- **컬럼 개명:** 타입·파티션 스펙에 영향 없이 이름만 바꿉니다.
- **타입 확장:** INT→BIGINT, DECIMAL(10,2)→DECIMAL(18,2) 같은 안전 승격은 재작성 없이 되므로 성장분을 염두에 두고 타입을 계획합니다.
- **테이블 속성 설정:** 압축 변경(예: `zstd`)은 이후 쓰기에만 적용되므로 대량 적재 전에 설정합니다.

## 파티션 진화

Iceberg는 기존 데이터를 재배치하지 않고 파티션 스펙을 바꿀 수 있습니다. 신규 쓰기는 새 스펙을 따르고 기존 파일은 기존 배치를 유지하며, 엔진이 양쪽을 투명하게 읽습니다.

- **필드 추가:** 일 파티셔닝 옆에 `bucket(16, customer_id)`를 더해 고카디널리티 분산을 얻는 식입니다.
- **원자적 교체:** `DAY(order_date)`를 `MONTH(order_date)`로 한 문장에 교체하면 파티션 없는 중간 상태가 생기지 않습니다.
- **다단계 스펙:** 필드를 하나씩 추가해(예: 월+버킷+일) 재작성 없이 다단계로 만들고, 하나씩 삭제해 단순화할 수도 있습니다. 삭제된 필드는 신규 데이터의 파티션 프루닝 혜택이 사라집니다. year·month·day·hour·bucket·truncate·identity 변환을 지원하며, 이미 파티션 필드에 쓰인 컬럼은 먼저 삭제·교체해야 재사용할 수 있습니다.

## 교차 엔진 접근과 운영 지침

기본 Glue 카탈로그에 S3 Tables 데이터베이스를 가리키는 Lake Formation 리소스 링크를 만들고 Redshift 역할에 DESCRIBE를 부여한 뒤, 외부 스키마를 만들면 깔끔한 2부(`스키마.테이블`) 표기로 조회할 수 있습니다. BI 도구·Data API·JDBC/ODBC에는 IAM 연합 인증이 필요한 3부 표기보다 이 방식이 낫습니다. 스키마 변경은 자동 전파되므로 `ALTER`+`UPDATE` 후 크로스 카탈로그 조인에서 즉시 보입니다. 안전 운영 수칙: ALTER는 비프로덕션에서 먼저 테스트, DROP+ADD보다 REPLACE 선호, SHOW TABLE로 스펙 확인, 잦은 변경 후 Glue 테이블 옵티마이저로 유지보수, Lake Formation 컬럼/행 보안, 명명된 역할에만 스키마 권한 부여(PUBLIC 금지), 테이블 삭제는 카탈로그 항목만 지우므로 S3 파일은 별도 정리.

## References

- 원문: [Getting started with Apache Iceberg write support in Amazon Redshift – Part 3](https://aws.amazon.com/blogs/big-data/getting-started-with-apache-iceberg-write-support-in-amazon-redshift-part-3)
