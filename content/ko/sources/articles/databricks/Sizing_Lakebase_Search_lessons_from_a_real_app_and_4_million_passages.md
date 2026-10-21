---
title: "Lakebase Search 크기 산정: 실제 앱과 400만 패시지에서 얻은 교훈"
description: "Lakebase Search가 벡터와 BM25 키워드 검색을 애플리케이션 데이터베이스 내 Postgres 확장으로 실행. Slide Hub 앱(700개 프레젠테이션) 벤치마크에서 로컬 파일 캐시를 벡터 인덱스 크기에 맞춰 95-98% 페이지 메모리 상주, 웜 벡터 지연시간을 한 자리 밀리초로 단축; 후보 풀 1000→200 축소로 top-10 결과 90.5% 보존하며 페이지 읽기 1/3로 감소."
tags: [source, databricks, lakebase-search, postgres, vector-search, bm25, hybrid-search, ko, ko]
locale: ko
source_url: "https://www.databricks.com/blog/sizing-lakebase-search-lessons-real-app-and-4-million-passages"
blog: databricks
published: "2026-10-15"
---

# Lakebase Search 크기 산정: 실제 앱과 400만 패시지에서 얻은 교훈

**Source**: Tiefenbacher, Databricks Blog, 2026-10-15

**핵심**: Lakebase Search가 벡터와 BM25 키워드 검색을 애플리케이션 데이터베이스 내 Postgres 확장으로 실행—별도 검색 시스템 없음, 두 번째 트랜잭션 경로 없음. Slide Hub 앱(내부 도구, 700개 프레젠테이션) 벤치마크가 실용적 크기 산정 규칙 공개: 벡터 인덱스 캐싱, 후보 풀 축소, 콜드 스타트 방지를 위한 최소 상시 가동 플로어 실행.

## 앱과 검색을 위한 단일 데이터베이스

Lakebase Search(2026년 9월 GA)는 Postgres 확장 세트:
- `lakebase_vector` + `lakebase_ann` (IVF + RaBitQ 양자화)으로 ANN 벡터 검색
- `lakebase_text` + `lakebase_bm25`로 BM25 키워드 검색
- `lakebase_tokenizer` (선택) 커스텀 토크나이징용

앱이 데이터를 별도 검색 시스템에 복사하지 않음. 유지할 두 번째 트랜잭션 경로 없음.

## Slide Hub: 실제 앱 기준선

Slide Hub는 내부 Databricks 앱. 필드 엔지니어들이 ~700개 프레젠테이션(이벤트 발표, 제품 데크, 아키텍처 데크)을 의미와 키워드로 검색. MCP 서버가 AI 에이전트에 동일한 검색 제공. 모든 데이터—슬라이드, 투표, 검색 텔레메트리, 변경 이력—가 Lakebase Postgres에 상주.

실제 앱에 실제 사용자라, 그 숫자들이 실제 워크로드 동작 반영.

## 주요 크기 산정 발견사항

### 1. 로컬 파일 캐시 ≈ 벡터 인덱스 크기
- 로컬 파일 캐시를 벡터 인덱스 크기와 대략 맞춰 **페이지 95-98% 메모리 상주**
- 웜 벡터 지연시간이 **한 자리 밀리초**로 하락
- 캐시가 인덱스보다 작으면 → 오브젝트 스토리지에서 페이지 읽기 → 지연시간 스파이크

### 2. 후보 풀: 1000 → 200
- ANN 후보 풀을 1,000에서 200으로 축소해 **top-10 결과의 90.5% 보존**
- 페이지 읽기 **1/3로 감소**
- 트레이드오프: 약간의 재현율 손실로 대량 지연시간/IO 이득

### 3. 스케일 테스트: 100만 → 400만 패시지
- 공개 코퍼스를 100만에서 400만 행으로 스케일링해 벤치마크
- 적절한 캐시 크기 시 지연시간이 아선형으로 스케일
- BM25는 잘 스케일; 벡터 검색이 적절한 캐시 없이는 병목

### 4. 비용: 109k 요청에 $0.02
- 14분 부하 테스트로 109k 요청 서비스에 Lakebase Postgres 컴퓨트 **$0.02** 사용
- **권장 프로덕션 기준선**: 콜드 스타트 방지를 위한 상시 가동 0.5 CU 플로어($31-40/월)
- Lakebase Postgres는 실행 중에만 컴퓨트 청구

## 실용적 권장사항

| 파라미터 | 권장사항 |
|-----------|----------------|
| 로컬 파일 캐시 | 벡터 인덱스 크기와 맞춤 (95-98% 적중률) |
| ANN 후보 풀 | 200 (기본 1000에서) 90.5% 재현율에 1/3 IO로 |
| 상시 가동 플로어 | 0.5 CU ($31-40/월) 콜드 스타트 제거용 |
| 하이브리드 검색 | BM25 + 벡터 함께 사용; BM25가 정확 매칭, 벡터가 의미적 처리 |

## 소프트웨어 엔지니어를 위한 시사점

**Databricks에서 애플리케이션에 검색 구축**하는 팀에게: Lakebase Search가 별도 검색 클러스터(Elasticsearch, OpenSearch, Pinecone 등) 제거. 다음 획득:
- **단일 데이터베이스**로 앱 데이터 + 검색 인덱스
- **트랜잭션 일관성** 앱 쓰기와 검색 업데이트 간
- **SQL-네이티브** 검색—새 쿼리 언어 불필요
- **예측 가능한 크기 산정** 실제 앱 벤치마크로부터

## 참고문헌

- 원문: [https://www.databricks.com/blog/sizing-lakebase-search-lessons-real-app-and-4-million-passages](https://www.databricks.com/blog/sizing-lakebase-search-lessons-real-app-and-4-million-passages)
- Lakebase Search GA 발표: [Databricks Blog](https://www.databricks.com/blog/lakebase-search-general-availability)