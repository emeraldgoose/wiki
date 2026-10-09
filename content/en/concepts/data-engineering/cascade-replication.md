---
title: "Cascade Replication"
description: "Cascade replication in distributed databases: purpose, consistency guarantees, performance characteristics, use cases in financial systems and geographic distribution, and common pitfalls"
tags: [concept, data-engineering, replication, distributed-systems, consistency]
locale: en
published: 2026-09-09
---

# Cascade Replication (캐스케이드 복제)

## 정의
분산 데이터베이스 시스템에서 데이터 일관성을 보장하면서 읽기 성능을 향상시키기 위해 사용되는 복제 전략입니다. primary-secondary 구조를 다단계로 연결하여 구현합니다.

## 왜 중요한가
- **읽기 확장성**: 여러 레플리카를 통해 읽기 트래픽 분산
- **지리적 분산**: 사용자 위치에 가까운 레플리카 제공, 지연 시간 감소
- **팔리오션 일관성**: 쓰기 작업이 모든 노드에 전파될 때까지 대기하지 않으면서도 점진적 일관성 보장

## 작동 원리
### 기본 구조
```
Primary → Secondary1 → Secondary2 → Secondary3
      ↑              ↑              ↑
    Clients     Clients       Clients
```

### 복제 흐름
1. **쓰기 (Write)**: 클라이언트가 Primary 노드에_write 요청을 보냄
2. **확인 (Acknowledge)**: Primary가 쓰기를 완료하고 Secondary1에 전파
3. **계단식 전파**: Secondary1이 Secondary2에, Secondary2가 Secondary3에 순차적으로 전파
4. **읽기 (Read)**: 클라이언트는 자신에게 가장 가까운 레플리카 또는 가장 최신의 레플리카에서 읽기

### 일관성 모델
- **준시점 일관성 (Bounded Staleness)**: 쓰기로부터 최대 K초 이내의 데이터 읽기 보장
- **세션 일관성**: 동일한 사용자의 세션 내에서 읽기 후 쓰기 보장
- **이벤ual consistency**: 업데이트가 propagate된 후후나 결국 모든 노드에서 동일한 값 보기 보장

## 일반적인 사용 패턴

### 금융 시스템에서의 활용
- **트랜잭션 기록**: 주요 데이터베이스에 쓰기 후, 보조 노드에 감사 로그 및 분석 목적의 복제
- **읽기 전용 라우팅**: 독자 조회를 메인 DB에 부하 분산
- **재해 복구**: 재해 발생 시 이전 시점 복구 (Point-in-Time Recovery)

### 지리적 분산 애플리케이션
- **글로벌 사용자 기반**: 사용자 위치에 가장 가까운 레플리카에서 읽기
- **콘텐츠 전파**: 전 세계 사용자에게 컨텐츠 빠르게 배포
- **오프라인 지원**: 레플리카가 오프라인 상태에서도 이전 데이터 제공

### 일반적인 배포 패턴
- **3계층 복제**: Primary + 2단계 Secondary (내결함성 + 읽기 확장성)
- **지역별 샤딩**: 지역별 Primary 노드와 해당 지역의 Secondary 체인 운영
- **활성-활성**: 여러 지역에서 Primary 운영, cross-region replicate for read

## 일반적인 함정

### 1. 쓰기 증폭 (Write Amplification)
- Secondary 체인 전체에 쓰기가 전파되면서 발생하는 트래픽 증폭
- 3계층 복제의 경우, 1건의 쓰기에 대해 2~3건의 네트워크 전파 발생
- **완화**: non-critical 쓰기는 Secondary에서만 처리하거나, 배치를 통해 전파 최적화

### 2. 읽기 스테일 (Stale Reads)
- 복제가 완전히 전파되지 않은 상태에서 읽기 수행하여 오래된 데이터 조회
- **완화**: 읽기 전용 노드에서 `sync` 상태 확인하거나, 세션 일관성 보장 정책 수립

### 3. 네트워크 파티션 시 데이터 분할
- 네트워크 단절 시 Primary와 Secondary 체인 분리 시 데이터 불일치 위험
- **완화**: 파티션 회복 후 동기화 프로세스 수립, split-brain 상황 예방 알고리즘 적용

### 4. Secondary 노드 장애 시 복구 지연
- Secondary 노드 복구 시, 누락된 쓰기들 재전파 및 인덱스 재구성 필요
- **완화**: 스냅샷 기반 복구 프로세스 자동화, incremental catch-up 메커니즘 제공

## 모니터링 지표
- **복제 지연 시간**: Primary → Secondary 전파까지의 시간 측정
- **복제 실패율**: 실패한 복제 전파 비율 및 원인 분류
- **레플리카 건강 상태**: 각 노드의 연결 상태 및 지연도 실시간 모니터링
- **읽기 후 쓰기 일관성**: 세션 내 읽기 후 쓰기 성공 여부 모니터링

## 참조
- "Designing Data-Intensive Applications" — Martin Kleppmann, Chapter 8
- Apache Cassandra 문서: Multi-DC replication
- Apache Kafka Replication 전략
- "Kubernetes Patterns" — volume mode와 replication 전략
