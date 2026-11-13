---
title: "Intuit가 Apache Hive Metastore에서 AWS Glue Data Catalog로 전환한 방법"
description: "Intuit가 자체 관리하던 Apache Hive Metastore를 완전관리형 AWS Glue Data Catalog로 전환한 사례. 1회성 Glue ETL 마이그레이션, 이벤트 기반 양방향 동기화(한쪽은 Debezium CDC→Kafka 토픽, 다른 쪽은 EventBridge→MSK·Flink 정렬), DynamoDB 진원장(source of truth) 중재 테이블, 시간별 Iceberg 기반 패리티 도구, ad hoc 수리 마이그레이션으로 구성된다."
tags: [source, aws-big-data, data-catalog, migration, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/how-intuit-migrated-from-apache-hive-metastore-to-aws-glue-data-catalog"
blog: aws-big-data
published_date: 2026-11-14
---

# Intuit가 Apache Hive Metastore에서 AWS Glue Data Catalog로 전환한 방법

**원문**: [AWS 빅데이터 블로그](https://aws.amazon.com/blogs/big-data/how-intuit-migrated-from-apache-hive-metastore-to-aws-glue-data-catalog) · **게시일**: 2026-11-11

## 개요

많은 기업이 빅데이터 여정을 Apache Hive Metastore(HMS)에서 시작했다. HMS는 테이블 정의와 메타데이터를 안정적으로 보관하는 카탈로그 서비스였다. 분석이 확장되고 클라우드 채택이 깊어지면서 요구는 세밀한 접근 통제와 완전관리형 서버리스 인프라로 이동하고, 이 때문에 Intuit를 포함한 조직들이 HMS에서 AWS Glue Data Catalog(GDC)로 메타스토어를 옮겨 AWS 분석·AI 서비스와의 네이티브 통합과 중앙화된 관리·거버넌스를 얻으려 한다. AWS와 Intuit 저자 아홉 명이 쓴 이 글은 열린·안전한 레이크하우스 아키텍처로 가는 여정의 일부인 Intuit의 마이그레이션을 문서화하며, 동기는 운영 부담 감소, 데이터 탐색 개선, AWS 분석 서비스 통합 강화다.

사전 작업은 카탈로그 위생과 할당량 계산이다. Intuit는 HMS 카탈로그를 감사해 미사용 테이블·뷰를 제거하거나 표시해 마이그레이션에서 걸러졌고, HMS 내부 테이블의 P99 읽기/쓰기 수치로 GDC API 한도를 추정해 할당량 증액을 신청했으며, 부하 테스트로 피크 처리량이 스로틀 없이 지원됨을 확인하고 남은 스로틀에는 재시도를 구현했다. 마이그레이션 범위는 데이터베이스·테이블·파티션뿐이었다. 컬럼 통계, 권한, 역할, 함수, 트랜잭션은 명시적으로 범위 밖이었다. GDC는 테이블·데이터베이스 이름 변경을 지원하지 않으므로, 원자적 갱신을 위해 비파티션·비오픈테이블포맷 테이블 이름을 바꾸던 파이프라인에는 새 S3 위치에 쓰고 ALTER TABLE ... SET LOCATION을 실행하는 방식을 권한다.

아키텍처는 허브-스포크다. 원본 스포크 계정(S3 데이터의 메타데이터를 HMS가 관리), 중앙 데이터 거버넌스 계정(동기화 프로세스가 중앙 GDC로 메타데이터를 전파하고 AWS Lake Formation이 거버넌스하며 CloudTrail이 카탈로그 작업을 기록), 소비자 스포크 계정(Athena·Redshift·EMR이 Lake Formation과 로컬 Glue Data Catalog로 역할 기반 접근)으로 구성된다. 마이그레이션 전략은 4개 요소다. 1회 전체 마이그레이션, 팀이 상하류 의존 없이 파이프라인을 전환할 수 있게 하는 지속적 HMS→GDC 동기화, 상류 테이블이 이미 GDC로 옮겨간 뒤에도 HMS를 보는 파이프라인을 보호하는 지속적 GDC→HMS 동기화, 그리고 두 카탈로그를 시간별로 비교해 드리프트를 잡는 패리티 도구와 전체 재동기화 없이 불일치를 수리하는 ad hoc 마이그레이션.

양방향 동기화의 미묘한 공학 문제는 순환 갱신 방지이며, 모든 테이블에 단일 진원장을 지정해 해결한다. Amazon DynamoDB 중재 테이블의 sourceCatalog 플래그(HMS 또는 GDC)가 그 역할을 한다. HMS→GDC 동기화는 진원장이 HMS인 테이블만 가져가고, GDC→HMS 동기화는 플래그를 확인해 변경이 HMS에서 건너온 연쇄가 아니라 진짜 GDC 발생인지 확인한다. 각 테이블의 메타데이터는 임의 시점에 한 방향으로만 흐른다.

## 핵심 내용

- 1회 마이그레이션: 배칭·재시도로 커스터마이즈한 AWS Glue Hive 메타스토어 마이그레이션 유틸리티가 Glue ETL 잡으로 HMS 뒤의 Aurora MySQL에서 JDBC로 데이터베이스·테이블·파티션을 읽어 DynamicFrame으로 변환해 GDC에 기록. Lambda가 cdk.json의 설정(워커 수, 데이터베이스/테이블/파티션 쓰기 팩터)으로 잡을 시작하고 CloudWatch가 지표를 수집. 주말에 걸쳐 계획되었고 증분 동기화 중지, GDC 정리, 전체·델타 동기화, 패리티 작업 가동 등 9단계 오케스트레이션을 포함.
- 레이트 리밋 계산: RatePerSecond = catalog.ratePerDPUSecond / DefaultExecutorsPerDPU. 기본값(10, 2)에서 DPU당 초당 5건이며 잘 분할된 DataFrame 기준 200-DPU 잡은 약 500건/초. catalog.overwriteIfExists=false로 기존 테이블 건너뛰기, 쓰기는 BatchCreatePartitions로 API 호출량 절감, 지수 백오프+재시도로 스로틀 흡수.
- HMS→GDC 증분 동기화: Debezium 커넥터가 HMS MySQL 인스턴스에서 변경 데이터 캡처(CDC)로 INSERT/UPDATE/DELETE를 감시하는 이벤트 기반 근실시간 전파(폴링·애플리케이션 훅 불필요). 객체 유형별 전용 Kafka 토픽으로 분리 — HMS-HIVE-DBS(데이터베이스), HMS-HIVE-TBLS(테이블), HMS-HIVE-TABLE_PARAMS(테이블 파라미터), HMS-HIVE-PARTITIONS(파티션), HMS-HIVE-SDS(파티션·테이블 위치 이벤트) — 유형별로 독립 처리·확장·재시도. 파티션은 테이블당 10초 롤링 윈도우로 누적 이벤트를 한 번의 배치 호출로 제출해 파티션 변동이 많을 때 스로틀을 줄인다. DynamoDB 스키마 옵트아웃 검사로 팀이 중앙 카탈로그로 흘러갈 메타데이터를 통제하고, 옵트아웃된 변경은 폐기된다. CDC 이벤트에 맥락이 부족하면(예: 파티션 갱신으로 완전한 테이블 정의 구성) 원본 Aurora MySQL에서 JDBC로 메타데이터를 보완 추출한다.
- GDC→HMS 증분 동기화: EventBridge 규칙이 데이터베이스/테이블/파티션 추가·삭제 이벤트를 감지해 Lambda(handle-eventbridge-events)를 호출하고, 원시 이벤트를 Amazon MSK 토픽 central-gdc-raw-events에 발행. Apache Flink 파이프라인이 스키마·테이블별 1분 롤링 윈도우로 버퍼링하고 이벤트 타임스탬프 순으로 정렬해 central-gdc-ordered-events에 재발행. 이후 두 소비 경로: Flink gdc-to-hms-sync 파이프라인이 DynamoDB 허용 목록을 검사(미허용 엔터티는 폐기)하고 Amazon Athena를 실행 엔진으로 써서 HMS에 변경을 반영하며, 데이터 레이크 크롤러가 데이터 레이크 컨트롤 플레인 메타데이터 인벤토리 DB를 갱신. 메타데이터는 EMR 클러스터에서 구동되는 Thrift 클라이언트와 Thrift SDK로 HMS에 동기화된다.
- 패리티 도구(시간별): 4단계 파이프라인 — 추출(DynamoDB에서 비교 대상 목록, HMS는 MySQL에서, GDC는 Glue API로), 저장(양쪽 추출을 S3에 Iceberg 테이블로), 비교(Spark로 양쪽 카탈로그의 데이터베이스 존재, 데이터베이스 내 테이블 존재, 컬럼·타입을 포함한 테이블 구조, 테이블 위치와 SerDe 경로, 파티션 값과 S3 위치, 뷰 정의 비교), 결과(차이 테이블, 집계 뷰, 패리티 상태·동기화 상태 뷰, 시간별 변경 이력 테이블).
- ad hoc 마이그레이션: 1회성 유틸리티를 확장해 데이터베이스·테이블·파티션 이름을 입력받아 해당 객체만 동기화. 패리티 도구가 찾은 불일치를 전체 재동기화 없이 수리.
- 마이그레이션 전 확인할 GDC 테이블 요건: 테이블 데이터는 S3에 있어야 하고(S3 위치의 데이터베이스만 마이그레이션), S3 위치 이름은 최대 701자, 가져오는 테이블 유형은 MANAGED_TABLE·EXTERNAL_TABLE·VIRTUAL_VIEW뿐, 컬럼 이름은 비어 있으면 안 되고 최대 255자(HMS는 256), 물음표·줄바꿈·백슬래시 문자 금지, 컬럼 타입 이름은 최대 131,072자.
- 전환 이후 방향: Intuit는 AWS Lake Formation에서 행·컬럼·셀 수준의 세밀한 접근 통제를 구현 중이며, 복잡한 솔루션과 애플리케이션에 이 수준의 통제가 필수라고 밝힌다. 카탈로그의 GDC 전환은 그 여정의 중요한 한 걸음이었다.

## 세부 사항

### 하드 커트오버 대신 양방향 동기화인 이유

Intuit의 중앙 팀은 데이터 카탈로그를 여러 팀이 쓰는 플랫폼으로 운영하며, 그 규모에서 일괄 전환은 불가능하다. 양방향 설계는 팀을 분리한다. 1회 마이그레이션 이후 팀은 준비되는 대로 파이프라인을 GDC로 옮길 수 있고(HMS→GDC 동기화가 중앙 카탈로그를 최신으로 유지), 아직 HMS를 보는 하류 파이프라인은 역방향 동기화가 보호한다. DynamoDB 중재 테이블이 쐐기다. 두 동기화 방향 사이의 순환 갱신 루프를 막고 거버넌스도 부호화한다(HMS→GDC는 옵트아웃, GDC→HMS는 허용 목록). 메타데이터는 팀이 동의한 곳으로만 흐른다.

### 1급 관심사로서의 이벤트 정렬

양방향 모두 정렬을 명시적으로 푸는 문제로 다룬다. HMS 쪽에서는 파티션 변동이 최대 볼륨 변경 유형이므로 테이블당 10초 롤링 윈도우로 이벤트를 합친다. GDC 쪽에서는 이벤트가 순서와 다르게 도착할 수 있으므로 Flink 파이프라인이 스키마·테이블별로 1분 버퍼링하고 타임스탬프 정렬 후 순서대로 재발행하며, 그다음에 소비자가 작동한다. 이 선택들은 유한한 지연을 지불하고 올바른 의미론과 크게 줄어든 API 호출을 얻는 거래다. 데모에서만 돌아가는 동기화와 기업 규모의 변동을 견디는 동기화의 차이다.

### 안전망으로서의 패리티와 수리

시간별 패리티 도구가 양방향 설계를 신뢰 가능하게 만든다. 쓰기를 받는 카탈로그가 둘이면 드리프트는 문제가 아니라 시간 문제다. 두 카탈로그의 Iceberg 표현을 Spark로 비교해 존재 여부, 컬럼·타입, 위치와 SerDe 경로, 파티션 값, 뷰 정의 같은 구조적 사실을 검증하고 차이·집계·상태·이력 뷰를 만든다. 드리프트가 보이면 ad hoc 마이그레이션이 영향받은 데이터베이스·테이블·파티션만 정확히 수리해 전체 재동기화를 피하고, 조정 비용을 불일치 크기에 비례하게 유지한다.
