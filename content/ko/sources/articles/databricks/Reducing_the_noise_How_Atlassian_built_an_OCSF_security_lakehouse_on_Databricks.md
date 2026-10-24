---
title: "노이즈 줄이기: Atlassian이 Databricks에서 OCSF 보안 레이크하우스를 구축한 방법"
description: "44억 건의 보안 이벤트를 OCSF 공통 스키마로 통합해 수집 비용과 분석 시간을 줄인 Atlassian 사례입니다."
tags: [source, databricks, data-engineering, security, ocsf, ko]
locale: ko
source_url: "https://www.databricks.com/blog/reducing-noise-how-atlassian-built-ocsf-security-lakehouse-databricks"
blog: databricks
published_date: 2026-10-15
---

# 노이즈 줄이기: Atlassian이 Databricks에서 OCSF 보안 레이크하우스를 구축한 방법

**원문**: [databricks](https://www.databricks.com/blog/reducing-noise-how-atlassian-built-ocsf-security-lakehouse-databricks) · **게시일**: 2026-10-15

## 개요

Atlassian은 35만 고객을 둔 글로벌 SaaS 기업으로, 20년간 성장하며 인수한 서비스마다 로그 형식이 달랐습니다. 그 결과 보안 데이터 파이프라인은 하루 440억 건의 이벤트를 받아들이면서도 로그 소스 간 공통 언어가 없었습니다. 타임스탬프와 스키마가 제각각이라 분석가는 데이터가 들어온 뒤 정규화에 시간을 썼고, 플랫폼마다 데이터가 흩어져 상관 분석이 제한됐습니다.

Atlassian은 OCSF(Open Cybersecurity Schema Framework)를 공통 스키마로 삼아 보안 레이크하우스를 구축했습니다. 반복 가능한 하나의 프로세스로 모든 도구의 텔레메트리를 통합한 것이 핵심입니다.

## 핵심 내용

- 보안 텔레메트리를 OCSF로 표준화해 수집 비용을 80% 줄였습니다.
- 500개 이상의 프로덕션 위협 탐지 시그널을 단일 스키마에서 운영합니다.
- 분석가 생산성이 60% 향상됐습니다.
- 쿼리 시간이 약 45초에서 2~3초로, 최대 95% 빨라졌습니다.
- 하루 440억 건 이벤트를 공통 스키마로 정규화합니다.

## 참고 자료

- 원문: https://www.databricks.com/blog/reducing-noise-how-atlassian-built-ocsf-security-lakehouse-databricks
