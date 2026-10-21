---
title: "EC2의 Amazon EMR에서 Spark Connect 발표: 어디서든 대화형 PySpark"
description: "Spark Connect로 자신의 IDE나 SageMaker Unified Studio에서 EC2의 EMR 클러스터를 상대로 대화형 PySpark를 실행합니다."
tags: [source, aws-big-data, spark, emr, ko, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/announcing-spark-connect-on-amazon-emr-on-ec2-interactive-pyspark-anywhere"
blog: aws-big-data
published_date: 2026-09-23
---

# EC2의 Amazon EMR에서 Spark Connect 발표: 어디서든 대화형 PySpark

## 개요

EC2의 Amazon EMR이 Spark용 AWS 런타임(emr-spark-8.0, Spark 4.0.2 이상)에서 Spark Connect를 지원합니다. SageMaker Unified Studio 데이터 노트북이나 VS Code, PyCharm, Kiro, Jupyter 같은 자신의 IDE에서 대화형으로 PySpark를 개발·디버깅하면서, Spark 실행은 전용 EMR 클러스터에 맡길 수 있습니다. Python은 로컬에서 돌므로 전체 규모 데이터에 대해 중단점과 DataFrame 검사가 가능하고, 세션마다 권한이 분리되어 팀 전체가 하나의 클러스터를 공유할 수 있습니다.

기존에는 클러스터에 묶인 노트북에서 작업하거나 잡으로 패키징해야 결과를 볼 수 있었고, 로컬과 클러스터의 버전 차이도 느린 배포-확인 루프에서야 드러났습니다.

## 동작 방식

Spark Connect는 애플리케이션과 엔진을 분리합니다. 노트북·IDE의 가벼운 PySpark 클라이언트가 DataFrame·SQL 연산을 gRPC/TLS 채널로 클러스터의 Spark Connect Server에 보내면, 서버가 실행 후 결과를 돌려줍니다. 로컬 머신에는 Spark 설치도, 워크로드급 사양도 필요 없습니다.

세션을 시작하면 EMR이 서버를 YARN 애플리케이션으로 띄우고 엔드포인트와 단기 토큰을 반환하므로, 직접 서버를 띄울 필요가 없습니다. 서버가 기존에 운영하던 클러스터 위에서 돌기 때문에 인스턴스 타입, 라이브러리, 부트스트랩 액션, Spark 설정을 그대로 물려받아, 디버깅한 환경이 배치 잡 실행 환경과 일치합니다.

## 팀 전체가 하나의 클러스터 공유

각 세션은 실행 역할, 태그, 수명주기를 가진 독립 리소스입니다. 클러스터 하나가 최대 1,000개 동시 세션과 1,000개 동시 실행 역할을 지원합니다(서비스 상한이며 실제 동시성은 클러스터 크기에 좌우). 공유의 이점:

- **추가 클러스터 없는 온디맨드 Spark** — 1인당 유휴 클러스터 비용 제거.
- **일관된 환경** — Spark 버전·라이브러리·보안 설정을 하나로 패치·모니터링.
- **격리와 귀속** — 세션별 역할·태그로 데이터 접근을 제한하고 사용자별 비용을 추적하며, 한 세션 중단이 타인에게 영향 없음.
- **가시성과 제어** — 실행 중 세션은 Spark UI, 종료된 세션은 History Server에서 확인, 콘솔·API·CLI·SDK로 관리.

## 시작하기

세션 활성화 클러스터 생성, 세션 시작, 연결의 3단계입니다.

- **사전 조건:** 세션 활성화된 emr-spark-8.0.0 이상 릴리스, Spark 설치, 클러스터와 버전이 일치하는 로컬 Python 3.9+ 및 `pyspark[connect]`, 세션 관련 권한과 `iam:PassRole`.
- **클러스터 생성** 후 WAITING 상태에서 세션을 시작하고 IDLE까지 대기합니다.
- **연결:** 엔드포인트와 토큰을 조회해 `sc://호스트:443/` URL을 만들고 원격 `SparkSession`을 생성합니다. `spark.stop()`은 로컬 연결만 끊으므로, 세션은 명시적으로 종료하거나 유휴 타임아웃(기본 60분, 최대 24시간)에 맡깁니다.
- **두 가지 진입점:** SageMaker Unified Studio는 클러스터 연결·세션 생성을 대신 처리하고, 로컬 IDE는 CLI 절차에 중단점·단계 실행을 곁들입니다.

주요 제한: 로컬 PySpark 버전은 클러스터와 일치해야 하고, DataFrame·SQL API만 지원(RDD 불가)하며, 토큰은 1시간 만료, 다중 프라이머리 HA·Trusted Identity Propagation·Lake Formation 세밀 접근제어는 미지원입니다. EC2 인스턴스 외 추가 요금은 없습니다.

## References

- 원문: [Announcing Spark Connect on Amazon EMR on EC2: Interactive PySpark anywhere](https://aws.amazon.com/blogs/big-data/announcing-spark-connect-on-amazon-emr-on-ec2-interactive-pyspark-anywhere)
