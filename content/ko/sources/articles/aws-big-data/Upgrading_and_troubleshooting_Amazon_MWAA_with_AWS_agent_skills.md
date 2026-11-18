---
title: "AWS 에이전트 스킬로 Amazon MWAA 업그레이드와 트러블슈팅하기"
description: "AWS가 Agent Toolkit for AWS의 aws-data-analytics 플러그인에 MWAA 에이전트 스킬 4종(작성·테스트·디버그·업그레이드)을 공개 — 2.11.x 징검다리 버전을 포함한 Airflow 2.x→3.x 업그레이드를 단계별 확인 기반으로 지원."
tags: [source, aws-big-data, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/upgrading-and-troubleshooting-amazon-mwaa-with-aws-agent-skills"
blog: aws-big-data
published_date: "2026-11-19"
---

# AWS 에이전트 스킬로 Amazon MWAA 업그레이드와 트러블슈팅하기

**출처**: [aws-big-data](https://aws.amazon.com/blogs/big-data/upgrading-and-troubleshooting-amazon-mwaa-with-aws-agent-skills) · **게시일**: 2026-11-16

## 개요

Amazon Managed Workflows for Apache Airflow(Amazon MWAA)는 관리형 Airflow 런타임의 프로비저닝과 업그레이드를 단순화하지만, 정작 어려운 부분은 DAG을 최신 상태로 유지하는 것이다. Airflow는 계속 진화하고 팀은 뒤처지며, 업그레이드는 코드를 깨뜨리고, 특히 2.x→3.x 점프는 breaking change, Python 전환, 필수 징검다리 버전을 동반한다. 기존 자동화는 오래된 Airflow 문법에 학습되었거나 버전 간 개념을 섞어 코드를 생성하기 쉽다. AWS는 오픈소스 Agent Toolkit for AWS에 MWAA 에이전트 스킬을 공개했다 — 코딩 어시스턴트(Kiro, Claude Code, Cursor, Codex 등)가 로드해 MWAA 업그레이드를 계획·실행·디버깅하도록 AWS가 작성한 지침 패키지다.

## 핵심 내용

- **`aws-data-analytics` 플러그인의 스킬 4종**: `authoring-mwaa-workflow`(프로비저닝 환경 Python DAG과 MWAA Serverless YAML 워크플로 작성·배포), `testing-mwaa-workflow`(배포된 DAG/워크플로 실행, 완료까지 모니터링, 수정 후 재테스트, 실패 시 디버깅·작성 스킬 호출), `debugging-mwaa-workflow`(실패한 실행·태스크, UI에 나타나지 않는 DAG, import 오류, 워커 메모리 부족, IAM 권한 오류의 근본 원인 분석), `upgrading-mwaa-environments`(프로비저닝 환경을 새 Airflow 버전으로 업그레이드 — 2.x→3.x도, 블루/그린 또는 인플레이스 전략; DAG 코드도 업데이트·테스트; 소스가 2.11.x보다 오래되면 2.x 최신 2.11.x를 경유하는 경로를 계획). 앞의 세 스킬은 MWAA Serverless도 지원한다.
- **동작 방식**: 스킬은 개방형 Agent Skills 표준을 따르며, 리소스에 AWS CLI 명령을 실행하고 AWS MCP Server(플러그인에 번들)를 통해 실행 시점에 최신 AWS 문서를 가져오고 샌드박스 실행·감사 로깅과 함께 CLI를 실행한다. 프롬프트에 따라 스킬이 자동 선택되므로 이름을 지정할 필요가 없다.
- **에이전트는 제안만이 아니라 변경을 수행한다**: 작업에 따라 DAG 파일을 편집·배포할 수 있다. 먼저 개발 환경에서 시도하고, DAG은 버전 관리에 두고, 제안된 각 변경을 검증하라.
- **전제 조건**: 기존 MWAA 프로비저닝 환경이 있는 AWS 계정(워크스루는 Airflow 2.11.x에서 시작), Agent Skills 호환 어시스턴트, `airflow`(프로비저닝 + REST API)와 `airflow-serverless`(Serverless 워크플로/실행) 액션 네임스페이스에 스코프된 IAM 권한, 조사 단계용 최소 권한 자격 증명(쓰기 권한은 확정된 변경 단계에만).
- **설치**: 옵션 A(Claude Code/Codex) — 먼저 마켓플레이스를 업데이트(`/plugin marketplace update claude-plugins-official`)한 뒤 `/plugin install aws-data-analytics@claude-plugins-official`를 실행한다(업데이트 없이 설치하면 "Plugin not found" 오류가 날 수 있고, Anthropic 디렉터리에는 더 오래된 버전이 등록되어 있을 수 있다). 옵션 B(Kiro) — `~/.kiro/settings/mcp.json`에 AWS MCP Server를 추가하고(AWS_REGION을 환경 리전으로 설정) `npx skills add aws/agent-toolkit-for-aws/skills`를 실행하거나, 자동 감지는 `aws configure agent-toolkit`로 수행한다.
- **워크스루 1 — 2.x→3.x 업그레이드(단계별 확인)**: 스킬이 순서가 지정된 버전 경로를 계산하고(2.x→3.x 경계를 넘으면 2.11.x 징검다리와 Python 전환 단계를 삽입), 실행 이력과 동일한 환경 URL/ARN 유지 여부에 따라 전략을 고른다(신규 환경 블루/그린, 테스트 사본으로 검증하는 계획된 인플레이스, 직접 인플레이스). 3.x 전환 시 Ruff 스캔, deprecation 경고 로그 스캔, Docker 검증으로 DAG을 점검하고, 배포·전환하며 중단 가능한 다중 세션 계획을 저장한다. 환경 생성·버전 변경·현재 환경 수정은 각 단계별 확인 없이 수행하지 않고, 각 버전 점프도 개별 확인한다.
- **워크스루 2 — 실패한 DAG**: 디버깅 스킬이 흔한 MWAA 실패 모드를 따라 근본 원인을 찾고, 이후 수동으로 수정하거나 작성 스킬에 DAG 업데이트를 요청하고, 테스트 스킬로 재실행한다.
- **샘플 프롬프트**: "Airflow 2.7.2에서 최신 3.x로 envname을 업그레이드하세요. 실행 이력은 필요하지 않습니다." · "Airflow 2.10.3에서 2.11.x로 envname을 업그레이드하세요. 실행 이력과 동일한 URL을 유지해야 합니다. DAG 개수가 많습니다." · "2.11.0에서 3.2.1로 인플레이스 방식으로 envname을 업그레이드하세요. 테스트 사본은 건너뛰세요. 일부 DAG는 airflow.datasets를 임포트하고 하나는 BashOperator에서 'airflow db clean'을 실행합니다."

## 세부 내용

고통의 핵심은 업그레이드 사이클이다 — 2.x→3.x 직접 점프 대신 2.11.x 다리를 이용한 점진적 업그레이드로 깨짐-수정 루프를 벗어나라. 스킬은 일반 자동화가 실패하는 지점, 즉 Airflow/MWAA의 최신 동작에 어시스턴트를 동기화한다. 예시 세션: "What AWS Regions are available?"로 MCP 연결을 확인하고 "What can MWAA Skills help me with?"로 스킬 인식을 확인한 뒤 위 샘플 프롬프트로 업그레이드를 진행한다. 워크스루에서 스킬은 구조화된 계획을 내보내고 모든 변경 단계를 확인 게이트 뒤에 둔다. 저장된 계획 덕분에 다중 세션 업그레이드를 중단했다가 재개할 수 있다.

네 스킬 모두 프로비저닝 환경을 지원하고, 작성·테스트·디버깅 스킬은 MWAA Serverless(YAML 워크플로)도 지원한다. 어시스턴트별 설정은 Agent Toolkit for AWS User Guide의 Getting started와 Amazon MWAA User Guide의 Using agent skills in MWAA를 따르라.

## 참고 자료

- 원문: [Upgrading and troubleshooting Amazon MWAA with AWS agent skills](https://aws.amazon.com/blogs/big-data/upgrading-and-troubleshooting-amazon-mwaa-with-aws-agent-skills)
