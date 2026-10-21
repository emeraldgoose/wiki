---
title: "EKS의 Amazon EMR에서 Spark Connect 발표: 어디서든 대화형 PySpark 개발"
description: "기존 EKS 클러스터에서 Spark를 대규모로 실행하면서 로컬 IDE·노트북에서 PySpark를 개발·디버깅합니다."
tags: [source, aws-big-data, spark, emr, kubernetes, ko, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/announcing-spark-connect-on-amazon-emr-on-eks"
blog: aws-big-data
published_date: 2026-09-29
---

# EKS의 Amazon EMR에서 Spark Connect 발표: 어디서든 대화형 PySpark 개발

## 개요

EKS의 Amazon EMR에서 Spark Connect를 지원합니다(EMR 7.14/Spark 3.5.8 및 emr-spark-8.1/Spark 4.1.1부터). VS Code, PyCharm, Jupyter, SageMaker Unified Studio에서 Spark를 만들고 테스트·디버깅하면서, 전체 규모 연산은 EKS에서 실행됩니다. 클라이언트-서버 분리로 로컬과 클러스터의 환경 차이가 사라지며, 대화형으로 검증한 코드가 그대로 배치 `StartJobRun`으로 배포됩니다.

## 동작 방식

네 가지 구성 요소로 동작합니다: 가벼운 PySpark 클라이언트(Spark 설치 불필요), EMR 관리 엔드포인트로의 보안 gRPC/TLS 채널, EMR-on-EKS 네임스페이스의 서버 파드(최소 2개 익스큐터, 오토스케일링), Arrow 인코딩 결과 스트리밍입니다. 엔드포인트를 만들면 EMR이 서버를 띄우고 ELB 기반 엔드포인트와 단기 토큰을 반환하므로 서버·네트워크를 직접 구성할 필요가 없고, 서버가 기존 클러스터의 노드 타입·컨테이너 이미지·Spark 설정을 물려받습니다.

클러스터에서 처음 사용하면 공유 컴포넌트 두 가지가 자동 프로비저닝됩니다: TLS 종료·토큰 검증을 맡는 Envoy 인증 프록시 라우터(기본 3개 복제본, NLB 앞단)와 단기 세션 자격증명을 관리하는 Secret Agent 파드입니다. 둘 다 엔드포인트 간에 공유되고, 개별 엔드포인트 삭제 후에도 남아 있어 새 엔드포인트를 1분 내 시작할 수 있습니다.

## 활용 이유

- **공유 클러스터에서 대화형 개발:** 배치 잡과 같은 엔진에 셀 단위로 반복하면서 EKS RBAC, 네트워크 정책, 오토스케일링, 관측 스택(Prometheus, Grafana, Container Insights)을 재사용.
- **내장형 Spark:** 가벼운 클라이언트를 웹 서비스·대시보드·스크립트·백엔드 API에 내장, 무거운 연산은 EKS 담당.
- **거버넌스 있는 멀티테넌시:** 세션마다 자체 IAM 실행 역할과 비용 태그, 가상 클러스터의 네임스페이스 격리, 쿠버네티스 쿼터와 EKS 분할 비용 배분으로 부서별 정산.
- **재사용 이미지와 스케줄링:** 배치·대화형이 같은 커스텀 이미지를 쓰고, 파드 템플릿·동적 할당·Spot·GPU 풀로 배치·비용 조정.
- **멀티 클러스터·하이브리드:** 클라이언트는 엔드포인트 도달만 하면 되므로 계정·리전·온프레미스 쿠버네티스 간 분석이 단순화.

## 시작하기

EKS에 EMR 네임스페이스 생성, 보안 구성 생성, 세션 활성화 가상 클러스터 생성, SPARK_CONNECT 관리 엔드포인트 생성, 세션 토큰 발급, 원격 `SparkSession` 연결의 6단계입니다.

- **사전 조건:** AWS Load Balancer Controller가 설치된 EKS 클러스터, 최신 AWS CLI·boto3, 버전이 맞는 `pyspark[connect]` 클라이언트, 잡 실행 IAM 역할.
- **보안:** 토큰은 단기(기본 15분, 최대 12시간)이므로 장기 세션은 주기적으로 재발급.
- **세션 동작:** 유휴 타임아웃(기본 60분) 동안 엔드포인트가 클라이언트 연결과 독립적으로 유지되어 캐시·임시 뷰가 보존되며, 새 토큰으로 재연결해 이어서 작업.
- **검증:** EMR Containers API로 상태 확인, `kubectl`로 드라이버·익스큐터 파드 점검, 드라이버 포트포워딩으로 실시간 Spark UI 확인.
- **정리:** 엔드포인트·가상 클러스터·보안 구성·네임스페이스 삭제, 공유 라우터와 Secret Agent는 마지막 세션 활성화 가상 클러스터 삭제 시 자동 제거.

GovCloud·중국을 제외한 모든 EMR-on-EKS 리전에서 EKS 리소스 외 추가 요금 없이 제공됩니다. Karpenter 오토스케일링, 영속 세션 파드의 온디맨드, Graviton, 비용 배분 태그, 단일 공유 라우터로 비용을 최적화합니다.

## References

- 원문: [Announcing Spark Connect on Amazon EMR on EKS: Interactive PySpark development, anywhere](https://aws.amazon.com/blogs/big-data/announcing-spark-connect-on-amazon-emr-on-eks)
