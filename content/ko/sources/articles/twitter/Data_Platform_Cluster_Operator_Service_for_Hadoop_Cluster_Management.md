---
title: Hadoop 클러스터 관리용 데이터 플랫폼 클러스터 오퍼레이터 서비스
description: Hadoop 호스트 수명주기·쿼터·keytab을 자동화한 Twitter의 Flask 기반 Python 오퍼레이터 DCO
tags: [source, twitter, x, hadoop, sre, automation, operators, ko]
locale: ko
source_url: "https://blog.x.com/engineering/en_us/topics/infrastructure/2023/the-data-platform-cluster-operator-service-for-hadoop-cluster-management"
blog: twitter
date: '2023-02-08'
---

# Hadoop 클러스터 관리용 데이터 플랫폼 클러스터 오퍼레이터 서비스

## 요약

Twitter는 엔터프라이즈 Hadoop 배포판 없이 Apache Hadoop을 운영하므로, 그 규모에 맞는 표준 클러스터 관리 도구가 없었다. 데이터 플랫폼 SRE는 호스트 추가/제거, 드레인, 용량 요청 대응, 호스트 수명주기, 클러스터 상태 관리 같은 일상 운영에 대부분의 시간을 썼다. 팀은 이런 작업을 API 기반·오케스트레이션·단일 단계 오퍼레이션으로 바꾼 **데이터 플랫폼 클러스터 오퍼레이터(DCO)** — Python/Flask 서비스 — 를 만들어 전 데이터센터·클라우드에서 Hadoop을 관리한다.

## 아키텍처

- **Flask** 웹 계층이 로드밸런서 + WSGI 게이트웨이 뒤에서 API 엔드포인트를 제공한다.
- Hadoop 관리 요청은 파싱되어 **샤딩된 MySQL** 데이터베이스에 저장되고(요청량 수평 확장을 위한 샤딩), **내부 관리형 신뢰성 워크플로 엔진**으로 전달되어 호스트별 작업 집합(플랜)으로 실행된다. 각 작업은 설정된 횟수만큼 재시도 가능하고 실패 양상에 따라 다른 작업 집합을 시도한다.
- 콜백이 DCO 데이터베이스의 작업 상태를 갱신하며, 콜백 시점에 DCO가 죽어 있으면 주기적 폴러가 플랜 상태를 조정(reconcile)한다. 즉 오케스트레이션은 DCO 장애에도 생존한다.
- **요청 관리 컨트롤러**가 API 호출을 받아 작업을 디스패치한다.
- 기술 스택: Flask, MySQL 백엔드, 서비스 배포 인프라, 워크플로 엔진.

## 기능

- **hadoop-admin 라이브러리** — Hadoop 관리 로직을 담은 Python 라이브러리. 클러스터/서비스 상태 조회와 노드 내 바이너리를 이용한 노드별 작업을 수행한다.
- **호스트 추가** — SRE가 호스트명 파일 + 클러스터 변수를 제출하면 DCO가 패키지 설치·설정 변경·서비스 재시작을 수행하고 작업 ID로 진행 상황을 추적한다. 여러 단계의 오류 유발 절차가 한 번의 호출이 된다.
- **호스트 제거** — 한 단계로 클러스터에서 제거하고 재설치 과정을 거쳐 다른 클러스터에 투입 가능한 상태로 만든다.
- **HDFS/YARN 쿼터 관리** — 스토리지·컴퓨트 할당/해제를 수행하고 변경 이력을 저장해 고객 과금(chargeback)에 활용한다.
- **Keytab 관리** — 모든 Twitter Hadoop 클러스터가 Kerberos 인증을 사용하므로, DCO가 각 노드의 keytab 수명주기를 프로비저닝·관리한다(Hadoop Kerberos화 작업의 동반 요소).
- **기능 플래그** — 클러스터별 YAML이 해당 클러스터에 필요한 기능을 선언해 롤아웃을 제어한다.
- **고가용성 입장** — DCO는 데이터센터별로 로컬 오퍼레이션을 처리하며, HDFS 데이터 경로·YARN 용량 경로에 관여하지 않으므로 의도적으로 적당한 uptime SLO를 가진다.

## 결과

DCO는 철저히 테스트되어 운영 클러스터에 배포됐고, Hadoop 운영을 더 빠르고 오류 적게, SRE 인력을 플릿 규모에 비례해 늘리지 않고도 확장 가능하게 만들었다.

## SW 엔지니어를 위한 시사점

- 오퍼레이터 프레임워크가 없는 시스템에 Kubernetes 오퍼레이터 패턴을 적용한 사례다: MySQL에 원하는 상태 저장, 워크플로 엔진에서 조정, 호스트별 재시도 가능 작업.
- 워커 장애뿐 아니라 수신자(DCO) 장애에도 대비한 콜백 경로 설계(폴 기반 조정을 백업으로)가 필요하다.
- 컨트롤 플레인을 데이터 경로에서 분리하면 데이터 플레인은 엄격한 SLO를 유지하면서 컨트롤 플레인 SLO는 낮게 가져갈 수 있다.
- 클러스터별 기능 플래그 YAML로 하나의 오퍼레이터 바이너리가 이기종 플릿을 안전하게 다룬다.

## 참고

- 원문: https://blog.x.com/engineering/en_us/topics/infrastructure/2023/the-data-platform-cluster-operator-service-for-hadoop-cluster-management (Ashwin Poojary, Lakshman Ganesh Rajamani, Sampath Kumar, 2023-02-08)
- 관련: `concepts/infrastructure/kubernetes.md`, `concepts/data-engineering/apache-kafka.md`
