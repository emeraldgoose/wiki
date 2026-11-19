---
title: "새로운 Azure Databricks on Azure Government 베타 출시"
description: "Azure Databricks on Azure Government가 베타에 진입했다. Unity Catalog, Databricks SQL, 클래식 및 서버리스 컴퓨트, 기본 Compliance Security Profile, Private Link, US Gov Virginia/Arizona 데이터 상주를 제공하며 FedRAMP Class D와 DoW IL5 인증(2027년 초 예상)을 추진 중이다."
tags: [source, article, databricks, azure-government, fedramp, il5, ko]
locale: ko
source_url: "https://www.databricks.com/blog/new-azure-databricks-azure-government-now-beta"
blog: databricks
published_date: 2026-11-19
---

# 새로운 Azure Databricks on Azure Government 베타 출시

**Source**: [Databricks Blog](https://www.databricks.com/blog/new-azure-databricks-azure-government-now-beta)
**게시일**: 2026-11-18

## 개요

Azure Databricks on Azure Government가 베타에 진입했다 — 미국 공공부문에 Databricks Data + AI Platform 전체를 제공하는 이정표다. 정부 기관과 파트너는 상용 환경에서 표준이 된 현대적 데이터 기반(Unity Catalog, Databricks SQL, 서버리스 컴퓨트)을 지금 사용할 수 있고, 전체 AI 제품군이 뒤따를 예정이며, FedRAMP Class D(구 High)와 DoW IL5 인증을 추진 중인 환경에서 제공된다. 퍼스트파티 Azure 서비스로서 Azure 포털에서 관리되고, Microsoft Entra ID와 네이티브로 통합되며, 기존 Azure 약정에 포함된다.

## 주요 내용

- 두 가지 경로: FedRAMP Class D에 맞는 워크로드를 가진 연방 민간기관·주/지방정부·파트너는 Azure Commercial을 오늘 바로 쓸 수 있다(FedRAMP Class D 오퍼링은 최근 출시). 전용 정부 클라우드와 FedRAMP Class D·DoW IL5로 가는 경로가 필요한 조직은 새 Azure Government 환경을 지금 베타로 쓸 수 있다.
- 레거시 환경과 달리 새 환경은 상용 Azure Databricks와 동일한 아키텍처로 동작하며, 모든 상용 기능이 동일한 지속적 릴리스를 통해 Azure Government에 제공되도록 설계됐다. 베타는 그 경로의 첫 릴리스다.
- 베타에서 제공: Unity Catalog(모든 데이터·AI 자산의 접근 관리·리니지·감사 — 한 번 정의한 정책을 어디에나 적용); 빠르고 고동시성인 분석을 위한 Databricks SQL(클래식 클러스터 또는 서버리스 컴퓨트); 모든 워크스페이스에 기본 활성화된 Compliance Security Profile(강화된 모니터링, 자동 클러스터 업데이트, 하드닝된 컴퓨트 이미지, 노드 간 트래픽 암호화); 프런트엔드와 백엔드 모두에 필수인 Azure Private Link(모든 트래픽이 Azure 백본에 유지); 관리자용 System tables(감사 로그·빌링·컴퓨트·파이프라인·ML 실험·쿼리 이력·스토리지의 단일 쿼리 뷰); 데이터는 US Gov Virginia와 US Gov Arizona에서만 저장·처리.
- AI 로드맵(Unity Catalog 거버넌스): Genie를 통한 대화형 분석; AI 지원 개발(코드 작성·설명·디버깅); Agent Bricks를 통한 프로덕션급 에이전트(자체 문서/데이터 위에서 에이전트 구축·평가·배포, 내장 품질 평가); Model Serving과 Foundation Model APIs; RAG 앱과 SQL 네이티브 분류/추출/요약을 위한 Vector Search와 AI Functions; 보안 애플리케이션과 운영 워크로드를 위한 Databricks Apps와 Lakebase.
- 인증: FedRAMP Class D와 DoW IL5를 적극 추진 중이며 2027년 초 예상. 인증되면 기관과 방산 파트너는 CUI 및 IL5 미션 크리티컬 워크로드(Azure Commercial에서 미지원)를 실행할 수 있다. 진행 상황은 FedRAMP Marketplace에서 확인 가능.
- 시작하기: Azure Databricks에 사용된 적 없는 전용 Azure Government 서브스크립션으로 옵트인; Azure 포털에서 프리뷰 기능을 등록하면 해당 서브스크립션의 모든 새 워크스페이스가 새 환경에 생성된다. 베타는 비프로덕션 워크로드를 대상으로 하며, 워크스페이스는 GA(2027년 초 예상) 시 프로덕션으로 이어진다.
- 레거시에서 마이그레이션: 기존 워크스페이스·노트북·데이터·구성은 영향 없음; 병행 탐색 권장. 시작 권장 영역 네 가지: Unity Catalog(레거시 Azure Government 워크스페이스에는 없었음), 서버리스 컴퓨트(정부 환경 최초 — 지금 보안/컴플라이언스 검토 시작), 네트워크 암호화(Compliance Security Profile은 Azure Virtual Network 암호화를 지원하는 인스턴스 타입 필요 — 클러스터 구성과 Terraform/ARM 템플릿 갱신), ATO(지금 보안·인가 담당자와 작업 시작; 베타 동안 SSP와 데이터 흐름을 갱신해 두면 GA에서 CUI 프로덕션 워크로드를 실행할 위치에 선다).

## 상세

- 새 환경은 퍼스트파티 Azure 서비스다: Azure 포털 관리, 네이티브 Entra ID 통합, Azure 약정 포함.
- 로드맵 기능과 일정은 전망이며 변경될 수 있다.
- Databricks Federal 팀이 워크로드 평가와 이전 계획을 도울 수 있다. Databricks 담당자에게 문의하거나 Azure Databricks 문서를 참고.
