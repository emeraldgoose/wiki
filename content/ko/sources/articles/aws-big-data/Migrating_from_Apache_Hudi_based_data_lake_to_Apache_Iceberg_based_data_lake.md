---
title: "Apache Hudi 기반 데이터 레이크를 Apache Iceberg 기반 데이터 레이크로 마이그레이션"
description: "AWS Glue 5.1 대화형 세션의 Jupyter 노트북에서 Spark add_files 프로시저나 Apache XTable로 Hudi CoW·MoR 테이블을 제자리 마이그레이션하거나 CTAS, CREATE + INSERT로 전체 재작성하는 방법을 정리했다."
tags: [source, aws-big-data, apache-iceberg, apache-hudi, data-lake, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/migrating-from-apache-hudi-based-data-lake-to-apache-iceberg-based-data-lake"
blog: aws-big-data
published_date: 2026-11-14
---

# Apache Hudi 기반 데이터 레이크를 Apache Iceberg 기반 데이터 레이크로 마이그레이션

**원문**: [AWS 빅데이터 블로그](https://aws.amazon.com/blogs/big-data/migrating-from-apache-hudi-based-data-lake-to-apache-iceberg-based-data-lake) · **게시일**: 2026-11-12

## 개요

개방형 테이블 포맷은 Amazon S3 위 데이터 레이크의 오랜 문제를 해결했다. Apache Hudi, Delta Lake, Apache Iceberg는 ACID 트랜잭션, 행 수준 업데이트와 삭제, 스냅샷 이력, 스키마 강제를 추가해 데이터 레이크를 감사하고 거버넌스하기 쉽게 만든다. 아키텍처가 성숙해지면서 Apache Hudi로 구축한 조직이 Apache Iceberg로 옮겨가는 사례가 늘고 있다. 전체 데이터 재작성 없이 파티션 구성을 동적으로 바꾸는 파티션 진화, 쿼리 필터와 물리 레이아웃을 분리하는 숨은 파티셔닝, 개방형 REST 카탈로그 프로토콜, Amazon Athena, Amazon Redshift, Amazon EMR, AWS Glue, Amazon SageMaker, Amazon Data Firehose와의 기본 통합이 그 이유다.

이 글은 AWS Glue 5.1 대화형 세션의 Jupyter 노트북에서 Apache Hudi 테이블을 Apache Iceberg로 변환하는 과정을 다룬다. Hudi의 두 테이블 유형을 모두 포함한다. Copy-on-Write(CoW)는 업데이트나 삭제가 영향을 받는 행을 담은 모든 base Parquet 파일을 완전히 재작성하고, Merge-on-Read(MoR)는 업데이트를 Avro 로그 파일에 추가했다가 읽을 때 병합한다. 마이그레이션 전략은 두 가지다. 제자리 마이그레이션은 데이터를 복사하지 않고 기존 Parquet 파일 위에 새 Iceberg 메타데이터를 생성하고, 전체 테이블(섀도) 마이그레이션은 데이터를 완전히 새로운 Iceberg 테이블로 재작성한다.

모든 대상 테이블은 AWS Glue Data Catalog에 등록되고, Amazon Athena로 마이그레이션 결과를 검증한다. 두 포맷이 같은 데이터 파일을 공유하는 동안 원본 Hudi 테이블을 지키는 운영 가드레일도 함께 설명한다.

## 핵심 내용

- 두 가지 접근이 있다. 제자리 마이그레이션은 데이터를 재작성하지 않아 빠르고 저렴하지만 소스의 스키마, 파티셔닝, 물리적 파일 형태를 그대로 물려받는다. 전체 테이블 마이그레이션은 연산 비용이 크고 전환까지 데이터가 두 번 저장되지만, 스키마 변경, Iceberg 숨은 파티셔닝, 프루닝을 위한 재정렬, 더 큰 대상 파일 크기를 적용할 수 있다.
- 제자리 마이그레이션은 Spark Iceberg add_files 프로시저와 Apache XTable(인큐베이팅) 동기화 도구, 두 기법으로 시연된다.
- add_files는 Hudi 파일 그룹 버저닝을 인식하지 못한 채 소스 위치 아래의 모든 Parquet 파일을 등록하므로, 레코드당 정확히 하나의 파일 버전만 남아 있어야 한다. CoW 테이블은 KEEP_LATEST_FILE_VERSIONS 정책(file_versions_retained = 1)으로 Hudi CLEAN을 실행하고, MoR 테이블은 add_files가 델타 로그 파일을 처리하지 못하므로 COMPACTION과 CLEAN을 먼저 실행한다.
- 샘플 실행에서 run_clean은 KEEP_LATEST_FILE_VERSIONS 정책으로 CoW 이벤트 테이블의 오래된 파일 3개를 382밀리초에 삭제했다.
- XTable은 데이터를 복사하지 않고 Hudi, Delta Lake, Iceberg 메타데이터를 상호 변환하며, 1회 변환과 지속적인 증분 동기화를 모두 지원한다. JVM만 있으면 어디서든 실행할 수 있어 Amazon ECS, Amazon EKS, Amazon EventBridge로 일정 트리거되는 AWS Lambda 함수에서도 구동된다. MoR 소스에는 base Parquet 파일만 읽으므로 먼저 컴팩션을 실행해야 하고, Hudi 메타데이터에서 Iceberg 매니페스트를 만들어 대체된 버전을 자동으로 무시하므로 CLEAN은 필요 없다.
- 전체 테이블 마이그레이션은 CREATE TABLE AS SELECT 한 문장 또는 작은 CTAS로 시드한 뒤 파티션 단위로 INSERT INTO ... SELECT를 배치로 나눠 실행하고 체크포인트를 남기는 CREATE + INSERT 패턴을 쓴다. Spark가 Hudi 실시간 뷰를 읽고 대기 중인 델타 로그까지 병합하므로 CoW와 MoR 절차는 동일하다.
- 알려진 문제: Iceberg 1.9.0~1.10.0에서는 ParquetUtil.footerMetrics의 NameMapping 손실 때문에 add_files와 snapshot 프로시저가 컬럼 통계를 생성하지 않아 쿼리 계획 시점의 파일 스킵 능력이 떨어진다. Iceberg 1.10.1(#14617)에서 수정됐고, 영향을 받는 런타임은 AWS Glue 5.1과 Amazon EMR 7.11-7.13이며, 프로덕션 마이그레이션에는 AWS Glue 6.0+ 또는 Amazon EMR 7.14+를 권한다.
- 제자리 마이그레이션은 Iceberg가 Hudi와 같은 Parquet 파일을 가리키게 된다. add_files 직후 테이블 속성 gc.enabled를 false로 바꾸고 전환 때까지 유지한다. XTable 증분 동기화는 GC가 켜져 있어야 정상 동작하므로, DROP TABLE ... PURGE, expire_snapshots, remove_orphan_files, 공유 프리픽스에 대한 수동 삭제를 하지 않는 운영 규율로 대신한다.
- 전환 전에는 AWS Glue Data Catalog 테이블 옵티마이저를 켜지 않는다. Glue가 관리하는 컴팩션, 스냅샷 보존, 고아 파일 정리가 Hudi 테이블이 아직 의존하는 Parquet 파일을 재작성하거나 삭제할 수 있다.
- 전체 마이그레이션 변형은 Amazon S3 Tables를 대상으로 할 수 있으며, S3 Tables는 컴팩션과 스냅샷 관리 같은 테이블 유지 관리를 자동으로 처리한다. 노트북 설정은 glue_version 5.1, worker_type G.1X, 워커 5개, --datalake-formats hudi,iceberg를 사용한다.
- 정리 단계에서는 마이그레이션된 Iceberg 테이블과 네임스페이스를 삭제하고, S3 Tables 리소스는 DROP TABLE ... PURGE와 DROP NAMESPACE로 제거한다.

## 세부 사항

### Hudi 소스 준비

노트북은 두 유형의 샘플 이벤트 테이블을 만들고 insert, update, delete를 수행한 뒤, list_table_files 헬퍼로 S3 레이아웃을 주석 달린 디렉터리 트리로 출력한다. CoW는 읽기가 저렴한 대신 수정된 파일 비율만큼 쓰기가 증폭되고, MoR는 업데이트를 Avro 로그 파일에 추가해 쓰기가 저렴하지만 컴팩션 전까지는 읽기 비용이 크다. 제자리 등록 전에 CLEAN을 실행해 최신 파일 슬라이스만 남기면 add_files가 대체된 버전을 중복 행으로 집어 올리지 않는다.

### add_files 경로

동일한 스키마와 파티셔닝(샘플은 year, month, day로 파티션)으로 대상 Iceberg 테이블을 만들고, 테이블마다 add_files를 한 번 실행한 뒤 Athena에서 Hudi 소스와 Iceberg 대상의 행 수와 샘플 행을 비교해 검증한다. MoR 테이블은 델타 로그가 base Parquet에 병합되도록 먼저 컴팩션을 실행하고, Spark가 캐시한 메타데이터를 무효화하도록 Hudi 테이블을 refresh한 다음 각 단계 후 파일 목록을 다시 확인한다.

### XTable 경로

XTable은 Hudi 메타데이터를 읽고 같은 Parquet 파일을 가리키는 동등한 Iceberg 메타데이터를 작성한다. 첫 실행이 전체 변환을 수행하고, 같은 명령을 다시 실행하면 이전 실행을 자동으로 감지해 증분 모드로 전환되므로 소비자가 옮겨가는 동안 Iceberg 테이블을 Hudi의 지속적인 쓰기와 계속 동기화할 수 있다. 모든 소비자의 전환이 끝나면 동기화를 멈추고 Hudi를 폐기한다.

### 전체 테이블 마이그레이션과 전환

섀도 마이그레이션은 Hudi 실시간 뷰를 읽어 CTAS 또는 CREATE + INSERT로 일반 S3 버킷이나 Amazon S3 Tables에 완전히 새로운 Iceberg 테이블을 작성한다. 데이터가 복사되므로 소스를 폐기할 때까지 저장 공간이 두 배가 되지만, 마이그레이션 전에 Hudi 소스의 컴팩션이나 정리가 필요 없다. 전환이 끝나면 마이그레이션된 테이블과 네임스페이스를 삭제해 정리하고, 이후에는 정상적인 Iceberg 유지 관리를 재개한다.
