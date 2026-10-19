---
title: "거버넌스 데이터 공유로 국방 공급망 가시성 풀기"
description: "원시 기록을 중앙화하지 않고 실시간 원가·공급망 근거를 주는 연방형 Databricks 데이터 교환으로 국방 조달 가시성을 확보한다." (한국어 번역)
tags: [source, databricks, data-sharing, unity-catalog, governance, ko, ko]
locale: ko
source_url: "https://www.databricks.com/blog/solving-defense-supply-chain-visibility-through-governed-data-sharing"
blog: databricks
published_date: 2026-10-09
---

# 거버넌스 데이터 공유로 국방 공급망 가시성 풀기

## 개요

20만 개가 넘는 공급업체, 수년씩 미끄러지는 사업, 실제 원가 데이터 요구가 이어지는데도 국방 조달은 여전히 수동 데이터 콜과 파편화된 스프레드시트에 의존한다. 제안은 연방형 데이터 교환이다. 각 계약업체가 자신의 데이터를 제자리에서 거버넌스하고, 버전·품질 검증된 근거만 지정 수신자에게 공개한다. 중앙 원시 저장소도, 벤더 종속도 없다.

## 가시성이 없는 이유

원가·가격 근거는 수동 요청으로 오가고, 하위 공급업체 출처는 대체로 불명이며, 협상 근거 부족으로 수천억 원대 문제 비용이 감사에서 지적됐다. 모든 계약업체 ERP에 직접 연결하는 것은 규모·수용성 모두에서 불가하므로, 무엇을 공개할지 합의하고 공개를 자동화하는 것이 대안이다.

## 연방형 교환의 동작 방식

계약업체는 쌍방 합의 조건으로 거버넌스된 근거를 공개하고, Unity Catalog가 접근 통제·CUI 마킹·리니지·감사 로깅을 강제하며, OpenSharing 프로토콜이 조직 경계를 넘어 데이터를 옮긴다. 진입로는 계층별로 맞춘다. 대형 프라임은 소스 시스템 파이프라인을, 중소 협력사는 동일한 데이터 계약을 만드는 검증 입력 폼을 쓰고, 새 회계 시스템은 필요 없다. GAAP 기반 보고 전환과 고정가 기본 흐름에도 부합한다. 기존 의무(CSDR, FlexFile, DD 1921 요약)는 중복 수동 콜 대신 자동 익스포트로 바뀐다.

## 이해관계자와 파일럿 경로

조달 리더는 연속 운영 상황을, 프라임은 사업당 수십 건의 중복 요청을 단일 공개 경로로, 중소 협력사는 저마찰 진입과 하방 이익 이전을, 납세자는 추적 가능한 가격 근거를 얻는다. 중앙 집중식 독점 플랫폼과 ERP 직접 연결은(고가치 단일 표적, 통합 병목, 종속) 이 규모에서 실패한다. 출범 단계는 작다. 원가·가격과 공급업체·생산 상태 두 데이터 계약을 정의하고 한 사업의 소수 프라임으로 파일럿을 열어 수개월 단위로 진척을 잰다.

## References

- 원문: [Solving defense supply chain visibility through governed data sharing](https://www.databricks.com/blog/solving-defense-supply-chain-visibility-through-governed-data-sharing)
