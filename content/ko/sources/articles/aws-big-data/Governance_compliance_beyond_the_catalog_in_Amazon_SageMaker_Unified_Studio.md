---
title: "Amazon SageMaker Unified Studio에서 카탈로그를 넘어선 거버넌스 컴플라이언스"
description: "SageMaker Unified Studio의 거버넌스 신호(메타데이터 폼, 데이터 품질 점수, 용어집, 구독)를 일일 보강 파이프라인으로 모아 자산별 가중 컴플라이언스 점수를 계산하고 S3 Table 스냅샷으로 발행하는 AWS 패턴. Athena·QuickSight 대시보드·EventBridge 알림이 소비하며, 소비 가중 리스크 매트릭스로 거버넌스되지 않은 데이터의 우선순위를 정한다."
tags: [source, aws-big-data, data-governance, catalog, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/governance-compliance-beyond-the-catalog-in-amazon-sagemaker-unified-studio"
blog: aws-big-data
published_date: 2026-11-14
---

# Amazon SageMaker Unified Studio에서 카탈로그를 넘어선 거버넌스 컴플라이언스

**원문**: [AWS 빅데이터 블로그](https://aws.amazon.com/blogs/big-data/governance-compliance-beyond-the-catalog-in-amazon-sagemaker-unified-studio) · **게시일**: 2026-11-11

## 개요

데이터 카탈로그는 대개 무엇이 존재하는지 답한다. 자산 이름, 스키마, 소유권이다. 카탈로그가 커지면 더 어려운 질문은 어떤 자산이 조직의 거버넌스 기준을 실제로 충족하는가다. Amom Luiz, Guilherme Monte, Brenda Medeiros de Florenco는 SageMaker Unified Studio의 거버넌스 구성 요소 — 메타데이터 폼 정의, 데이터 품질 점수, 용어집 연결, 구독 데이터, SQL로 질의 가능한 일일 카탈로그 내보내기 — 위에 모든 자산의 가중 컴플라이언스 점수를 계산해 질의 가능한 테이블로 발행하는 거버넌스 보강 파이프라인을 만든다.

파이프라인은 매일 실행되며 보강 Lambda를 통해 다섯 소스를 조인한다. SageMaker 자산 메타데이터 내보내기(기본 자산 목록, S3 Table로 저장), 프로젝트·자산 유형별 조직 수준 필수 폼을 정의하는 S3의 Form Policy Config JSON, Search/GetListing API(자산별 용어집 항목·첨부된 메타데이터 폼·데이터 품질 요약), GetAssetType API(완전한 데이터 품질 규칙 수), ListSubscriptions API(공개된 자산별 활성 소비자 구독 수)다. 그 결과인 자산별 보강 컴플라이언스 레코드(가중 점수 포함)는 governance_metadata.asset_compliance S3 Table의 일일 스냅샷 파티션으로 기록되는데, 이 테이블 자체도 SageMaker 카탈로그의 자산이라 Unified Studio 안에서 도메인 자산들과 나란히 질의된다. 하류 소비자는 Amazon Athena 질의, AWS QuickSight 컴플라이언스 대시보드, Amazon EventBridge 컴플라이언스 알림이다.

컴플라이언스 점수는 설정 가능한 가중치의 다섯 차원을 결합한다. 폼 커버리지 50%(정책 대비 필수 폼 충족률), 데이터 품질 점수 20%(통과/실패 비율), 데이터 품질 규칙 커버리지 10%(실제 규칙 대 최소 기대치), 용어집 존재 10%(용어집 항목 1개 이상), 설명 10%(비즈니스 또는 리소스 설명)이다. '필수'는 이 설계에서 2계층 개념이다. SageMaker Unified Studio 자체의 강제 규칙(자산 유형 수준의 필수 메타데이터 폼, GetAssetType의 formsOutput required 플래그)과 강제 규칙은 없지만 조직이 필수로 여기는 요구(예: 모든 Glue 테이블에 DataClassificationForm을 요구하는 프로젝트)로, 후자는 S3 정책 파일에 저장한다. 파이프라인은 두 계층의 합집합을 취한다.

글이 강조하는 핵심은 구체적 가중치가 아니라 패턴이다. 신호들이 한곳에 모이면 팀이 자기 맥락에서 '컴플라이언트'의 의미를 정의한다. 역할별 네 질문이 이점을 보여준다. 데이터 소유자는 필수 메타데이터 폼이 빠진 자산을, 데이터 스튜어드는 용어집 항목이 없는 자산을, 플랫폼 팀은 새 거버넌스 규칙 발표 이후 컴플라이언스가 개선 중인지를, 최고데이터책임자는 더 신뢰할 수 있는 데이터 제품을 만들어야 할 부서를 묻는다.

## 핵심 내용

- 솔루션 구조: 일일 보강 파이프라인(Lambda)이 다섯 소스(자산 메타데이터 내보내기 S3 Table asset_metadata.asset, S3 Form Policy Config JSON, Search/GetListing·GetAssetType·ListSubscriptions API)를 조인해 governance_metadata.asset_compliance S3 Table에 일일 스냅샷을 기록.
- 내보내기 활성화: aws datazone put-data-export-configuration --domain-identifier DOMAIN_ID --region REGION --enable-export를 도메인당 1회 실행, 24시간 안에 S3 Table로 읽힌다. 파이프라인은 asset_id(조인 키), extended_metadata['owningEntityId'](프로젝트별 정책 조회), business_description/resource_description(설명 신호)을 사용.
- 2계층 '필수': 1계층은 SageMaker Unified Studio 자산 유형 수준 강제 규칙(GetAssetType, formsOutput의 required 불리언), 2계층은 네이티브 강제가 없는 조직 요구(프로젝트별 필수 폼)로 S3 JSON 정책 파일(default와 프로젝트별 required_forms)에 저장. 파이프라인은 둘의 합집합.
- 컴플라이언스 점수 차원과 가중치(설정 가능): 폼 커버리지 50%, 데이터 품질 점수 20%, 품질 규칙 커버리지 10%, 용어집 존재 10%, 설명 10%. 가중치와 최소 품질 규칙 임계값은 조직별 조정 가능.
- 점수 해석용 밴드: 80-100 완전 거버넌스, 60-79 대체로 거버넌스, 40-59 부분 거버넌스, 20-39 데이터 품질만, 1-19 최소 문서화, 0 무거버넌스.
- 보강 테이블 위의 SQL 답변: 필수 폼 누락 자산 목록, 프로젝트별 스코어카드(자산 수, 평균 컴플라이언스 점수, 폼 공백 자산 수, 품질 통과 자산 수), 거버넌스 정책 발행일 이후 일별 컴플라이언스 추이.
- 알림: EventBridge Scheduler + Lambda가 주간(또는 일간) 보고서를 보내고 컴플라이언스가 임계값 아래로 떨어지면 알린다. SNS·SES·Slack 웹훅으로 라우팅하며 샘플 질의는 프로젝트별 비컴플라이언스 자산 수를 센다.
- 대시보드: QuickSight가 Athena를 통해 보강 테이블에 직접 연결(aws-quicksight-service-role-v0 역할에 Lake Formation DESCRIBE/SELECT 부여). aws-samples 저장소의 Python 스크립트가 데이터 소스·데이터셋·대시보드를 만들고, QuickSight 자연어 Build 기능으로 일상어 프롬프트(프로젝트별 평균 점수 막대, 밴드 파이, 스냅샷 날짜별 추이 선, 폼 공백 누적 막대, 용어집 커버리지 KPI, 프로젝트별 평균 품질 규칙 수)로 시각화를 생성.
- 소비 가중 리스크: ListSubscriptions의 구독 수(공개 자산별 승인 구독 프로젝트 수)와 컴플라이언스 점수를 결합한 리스크 매트릭스 — 골드 스탠다드(점수 ≥ 80, 높은 채택, 조치 없음), 과잉 투자(≥ 80, 구독 0, 검토), 백로그(< 50, 구독 0, 점진 개선), 위기(< 50, 구독 2 이상, 즉시 조치). CASE 질의가 CRITICAL/MEDIUM_RISK/OK를 태그하고 구독 수·점수 순으로 정렬해 대시보드를 하류 영향 기반 우선순위 엔진으로 바꾼다.
- 데이터 제품: SageMaker Unified Studio에서 생산자는 관련 자산을 버전 관리되는 자족적 데이터 제품으로 묶고 소비자는 한 번의 요청으로 구독한다. 모든 프로젝트를 순회해 만든 asset_id-제품 매핑으로 컴플라이언스를 제품 수준에 집계한다(제품별 자산 수, 제품 컴플라이언스 점수, 총 구독, 폼 공백 자산 수).
- 예시: 서로 다른 성숙도의 세 프로젝트에 걸친 공개 Glue 테이블 20개 — 메타데이터 폼·용어집·품질 규칙을 갖춘 프로젝트가 스코어카드를 이끌고 나머지는 기본 품질 점검만으로 뒤처진다.
- 확장성과 비용: 테스트 도메인(공개 Glue Table 29개, 3프로젝트)에서 보강 Lambda는 약 30초 만에 완료. 프로덕션 규모에서는 보강 호출 병렬화, Lambda 메모리 상향, 대형 카탈로그는 AWS Step Functions 팬아웃. 배포는 sample-smus-asset-scorecard CDK 저장소(보강 Lambda, S3 정책 버킷, EventBridge Scheduler 규칙, IAM 역할, S3 Table 네임스페이스). 내보내기와 보강 테이블 모두 Lake Formation 거버넌스라 Lambda·서비스 역할에 DESCRIBE/SELECT 권한 필요. 예상 소요 약 2시간, 소형 테스트 도메인 비용 월 5달러 미만.

## 세부 사항

### 또 다른 카탈로그 뷰가 아니라 보강인 이유

메타데이터 내보내기는 어떤 폼 필드가 채워졌는지는 알려주지만 '채워짐'은 '필수'가 아니며, 이 설계에서 필수는 플랫폼 강제 규칙과 플랫폼이 강제하지 않는 조직 정책이라는 두 출처를 가진다. 파이프라인의 정책 계층은 GetAssetType의 자산 유형별 required 플래그와 S3 정의 프로젝트별 폼 요구의 합집합을 취해, 프로젝트가 플랫폼 수준 지원을 기다리지 않고 모든 Glue 테이블에 DataClassificationForm을 요구할 수 있게 한다. 나머지 — 용어집 항목, 품질 요약, 구독 수 — 는 내보내기에 없어 카탈로그 API로 들어온다.

### 스코어카드에서 우선순위화로

가장 흥미로운 설계는 소비로 가중하는 것이다. 컴플라이언스 점수만 있으면 자산을 자기 성숙도로 순위 매기지만, 공개 자산별 승인 구독자 수를 더하면 사분면이 만들어진다. 소비자가 많은 거버넌스되지 않은 자산(위기: 점수 < 50, 구독 ≥ 2)이 아무도 안 쓰는 청결한 자산(과잉 투자)보다 앞선다. 리스크 질의의 CASE 로직(CRITICAL, MEDIUM_RISK, OK)은 의도적으로 단순하며, 글은 이것이 수동 스코어카드와 컴플라이언스 공백·하류 영향을 함께 반영해 자산 팀이 어디에 집중할지 알려주는 우선순위 엔진의 차이라고 본다.

### 소비자 수준까지의 롤업

데이터 제품은 소비자가 실제로 구독하는 단위이므로 패턴은 그 수준에서도 컴플라이언스를 집계한다. 모든 프로젝트를 순회해 만든 asset_id-데이터 제품 매핑으로 롤업 질의가 제품별 총 자산 수, 제품 컴플라이언스 점수, 총 구독, 폼 공백 수를 보고하고, 배정되지 않은 자산은 '(unassigned)' 그룹으로 표면화되어 집계에 숨는 것이 없다. 이렇게 경영진 뷰가 접근과 책임이 실제로 부여되는 수준과 정렬된다.
