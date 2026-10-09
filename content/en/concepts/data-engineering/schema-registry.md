---
title: "Schema Registry"
description: "Schema management for streaming data: Confluent Schema Registry, Avro/Proto schemas, compatibility modes, evolution, versioning, and downstream impact management"
tags: [concept, data-engineering, schema-registry, streaming, kafka]
locale: en
published: 2026-09-08
---

# Schema Registry (스키마 레지스트리)

## 정의
스트리밍 데이터 파이프라인에서 스키마를 중앙 집중화하여 관리하는 시스템입니다. 프로듀서와 컨슈머가 서로 다른 버전의 스키마를 안전하게 호환되며 사용할 수 있게 해줍니다.

## 왜 중요한가
- **호환성**: 오래된 프로듀서의 메시지가 새 컨슈머에서 제대로 해석되도록 보장
- **버전 관리**: 스키마의 점진적 진화 추적 및 이전 버전 되돌리기
- **데이터 품질**: 스키마 위배 메시지 조기 발견 및 필터링

## 핵심 기능
- **스키마 등록**: Avro, Protobuf, JSON Schema 등 형식 지원
- **호환성 모드**: 
  - **Backward**: 새 버전이 오래된 데이터 읽기 가능
  - **Forward**: 새 버전이 오래된 데이터 쓰기 가능  
  - **Full**: 양방향 호환성 보장
  - **None**: 검증 비활성화 (운영자 의도적 선택)
- **스키마 진화**: 필드 추가, 제거, 타입 변경 등 안전하게 진행
- **카탈로그**: 스키마 메타데이터 탐색 및 검색

## 일반적인 사용 패턴
### Kafka + Confluent Schema Registry
```bash
# Confluent CLI로 등록
confluent schema-registry schema register \
  --subject orders-value \
  --schema '{"type":"record","name":"Order","fields":[{"name":"id","type":"int"},{"name":"amount","type":"float"}]}'

# 호환성 정책 조회
confluent schema-registry compatibility authorize \
  --subject orders-value \
  --compatibility BACKWARD
```

### Schema evolution 예시
1. **필드 추가**: 새로운 옵션 필드 추가 (`{"name":"color","type":"string","default":""}`)
2. **필드 삭제**: 폐기 예정 플래그 후 다음 메이저 버전에서 제거
3. **타입 변경**: 호환성 모드에 따라 허용 여부 결정

## 일반적인 함정
- **호환성 모드 설정 누락**: 기본값(None)이면 임의Break 가능
- **백호드(Hidden Schema)**: 프로듀서에서 레지스트리에 등록하지 않고 직접 전송
- **버전 락**: 불필요한 호환성 정책으로 인해 legitimate한 진화도 막힘
- **성능 병목**: 초당 수백 TPS 이상 시 레지스트리 캐시 설정 검토 필요

## 참조
- Confluent Schema Registry 문서 (docs.confluent.io/platform/current/schema-registry)
- "Kafka: The Definitive Guide" — 이스마일라 바예, 제프리 리처즈
- Schema Evolution Best Practices 가이드라인
