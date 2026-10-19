---
title: "Lakebase Postgres에 수 분 만에 테라바이트 적재하기"
description: "LTAP 아키텍처로 대량 적재를 프라이머리에서 Spark로 오프로드해 유효한 Postgres 페이지를 병렬 생성, 최대 147배 빠른 적재를 달성한다." (한국어 번역)
tags: [source, databricks, lakebase, postgres, data-ingestion, ko, ko]
locale: ko
source_url: "https://www.databricks.com/blog/load-terabytes-data-minutes-lakebase-postgres"
blog: databricks
published_date: 2026-10-08
---

# Lakebase Postgres에 수 분 만에 테라바이트 적재하기

## 개요

대량 적재는 운영용 Postgres의 고전적 위협이다. 단일 프라이머리 라이터에 테라바이트를 밀어 넣으면 라이브 트래픽의 CPU·I/O·WAL 대역폭을 빼앗는다. Lakebase의 LTAP(Lake Transactional/Analytical Processing) 설계는 Spark가 스토리지에 유효한 Postgres 상태를 직접 만들고 프라이머리는 결과만 공표하게 하여, 하루 10억 행 동기화에 8시간 걸리던 사례를 대폭 단축했다(내부 벤치마크 1TB 5분 미만, 프라이머리 무영향).

## 대량 적재가 Postgres를 괴롭히는 이유

Spark가 소스를 병렬로 읽어도 모든 행은 하나의 라이터를 통과한다. 프라이머리가 행을 힙·인덱스 페이지로 바꾸고 WAL을 기록·플러시한 뒤에야 커밋된다. 처리량이 단일 관문에 묶이고 같은 인스턴스가 OLTP를 서빙하므로, 팀은 심야 적재, 프라이머리 과다 프로비저닝, 백필·체크포인트 수동 관리에 시달린다.

## LTAP의 변화

Lakebase에서는 내구 상태가 프라이머리 로컬 디스크가 아닌 분산 스토리지 계층에 있어, 프라이머리가 유일한 영속 경로가 아니다. Spark가 힙·인덱스 슬라이스를 만들어 오브젝트 스토리지에 쓰고, 프라이머리는 전체 데이터가 아닌 간결한 WAL 레코드 하나로 임포트를 기록한다. 효과는 세 가지다. 적재가 OLTP와 경쟁하지 않고, 동시 임포트가 서로의 `COPY` 스트림 뒤에 줄 서지 않으며, 작은 프라이머리로 트래픽을 서빙하면서 Spark가 데이터 규모에 거의 선형으로 처리량을 내고 끝나면 종료된다.

## 병렬 페이지·인덱스 생성 방식

각 Spark 익스큐터는 binary-upgrade 모드의 샌드박스 Postgres를 띄워 카탈로그 OID를 이식하고(대상과 일치하는 페이지 생성), binary `COPY ... FREEZE`로 담당 힙 슬라이스를 만들며, 겹치지 않는 OID 범위를 배정받고, 페이지마다 체크섬을 계산해 페이지서버가 검증한다. 전부 확장·테이블 액세스 메서드 방식이라 Postgres 코어 수정은 없다. 인덱스는 분산 힙을 내려받지 않는다. 워커가 키·튜플 ID의 경량 스트림을 내보내면 헬퍼 테이블과 커스텀 액세스 메서드가 표준 B-tree 빌더에 먹여 슬라이스-로컬 ID를 최종 위치로 재매핑한다. 드라이버가 매니페스트를 쓰고 SQL 함수 하나로 호출하면, 페이지서버가 페이지를 확정·프리웜하고 스테이징 데이터가 사용자 테이블에 원자적으로 교체된다.

## References

- 원문: [Load terabytes of data in minutes into Lakebase Postgres](https://www.databricks.com/blog/load-terabytes-data-minutes-lakebase-postgres)
