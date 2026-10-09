---
title: Twitter Blobstore 하드웨어 수명주기 모니터링 및 리포팅 서비스
description: Blobstore 사진/동영상 스토리지를 위한 베어메탈 수명주기(allocated, managed, maintenance, repair) 관리 방식
tags: [source, twitter, x, blobstore, storage, hardware, sre, ko]
locale: ko
source_url: "https://blog.x.com/engineering/en_us/topics/infrastructure/2023/twitters-blobstore-hardware-lifecycle-monitoring-and-reporting-service"
blog: twitter
date: '2023-02-23'
---

# Twitter Blobstore 하드웨어 수명주기 모니터링 및 리포팅 서비스

## 요약

[Blobstore](https://blog.twitter.com/engineering/en_us/a/2012/blobstore-twitter-s-in-house-photo-storage-system)는 사진·동영상 등 대용량 바이너리 객체를 저장하는 Twitter 자체 저비용·고성능 스토리지이며, 대부분 온프레미스 데이터센터의 베어메탈 서버에서 동작한다. 이 글은 가시성 없이 운영되던 시기를 끝낸 하드웨어 수명주기 관리 서비스를 다룬다. 과거에는 호스트가 상태 사이를 표류했고, 수동 임시 쿼리로만 파악했으며, 머신은 알림 없이 특정 상태에 무기한 머물렀고, 물리 용량 알림도 없어 용량 부족이 다른 알림이나 수동 개입으로 뒤늦게 발견됐다.

## 목표

1. Blobstore 서비스 상태 및 인프라 모니터링 개선
2. 수동 토일(toil) 감소
3. 프로비저닝 위기 시 대응·복구 속도 향상
4. 베어메탈 서버 상태 통찰 확보
5. Blobstore 베어메탈 관리 지원
6. 용량 부족·수명주기 문제 탐지 및 예방

## 4가지 수명주기 상태

- **Allocated** — 용량 관리 팀에서 새로 할당받았거나, 수리 후 재이미징되어 복귀한 상태
- **Managed** — 기대되는 운영 설정과 일치하여 트래픽을 처리하는 상태
- **Maintenance** — 커널/펌웨어 업데이트가 필요하거나 이상 징후가 보이는 상태
- **Repair** — 치명적 오류(예: I/O 에러 디스크)로 Site Operations 팀이 소유하는 상태. 수리 성공 시 초기화 후 **allocated**로 복귀하며 순환이 완성된다.

## 핵심 메커니즘

### 프로비저닝 (allocated → managed)

프로비저너 서비스가 각 호스트에서 24시간마다 무작위 시각에 실행된다. 재이미징/할당 후 호스트가 올바르게 구성됐는지 검증하고, 데이터 디스크를 포맷한 뒤(UUID 갱신, FAT 파일, 최상위 파일/디렉터리 설정) Puppet을 실행해 소프트웨어를 수렴시킨다. 성공하면 **managed**로 전환하고 데이터센터에 편입한다.

### Airflow 기반 펌웨어/커널 컴플라이언스 (managed → maintenance → managed)

Airflow와 Airflow-Compliance가 구식 펌웨어·커널 호스트를 스캔한다. 대상 호스트의 모니터링 알림을 무음 처리하고 **maintenance**로 옮겨 펌웨어를 업그레이드한 뒤, 완료되면 **managed**로 복귀·알림 해제한다. 실패는 Slack으로 Blobstore에 통지되며, 업데이트 실패 호스트는 항상 리스를 해제해(오탐 방지) 다른 자동화나 수동 점검이 이어받는다.

### 수명주기 메트릭 파이프라인

Blobstore 에이전트에 수명주기 메트릭을 추가했다: 프로비저닝 수, **allocated** 호스트 수, **repair** 이송·대기 수, **managed** 전환 수, 재부팅 목록. Twitter 메트릭 라이브러리는 2분 미만 cron 작업의 통계를 안정적으로 수집하지 못하므로, 각 머신의 단기 Python 서비스가 CuckooScribePublisher로 로컬 Scribe 데몬에 전송하고, 이를 거쳐 Cuckoo·대시보드로 전달한다.

### 디스크 복구 자동화 (managed → repair)

고장 호스트의 **repair** 이송을 자동화했다: Blobstore 매핑 서비스에서 실패·미사용 노드를 수집하고, **maintenance** 중이거나 수리 티켓이 있는 호스트는 제외한다. 경험적 기준으로 재부팅/수리를 결정한다(예: 한 달 6회 초과, 한 주 3회 초과, 하루 2회 초과 시 **repair** 이송·무음·티켓 생성·이력 초기화, 그 외는 재부팅 후 이력 정리). 플릿 전체의 죽은 디스크 수를 집계하고, 운영에서 제외하며, Site Operations로 보내는 속도를 조절한다. 핫스왑이 안 되는 플릿 특성상 수동 절차의 자동화가 엔지니어 토일 감소와 가시성 확보에 결정적이었다.

## 결과와 교훈

- 토일 감소: 프로비저닝·컴플라이언스 업그레이드·수리 분류가 스케줄/자동화로 동작
- 가시성: 상태별 대시보드로 용량 부족과 정체 호스트 조기 경보
- 실패 처리 규율: maintenance 중 무음, 실패 시 리스 해제, maintenance 호스트 제외로 알림 폭풍과 오작동 재부팅 방지

## SW 엔지니어를 위한 시사점

- 플릿 하드웨어를 명시적 유한 상태 기계(allocated/managed/maintenance/repair)로 모델링하면 자동화·대시보드·소유권 경계가 명확해진다.
- 단기 cron 텔레메트리는 푸시 기반 부채널(여기서는 로컬 Scribe 데몬 → Cuckoo)이 필요하다.
- 수리 제출을 속도 제한하고, 일/주/월 윈도우의 점진적 기준으로 처리해 불량 디스크 배치가 수리 큐를 폭주시키지 않게 한다.

## 참고

- 원문: https://blog.x.com/engineering/en_us/topics/infrastructure/2023/twitters-blobstore-hardware-lifecycle-monitoring-and-reporting-service (Taylor Olson, Ashwin Poojary, 2023-02-23)
- 관련: `concepts/infrastructure/kubernetes.md`, `concepts/data-engineering/delta-lake.md`
