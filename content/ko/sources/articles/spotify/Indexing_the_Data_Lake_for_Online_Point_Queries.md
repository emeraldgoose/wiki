---
title: 온라인 포인트 쿼리를 위한 데이터 레이크 인덱싱
description: Spotify의 Random Access Parquet(RAP) — 레이크 Parquet 파일 위 외부 인덱스로 정밀 ranged read를 수행해 KV-store 복제 없이 저지연 포인트 쿼리를 제공하는 아키텍처
tags: [source, rss, spotify, data-lake, parquet, indexing, ko]
locale: ko
source_url: "https://engineering.atspotify.com/2026/7/indexing-the-data-lake-for-online-point-queries"
blog: spotify
published_date: 2026-07-27
---

# 온라인 포인트 쿼리를 위한 데이터 레이크 인덱싱

원저자: Will Edwards, Staff Data Engineer. 출처: Spotify Engineering, 2026-07-27. 영문 원문: `en/sources/articles/spotify/Indexing_the_Data_Lake_for_Online_Point_Queries.md`.

**요약**: 엑사바이트급 데이터 레이크는 키-값 저장소에 복제하기에 너무 크고, 분산 SQL 엔진은 조회 한 번에 수 초의 오버헤드를 더한다. Random Access Parquet(RAP)이 간극을 메운다. 외부 인덱스가 키를 파일·행 위치에 직접 매핑하고, 정밀 ranged read로 필요한 바이트만 가져온다. 같은 Parquet 파일로 분석과 인터랙티브 포인트 쿼리를 모두 처리하는 "한 번 저장, 한 번 지불" 구조다.

## 배경: 서빙 간극

두 워크로드가 같은 기본 연산(키 기반 고속 포인트 쿼리)을 필요로 하지만, 데이터는 KV 저장소에 상주시키기에 너무 크다.

- **온라인 서비스**: 사용자 청취 기록 조회·페이지네이션 같은 포털·개인화 기능을 인터랙티브 속도로 제공해야 한다.
- **AI 에이전트**: "지난여름에 뭘 들었지?" 같은 질문에 답하려면 사용자 데이터를 빨리 가져와 필터·집계·로컬 SQL로 LLM 프롬프트 컨텍스트를 만들어야 한다.

Spotify 규모: 온라인용 Bigtable에 페타바이트, GCS 데이터 레이크에 **엑사바이트**. 오브젝트 스토리지 자체는 빠르고 빨라지는 중(GCS 요청당 30~100ms, S3 Express One Zone·GCS Rapid Storage는 한 자릿수 ms)이다. 병목은 쿼리 엔진이다. Trino·BigQuery는 분석 처리량용으로 설계돼 단일 행 조회에도 수 초의 스케줄링·계획 오버헤드를 더한다.

## 순진한 레이크 조회가 실패하는 이유

"지난여름" 청취 기록 조회는 수십억 사용자의 수천 개 일일 파일, 약 90일 × 1,000파일 = **90,000개 Parquet 파일**에 걸친다. 표준 축소는 도움이 되지만 부족하다.

1. **키 파티셔닝**: 파일명으로 해당 사용자 포함 가능 여부를 판단해 후보를 90,000개에서 약 90개로 줄인다.
2. **Bloom filter**(메타데이터 저장소에 캐시): 파일을 열지 않고 제외해 약 90개를 사용자가 실제 활동한 12일분 정도로 좁힌다.
3. **그러나 12개의 큰 파일을 여전히 읽어야** 하고, 각 파일 안에서 한 사용자의 행을 찾으려면 row group을 열어 스캔하는 종속 읽기 체인이 필요해 지연이 쌓인다.

## RAP 방식: 스캔 대신 조회

외부 인덱스가 각 키를 데이터가 있는 모든 파일·행 번호에 직접 매핑한다. 키가 주어지면 인덱스를 조회하고, 캐시된 파일 메타데이터로 행 번호를 페이지 위치로 변환한 뒤, 정확히 필요한 페이지만 ranged read로 가져온다.

- 인덱스 조회는 **O(1)**, 페이지 매핑은 저지연 캐시 연산, 데이터 읽기는 소수의 정밀 ranged read이며 **병렬 발행** 가능하다.
- ML 파이프라인·노트북·실험 플랫폼·배치 분석이 이미 공유하는 **같은 Parquet 파일** 위에서 동작한다. 별도 서빙 시스템에 복사본을 유지할 필요가 없다.
- **사전 준비 불필요**: 기존 Parquet 파일에 그대로 적용된다. 인덱스 빌더가 푸터·페이지 위치를 읽고 키 컬럼을 스캔해 키→위치 매핑을 만든다.
- **증분식**: Apache Iceberg 테이블에 새 데이터가 들어오면 불변 Parquet 파일을 고치지 않고 append-only 인덱스 조각을 생성한다.

## 쓰기 시점 최적화

서빙을 염두에 둔 데이터셋에는 Parquet 레이아웃 최적화가 겹겹이 이득을 준다. 키 정렬, 관련 행 co-grouping, one-page-per-key 레이아웃, ZSTD 압축이 포인트 조회당 바이트를 줄인다. 보조 인덱스는 기본 키 너머로 패턴을 확장한다.

## 엔지니어 관점 시사점

- 서빙용으로 레이크 데이터를 DynamoDB/Bigtable에 복제하기 전에 외부 인덱스 + ranged read 설계를 검토하라. 이중 쓰기 정합성과 중복 저장 문제를 없앨 수 있다.
- 포인트 쿼리가 레이크에 닿는 순간 Parquet 파일 레이아웃(정렬 키, 페이지 크기, 압축)은 스캔뿐 아니라 서빙의 문제이기도 하다.

## 참고

- 원문: https://engineering.atspotify.com/2026/7/indexing-the-data-lake-for-online-point-queries
