---
title: "비하인드 스토리: 라이브를 위한 Netflix 광고 이벤트 파이프라인 진화 — Part II"
description: "라이브 광고 텔레메트리를 중앙 집중화하고 풍부하게 만들어 하류 소비자에게 단일 이벤트 스트림으로 제공하는 Netflix의 설계를 설명합니다."
tags: [source, netflix, data-engineering, ads, streaming, ko]
locale: ko
source_url: "https://netflixtechblog.com/behind-the-scenes-evolving-netflixs-ads-event-pipeline-for-live-part-ii-826ebf9ad9fb"
blog: netflix
published_date: 2026-10-14
---

# 비하인드 스토리: 라이브를 위한 Netflix 광고 이벤트 파이프라인 진화 — Part II

**원문**: [netflix](https://netflixtechblog.com/behind-the-scenes-evolving-netflixs-ads-event-pipeline-for-live-part-ii-826ebf9ad9fb) · **게시일**: 2026-10-14

## 개요

Part I에서는 Netflix가 광고 이벤트 파이프라인을 시스템 설계 문제로 접근해, 파편화된 파이프라인을 중앙 수집·보강·표준 데이터 계약으로 바꾼 과정을 다뤘습니다. 그 결과로 Ads Event Publisher가 만들어졌습니다. 이 시스템은 클라이언트 기기에서 광고 텔레메트리를 모으고, 실제로 제공된 광고의 맥락으로 보강한 뒤, 빈도 제한·지표·청구·측정 파트너·리포팅 같은 모든 하류 소비자에게 하나의 통합된 광고 이벤트 스트림을 발행합니다.

광고 서빙이 두뇌라면 광고 이벤트는 심장 박동이고, 보강은 각 박동에 의미를 부여하는 과정입니다. 단순히 "누군가 광고를 끝까지 봤다"는 신호를, 어떤 광고가 어떤 맥락에서 노출됐는지까지 담은 이벤트로 바꿉니다.

## 핵심 내용

- 광고 서버가 결정을 내리면 해당 노출의 메타데이터를 레지스트리에 기록합니다.
- 기기에는 참조 식별자만 담은 작은 불투명 토큰을 반환합니다.
- 클라이언트가 토큰을 담아 이벤트를 보내면, Ads Event Publisher가 토큰을 해독해 레지스트리 메타데이터와 결합합니다.
- 라이브에서는 수천만 동시 시청자와 급격한 트래픽 변동이 발생하므로, 모든 광고·광고 브레이크 쓰기를 손실 없이 처리하는 것이 큰 확장 과제입니다.
- 중앙화된 수집과 표준 계약으로 핵심 경로의 의존성을 줄이고 하류 소비자를 단순화합니다.

## 참고 자료

- 원문: https://netflixtechblog.com/behind-the-scenes-evolving-netflixs-ads-event-pipeline-for-live-part-ii-826ebf9ad9fb
