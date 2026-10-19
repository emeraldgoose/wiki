---
title: "Concurrence는 Unity Gateway로 조 단위 토큰 임상 AI를 어떻게 거버넌스하나"
description: "불변 이벤트 기반 환자 상태, 출시 전 시뮬레이션, 컴플라이언스 우선 라우팅, Unity Gateway 단일 AI 접점으로 임상 AI를 통제한 Concurrence 사례." (한국어 번역)
tags: [source, databricks, unity-catalog, ai-agents, unity-gateway, ko, ko]
locale: ko
source_url: "https://www.databricks.com/blog/how-concurrence-governs-clinical-ai-trillion-token-scale-unity-gateway"
blog: databricks
published_date: 2026-09-23
---

# Concurrence는 Unity Gateway로 조 단위 토큰 임상 AI를 어떻게 거버넌스하나

**출처**: [Databricks Blog](https://www.databricks.com/blog/how-concurrence-governs-clinical-ai-trillion-token-scale-unity-gateway) · **발행**: 2026-09-23

## 개요

임상 AI 기업 Concurrence는 30일 기준 약 1,000억 입력 토큰·1,120만 LLM 호출(연 환산 약 1.2조, 1년 새 5배 성장)을 환자·의료진 대면 에이전트에 쓰고 있다. Zerobus 수집- Delta, Declarative Pipeline의 월드모델 환자 상태, Lakebase 운영 상태, Unity Catalog 거버넌스, Unity Gateway AI 접점이라는 Databricks 기반이 그 규모에서도 신뢰성과 컴플라이언스를 지킨다.

## 신뢰 데이터와 출시 전 테스트

기존 기록을 덮어쓰는 대신 불변 이벤트로 남기고 출처가 보이는 현재 환자 상태를 계산하므로 에이전트는 일관된 맥락을 보고 학습이 다음 워크플로에 환류된다. 상태가 재생 가능한 이력에서 유도되므로 모든 에이전트는 실제 환자에게 닿기 전 가상 환자로 테스트받으며(시뮬레이션 트래픽이 프로덕션의 약 7배), 트레이스·임상 데이터·ai_query 평가가 하나의 거버넌스 기반에 있어 성능 변화의 원인을 모델·데이터·워크플로로 추적할 수 있다.

## 컴플라이언스 우선 거버넌스와 단일 AI 접점

고객사마다 별도 스키마·서비스 주체를 두고, 배치 워크로드는 BAA 적용 Databricks 호스팅 모델에서 엔드포인트 리졸버가 PHI의 미적용 모델 유출을 차단하며, 라우팅은 비용보다 컴플라이언스가 먼저다. 코딩 에이전트 트래픽은 이미 Unity Gateway `ug` CLI로 흐르고(누적 610억 토큰·36만 요청, 요청자 귀속과 중앙 MCP 관리), 실시간 추론은 합성 카나리 뒤 feature flag로 대기 중이다. 누적 효과는 복리다. 각 상호작용이 공유 환자 상태를 풍부하게 해 다음 워크플로의 한계 비용을 낮춘다.

## References

- [How Concurrence governs clinical AI at a trillion-token scale with Unity Gateway](https://www.databricks.com/blog/how-concurrence-governs-clinical-ai-trillion-token-scale-unity-gateway)
