---
title: "Veeva가 Amazon EMR on EKS로 빅데이터를 확장한 방법"
description: "Veeva Compass는 페타바이트급 Spark 배치 처리를 EMR on EC2에서 Karpenter 기반 EMR on EKS로 옮겨 스큐 조인 단계를 7시간에서 55분으로 줄이고, 4계층 관측가능성·IRSA 멀티테넌트 격리·Lake Formation/OpenLineage 감사를 갖췄다."
tags: [source, article, aws-big-data, emr, spark, life-sciences, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/how-veeva-scaled-big-data-with-amazon-emr-on-eks"
blog: aws-big-data
published_date: 2026-11-19
---

# Veeva가 Amazon EMR on EKS로 빅데이터를 확장한 방법

**Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/how-veeva-scaled-big-data-with-amazon-emr-on-eks)
**게시일**: 2026-11-18

## 개요

글로벌 생명과학 산업을 위한 클라우드 소프트웨어 선도 기업 Veeva Systems는 Veeva Compass와 Compass Data Network를 운영하며, 처방·원내 시술·진단 데이터를 통합해 바이오파마 고객용 데이터 제품으로 제공한다. 원래 하루 수백 테라바이트를 처리하도록 설계된 분석 레이크는 고객 확대와 데이터 소스·제품 증가로 기하급수적으로 커졌다. 배치 작업의 변동성이 커지면서 Spark 셔플 단계에서 메모리가 부족해진 실행기가 디스크로 스필했고, 작업 시간이 몇 시간씩 늘어났다. Veeva는 Amazon EMR on EC2 아키텍처를 재검토하고 Karpenter 기반 Amazon EMR on EKS로 마이그레이션했다.

## 주요 내용

- 배경: 2025년 미국 신규 의약품 승인의 절반이 희귀질환(환자 20만 명 미만)을 대상으로 하는 '오펀' 치료제였고, 이는 희귀·복합 질환 치료제를 위한 확장 가능한 분석 인프라 수요를 키웠다.
- Compass는 공급사에서 고객까지 몇 시간 만에 데이터를 전달하고 분석·AI 워크플로를 가속화하며, 신규 환자·의료진(HCP) 이벤트를 더 일찍 감지해 영업 담당자가 적절한 시점에 더 정확한 정보로 관여할 수 있게 한다.
- Spark 튜닝: 파티셔닝, 지속적 컴팩션, Adaptive Query Execution(AQE) 튜닝으로 스큐 조인 단계를 7시간에서 55분으로 줄였다. 룩업 테이블을 메모리에 캐시해(반복 S3 읽기 방지) 동일 테이블을 여러 번 참조하는 작업의 런타임을 20–30% 단축했다.
- 관측가능성은 4계층: (1) S3 기반 이벤트 로그를 쓰는 EKS 위의 Spark History Server(실행 그래프 리플레이, 스테이지별 지표); (2) Prometheus+Grafana 실시간 지표(실행기 CPU/메모리, pending-pod 큐 깊이, shuffle-spill 비율, Karpenter 프로비저닝 지연); (3) CloudWatch Logs Insights로 드라이버/실행기 로그를 집계하고 자동 알림; (4) OpenTelemetry 트레이스로 Spark 작업을 Airflow/Step Functions 오케스트레이션과 연결.
- 핵심 알림: pending pod 임계값 초과(용량 제약), shuffle-spill 비율 급증(메모리 압박), 과도한 repartitioning(데이터 스큐).
- 보안: IRSA로 각 Spark 작업에 특정 S3 프리픽스와 Lake Formation 권한으로 제한된 임시 자격 증명 부여(브론즈/실버 읽기, 지정된 출력 경로에만 쓰기); taints/tolerations를 적용한 Kubernetes 네임스페이스로 팀 격리; 저장 시 KMS, 전송 시 TLS, S3는 고객 관리 키, Spark 내장 셔플 암호화; Lake Formation + OpenLineage로 리니지와 감사.
- EMR on EC2에서 EMR on EKS + Karpenter로의 마이그레이션은 핵심 지표 전반에서 측정 가능한 개선을 냈다(전체 bronze→silver 표는 원문 참조).

## 상세

- Veeva Compass는 처방·시술·진단을 통합하며, Compass Data Network는 전통적 환자 데이터 제품의 공백을 메우기 위해 폐쇄형·개방형 데이터 파트너를 계속 추가하고 있다.
- 기존 EMR on EC2 설계는 변동이 큰 배치 물량에 취약했다. 메모리가 부족한 실행기가 셔플 데이터를 디스크로 스필하면서 작업당 몇 시간이 추가되었다.
- Karpenter 기반 EMR on EKS는 작업 변동성에 맞는 탄력적 컴퓨팅을 제공해 데이터 볼륨이 계속 증가하는 동안에도 실행 지연을 피했다.
- 주목할 세부: 메모리에 캐시된 룩업, AQE를 통한 스큐 조인 개선, SLA 기반 알림에 연결된 4계층 관측가능성 스택.
