---
title: "CUDOS로 Amazon Redshift RA3에서 RG로의 현대화 평가하고 추적하기"
description: "CUDOS 5.10에 추가된 Amazon Redshift RA3→RG 섹션이 마이그레이션 절감액을 추정하고 인스턴스 세대 구성 변화를 추적하며 Graviton 기반 RG에서 이미 얻은 효율을 수치화한다."
tags: [source, aws-big-data, data-engineering, finops, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/assess-and-track-your-amazon-redshift-ra3-to-rg-modernization-with-cudos"
blog: aws-big-data
published_date: 2026-11-10
---

# CUDOS로 Amazon Redshift RA3에서 RG로의 현대화 평가하고 추적하기

**원문**: [Assess and track your Amazon Redshift RA3 to RG modernization with CUDOS](https://aws.amazon.com/blogs/big-data/assess-and-track-your-amazon-redshift-ra3-to-rg-modernization-with-cudos) · **게시일**: 2026-11-09

## 개요

2026년 5월 12일에 출시된 Graviton 기반 RG 인스턴스는 모든 Amazon Redshift RA3 고객에게 더 나은 가격 대비 성능으로 이전할 수 있는 경로를 제공한다. 데이터 웨어하우스 워크로드는 최대 2.2배, 데이터 레이크 워크로드는 최대 2.4배 빠르고, vCPU당 가격은 RA3보다 30% 낮으며, 기능은 완전히 동일하고 Redshift Spectrum의 TB당 스캔 요금도 사라진다. 수동 스냅샷 스토리지도 클러스터 스냅샷 간에 저장된 고유 데이터 블록을 기준으로 과금되어 비용이 낮아진다. 문제는 기술이 아니라 조직에 있다. 여러 계정과 팀에 걸쳐 측정 가능한 마이그레이션을 수행하려면 무엇을 절약할 수 있는지, 도입이 얼마나 진행됐는지, 이미 무엇을 얻었는지를 볼 수 있어야 한다.

이 글은 오픈소스 Cloud Intelligence Dashboards(CID) 프레임워크 안의 CUDOS(Cost and Usage Dashboard Operations Solution)가 이 세 가지 질문에 어떻게 답하는지 보여준다. CID 대시보드는 전부 AWS Cost and Usage Report 데이터로 만들어지며, CUDOS는 그중 세밀하고 권장 사항 중심인 구성원이다. Quick Sight SPICE 데이터셋 위에서 경영진 요약과 리소스 수준의 상세 분석을 함께 제공하고, Executive summaries와 Compute, Databases, Storage, AI/ML, Analytics, Security, Data Transfer 등의 탭으로 비용과 사용량을 정리한다. 지출 추이, 유휴 리소스 낭비, Reserved Instance와 Savings Plans 약정 추적, 태그와 계정 매핑으로 그룹화하는 Taxonomy Explorer도 포함한다.

버전 5.10에는 Amazon Redshift RA3→RG 전용 섹션이 추가되었고, 이는 "무엇을 절약할 수 있는가", "마이그레이션은 어떻게 진행되고 있는가", "이미 무엇을 얻었는가"라는 세 질문을 중심으로 구성된다.

## 핵심 내용

- 지난 30일 기준 "Monthly Cost Savings Opportunities with Migration to Redshift RG"라는 대표 KPI가 이전 대상 RA3 리소스가 RG로 옮겨 갈 때 절약할 수 있는 월 예상 절감액 합계를 보여 주고, 함께 제공되는 리소스 수준 표가 이를 계정, 클러스터, 구매 유형, 라인 아이템 계층으로 펼쳐 준다.
- 추정치는 Current Cost on RA3, Estimated Cost on RG, Estimated Savings on RG 세 컬럼으로 구성되며 합계 행이 KPI와 연결된다. 정가 기준 추정이므로 실제 절감액은 달라질 수 있고 성능, 데이터 전송 등 사용량별 요인은 제외된다.
- 도입 현황은 인스턴스 세대별 비용 비중을 월 단위로 보여 주는 100% 누적 막대 차트로 추적한다. 마이그레이션이 진행되면 RA3에서 RG로 구성이 옮겨 가는 모습을 경영진이 한눈에 볼 수 있다.
- 이미 얻은 효과는 별도 차트로 측정한다. RA3→RG 마이그레이션 모범 사례 글의 4xlarge 노드 감소 비율을 적용해 RG에서 실제로 달성한 월별 효율 향상을 막대 차트로 보여 주므로, 앞으로의 기회가 아니라 마이그레이션의 성과를 수치로 제시한다.
- 두 가지 인플레이스 필터로 추정치를 환경에 맞춘다. Purchase Option 메뉴에서 온디맨드 또는 예약 가격을 모델링할 수 있고(예약은 참고용이며, 노드 유형을 바꿔도 기존 예약이 자동으로 옮겨 가지 않으므로 Billing Support나 계정 팀에 문의해야 한다), Incremental Snapshot Size 슬라이더로 수동 스냅샷 사이에 변경되는 데이터 비율을 조정해 스냅샷 비용 부분을 정교하게 만든다.

## 상세

배포는 AWS CloudFormation 또는 CID Terraform 모듈로 수행하며, AWS는 관리 계정이나 결제 계정과 분리된 전용 데이터 수집 계정을 권장한다. 첫 단계는 데이터 수집 계정에 CUR 대상 위치를 만드는 것으로, AWS Data Exports가 쓸 수 있도록 정책을 설정한 S3 버킷과 AWS Glue, Amazon Athena 테이블을 만들고 대상 계정 ID와 소스 계정 ID를 지정하며 5~15분이 걸린다. 두 번째 단계는 각 소스 계정에서 그 대상을 가리키는 CUR 2.0을 생성하는 스택을 실행하는 것이며 계정당 약 5분이 걸린다. 다만 첫 Data Exports 전송은 보통 24시간, 최대 72시간이 걸리고, Billing 지원 케이스로 최대 14개월의 과거 데이터를 채울 수 있다. 세 번째 단계는 데이터 수집 계정에 대시보드를 배포하는 것으로, Amazon Quick Sight 가입과 리전 선택, 약 40GB의 SPICE 용량 확보가 필요하며 CUDOS와 선택적으로 Cost Intelligence, KPI 대시보드를 고를 수 있다.

자동화를 쓰면 직접 작업 시간은 대략 15~30분이지만 첫 CUR 리프레시가 나타나기까지는 최대 24시간이 걸릴 수 있다. 모든 스택은 리전 간 데이터 전송 요금을 피하기 위해 같은 리전에 배포해야 하며, 이미 CUDOS를 사용 중이라면 Update Dashboards 가이드에 따라 5.10으로 업데이트할 수 있다.

## 참고 자료

- 원문: [Assess and track your Amazon Redshift RA3 to RG modernization with CUDOS](https://aws.amazon.com/blogs/big-data/assess-and-track-your-amazon-redshift-ra3-to-rg-modernization-with-cudos)
