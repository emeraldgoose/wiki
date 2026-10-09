---
title: 사일로에서 인사이트로 - AI 에이전트를 위한 연합 데이터 접근 패턴
description: "MCP와 Bedrock AgentCore를 통한 AI 에이전트 연합 데이터 접근: 카탈로그 우선(Glue + Athena), 직접 접근(Aurora MySQL), 하이브리드 패턴과 게이트웨이 라우팅 및 거버넌스."
date: 2026-09-04
tags: [aws, ai-agents, mcp, bedrock-agentcore, athena, glue, aurora, data-governance]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/from-silos-to-insights-federated-data-access-patterns-for-ai-agents/"
blog: aws
---

# 사일로에서 인사이트로 - AI 에이전트를 위한 연합 데이터 접근 패턴

**저자**: James Wu · **발행**: 2026년 9월 4일 · **출처**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/from-silos-to-insights-federated-data-access-patterns-for-ai-agents/)

## 문제

기업 데이터는 접근 방식이 서로 다른 시스템에 분산되어 있다: S3의 배치 데이터는 Athena·Trino 같은 엔진이, Kinesis의 실시간 �елем트리는 스트리밍 전문 지식이, OLTP/CRM 레코드는 관계형 DB에 대한 SQL이 필요하고, 각 SaaS 앱은 고유한 API와 인증 모델을 갖는다. 이를 모두 다룰 수 있는 데이터 엔지니어는 소수뿐이라, 시스템을 넘나드는 일회성 질문("지난 분기 구독자 성장을 견인한 타이틀은?", "마케팅 지출과 완주율이 상관있는가?", "신규 콘텐츠를 안 보는 사용자의 이탈이 급증하는가?")은 매번 티켓 대기열에 쌓인다. 중앙 데이터 레이크나 데이터 메시 같은 전통적 해법은 큰 엔지니어링 투자와 지속적인 유지보수를 요구하고, 대시보드는 어제의 질문에만 답한다.

## 해결책: MCP + Bedrock AgentCore를 통한 연합 접근

모든 데이터를 한곳으로 옮기는 대신, AI 에이전트가 데이터가 있는 시스템에 직접 대화하게 한다. Model Context Protocol(MCP)은 도구 탐색·호출·응답 처리를 표준화하므로, 자연어 앞단의 Strands 에이전트가 API·인증·쿼리 언어를 사용자가 몰라도 올바른 저장소에 도달한다.

참조 아키텍처(스트리밍 미디어 예시, 합성 데이터, 코드 `aws-samples/sample-aws-semantic-data-access-ai-agents`):

- **생성형 AI 계층** — **Amazon Bedrock AgentCore Runtime** 위의 Strands 에이전트(LLM: Bedrock 경유 Claude Haiku 4.5), 의도 기반 라우팅 규칙 + 필수 스키마 탐색 워크플로를 담은 시스템 프롬프트. **AgentCore Gateway**가 모든 MCP 서버를 단일 엔드포인트 뒤에 묶어 도구 탐색(시맨틱 검색 포함)·인증·라우팅 담당.
- **컴퓨트/MCP 계층** — AgentCore Runtime에서 Gateway 뒤에 동작하는 3개 MCP 서버: (1) **데이터 처리 MCP 서버**(Glue Data Catalog 메타데이터 + Athena 쿼리 실행 래핑, `manage_aws_glue_tables` 도구), (2) **Aurora MCP 서버**(RDS Data API로 Aurora MySQL에 대한 SQL로 변환, Secrets Manager 인증, `run_query` + `get_table_schema` 2개 도구만 노출), (3) **AWS 문서 MCP 서버**(서비스 컨텍스트 제공).
- **데이터/거버넌스 계층** — 배치 데이터셋(고객 프로필, 콘텐츠 타이틀, 광고 캠페인)은 **EventBridge 스케줄의 Lambda**가 Parquet으로 S3에 생성, 스트리밍 시청 텔레메트리(시청·일시정지·이탈)는 **Kinesis Data Streams → Data Firehose → S3**, CRM 레코드(요금제, 지원 티켓, 계정 상태)는 **Aurora MySQL**에 저장. **Glue Data Catalog**가 S3 메타데이터(스키마, 비즈니스 컨텍스트, 품질, 리니지) 통합, **Lake Formation**이 세밀한 접근 정책 집행. 프론트엔드: **S3 + CloudFront**의 React 앱, **Cognito** 인증(신원 토큰이 요청과 함께 에이전트 계층까지 전달).
- **세 가지 패턴**(거버넌스↔유연성 스펙트럼): **패턴 1 카탈로그 우선**(Glue + Athena 경유의 거버넌스된 S3), **패턴 2 직접 접근**(카탈로그 없이 Aurora 전용 MCP 서버), **패턴 3 하이브리드**(하나의 오케스트레이터 뒤에 둘을 결합 — 현실의 권장 형태).

## 구현

