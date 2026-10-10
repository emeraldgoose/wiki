---
title: "Unity Catalog의 Workday Data Connect 페더레이션"
description: "네이티브 Data Connect 페더레이션 커넥터(Beta)로 Unity Catalog에서 Workday HR·재무 데이터를 zero-copy로 조회"
tags: [source, databricks, data-engineering, federation, iceberg, unity-catalog, ko]
locale: ko
source_url: "https://www.databricks.com/blog/announcing-workday-data-connect-federation-unity-catalog"
blog: databricks
published: "2026-10-08"
---

# Unity Catalog의 Workday Data Connect 페더레이션

**출처**: [Databricks 블로그](https://www.databricks.com/blog/announcing-workday-data-connect-federation-unity-catalog)
**날짜**: 2026-10-08

## 출시 내용

Workday Data Connect를 Unity Catalog에 페더레이션하는 공개 Beta 커넥터다. Workday Data Cloud로 공유된 HR·재무 테이블을 수집 파이프라인도 중복 복사도 없이 Databricks에서 질의한다. Databricks는 Workday Rising 2025에서 발표된 Data Cloud 론치 파트너다. 범위 구분에 유의한다. 이 커넥터는 수집·복사를 하지 않으며, 이력 보관(SCD2 등)이 필요하면 Lakeflow Connect 수집 커넥터를 쓴다.

## 동작 방식

두 관리자의 짧은 협업으로 끝난다.

- Workday 쪽: Data Connect를 켜고 Iceberg REST 카탈로그로 테이블을 공유한다. API 클라이언트(JWT Bearer Grant)를 등록하고 Integration System User에 읽기 권한을 준다.
- Databricks 쪽: OAuth 연결 하나와 외부(foreign) 카탈로그를 만든다. Workday Iceberg REST 카탈로그와의 토큰 교환은 Databricks가 대신하므로 토큰 엔드포인트를 직접 다룰 일이 없다. Unity Catalog 워크스페이스, Runtime 19 이상, Previews 페이지에서 Beta를 켤 workspace admin이 필요하다.

쿼리는 Databricks 컴퓨트에서 Workday 관리 오브젝트 스토리지의 데이터를 직접 읽고, Unity Catalog가 끝까지 거버넌스한다. 카탈로그·스키마·테이블 권한, 리니지, 감사가 네이티브 자산과 동일하다. 접근은 읽기 전용이라 Workday가 HR·재무의 시스템 오브 레코드로 남는다.

## 카탈로그 vs 쿼리 페더레이션

쿼리 페더레이션은 SQL을 외부 시스템에 보내 거기서 실행한다. 이 커넥터가 쓰는 카탈로그 페더레이션은 테이블 메타데이터만 Workday Iceberg REST 카탈로그에서 가져오고, 데이터 읽기·쿼리 실행은 Databricks 컴퓨트가 직접 한다. 어느 쪽이든 Unity Catalog가 접근을 통제한다.

## Workday 데이터를 가져오는 세 가지 길

- **Lakeflow Connect**: Delta로의 관리형 증분 수집. durable 복사본·정기 파이프라인용.
- **Data Connect 페더레이션 (Beta)**: 공유 Iceberg 테이블 위의 zero-copy 실시간 분석. 나머지 기업 데이터와 조인 가능.
- **JDBC Live Data Query**: 저장 없이 그때그때 보는 실시간 조회.

하나의 파이프라인에 억지로 끼워 맞추지 말고 용도별로 고른다.

## 열리는 활용

제자리에서 인사·재무 데이터가 기업 데이터와 합쳐진다. 인력·재무 동향에 대한 Genie 자연어 탐색, 시장·매출 데이터와 합친 실시간 계획, 운영 지표와 섞은 인력 분석, 오래된 익스포트가 아닌 거버넌스된 최신 데이터를 먹는 AI 에이전트다. 예시 질문: 분기 인력 증가가 가장 빠른 코스트센터, 지역·직군별 이직률, 인력 변동 vs 수주·판관비.

## 세미나 요약

- 페더레이션 형태는 접근 패턴을 따른다. durable 복사·라이브 뷰·조회는 같은 도구의 등급이 아니라 별개의 도구다.
- zero-copy는 읽기 경로의 거버넌스가 전제다. 권한·리니지·감사가 네이티브 테이블과 동일하게 동작해야 한다.
- 원천을 시스템 오브 레코드로 남기는 읽기 전용이 stale 데이터 버그 한 부류를 통째로 없앤다.
- 토큰 교환을 플랫폼이 대신해야 "두 관리자 10분 설정"이 실제로 성립한다.

## 관련 개념

- [Apache Iceberg](concepts/data-engineering/apache-iceberg.md) (상호 운용 표면으로서의 공유 Iceberg 테이블)
