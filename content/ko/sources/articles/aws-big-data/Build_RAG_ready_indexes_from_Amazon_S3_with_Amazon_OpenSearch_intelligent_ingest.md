---
title: "Amazon OpenSearch 지능형 수집으로 Amazon S3에서 RAG 준비 인덱스 구축하기"
description: "Amazon OpenSearch 지능형 수집은 Amazon S3에 저장된 문서를 수동 파싱·임베딩 파이프라인 없이 검색 가능한 인덱스로 변환합니다."
tags: [source, aws-big-data, search, rag, opensearch, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/build-rag-ready-indexes-from-amazon-s3-with-amazon-opensearch-intelligent-ingestion"
blog: aws-big-data
published_date: "2026-10-23"
---

# Amazon OpenSearch 지능형 수집으로 Amazon S3에서 RAG 준비 인덱스 구축하기

**원문**: [aws-big-data](https://aws.amazon.com/blogs/big-data/build-rag-ready-indexes-from-amazon-s3-with-amazon-opensearch-intelligent-ingestion) · **게시일**: 2026-10-23

## 개요

조직의 가장 귀중한 지식 중 많은 부분은 계약서, 제품 매뉴얼, 연구 보고서, 지원 런북, 재무 문서 같은 문서에 담겨 있습니다. 이 콘텐츠는 Amazon S3에 구조화 데이터(JSON, NDJSON, JSON 배열)와 비구조화 데이터(PDF, Word, 텍스트, Markdown)로 저장됩니다. 생성형 AI 애플리케이션, RAG 어시스턴트, 엔터프라이즈 검색 경험은 이 콘텐츠에 대한 접근성에 좌우되지만, 검색 가능하게 만들기는 가장 어려운 작업인 경우가 많습니다. 고객은 보통 별도의 파싱, 차트 해석, 청킹, 임베딩, 인덱싱 파이프라인을 운영해야 하며 각 레이어마다 인프라와 장애 모드가 따릅니다.

Amazon OpenSearch 지능형 수집은 이러한 수동 파이프라인 없이 원문 문서를 의미 기반 검색으로 이어지게 합니다.

## 핵심 내용

- 레이아웃, 읽기 순서, 표를 유지한 채 텍스트를 추출하는 문서 파서를 사용합니다.
- 문서 안의 차트, 도표, 스크린샷을 해석합니다.
- 추출한 텍스트를 청킹하고 임베딩한 뒤 벡터 인덱스에 기록합니다.
- PDF, Word, Markdown 파일을 레이아웃과 표가 보존된 채로 의미·하이브리드 검색 준비 인덱스에 수집합니다.
- 비전-언어 모델로 차트, 도표, 스크린샷, 사진의 텍스트 설명을 생성해 시각 콘텐츠를 검색 가능하게 만듭니다.
- JSON, NDJSON, CSV 같은 구조화 데이터를 수집 중 변환과 선택적 의미 검색 보강과 함께 로드합니다.

## 상세

전통적으로 문서 처리의 각 레이어는 별도 인프라와 복잡성을 만들어, 종단간 파이프라인 구축에 수주가 걸리기도 합니다. 지능형 수집은 이 단계들을 통합해 팀이 수동 작업을 줄이면서 엔터프라이즈 문서를 의미·하이브리드 검색에 준비할 수 있게 합니다.

파싱, 시각 콘텐츠 처리, 구조화 데이터 변환을 수집 안에 포함함으로써 Amazon S3에 저장된 PDF, Word, Markdown, JSON, CSV 콘텐츠를 RAG와 검색에서 활용하기 쉽게 만듭니다.

## 참고 자료

- 원문: https://aws.amazon.com/blogs/big-data/build-rag-ready-indexes-from-amazon-s3-with-amazon-opensearch-intelligent-ingestion
