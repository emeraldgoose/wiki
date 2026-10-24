---
title: "온톨로지 기반 관측성: Netflix 규모의 종단 간 지식 그래프 구축"
description: "초당 3,800만 건 로깅 이벤트를 다루는 Netflix가 온톨로지와 지식 그래프로 시스템 관측성을 높인 방법입니다."
tags: [source, netflix, data-engineering, observability, knowledge-graph, ko]
locale: ko
source_url: "https://netflixtechblog.com/ontology-driven-observability-building-an-end-to-end-knowledge-graph-at-netflix-scale-421392cf5adf"
blog: netflix
published_date: 2026-10-16
---

# 온톨로지 기반 관측성: Netflix 규모의 종단 간 지식 그래프 구축

**원문**: [netflix](https://netflixtechblog.com/ontology-driven-observability-building-an-end-to-end-knowledge-graph-at-netflix-scale-421392cf5adf) · **게시일**: 2026-10-16

## 개요

2024년 11월 Jake Paul과 Mike Tyson의 경기에서 Netflix는 약 6,500만 동시 스트림에 경기를 전송했습니다. 평소에도 인프라는 하루 20억 건 이상의 요청과 초당 3,800만 건 이상의 실시간 로깅 이벤트를 처리합니다. 이 규모에서는 전체 그림을 한 엔지니어링 팀의 머리나 하나의 대시보드에 담을 수 없습니다.

라이브 콘텐츠와 실시간 스트림이 늘면서 시스템을 빠르게 이해하고 갱신하는 능력이 좋은 사용자 경험에 필수적이 되었습니다. 이 글은 온톨로지 기반 지식 그래프로 종단 간 관측성을 구축한 Netflix의 접근을 설명합니다.

## 핵심 내용

- 모든 URI가 하나의 명명 규칙을 따르고, 카탈로그가 모든 `ops:Application`을 검증합니다.
- 엔티티 종류마다 하나의 권위 있는 카탈로그를 정하고, 엔티티 생성 전에 검증합니다.
- 온톨로지를 코드처럼 버전 관리하고 리뷰·테스트하며 PR로 변경합니다.
- 개념과 인스턴스를 분리합니다. 개념은 인간 시간 규모로, 인스턴스는 연속적으로 변합니다.
- RDF, OWL, SHACL, SPARQL 같은 오픈 표준 위에 구축합니다.
- 홈 화면 렌더링이 1.5초 느려지는 회귀 같은 문제를 그래프로 추적합니다.

## 참고 자료

- 원문: https://netflixtechblog.com/ontology-driven-observability-building-an-end-to-end-knowledge-graph-at-netflix-scale-421392cf5adf
