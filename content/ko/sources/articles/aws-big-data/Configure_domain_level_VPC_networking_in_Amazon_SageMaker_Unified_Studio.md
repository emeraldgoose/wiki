---
title: "Amazon SageMaker Unified Studio에서 도메인 수준 VPC 네트워킹 구성"
description: "도메인에 VPC 하나를 설정해 모든 신규 프로젝트가 프라이빗 서브넷·엔드포인트·보안 상태를 자동 상속받게 합니다."
tags: [source, aws-big-data, sagemaker, vpc, networking, ko, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/configure-domain-level-vpc-networking-in-amazon-sagemaker-unified-studio"
blog: aws-big-data
published_date: 2026-09-23
---

# Amazon SageMaker Unified Studio에서 도메인 수준 VPC 네트워킹 구성

## 개요

수십 개 프로젝트를 운영하는 팀이 프로젝트마다 프라이빗 연결을 조율하면 서브넷 불일치, 누락된 엔드포인트, 디버깅 어려운 장애, 감사 불가 상태가 생깁니다. 도메인 수준 VPC 네트워킹은 네트워크를 한 번만 구성하면(IAM 기반 도메인 대상) 모든 신규 프로젝트가 VPC 설정을 자동 상속받습니다. 이 글은 설정법, 서브넷·보안 그룹 선택, 기존 프로젝트 이전, 프로젝트 내부에서의 연결 검증을 다룹니다.

## 사전 조건

도메인 관리자 권한과 동일 리전 VPC가 필요합니다. 서로 다른 AZ에 최소 2개의 프라이빗 서브넷, DNS 호스트명/지원 활성화, 예상 프로젝트당 약 5개의 여유 IP가 기준선입니다(Glue·EMR·Redshift Serverless는 ENI를 더 쓰므로 프로덕션은 /24 이상 권장). 서브넷이 프라이빗이므로 프로젝트가 쓰는 모든 서비스의 VPC 엔드포인트가 필요합니다. S3 게이트웨이 엔드포인트(라우트 테이블 연결 포함)와 Glue, SageMaker API/런타임, CloudWatch Logs/모니터링, STS, DataZone, ECR API/DKR, KMS 인터페이스 엔드포인트를 프라이빗 DNS와 함께 구성합니다. 관리자 역할에 EC2 조회/생성과 DataZone 권한이 필요하고, 보안 그룹은 생략하면 스튜디오가 자동 생성합니다. 인터페이스 엔드포인트 시간당 비용과 VPC당 엔드포인트·ENI 쿼터를 고려합니다.

## 따라하기

1. **이동:** 도메인 로그인 역할로 콘솔에 들어가 SageMaker 콘솔에서 IAM 기반 도메인을 열고 Domain management로 갑니다.
2. **VPC 추가:** Settings > Networking in this account에서 Add VPC를 눌러 VPC, 최소 2개 프라이빗 서브넷, 선택적으로 보안 그룹을 고르고 저장한 뒤 Ready 상태를 확인합니다. IAM 기반 도메인은 VPC 구성을 하나만 허용하며, 이후 신규 프로젝트가 이를 상속합니다.
3. **기존 프로젝트 업데이트:** VPC가 없는 프로젝트는 업데이트 배너에서 제자리 적용이 가능합니다. 이미 VPC가 있는 프로젝트는 전환이 안 되므로 새 프로젝트 생성 → 연결 재생성 → 자산 이전 → 데이터 백업 → 기존 프로젝트 삭제 순으로 유지보수 시간에 진행합니다.
4. **검증:** 프로젝트 노트북에서 Boto3로 S3·Glue·STS 도달성을 테스트하고 인터페이스 엔드포인트가 프라이빗 IP로 해석되는지 확인합니다. `AccessDenied`는 연결은 되지만 IAM 수정이 필요하다는 뜻이고, 타임아웃은 엔드포인트·라우트·보안 그룹 문제입니다(아웃바운드 443 허용, 분산 컴퓨트용 자기참조 인바운드 규칙 추가).

## 구성 변경과 제거

나중에 VPC·서브넷·보안 그룹을 바꾸려면 같은 Settings에서 Actions > Update를 쓰되, 새로 만드는 리소스에만 적용됩니다. VPC가 이미 적용된 기존 프로젝트는 재생성해야 하고, VPC 없는 프로젝트는 제자리 업데이트가 됩니다. 구성 제거(Actions > Remove)는 이미 프로비저닝된 프로젝트에 영향을 주지 않으며, 이후 신규 프로젝트는 VPC 없이 생성됩니다. 다음 단계로 자동 생성된 보안 그룹을 최소 권한으로 조이고, 필요에 따라 엔드포인트를 추가하며, 서브넷 `AvailableIpAddressCount` 알람으로 용량을 계획합니다.

## References

- 원문: [Configure domain-level VPC networking in Amazon SageMaker Unified Studio](https://aws.amazon.com/blogs/big-data/configure-domain-level-vpc-networking-in-amazon-sagemaker-unified-studio)
