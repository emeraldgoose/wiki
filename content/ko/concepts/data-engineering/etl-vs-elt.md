---
title: ETL과 ELT
description: "Extract-Transform-Load와 Extract-Load-Transform: 정의, 선택 기준, 실무 예시"
tags: [concept, data-engineering, etl, elt, data-warehouse, ko]
locale: ko
published: 2026-09-07
---

# ETL과 ELT

**요약:** ETL(Extract-Transform-Load)은 데이터를 웨어하우스에 적재하기 **전**에 변환하고, ELT(Extract-Load-Transform)는 원본 데이터를 **먼저** 적재한 뒤 목적지 플랫폼 안에서 변환한다. ETL은 엄격한 스키마, 레거시 웨어하우스, 규제 대상 파이프라인에 맞고, ELT는 저장소가 싸고 연산이 탄력적인 클라우드 웨어하우스와 레이크하우스에 맞는다. 선택에 따라 비용, 지연, 디버깅 방식, 로직 변경 주체가 달라진다.

## 정의

- **ETL:** 소스에서 추출하고, 전용 처리 엔진에서 변환한 뒤(정제, 조인, 집계, 스키마 맞춤), 완성된 테이블을 웨어하우스에 적재한다. 웨어하우스는 정제된 데이터만 받는다.
- **ELT:** 소스에서 추출해 목적지(클라우드 웨어하우스, 데이터 레이크, 레이크하우스)에 원본 그대로 적재한 뒤, SQL이나 SQL 기반 도구로 변환한다. 원본 계층이 보존된다.
- **진짜 차이**는 변환 연산이 *어디서* 일어나고 *원본 이력이 남는지*이다. ETL은 입구에서 원본 세부 정보를 버리고, ELT는 원본을 남기고 필요할 때 변환한다.
- **관련 변형:** EtLT(가벼운 스테이징 변환 후 웨어하우스 내 본 변환), 리버스 ETL(웨어하우스에서 운영용 SaaS 도구로 내보내기), 제로 ETL(클라우드 업체가 파는 연합 쿼리 방식)이 있다.

## 왜 중요한가

- **비용 구조.** ETL은 별도 변환 클러스터 비용을 낸다(상시 구동 Informatica, SSIS, Spark 잡). ELT는 그 비용을 웨어하우스 연산으로 옮기며 쿼리 단위로 늘어난다. 규모가 작으면 싸고 규모가 크면 요금이 튈 수 있다.
- **민첩성.** ELT에서는 컬럼 추가가 보관된 원본에 SQL 모델을 다시 돌리는 일이다. ETL에서는 파이프라인 수정, 재배포, 소스에서 이력 재추출이 필요하며 소스에 이력이 없을 수도 있다.
- **컴플라이언스와 개인정보.** ETL은 분석가가 조회하기 *전*에 주민번호나 카드번호 같은 민감 정보를 마스킹할 수 있어 규제가 센 조직의 필수 조건이 된다. ELT는 뷰, 정책, 원본 영역 삭제로 같은 효과를 내야 한다.
- **디버깅.** ELT의 원본 계층은 다시 돌릴 수 있는 감사 추적이다. 지표가 이상하면 손대지 않은 소스 스냅샷까지 거슬러 올라갈 수 있다. 원본을 버리는 ETL에서는 소스 시스템에서 버그를 재현해야 한다.

## 동작 방식

### ETL 파이프라인 (구체 예시)

Postgres와 협력사 CSV를 레거시 웨어하우스로 보내는 일일 매출 보고:

1. **추출:** Sqoop이나 파이썬 잡이 어제 이후 변경분(`WHERE updated_at > :watermark`)과 SFTP 경유 CSV를 가져온다.
2. **변환 (Spark 안에서):** 통화를 달러로 통일하고, `order_id` 기준 중복 제거를 하고, 표준 고객 차원과 조인하고, `amount`가 비어 있는 행은 격리 테이블로 보낸다.
3. **적재:** 완성된 `fact_orders`를 웨어하우스에 대량 삽입한다. 분석가는 정제 테이블만 본다.

```python
# ETL 변환 단계 단순 예시 (웨어하우스 도착 전에 실행)
clean = (
    orders.dropna(subset=["amount"])
          .drop_duplicates(subset=["order_id"])
          .merge(fx_rates, on="currency", how="left")
          .assign(amount_usd=lambda d: d["amount"] * d["rate"])
)
clean.to_sql("fact_orders", warehouse_engine, if_exists="append", index=False)
```

### ELT 파이프라인 (구체 예시)

