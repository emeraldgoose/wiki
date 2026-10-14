---
title: "AWS Glue Data Quality 기반 Amazon EMR Data Quality로 EMR 워크로드에 데이터 품질 적용하기"
description: "Amazon EMR Data Quality는 AWS Glue의 DQDL 규칙 엔진을 EC2·Serverless·EKS의 EMR Spark 잡 안에서 네이티브 실행한다 — 애드혹 인라인 검증과 Glue Data Catalog 관리형 규칙셋 기반 Iceberg Write-Audit-Publish 승격 게이트 두 패턴을 지원한다."
tags: [source, aws-big-data, emr, data-quality, glue, apache-iceberg, spark, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/bring-data-quality-to-your-amazon-emr-workloads-with-amazon-emr-data-quality-built-on-aws-glue-data-quality"
blog: aws-big-data
published: "2026-10-12"
---

# AWS Glue Data Quality 기반 Amazon EMR Data Quality로 EMR 워크로드에 데이터 품질 적용하기

**Source**: AWS Big Data Blog, 2026-10-12

**핵심**: 나쁜 데이터는 EMR 파이프라인에 조용히 스며든다 — 있어야 할 값의 null, 잘못된 타임스탬프 형식, 끊긴 참조 키 — 그리고 틀린 대시보드·실패한 잡으로 나타난다. 기존 선택지는 직접 만든 Spark 검사(Deequ 등, 맞춤 가능하지만 자체 유지·중앙 규칙셋 없음)와 Glue 경유 관리형 품질(코드 적지만 별도 엔진·별도 단계)이었다. Amazon EMR Data Quality는 세 번째 길이다: AWS runtime for Apache Spark(emr-spark-8.1.0+)에 내장되어 EC2·Serverless·EKS 어디서든 Glue Data Quality 규칙을 같은 DQDL 문법으로 EMR Spark 잡 안에서 직접 실행한다.

## 배경

AWS Glue Data Quality의 중심은 Data Quality Definition Language(DQDL)다 — 완전성·유일성·범위·참조 무결성·분포를 선언적으로 표현하는 문법이며, 고정 임계값 대신 실행별 베이스라인을 학습하는 ML 기반 `DetectAnomalies` 규칙도 포함한다. 규칙은 잡 내 인라인 또는 Glue Data Catalog의 버전 관리·공유 가능한 관리형 규칙셋으로 살 수 있다. 평가기는 규칙별 통과/실패와 전체 점수를 돌려주고, 잡은 그에 따라 파이프라인 실패·격리·알림·병합 게이트를 수행한다. EMR Data Quality는 이 동일 엔진을 Spark 안에서 돌리므로 Glue용 규칙셋을 수정 없이 쓴다.

## 사전 준비

- `emr-spark-8.1.0` 이상 Amazon EMR 릴리스(부트스트랩 액션 불필요).
- 잡 실행 역할의 IAM 권한: `glue:AccessDataQualityRuntimeConfiguration`, `glue:CreateDataQualityRuleset`, `glue:GetDataQualityRuleset`, `glue:GetDataQualityResult`, `glue:PublishDataQuality`, `glue:GetDatabase`/`glue:GetTable`, S3 읽기/쓰기.

## 패턴 1: 애드혹 인라인 검증

탐색·초기 파이프라인용으로 규칙이 잡 안에만 산다 — 예컨대 벤더 CSV를 레이크 적재 전 검증(ID 비어 있지 않음, 매출 음수 아님, 허용 국가 코드). 잡은 DataFrame과 DQDL 문자열을 `EvaluateDataQuality.apply()`에 넘겨 결과 DataFrame을 받고, `Failed`가 하나라도 있으면 중단, 전부 통과하면 적재한다:

```python
from awsdataquality.transforms import EvaluateDataQuality

ruleset = """
Rules = [
 RowCount > 0,
 IsPrimaryKey "order_id",
 Completeness "customer_email" >= 0.95,
 ColumnValues "order_status" in ["PENDING","SHIPPED","DELIVERED","RETURNED"],
 ColumnValues "net_amount" between 0.0 and 25000.0
]
"""

dq_results = EvaluateDataQuality.apply(input_df, ruleset, publishing_opts,
                                       additional_opts, additional_sources)
failures = [r for r in dq_results.collect() if r["Outcome"] == "Failed"]
if failures:
    raise RuntimeError(f"Data quality checks failed:\n{failures}")
input_df.writeTo("company_sales.sales_data").append()
```

글의 평가 예시:

| 규칙 | 결과 | 평가 지표 |
|------|---------|-----------|
| `RowCount > 0` | 통과 | RowCount → 50000.0 |
| `IsPrimaryKey "order_id"` | 통과 | 유일성 1.0, 완전성 1.0 |
| `Completeness "customer_email" >= 0.95` | 통과 | 완전성 → 0.979 |
| `ColumnValues "order_status" in [...]` | 실패 | 준수율 0.996 |
| `ColumnValues "net_amount" between 0.0 and 25000.0` | 실패 | 최소값 −2228.87 |

## 패턴 2: 관리형 규칙셋의 Iceberg Write-Audit-Publish

프로덕션 ETL은 중앙 관리형 규칙셋으로 승격을 게이트하고 Iceberg WAP(Write-Audit-Publish) 패턴으로 원자적 승격을 보장한다:

1. **조회**: Glue Data Catalog에서 관리형 규칙셋을 가져온다(`aws glue create-data-quality-ruleset`으로 한 번 생성, 거버넌스 팀 소유·버전 관리).
2. **기록**: ETL 출력을 `main`이 아닌 Iceberg 스테이징 브랜치에 쓴다(브랜치명에 Spark application ID를 넣어 동시 실행 충돌 방지).
3. **평가**: 카탈로그 규칙셋으로 브랜치 데이터를 `EvaluateDataQuality` 평가.
4. **병합/폐기**: 품질 점수가 임계값을 넘을 때만 `main`에 병합, 아니면 폐기 후 알림.

규칙이 파이프라인 코드와 분리되므로 거버넌스 변경이 잡 수정 없이 전파되고, `main` 리더는 부분·실패 쓰기를 절대 보지 않는다.

## 소프트웨어 엔지니어를 위한 시사점

- **거짓 이분법을 버려라**: Deequ 검사를 직접 유지 중이라면 EMR Data Quality로 규칙셋·결과를 Glue Catalog에 중앙화하면서 실행은 기존 Spark 잡에 둔다.
- **애드혹으로 시작해 WAP로 졸업하라**: 진화 중인 파이프라인은 인라인 규칙, 거버넌스 팀이 기준을 소유하면 브랜치 게이트 병합으로 원자성을 확보한다.
- **드리프트 지표는 이상 탐지로**: 시간에 따라 변하는 건수·합계는 손으로 tuned 임계값 대신 `DetectAnomalies`가 맡는다.
- **IAM 표면을 챙겨라**: 서비스 간 결과 게시에는 6개 Glue 액션 + 카탈로그 + S3 권한이 필요 — 실행 역할은 계정이 아니라 파이프라인 단위로 scope를 좁힌다.

## 참고문헌

- 원문: [https://aws.amazon.com/blogs/big-data/bring-data-quality-to-your-amazon-emr-workloads-with-amazon-emr-data-quality-built-on-aws-glue-data-quality](https://aws.amazon.com/blogs/big-data/bring-data-quality-to-your-amazon-emr-workloads-with-amazon-emr-data-quality-built-on-aws-glue-data-quality)
- AWS Glue Data Quality 문서(DQDL 레퍼런스, 원문 내 링크)
- 관련: Apache Iceberg 브랜칭과 AWS Glue Data Quality의 Write-Audit-Publish 패턴(원문 내 링크)
