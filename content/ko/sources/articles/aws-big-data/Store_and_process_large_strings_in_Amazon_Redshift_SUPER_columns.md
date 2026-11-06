---
title: "Amazon Redshift SUPER 컬럼에 대용량 문자열 저장 및 처리"
description: "Amazon Redshift SUPER 데이터 형식이 최대 16MB 문자열과 메모리 내 문자열 처리를 지원한다."
tags: [source, aws-big-data, data-engineering, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/store-and-process-large-strings-in-amazon-redshift-super-columns"
blog: aws-big-data
published_date: "2026-11-07"
---

# Amazon Redshift SUPER 컬럼에 대용량 문자열 저장 및 처리

**원문**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/store-and-process-large-strings-in-amazon-redshift-super-columns) · **게시일**: 2026-11-06

## 개요

Amazon Redshift는 SUPER 데이터 형식을 확장해 JSON, 배열 같은 반정형 데이터를 대용량 문자열로 끊거나 잘라 내지 않고 수집, 저장, 변환, 분석할 수 있게 했다. 대용량 문자열 지원을 활성화하면 SUPER는 개별 문자열 최대 16MB를 지원하며 65,535바이트 VARCHAR 제한을 넘는 문자열을 메모리에서 처리한다.

게시글은 세 가지 개선 사항을 설명한다. 확장 문자열 지원은 대용량 JSON 문서 보관을 가능하게 하며, 메모리 내 문자열 함수 처리는 부분 문자열 추출과 패턴 매칭을 잘라 내지 않고 실행한다. 대소문자 구분이 없는 데이터베이스 호환성은 레거시 데이터베이스에서의 마이그레이션을 단순화한다.

이 변화는 대용량 JSON, 웹 로그, IoT 텔레메트리, 애플리케이션 로그 처리에 흔히 발생하던 문제를 줄인다. 사용하려면 enable_large_strings_opt_in이 Yes로 설정된 parameter group 또는 workgroup과 호환되는 Redshift maintenance track이 필요하다.

## 핵심 내용

- SUPER 컬럼이 개별 문자열 최대 16MB를 지원한다.
- 대용량 문자열 처리가 메모리에서 이루어져 잘라 내기나 디스크 spill을 피한다.
- 대소문자 구분 없는 데이터베이스 호환성이 레거시 시스템 마이그레이션을 쉽게 한다.
- enable_large_strings_opt_in을 parameter group 또는 workgroup에서 활성화해야 한다.
- 적재, 조회, 문자열 연산 사용 사례를 SQL 예제로 설명한다.

## 상세

게시글에는 대용량 문자열 지원 활성화, orders 테이블 생성, Amazon S3에서 JSON 적재, nested field 조회, 이전 65,535바이트 제한을 넘는 문자열에 LISTAGG와 LEN을 실행하는 SQL 예제가 포함된다. VARCHAR 컬럼, 뷰, UDF, stored procedure의 동작도 설명한다.

## 참고 자료

- 원문: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/store-and-process-large-strings-in-amazon-redshift-super-columns)
