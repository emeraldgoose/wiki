---
title: "AI 기반 Migration Assistant로 Apache Solr를 Amazon OpenSearch Service로 마이그레이션하기"
description: "Amazon EKS 위의 AI 기반 Migration Assistant for Amazon OpenSearch Service로 Solr 9.6 → Amazon OpenSearch Serverless를 평가(assess)→백필(Reindex-from-Snapshot)→검증까지 엔드투엔드로 이전한 600K 문서 데모."
tags: [source, aws-big-data, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/migrate-apache-solr-to-amazon-opensearch-service-with-the-ai-driven-migration-assistant"
blog: aws-big-data
published_date: "2026-11-19"
---

# AI 기반 Migration Assistant로 Apache Solr를 Amazon OpenSearch Service로 마이그레이션하기

**출처**: [aws-big-data](https://aws.amazon.com/blogs/big-data/migrate-apache-solr-to-amazon-opensearch-service-with-the-ai-driven-migration-assistant) · **게시일**: 2026-11-16

## 개요

수년간 Apache Solr를 운영해 온 조직은 ZooKeeper 쿼럼, JVM 패치, GC 튜닝, 커스텀 플러그인 같은 차별화되지 않는 운영 부담에서 벗어나고 싶어 하지만, 정작 이전 자체가 발을 묶는다. Solr와 OpenSearch의 스키마가 다르고, 애플리케이션 코드는 Solr HTTP API에 맞춰져 있으며, 커스텀 분석기(analyzer)가 내장되어 있다. 이 글은 AWS Solutions Library의 Migration Assistant for Amazon OpenSearch Service를 Amazon EKS에서 실행하고, Migration Assistant CLI의 대화형 AI 에이전트 모드로 Solr→OpenSearch Serverless 마이그레이션을 처음부터 끝까지 수행한다. 워크스루는 Apache Solr 9.6 소스에 600,000건의 합성 제품 카탈로그를 사용하며, Elasticsearch 5.x+나 자체 관리 OpenSearch 소스에도 같은 흐름이 적용된다. 평가만 필요하다면 인프라를 프로비저닝하지 않고 AI 어드바이저만 단독으로 실행할 수 있으며, 에이전트 모드는 실행하는 각 명령을 먼저 보여 주고 자격 증명을 저장하지 않는다.

## 핵심 내용

- **세 단계**: (1) Assess — 소스 스키마와 쿼리 패턴을 인벤토리화하고, 권한·접근성을 확인하며, 데이터가 움직이기 전에 비호환성을 드러낸다. (2) Backfill — 소스를 S3에 스냅샷으로 저장한 뒤 Reindex-from-Snapshot(RFS)으로 대상에 스트리밍한다. (3) Validate — 문서 수, 매핑, 샘플 쿼리 결과, 소스-대상 간 리플레이 일관성을 비교한다.
- **아키텍처**: Amazon EKS 위의 Migration Assistant가 백필용 RFS 워커와 라이브 트래픽용 캡처 프록시를 실행한다. 워크플로 파드는 EKS Pod Identity로 스냅샷/캡처 S3 버킷과 대상 OpenSearch Serverless 컬렉션에만 한정된 역할을 assume한다(계정 전역 권한 아님). CloudFormation이 VPC, NAT 게이트웨이, EKS 클러스터, IAM 역할, ECR 리포지토리, S3 버킷을 만들므로 배포 주체에게 해당 리소스 생성 권한과 `iam:PassRole`이 필요하다.
- **설치**: 공식 Solutions 채널에서 한 줄 설치 — `curl -fsSL https://solutions-reference.s3.us-east-1.amazonaws.com/migration-assistant-for-amazon-opensearch-service/3.98.7/install.sh | bash` (3.98.7 고정; 더 안전한 경로는 먼저 스크립트를 내려받아 검토하는 것 — sudo 없이 실행되고 ~/.local/bin에 바이너리를 두며, 체크섬/서명을 게시하지 않으므로 HTTPS만이 보호 장치다). 소스는 GitHub의 aws-solutions/migration-assistant-for-amazon-opensearch-service에 있다. CLI v2, kubectl, Helm이 필요하고 에이전트 모드에는 지원되는 코딩 어시스턴트가 필요하다.
- **일상 언어의 에이전트 모드**: 목표를 설명하면 된다("Assess my Solr 9.6 cluster…" / "Migrate my Solr 8.11 cluster to OpenSearch Serverless"). 평가에서는 에이전트가 읽기 전용으로 연결하고, 배포에서는 인프라를 프로비저닝하며, 마이그레이션에서는 과거 데이터 백필과 선택적 라이브 트래픽 캡처/리플레이를 포함한 워크플로를 구성·실행한다. 데이터 취급 참고: 에이전트 모드는 Solr 스키마/solrconfig.xml, 샘플 쿼리, 소스·대상 엔드포인트를 서드파티 모델에 전송하므로, 데이터 취급 규칙이 있다면 코딩 어시스턴트가 무엇을 전송하는지 먼저 확인하라. `./migration-assistant-workspace/`(상태, 로그, 평가 보고서)는 자격 증명에 준하는 것으로 간주하고 보호하라.
- **계정 위생**: 전용 비프로덕션 계정 또는 IAM Identity Center의 단기 자격 증명으로 assume한 스코프된 배포 역할을 사용하고, 평가 대상은 비프로덕션 Solr/Elasticsearch/OpenSearch로 지정하라.
- **결과**: 600K 문서 Solr 카탈로그가 OpenSearch Serverless로 — 평가, 백필, 검증까지 — 이전되며, 대상에서는 ZooKeeper·JVM·커스텀 플러그인을 더 이상 유지할 필요가 없고 벡터 검색과 AWS 네이티브 연동을 얻는다.

## 세부 내용

평가 단계는 읽기 전용이다. 에이전트가 소스에 연결해 스키마를 분석하고 비호환성(필드 매핑, 분석기, 쿼리 패턴 차이)을 식별해 데이터가 이동하기 전에 마이그레이션 평가 보고서를 만든다. 프롬프트에 소스를 직접 전달한다(SolrCloud 엔드포인트 또는 ZooKeeper 연결 문자열, 컬렉션 이름, 인증 방식). 빠진 정보는 에이전트가 물어본다.

백필 단계는 소스를 S3로 스냅샷한 뒤 RFS로 Serverless 컬렉션에 스트리밍한다. 라이브 시스템이면 캡처 프록시가 트래픽을 기록해 리플레이 기반 검증에 쓴다. 검증 단계는 문서 수, 매핑, 샘플 쿼리 결과, 리플레이 일관성을 소스와 대상에서 비교한다 — 애플리케이션을 전환하기 전에 필요한 점검이다.

이 글은 Solr vs OpenSearch를 계획 수준에서 비교한 2024년 AWS Big Data Blog 글의 실행 편이며, 재현 가능한 결과를 위해 Migration Assistant 3.98.7을 고정했다(최신 릴리스로 대체). 대화형 모드는 자연어 기반이라 글에 나온 프롬프트·응답은 방향성이며, 버전과 환경에 따라 달라진다.

## 참고 자료

- 원문: [Migrate Apache Solr to Amazon OpenSearch Service with the AI-driven Migration Assistant](https://aws.amazon.com/blogs/big-data/migrate-apache-solr-to-amazon-opensearch-service-with-the-ai-driven-migration-assistant)
