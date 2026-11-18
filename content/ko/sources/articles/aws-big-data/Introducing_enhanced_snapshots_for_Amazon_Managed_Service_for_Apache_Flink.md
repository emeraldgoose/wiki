---
title: "Amazon Managed Service for Apache Flink 향상된 스냅샷(enhanced snapshots) 소개"
description: "향상된 스냅샷이 Apache Flink 애플리케이션의 상태를 독립적인 AWS 리소스로 만든다 — 다른 애플리케이션에서 복원, S3 내보내기/가져오기, 블루/그린 배포·리전 간 재해 복구·상태 유지 마이그레이션을 지원."
tags: [source, aws-big-data, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/introducing-enhanced-snapshots-for-amazon-managed-service-for-apache-flink"
blog: aws-big-data
published_date: "2026-11-19"
---

# Amazon Managed Service for Apache Flink 향상된 스냅샷(enhanced snapshots) 소개

**출처**: [aws-big-data](https://aws.amazon.com/blogs/big-data/introducing-enhanced-snapshots-for-amazon-managed-service-for-apache-flink) · **게시일**: 2026-11-16

## 개요

집계·조인·윈도우를 수행하는 Apache Flink 애플리케이션은 이벤트를 처리하며 상태(state)를 쌓아 가고, Amazon Managed Service for Apache Flink는 그 상태를 스냅샷으로 저장한다. 지금까지 스냅샷은 그것을 만든 애플리케이션에 종속되어 같은 애플리케이션·같은 리전에서만 복원할 수 있었다. 현재 GA로 발표된 향상된 스냅샷은 자체 ARN을 가진 독립적인 AWS 리소스로, 생성 애플리케이션과 분리된다. 같은 계정·리전의 *다른* 애플리케이션을 이것으로 시작할 수 있고, 소유한 S3 버킷으로 내보낼 수 있으며, S3의 Flink 세이브포인트를 새 향상된 스냅샷으로 가져와 애플리케이션을 시작할 수 있다.

향상된 스냅샷으로 상태ful 애플리케이션 업데이트를 긴 처리 중단 없이 배포하고, 두 번째 리전에서 복구하고, 자체 관리 Flink 작업을 상태와 함께 관리형 서비스로 옮길 수 있다. Apache Flink 1.20 이상에서 동작한다.

## 핵심 내용

- **상태ful 앱의 블루/그린 배포**: 실행 중인 blue의 향상된 스냅샷을 찍고 새 코드의 green을 그 스냅샷에서 시작한다 — green은 blue의 상태로 시작해 스냅샷 이후 기록된 이벤트만 처리한다. green이 따라잡으면 다운스트림 소비자를 전환하고 blue를 중지한다. green에 문제가 생기면 blue가 그대로 실행 중이다. 주의점: 둘 다 실행되는 동안 양쪽의 컴퓨트 비용을 낸다. green은 스냅샷 이후 이벤트를 재처리하므로 출력이 blue와 겹치며, 다운스트림은 중복을 허용하거나 제거해야 한다(전환 구간에 exactly-once 없음). 프로덕션 상태 대상 A/B 테스트, 버그 재현용 상태 복제에도 쓸 수 있다.
- **두 번째 리전 재해 복구**: 스냅샷을 주기적으로 기본 리전 버킷에 내보내고, S3 Cross-Region Replication으로 대기 리전에 복제한다. 페일오버 시 대기 리전에서 최신 복제 스냅샷을 가져와 대기 애플리케이션을 시작한다. 내보내기 빈도는 비용(작업 수 + S3 스토리지/복제)과 복구 시점 목표(RPO) 사이의 트레이드오프이며, RTO에 맞춰 주기를 정한다.
- **상태와 함께 자체 관리 Flink 마이그레이션**: 자체 관리 클러스터에서 세이브포인트를 찍고, 대상 계정/리전의 S3로 복사한 뒤, 향상된 스냅샷으로 가져와 관리형 애플리케이션을 시작한다 — 앱은 세이브포인트 오프셋부터 재개해 이후 데이터만 처리한다(전체 리플레이 불필요). 가져오기 전에 세이브포인트를 검증하며(원본 객체는 CRC-64/NVME 전체 객체 체크섬 포함 문서화된 요구 사항 충족 필요), 연산자 ID(UID)와 상태 타입이 일치해야 하고 지원되는 Flink 버전이어야 한다. 가져온 스냅샷에는 소스 애플리케이션이 없어 애플리케이션별 스냅샷 목록에 나타나지 않으므로, ListSnapshots를 SnapshotInitiatorOperation=ImportSnapshot으로 호출해 추적한다.
- **켜는 방법**: 신규 앱은 `ApplicationSnapshotConfiguration`에 `SnapshotMode: ENHANCED_SNAPSHOTS`를 설정한다. 기존 실행 중인 앱도 상태를 유지한 채 전환할 수 있다(`update-application`의 `SnapshotModeUpdate`). `RollbackApplication`은 다음 업데이트 전까지만 전환을 되돌릴 수 있고, 전환 후에는 `CreateApplicationSnapshot`이 오류를 반환하므로 주기적 스냅샷 스크립트를 `CreateSnapshot`으로 옮겨야 한다. 전환 직후 향상된 스냅샷을 하나 찍어 두라.
- **복원**: `create-snapshot`은 비동기이며(`describe-snapshot`을 SnapshotStatus가 READY가 될 때까지 폴링; 응답에 SnapshotArn 포함), 대상 앱을 `RESTORE_FROM_CUSTOM_SNAPSHOT` + `SnapshotArn`으로 시작한다(기존 애플리케이션 스냅샷은 `SnapshotName`). 복원 앱의 연산자 UID·상태 타입·maxParallelism이 호환되어야 하고 호환되는 Flink 버전이어야 한다. 향상된 스냅샷은 `DeleteSnapshot`으로 삭제하기 전까지, 생성 앱을 삭제한 뒤에도 남는다.
- **내보내기/가져오기 권한**: 내보내기·가져오기는 요청에 전달한 IAM 역할을 서비스가 assume하므로 S3 권한은 호출자가 아니라 역할에 있어야 한다. 역할의 트러스트 정책은 `kinesisanalytics.amazonaws.com`을 `aws:SourceAccount`/`aws:SourceArn`으로 스코프한다. 버킷은 스냅샷과 같은 계정·리전에 있어야 한다. `KeyPrefix`는 슬래시로 끝나야 하고, 내보내기마다 새 폴더가 생성되며 위치는 `ExportedPrefix`로 보고된다 — 가져오기는 상위 프리픽스가 아니라 그 정확한 폴더를 가리켜야 한다. 목적지 암호화에 고객 관리형 KMS 키를 쓸 수 있다.

## 세부 내용

세 가지 사용 사례는 모두 하나의 개념으로 귀결된다: 애플리케이션 상태를 재사용 가능한 AWS 리소스로 만드는 것. 블루/그린은 상태ful Flink 작업의 전통적 중지-재시작 배포가 초래하는 긴 중단과 전체 이력 재처리를 없앤다. 리전 간 DR은 리전 장애 시 처음부터 상태를 재구성해야 하는 문제를 없앤다. 상태 유지 마이그레이션은 관리형 서비스 도입 시 "빈 상태로 시작해 전체 리플레이" 전환의 고통을 없앤다.

기계적으로는 API 몇 번과 앱 설정 하나면 된다: 스냅샷 모드를 켜고, `create-snapshot`(또는 교차 리전/마이그레이션이면 export/import)을 실행한 뒤, 새 앱을 `RESTORE_FROM_CUSTOM_SNAPSHOT` + `SnapshotArn`으로 시작한다. 글의 AWS CLI 예시는 `update-application`, `create-snapshot`, `describe-snapshot`, `start-application`, `export-snapshot`, `import-snapshot`을 다룬다. 글 말미의 Agent Skill은 코딩 에이전트에 같은 안내를 제공한다. 전체 레퍼런스(가져오기 전제 조건, export/import 역할의 완전한 트러스트/권한 정책 포함)는 Managed Service for Apache Flink Developer Guide의 Enhanced snapshots를 참고하라.

## 참고 자료

- 원문: [Introducing enhanced snapshots for Amazon Managed Service for Apache Flink](https://aws.amazon.com/blogs/big-data/introducing-enhanced-snapshots-for-amazon-managed-service-for-apache-flink)