1. **사전 준비**: Bedrock AgentCore 접근 권한이 있는 AWS 계정(AgentCore Runtime 권한 문서 참조), AWS CLI 설정, Python 3.10+, Docker 또는 Finch. 샘플 저장소 README 순서대로 배포(데이터 CDK 스택 후 에이전트 스택, 정리 시 에이전트 스택부터 삭제하고 고아 Kinesis 스트림/CloudWatch 로그 그룹 제거).
2. **패턴 1 — 카탈로그 우선(예: "2026년 2월 스트리밍 이벤트를 유형별로 집계")**: (a) 라우팅 규칙이 "스트리밍 이벤트"를 Glue/Athena 경로에 매칭(보조로 Gateway 시맨틱 검색), (b) 에이전트가 `manage_aws_glue_tables`로 스키마·타입·파티션 키(`year, month, day, hour`)·저장 포맷 조회, (c) 파티션 필터가 포함된 Presto/Trino SQL 작성(`WHERE year='2026' AND month='02'`) 후 Athena 실행, (d) 신규 테이블·컬럼은 라우팅 로직 변경 없이 카탈로그를 통해 즉시 노출. 트레이드오프(Databricks Unity Catalog MCP 서버도 동일): 모든 데이터를 먼저 카탈로그에 등록해야 해서 빠르게 변하는 환경에서는 병목 가능.
3. **패턴 2 — 직접 접근(예: "긴급 미해결 지원 티켓을 카테고리별로")**: 에이전트가 "지원 티켓"을 MySQL 경로에 매칭해 `run_query`로 `SELECT ... WHERE status='open' AND priority='critical'` 호출, MCP 서버가 RDS Data API로 Aurora에 실행 후 Gateway 경유 반환. 시스템 프롬프트에는 테이블명·주요 enum 값 같은 경량 힌트만 유지하고, 조인·낯선 컬럼은 먼저 `get_table_schema` 호출. 카탈로그 등록 단계가 없어 Aurora 스키마 변경이 즉시 반영되며, 안정적이고 잘 알려진 운영 테이블에 적합. 범용 대안: 정식 출시된 **AWS MCP Server**(Agent Toolkit for AWS)의 `aws___run_script`(샌드박스 Python, SigV4, IAM 범위 인증)로 RDS Data API 경유 Aurora나 `GetShardIterator`/`GetRecords` 경유 Kinesis 접근.
4. **검증**: 스택 출력의 CloudFront URL 접속, 테스트 사용자로 로그인 후 시도: (a) *"구독 유형별 고객 분포 차트"* → Athena `customers` 테이블 + 에이전트 생성 막대/원형 차트, (b) *"카테고리·우선순위별 지원 티켓 분포"* → Aurora 전용 경로, (c) *"평점 상위 5개 타이틀과 스트리밍 시간"* → 연합 쿼리: Aurora의 `content_ratings`와 Athena의 `streaming_events` + `titles` 상관 분석.
5. **프로덕션 강화**: 사용자 인증(Cognito)과 별개로 에이전트가 백엔드에 쓰는 신원을 검토하고, 카탈로그 자산에 Lake Formation 정책을 적용하며, 시맨틱 계층(Glue 카탈로그 비즈니스 컨텍스트 + 시맨틱 검색, 2026년 6월 발표)을 추가해 에이전트가 비즈니스 용어를 해석하고 환각 조인을 피하도록 한다.

## 왜 중요한가

- **티켓 대기에서 셀프서비스로**: 사용자가 자연어로 질문하면 탐색 후 조회(discover-then-query) 워크플로(카탈로그 도구 또는 SQL 작성 전 `get_table_schema`)가 API·파티션 전략·자격증명을 숨긴다.
- **강제 중앙화 불필요**: 거버넌스가 필요한 소스는 카탈로그 규율로, 운영 소스는 직접 속도로 — 하나의 프로토콜·게이트웨이·에이전트 뒤에 공존. 신규 소스 온보딩 = MCP 서버 배포이며 파이프라인 재설계가 아니다.
- **핵심 거버넌스 유지**: S3 데이터는 Glue + Lake Formation이, 직접 경로는 Secrets Manager + IAM이 범위를 제한한다.

## 세미나용 요점 정리

- 발표의 뼈대는 스펙트럼: 카탈로그 우선(거버넌스, Athena 조인, 파티션 인식 SQL) → 직접(속도, `run_query`/`get_table_schema`, RDS Data API) → 하이브리드(단일 오케스트레이터, 동일 프로토콜).
- "필수 스키마 탐색" 시스템 프롬프트 규칙과 Gateway 시맨틱 도구 탐색이 코드 변경 없이 신규 테이블·서버에 대응하는 핵심이다.
- 솔직히 남길 열린 문제: 에이전트 합성 답변의 교차 소스 리니지, 에이전트가 주 소비자인 시대의 신원/인가, *무엇에* 접근했는지뿐 아니라 *왜* 접근했는지를 기록하는 감사 추적 — AWS Labs MCP 서버, MCP Gateway Registry, Agent Toolkit 문서 참조.

## 관련 개념

- `concepts/data-engineering/data-lake.md`, `concepts/data-engineering/data-mesh.md`, `concepts/ai-agents/mcp.md`, `concepts/ai-agents/agent-orchestration.md`
