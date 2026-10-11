---
title: "Funke 소개: Databricks 네이티브 HL7v2 파싱"
description: "Smolder의 PySpark 후계자로 HL7v2 임상 메시지를 계층 그대로 네이티브 Spark 타입으로 파싱하는 오픈소스 Funke 가속기."
tags: [source, databricks, healthcare, data-engineering, lakehouse, ko]
locale: ko
source_url: "https://www.databricks.com/blog/introducing-funke-native-hl7v2-parsing-databricks"
blog: databricks
published_date: 2026-10-08
---

# Funke 소개: Databricks 네이티브 HL7v2 파싱

**출처**: [Databricks Blog](https://www.databricks.com/blog/introducing-funke-native-hl7v2-parsing-databricks) · **발행**: 2026-10-08

## 개요

HL7v2는 여전히 의료 메시징을 떠받치지만 중첩된 구분자 구조 탓에 손실 있는 FHIR 변환이나 서드파티 평탄화 엔진에 의존해야 했다. Funke(독일어로 spark)는 2021년 Scala 라이브러리 Smolder의 Python/PySpark 후계자로, 모든 HL7v2 메시지·버전을 세그먼트/필드/컴포넌트/서브컴포넌트 계층 그대로 네이티브 Spark 타입에 무손실 파싱하고 실행 가능한 데모와 함께 에셋 번들로 배포된다.

## 파이프라인 동작

메달리온 Declarative Pipeline으로 배포되며, Auto Loader가 Unity Catalog 볼륨의 원본 HL7 파일을 추적 메타데이터와 함께 브론즈 `raw_messages`에 적재하고, 파서 단계가 MSH 선언 구분자·이스케이프를 반영한 네이티브 `hl7` 컬럼을 실버에 더한다. 분석가는 일반 SQL이나 `get_value` 같은 접근 헬퍼로 임의 원소에 닿아 골드 테이블을 직접 만들고, 데모는 ADT 이력→CDC 기반 실시간 병상 현황→병상 가동률 지표로 이어지는 종단 흐름을 컨트롤룸 앱과 함께 보여준다.

## 범위와 시작법

Funke는 파서이자 수집 가속기이지 인터페이스 엔진이 아니다. 완전하고 거버넌스된 조회 가능 메시지를 주고, 세그먼트를 업무 개념에 매핑하는 일은 임상 도메인 지식의 몫으로 남긴다. 시작은 저장소를 워크스페이스에 클론→번들 에디터 Deploy(또는 CLI)→landing 볼륨에 HL7 업로드→파이프라인 Run의 순서로, 수 분이면 스트리밍 임상 피드가 선다.

## References

- [Introducing Funke: Native HL7v2 Parsing on Databricks](https://www.databricks.com/blog/introducing-funke-native-hl7v2-parsing-databricks)
