---
title: "dbt ETL 파이프라인을 Databricks로 옮기는 방법"
description: "어댑터 교체, Unity Catalog 네임스페이스, SQL 방언 수정, audit-helper 검증, Lakeflow Jobs 배포까지 dbt 전환 7단계 레시피."
tags: [source, databricks, dbt, data-engineering, lakehouse, ko]
locale: ko
source_url: "https://www.databricks.com/blog/how-repoint-dbt-etl-pipelines-databricks"
blog: databricks
published_date: 2026-10-06
---

# dbt ETL 파이프라인을 Databricks로 옮기는 방법

**출처**: [Databricks Blog](https://www.databricks.com/blog/how-repoint-dbt-etl-pipelines-databricks) · **발행**: 2026-10-06

## 개요

dbt 로직은 어댑터 프레임워크로 웨어하우스와 분리된 버전 관리 SQL에 살므로, 변환 계층 이전은 전체 이전 중 가장 위험이 낮은 첫걸음이다(Databricks에서 dbt를 쓰는 조직이 3,000곳 이상). 이 글은 팩트 모델 하나를 끝까지 옮긴다. 공동 개발된 dbt-databricks 어댑터를 설치하고 기존 타깃 옆에 Databricks 타깃을 추가하며, 변환 로직은 dbt 안에 그대로 둔다.

## 방언 수정과 검증

대표 컴파일 오류 세 가지가 패턴을 보여준다. `REGEXP_SUBSTR`→`regexp_extract`, 웨어하우스 고유 `DIV0`→`dbt_utils.safe_divide`, `OBJECT_CONSTRUCT`→`named_struct`로, 크로스 DB 매크로와 AI assisted 변환으로 수백 개 모델에 같은 수정을 확장한다. 실행 성공은 시작일 뿐이므로 `dbt-audit-helper`로 레거시 웨어하우스와 행 단위 대조를 100% 일치까지 반복한다(소수점 정밀도·콜레이션이 단골 범인).

## 배포, 전환, 확장

dbt는 외부 오케스트레이터 없이 Lakeflow Jobs의 일급 태스크로 수집·후속 새로고침과 한 파이프라인에서 돈다. 전환은 프로덕션 타깃 전환, CI 자격을 스테이징 카탈로그로 이전, `system.billing.usage`로 비용 확인, 롤백 기간 후 레거시 해제의 순서다. 전체로 확장할 땐 DAG 순서(소스→스테이징→중간→마트)로 소량씩, 증분 전략·스냅샷은 플랫폼에 맞게 재선택하고, 대량 SQL 변환엔 Lakebridge를 쓴다.

## References

- [How to Repoint dbt ETL Pipelines to Databricks](https://www.databricks.com/blog/how-repoint-dbt-etl-pipelines-databricks)
