---
title: "생성형 AI로 Amazon SageMaker Catalog의 비정형 데이터 조회하기"
description: "SageMaker Catalog에 발행된 보강된 비정형 자산을 구독하고 노코드 Bedrock 채팅 에이전트 또는 프로그래밍 방식 모델 추론으로 조회."
published: "2026-09-23"
source_url: "https://aws.amazon.com/blogs/big-data/query-unstructured-data-in-amazon-sagemaker-catalog-using-generative-ai"
blog: aws-big-data
locale: ko
tags: [source, aws-big-data, sagemaker, bedrock, ko, ko]
---

# 생성형 AI로 Amazon SageMaker Catalog의 비정형 데이터 조회하기

## 개요

비정형 문서를 보강(Textract 추출 + Claude 요약)해 SageMaker Catalog에 발행한 시리즈 전편의 소비자 편이다. 데이터 소비자가 카탈로그에서 보강된 자산을 검색·구독하고(프로듀서 승인 포함), 두 가지 방식으로 조회한다. 분석가용 노코드 채팅 에이전트와, 애플리케이션에 자연어 질의를 내장하려는 엔지니어용 Bedrock 모델 추론이다.

## 자산 구독

SageMaker Unified Studio 소비자 프로젝트에서 AI 생성 README의 키워드로 카탈로그를 검색하고, 자산의 비즈니스 메타데이터·용어집을 확인한 뒤 사유를 적어 구독을 요청한다. 프로듀서가 자신의 프로젝트에서 승인하면 소비자 구독 자산 목록에 나타나며, 전 과정에서 거버넌스된 접근이 유지된다.

## 두 가지 조회 경로

첫째, 구독한 S3 위치를 프로젝트에 등록하고 PDF 위에 지식 베이스를 만들어 Bedrock 채팅 에이전트 앱으로 대화한다. 평문 질문에 문서 근거 답을 돌려주고, 민감 도메인은 Guardrails를 붙인다. 둘째, 구독 자산에서 JupyterLab 노트북을 열어 Bedrock 추론을 프로그래밍 방식으로 실행한다. 근거 있는 답을 외부 채팅·BI 도구에 연결할 수 있다. 두 경로 모두 파일 위치를 몰라도 거버넌스된 데이터를 쓴다.

## 참고 자료

- [원문: Query unstructured data in SageMaker Catalog using generative AI](https://aws.amazon.com/blogs/big-data/query-unstructured-data-in-amazon-sagemaker-catalog-using-generative-ai)
- [시리즈 전편: Improve discoverability of unstructured data in SageMaker Catalog](https://aws.amazon.com/blogs/big-data/improve-the-discoverability-of-your-unstructured-data-in-amazon-sagemaker-catalog-using-generative-ai/)
