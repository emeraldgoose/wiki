---
title: "Sitar-Agent: 대규모 동적 설정 사이드카 구축기"
description: 동적 설정 전달용 쿠버네티스 사이드카 — S3 스냅샷, 캐시형 풀, SQLite 전환, 메인-vs-사이드카 트레이드오프
tags: [source, airbnb, infrastructure, kubernetes, configuration, distributed-systems, ko]
locale: ko
source_url: "https://medium.com/airbnb-engineering/sitar-agent-building-a-reliable-dynamic-configuration-sidecar-at-scale-b7e00c152068"
blog: airbnb
date: 2026-06-04
---

# Sitar-Agent: 대규모 동적 설정 사이드카 구축기

**출처**: Airbnb Engineering (Medium) · **발행**: 2026-06-04 · **저자**: Bo Teng, Cosmo Qiu, Siyuan Zhou, Ankur Soni, Xin Huang, Willis Harvey. Sitar 서비스 아키텍처/안전성 편의 동반 글.

## 문제

분당 수 차례 커밋되는 설정 변경을 수천 서비스 인스턴스에 **재배포 없이, 수 초 내, 신뢰성 있게** 전달하려면? 제약: Sitar 장애 시에도 설정은 항상 읽혀야 함(예전 값 > 읽힘 불가), 수만 파드에 수십 초 전파, 다언어 함대(Java, Python, Go, TypeScript, Ruby)에 언어별 유지보수 최소.

## 전달 수명주기

1. **생성/수정** (Git 플로우·웹 UI) → Sitar Service (버전·변경이력·ACL).
2. **시간 단위 스냅샷** — 전체 설정 그룹 상태를 S3에 압축 저장.
3. **파드 기동**: (3.1) 사이드카가 S3 스냅샷을 공유 디스크에 프리로드(빠른 재시작, Sitar 장애 생존, 배포 시 폭주 방지) → (3.2) Sitar와 초기 동기화로 스냅샷 이후 변경 따라잡기 → readiness 신호 후 메인 컨테이너 시작.
4. **정상 상태**: 수 초+지터 폴링 루프.
5. **읽기**: 메인 컨테이너가 마운트 디스크를 클라이언트 라이브러리(투명 인메모리 캐시 갱신)로 읽기.

## 핵심 결정 (2024년 Ruby → Java 재작성)

**사이드카 vs 인프로세스 라이브러리**: 라이브러리는 파드당 JVM 오버헤드·운영 표면 절감 — 그러나 5개 언어 재구현, 격리 상실(Sitar 버그가 앱을 죽이거나 그 반대), 로그/메트릭 혼합, 컨테이너 단위 최적화 불가. **사이드카 유지**: 절감액이 신뢰성/유지보수 비용을 정당화 못함.

**풀 vs 푸시**: 10초 풀은 단순하나 유휴 부하, 푸시는 효율적이나 복잡. 풀 유지 + 서버 최적화 둘: (1) **짧은 TTL(10초) 서버 캐시** — 수동 변경은 약간의 지연 허용, 대부분 폴링이 캐시 적중 (2) 캐시 미스 시 **변경 토큰**(마지막 스캔 DB 행) 전달 — 이미 본 행 스캔 생략. 단순·무상태·확장 가능.

**로컬 저장소 Sparkey → SQLite**: 둘 다 Sparkey 대비 크기/메모리/QPS 우위이나, RocksDB 대신 SQLite — 워크로드가 여유롭게 범위 내, 다언어 라이브러리 성숙, WAL 동시 접근, 운영 단순(컴팩션/컬럼패밀리 튜닝·전문성 불필요). **안전 전환**: 서비스별 섀도 읽기 비교(Sparkey 서빙 + SQLite 병렬 검증) + 플래그 점진 롤아웃, Tier-0 마지막.

## 엔지니어 관점 시사점

- **예전 값 > 읽힘 불가를 명시 설계 목표로** — 스냅샷 프리로드+디스크 읽기로 귀결.
- 푸시로 가기 전 단순 구조(풀) 유지 + **서버 측 최적화**(TTL 캐시+증분 토큰) 먼저.
- 다언어 함대는 라이브러리보다 사이드카, 파드당 비용은 격리 값어치.
- 저장소 전환: 섀도 읽기 + 플래그 롤아웃, 핵심 등급 마지막.
