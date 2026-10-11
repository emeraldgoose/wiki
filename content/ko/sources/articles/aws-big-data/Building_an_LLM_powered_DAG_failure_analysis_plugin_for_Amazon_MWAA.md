---
title: "Amazon MWAA용 LLM 기반 DAG 실패 분석 플러그인 만들기"
description: "Bedrock으로 실패한 태스크를 코드 수준 맥락과 함께 진단하는 Analyze Task 버튼을 MWAA의 Airflow에 추가합니다."
tags: [source, aws-big-data, mwaa, airflow, bedrock, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/building-an-llm-powered-dag-failure-analysis-plugin-for-amazon-mwaa"
blog: aws-big-data
published_date: 2026-09-29
---

# Amazon MWAA용 LLM 기반 DAG 실패 분석 플러그인 만들기

## 개요

Glue·EMR·Athena·Redshift에 걸친 수백 개 DAG 환경에서는 태스크 하나가 실패해도 로그·DAG 설정·오류 메시지를 수작업으로 뒤져야 합니다. 이 글은 MWAA용 커스텀 Airflow 플러그인에 Amazon Bedrock(Claude)을 붙여, 주문형 근본 원인 분석과 실행 가능한 수정안을 제공하는 방법을 보여줍니다. 전체 소스는 `sample-aws-mwaa-llm-powered-plugin` 저장소에 있고, 연산자 유형별 실패를 재현하는 예제 DAG도 포함됩니다.

## 동작 방식

Airflow UI에서 실패한 태스크를 고르고 **Analyze Task**를 누르면 플러그인이 다음을 수행합니다: 메타데이터 DB에서 태스크 정보 조회, 로그·DAG 소스·연산자의 실제 코드/쿼리 수집, 보강된 맥락을 Bedrock에 전송, 근본 원인·단계별 해결책·예방 권고가 담긴 구조화 리포트 표시. AWS 호출은 `aws_default` 연결로 인증되며 MWAA에서는 실행 역할을 사용하므로 정적 키가 필요 없습니다.

차별점은 연산자 인식 보강입니다. Glue·EMR 연산자는 잡 정의를 해석해 S3에서 PySpark 스크립트를 읽고, Athena·Redshift·Bash·Python·dbt 연산자는 렌더링된 템플릿 필드에서 쿼리·명령을 인라인으로 읽습니다. 스마트 페치로 타임아웃 같은 인프라 오류에는 S3 조회를 건너뛰고 코드 관련 오류 패턴에서만 코드를 가져옵니다.

## 플러그인 설계

- **등록:** Airflow 3.x에서는 웹 UI를 `fastapi_apps`로 `/task-analyzer`에 FastAPI 앱 등록하고, 태스크 인스턴스 페이지에 `Analyze Task` 외부 뷰를 추가합니다. `plugins.zip` 안에 넣어 배포하면 자동 탐색되므로 별도 등록 호출이 필요 없습니다.
- **분석 엔진:** `POST /api/analyze-task` 엔드포인트가 맥락을 조립하고 연산자별로 보강한 뒤 `prompts.py` 템플릿으로 프롬프트를 만들어 Bedrock을 호출하고 리포트를 반환합니다. 모델 ID는 Airflow 변수이므로 재배포 없이 모델 교체가 가능합니다.
- **프롬프트와 안전장치:** 태스크 메타데이터·오류문·로그·DAG 소스·연산자 스크립트를 묶어 보내고, 모델은 근본 원인·해결 단계·예방책을 반환합니다. 전송 전에 자격증명 마스킹, 컨텍스트 윈도우 맞춤 자르기, 경로 탐색 차단, 필요시 Comprehend PII 탐지 패스를 적용합니다. 오류 맥락 해시 기반 캐시로 반복 추론 비용을 아낍니다.

## 배포, 테스트, 운영

`plugins/`를 `plugins.zip`으로 묶어 MWAA S3 버킷에 올리고 버전 ID와 함께 환경을 업데이트합니다(10~30분 소요. FastAPI·Boto3가 사전 설치되어 있어 `requirements.txt` 불필요). 필요하면 `aws_default` 연결 extra로 리전을 재정의하고 Admin > Plugins에서 확인합니다. 예제 DAG를 DAG 폴더에 복사해 의도적 실패를 유발하면 수 초 내 파일·줄 번호가 포함된 분석이 나오는지 검증합니다.

프로덕션에서는 선택 모델의 `bedrock:InvokeModel`과 스크립트 경로의 `s3:GetObject`로 IAM을 최소화하고, 비밀값은 DAG 파일 대신 Secrets Manager에 두며, Airflow 인증 기반 엔드포인트 보호(대규모는 태그 기반 DAG 권한)와 Bedrock 호출 재시도·서킷브레이커·CloudWatch 알람을 갖춥니다. SNS/Slack 알림, 과거 분석 기반 Bedrock Knowledge Bases RAG, 커스텀 연산자 핸들러, 알려진 패턴 자동 복구로 확장할 수 있습니다.

## References

- 원문: [Building an LLM-powered DAG failure analysis plugin for Amazon MWAA](https://aws.amazon.com/blogs/big-data/building-an-llm-powered-dag-failure-analysis-plugin-for-amazon-mwaa)
