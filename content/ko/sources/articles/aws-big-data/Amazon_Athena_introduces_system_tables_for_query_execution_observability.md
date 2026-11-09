---
title: "Amazon Athena, 쿼리 실행 관측성을 위한 시스템 테이블 도입"
description: "Athena의 새 시스템 테이블 query_executions가 쿼리별 사용 데이터를 S3 Tables의 Iceberg 테이블로 보관하므로 비용 배분·성능 분석·감사 질문을 평범한 SQL로 해결할 수 있다."
tags: [source, aws-big-data, data-engineering, observability, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/amazon-athena-introduces-system-tables-for-query-execution-observability"
blog: aws-big-data
published_date: 2026-11-10
---

# Amazon Athena, 쿼리 실행 관측성을 위한 시스템 테이블 도입

**원문**: [Amazon Athena introduces system tables for query execution observability](https://aws.amazon.com/blogs/big-data/amazon-athena-introduces-system-tables-for-query-execution-observability) · **게시일**: 2026-11-09

## 개요

Amazon Athena에서 SQL을 실행하는 팀은 개별 쿼리는 볼 수 있었지만 워크로드 전체를 파악하지는 못했다. 어떤 워크그룹이 가장 많은 데이터를 스캔하는지, 특정 쿼리가 지난주보다 느려졌는지, 지난 분기에 누가 어떤 테이블을 조회했는지 같은 질문에 답하려면 Athena API와 CloudWatch 지표, CloudTrail 로그를 직접 조인해야 했다. 즉 분석 파이프라인을 분석하기 위한 파이프라인을 따로 만들어야 했다. Athena는 이제 시스템 테이블을 제공하며, 첫 번째 테이블인 `query_executions`는 계정에서 완료된 모든 쿼리를 한 행씩 기록한다.

기능을 켜는 것은 콘솔에서 몇 단계면 된다. 활성화하면 현재와 앞으로 생성될 모든 워크그룹의 사용 데이터가 쿼리 완료 후 수 분 이내에 나타난다. Athena는 이 기록을 Amazon S3 Tables의 Apache Iceberg 테이블로 저장하고, 스키마 정의와 파티셔닝, 컴팩션, 스냅샷 유지 관리를 대신 처리한다. 형식이 개방형이므로 Athena뿐 아니라 DuckDB, Amazon Redshift 등 Iceberg 호환 엔진에서도 같은 데이터를 읽을 수 있다.

`query_executions`의 각 행에는 쿼리 식별 정보(실행 ID, 쿼리 문자열, 제출 시각), 컨텍스트(워크그룹, 카탈로그, 데이터베이스, 접근한 테이블), 성능 지표(전체 실행·계획·대기 시간), 자원 소비(스캔한 바이트, 용량 예약 쿼리의 DPU 수), 그리고 실행 상태와 상세 오류 정보가 담긴다. CloudWatch의 집계 지표로는 구분할 수 없는 지점이 바로 이 쿼리 단위 세부 정보이며, 사용자 문법 오류의 무해한 급증과 조치가 필요한 시스템 오류 급증을 나눠 볼 수 있다.

## 핵심 내용

- `query_executions`는 완료된 모든 쿼리에 대해 식별 정보, 워크그룹과 카탈로그 컨텍스트, 소요 시간, 스캔 바이트, DPU 수, 최종 상태와 오류 상세를 기록한다.
- 설정은 Administration → System tables → Configure 경로에서 한 번만 하면 되고, 선택적으로 AWS KMS 키로 암호화를 지정할 수 있으며(미지정 시 SSE-S3), Athena가 서비스 관리형 S3 테이블 버킷을 프로비저닝한다.
- 테이블이 AWS Glue 데이터 카탈로그에 등록되므로 AWS MCP 서버를 통해 Kiro나 Claude Code 같은 MCP 호환 에이전트를 연결할 수 있다. AWS가 공개한 Athena 시스템 테이블용 Agent Skill은 스키마와 예제 쿼리, 파티션 프루닝 규칙을 제공하며 읽기 전용 IAM 권한으로 제한해 쓸 수 있다.
- 글의 쿼리 모음은 사용 패턴(일별·주별 볼륨, 순사용자 수, 스캔 크기 구간별 분포), 워크그룹과 사용자별 비용 배분, 성능 회귀(주간 평균과 p95 실행 시간, 대기 시간 이상치), 스캔량 상위 쿼리를 다룬다.
- 감사와 운영 용도도 포함된다. 특정 주체의 쿼리 이력을 재생하고, 특정 데이터베이스와 테이블을 조회한 모든 쿼리를 찾고, 실패 쿼리를 시스템 오류와 사용자 오류로 나누며, Capacity Reservations가 소비한 DPU-시간 추이를 볼 수 있다.
- 기록은 불변이며 Athena 서비스만 테이블에 쓸 수 있어 어떤 IAM 주체도 개별 행을 수정하거나 삭제할 수 없다. 반면 보존 기간과 접근 정책, 암호화 키는 고객이 직접 관리한다.

## 상세

보존 기간에는 기본값이 없다. S3 Tables의 레코드 만료를 설정할 때까지 기록이 유지되며, 최소 1일이고 상한은 없다. 데이터는 보통 몇 분 안에 배치 단위로 도착하고, 서비스가 효율적인 스캔을 위해 테이블을 파티셔닝한다. 파티션 컬럼은 `DESCRIBE`로 확인할 수 있다. 기능을 켜는 순서는 왼쪽 내비게이션의 Administration 아래에서 System tables를 고르고, Configure에서 현재와 향후 리소스에 대해 시스템 테이블을 활성화한 뒤, 필요하면 KMS 키를 선택하고 저장하는 것이다. 이후에는 쿼리 편집기와 API, SDK, JDBC·ODBC 드라이버에서 다른 테이블과 똑같이 조회할 수 있다.

예제 쿼리는 목적별로 묶여 있다. 워크그룹별 지출은 `work_group_name`별로 `data_scanned_size`를 합산하고 TB당 단가(AWS Price List API로 최신 값을 프로그래밍 방식으로 받을 수 있다)를 곱해 구하며, 그룹 기준을 `principal_arn`으로 바꾸면 같은 보고서를 사용자 단위로 볼 수 있다. 성능 분석에서는 이번 주와 지난주의 쿼리 수, 평균 소요 시간, p95 지연을 워크그룹별로 비교하고 평균 대기 시간이 기준을 넘는 워크그룹을 표시한다. 비용을 가장 많이 유발하는 쿼리는 스캔 바이트 기준으로 정렬해 찾으며, 이는 파티셔닝과 조건자 푸시다운, 포맷 변경의 후보가 된다. 특정 테이블에 대한 추적은 `tables_accessed` 배열을 펼쳐 조인하고 데이터베이스와 테이블 이름으로 필터링한다.

운영 모니터링은 `error_category_enum` 컬럼으로 엔진 측 실패와 사용자 문법 오류를 구분하고, 실패를 오류 메시지별로 묶어 살핀다. 예를 들어 리소스를 소진한 쿼리는 파티셔닝 개선이나 쿼리 재작성, 또는 용량 증설의 후보가 된다. `dpu_count` 컬럼은 용량 예약에서 실행된 쿼리에만 채워지므로 DPU 수와 실행 시간을 곱한 값을 주 단위로 합산하면 예약의 DPU-시간을 얻어 규모가 적절한지 판단할 수 있다. 마지막으로 테이블이 고객 계정 안의 평범한 Iceberg 데이터이므로 Amazon Quick Sight나 다른 BI 도구를 바로 연결할 수 있어, 이전에는 이런 보고서를 위해 필요했던 사용자 정의 파이프라인이 사라진다.

## 참고 자료

- 원문: [Amazon Athena introduces system tables for query execution observability](https://aws.amazon.com/blogs/big-data/amazon-athena-introduces-system-tables-for-query-execution-observability)