클릭스트림과 Postgres를 Snowflake나 BigQuery에 dbt와 함께 적재:

1. **추출과 적재:** Fivetran이나 Airbyte가 원본 테이블(`raw.orders`, `raw.events`)을 주기적으로 그대로 복사한다. 양이 많으면 먼저 JSON이나 Parquet 파일로 오브젝트 스토리지에 둔다.
2. **변환 (웨어하우스 안 SQL):** 단계별 dbt 모델이 `stg_orders`(이름 정리, 타입 변환)를 만들고 이어서 `marts.fact_orders`(조인, 집계)를 만든다. 각 계층은 웨어하우스 안의 뷰나 테이블이다.

```sql
-- dbt식 ELT: 원본은 이미 웨어하우스에 있고 SQL로 변환
with stg as (
    select
        id::bigint            as order_id,
        lower(email)          as email,
        (payload:amount)::numeric as amount
    from raw.orders
)
select o.order_id, c.customer_key, o.amount * f.rate as amount_usd
from stg o
left join marts.dim_customer c on c.email = o.email
left join marts.fx_rates f on f.currency = o.currency;
```

### 나란히 비교

| 항목 | ETL | ELT |
|-----------|-----|-----|
| 변환 위치 | 적재 전 외부에서 | 목적지 안에서 |
| 원본 보관 | 보통 안 함 | 보통 함 |
| 어울리는 목적지 | 레거시 웨어하우스, 엄격한 스키마 | 클라우드 웨어하우스, 레이크, 레이크하우스 |
| 스키마 방식 | 쓰기 시점 스키마 | 읽기 시점 스키마 (유연함) |
| 지연 특성 | 배치 윈도우, 무거운 스케줄링 | 준실시간 가능 (잘게 나눈 적재와 SQL) |
| 변환 주체 | 데이터 엔지니어 (파이썬, Spark, 자바) | 엔지니어와 분석가 (SQL, dbt) |
| 주요 위험 | 이력 소실, 굳어진 변경 | 연산 요금 폭증, 어지러운 원본 방치 |

## 함정

- **ELT를 모델링 면제로 착각.** 원본 테이블을 쌓기만 하고 스테이징 모델 없이 두면 중복되고 서로 어긋나는 SQL이 쌓여 늪이 된다. ELT에도 모델링 규율이 필요하다([[concepts/data-engineering/data-modeling|데이터 모델링]] 참고).
- **깜짝 웨어하우스 요금.** 수십억 행을 매시간 전체 새로고침하는 dbt 모델은 ELT 요금 사고의 단골이다. 점증 모델, 클러스터링 키, 요금 알람을 쓴다.
- **원본 영역의 개인정보.** 전부 원본으로 적재하면 마스킹 전에 이메일과 카드 토큰이 저장소에 눕는다. 컬럼 마스킹 정책, 짧은 원본 보관, 민감 필드 사전 해시와 함께 쓴다.
- **ETL의 되돌릴 수 없음.** 적재 전에 일단위로 뭉개면 상세 파고들기가 영원히 사라진다. ETL 설계에도 원본 보관을 둔다.
- **제로 ETL 과장.** 연합 쿼리도 데이터를 옮기고 비용이 든다. 파이프라인이 안 보일 뿐이다. 로더를 지우기 전에 쿼리 요금을 잰다.

## 관련 개념

- [[concepts/data-engineering/data-modeling|데이터 모델링]] — 변환 단계의 스테이징과 마트 설계
- [[concepts/data-engineering/batch-vs-stream|배치와 스트림]] — 파이프라인 지연 선택
- [[concepts/data-engineering/orchestration-basics|오케스트레이션 기초]] — 스케줄과 의존성 관리
- [[concepts/data-engineering/cdc-change-data-capture|CDC (변경 데이터 캡처)]] — 두 방식 모두에 쓰는 저지연 추출
- [[concepts/data-engineering/data-quality|데이터 품질]] — 변환 결과에 대한 테스트와 계약

## 참고 자료

- Ralph Kimball and Margy Ross, *The Data Warehouse Toolkit* (3판, Wiley) — 변환 단계 뒤의 차원 모델링 정석.
- Martin Kleppmann, *Designing Data-Intensive Applications* (O'Reilly) — 배치와 스트림 기초. https://dataintensive.net 참고.
- AWS, "What is ETL?": https://aws.amazon.com/what-is/etl/
- Google Cloud, "What is ETL?": https://cloud.google.com/learn/what-is-etl
- Snowflake, "ETL vs ELT": https://www.snowflake.com/guides/etl-vs-elt/
- dbt 문서: https://docs.getdbt.com/
