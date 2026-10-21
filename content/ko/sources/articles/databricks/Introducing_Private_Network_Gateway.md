---
title: "프라이빗 네트워크 게이트웨이 소개"
description: "Databricks 프라이빗 네트워크 게이트웨이(PNG)가 단일 관리형 게이트웨이로 서버리스 네트워킹 단순화—한 번 구성하면 기존 라우트, DNS, 방화벽 규칙이 서버리스 워크로드 도달 범위 제어. Azure 퍼블릭 프리뷰, AWS 프라이빗 프리뷰."
tags: [source, databricks, private-network-gateway, serverless, networking, security, ko, ko]
locale: ko
source_url: "https://www.databricks.com/blog/introducing-private-network-gateway"
blog: databricks
published: "2026-10-14"
---

# 프라이빗 네트워크 게이트웨이 소개

**Source**: Databricks Blog, 2026-10-14

**핵심**: Databricks 프라이빗 네트워크 게이트웨이(PNG)가 리소스별 프라이빗 엔드포인트, 로드 밸런서, 프록시 VM을 단일 관리형 게이트웨이로 대체. 서브넷 위임 한 번 구성으로 서버리스 워크로드가 네트워크가 이미 도달하는 모든 것(데이터베이스, Kafka 클러스터, 내부 API, 온프레미스 시스템)에 접근 가능—기존 라우트, DNS, 방화벽 규칙 사용.

## 서버리스 네트워킹 과제

Databricks 서버리스 컴퓨트는 Databricks 관리 네트워크에서 실행돼 운영 오버헤드 제거하지만 프라이빗 리소스에 명시적 경로 필요. 클라우드 관리 서비스(S3, ADLS)엔 Serverless Private Link가 작동. 하지만 **자체 호스팅 리소스**(데이터베이스, Kafka, 내부 API)엔 리소스별 접근이 의미:
- 리소스별 별도 프라이빗 엔드포인트 + 로드 밸런서 + 프록시 VM
- Databricks 관리자, 클라우드 관리자, 네트워크 보안 팀 간 조정
- VNet, 피어드 네트워크, 온프레미스 전반에서 수십 개 리소스 접근 시 병목

> 고객 75%가 네트워크 구성 복잡성이 워크로드가 클래식 컴퓨트에 머무는 주된 이유라고 답함.

## PNG 작동 방식

**설정**: 내 VNet/VPC의 서브넷 하나를 Databricks에 위임. PNG가 해당 서브넷으로 서버리스에서 관리형 암호화 게이트웨이 구축. Network Connectivity Configuration(NCC) 내부에서 구성—서버리스 네트워킹에 이미 쓰이는 계정 수준 객체.

**배포, 패치, 스케일할 게이트웨이 VM 없음**—Databricks가 실행. 네트워크 제어권은 사용자 보유.

### 네트워크 경계 제어권 유지

- **전용 게이트웨이**: 내 전용 경로, 타 고객과 공유 안 함; 캡슐화와 보안 규칙으로 격리
- **워크스페이스 수준 접근 제어**가 게이트웨이 떠나기 전 적용
- **내 라우트 테이블, NSG, DNS, 보안 어플라이언스**가 서브넷 너머 도달 가능 범위 결정—나머지 네트워크와 동일

### 두 가지 트래픽 모드

1. **`specific_destinations`**: 나열된 FQDN만 PNG 경유; 다른 트래픽은 정상 경로 유지. 정밀 제어용.
2. **`all_traffic`**: 모든 아웃바운드가 내 네트워크 경유(더 구체적인 Private Link 경로 제외). 방화벽 검사나 일관된 소스 IP용.

PNG는 추가적—기존 프라이빗 연결/이그레스 제어와 나란히 위치, 기존 설정 영향 없이 활성화/제거 가능.

## 지원되는 유스케이스

- **서버리스에서 Lakeflow Connect**: VNet/VPC 및 온프레미스 전반의 프라이빗 데이터베이스에서 인제스트
- **AI 에이전트에서 프라이빗 서비스**: 직접 호스팅하는 프라이빗 MCP 서버 호출
- **프라이빗 패키지 저장소**: 네트워크 내부 프라이빗 PyPI, Artifactory, Nexus에서 설치
- **내 방화벽 통한 이그레스**: 자체 도구로 필터링/로깅
- **일관된 고객 소유 소스 IP**: SaaS 앱이 내 IP 확인

## 가용성

- **Azure 퍼블릭 프리뷰** — [Azure 문서](https://learn.microsoft.com/en-us/azure/databricks/security/network/serverless-network-security/private-network-gateway)
- **AWS 프라이빗 프리뷰** — Databricks 계정 팀에 문의
- **Google Cloud** — 개발 중

## 소프트웨어 엔지니어를 위한 시사점

**네트워킹 때문에 서버리스 컴퓨트 도입 막힌 팀에게**: PNG가 리소스별 네트워킹 세금 제거. 서브넷 위임 하나가 수십 개 조정된 배포 대체. 기존 네트워크 정책(라우트, DNS, 방화벽)이 서버리스 접근의 단일 진실 원천 됨—유지할 중복 규칙 세트 없음.

## 참고문헌

- 원문: [https://www.databricks.com/blog/introducing-private-network-gateway](https://www.databricks.com/blog/introducing-private-network-gateway)
- Databricks 플랫폼 보안 최신 소식: [Data+AI Summit 2026](https://www.databricks.com/blog/whats-new-databricks-platform-security-and-compliance-data-ai-summit-2026)