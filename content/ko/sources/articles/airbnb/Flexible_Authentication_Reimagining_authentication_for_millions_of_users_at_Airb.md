---
title: "유연한 인증: 수백만 사용자를 위한 Airbnb 인증의 재구상"
description: "서버 주도 식별-후-인증 모델과 Challenge Picker로 클라이언트 코드를 줄이고 로그인 성공률을 높인 Airbnb 사례." (한국어 번역)
tags: [source, airbnb, auth, server-driven-ui, experimentation, ko, ko]
locale: ko
source_url: "https://airbnb.tech/uncategorized/flexible-authentication-reimagining-authentication-for-millions-of-users-at-airbnb"
blog: airbnb
published: "2026-08-12"
---

# 유연한 인증: 수백만 사용자를 위한 Airbnb 인증의 재구상

## 개요

Airbnb 마켓플레이스 사용자는 불규칙하게 로그인한다. 몇 달 만에 돌아온 게스트의 로그인 실패는 곧 예약 손실로 이어진다. 10년간 유기적으로 늘어난 로그인 방식을 정리하기 위해 팀은 유연한 인증(Flexible Authentication)으로 로그인 체계를 재구축했다. 로그인을 식별 단계와 인증 단계로 나누고, 서버가 사용자·지역별로 가장 쉬운 인증 수단을 고르며, 모든 화면에 대안 경로를 보장한다.

## 먼저 식별하고, 그 다음 인증한다

핵심 통찰은 로그인을 "본인임을 증명하라"가 아니라 "이 사람이 세션을 확인하는 가장 쉬운 방법은 무엇인가"로 다시 정의한 것이다. 사용자가 이메일·전화번호·소셜 로그인으로 먼저 신원을 밝히면, 설정 가능한 정책 엔진이 계정 이력과 문맥을 보고 성공 가능성이 가장 높은 인증 수단을 고른다. 브라질 여행자에게는 WhatsApp OTP를, 한국 호스트에게는 네이버 로그인을 우선 제시하고 나머지는 대안으로 둔다.

결정적으로 어떤 인증 화면을 보여줄지는 클라이언트가 아니라 서버가 정하고, 클라이언트는 받은 화면을 그리기만 한다. 덕분에 웹·iOS·안드로이드에 새 코드를 배포하지 않고도 지역별 전략 조정과 실험이 가능해졌다.

## Challenge Picker와 서버 주도 화면

기존 시스템의 막다른 골목이 사라졌다. 인증에 실패하면 처음부터 다시 시작해야 했지만, 새 설계는 모든 인증 화면에 "다른 방법으로 시도" 탈출구를 강제하고, 서버 주도 Challenge Picker가 주 인증 수단과 성공 확률순 대안 목록을 함께 반환한다. 버튼을 누르면 흐름이 처음부터 재시작되는 게 아니라 적응한다.

인증의 각 단계는 서버 응답으로 완전히 정의되는 화면이며, 클라이언트는 생성된 타입 정의를 쓰는 얇은 렌더러 역할을 한다. 화면 순서와 흐름 로직을 서버로 옮기면서 코드 60%와 웹 번들 100KB가 줄었고, 실험 주기가 수 주에서 수 일로 단축되어 출시 후 3개월간 20회 이상 실험을 진행했다.

## 결과

성공 가능성이 가장 높은 수단을 먼저 제시하면서 로그인 소요 시간이 줄고 인증 성공률이 수백만 세션에서 2.6%p 상승했다. 기존 계정 복구가 쉬워져 중복 계정 생성률이 27% 감소했고, SMS OTP 발송 감소로 일회성 코드 비용이 약 11% 절감됐다. 한 인증 수단에 장애가 생겨도 대안이 한 번의 탭 거리에 있어 사용자가 막히지 않는다.

## References

- 원문: https://airbnb.tech/uncategorized/flexible-authentication-reimagining-authentication-for-millions-of-users-at-airbnb
