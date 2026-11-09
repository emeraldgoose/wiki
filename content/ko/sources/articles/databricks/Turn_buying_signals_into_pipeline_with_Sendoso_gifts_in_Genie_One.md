---
title: "Genie One에서 Sendoso 선물로 구매 신호를 파이프라인으로 전환하기"
description: "Unity Catalog의 거버넌스형 MCP 서비스로 설치되는 Sendoso MCP 서버를 통해, Genie One 사용자는 Databricks를 벗어나지 않고 자사 데이터의 의도 신호에서 승인된 추적 가능한 선물까지 도달할 수 있다."
tags: [source, databricks, agents, ai-engineering, ko]
locale: ko
source_url: "https://www.databricks.com/blog/turn-buying-signals-pipeline-sendoso-gifts-genie-one"
blog: databricks
published_date: 2026-11-10
---

# Genie One에서 Sendoso 선물로 구매 신호를 파이프라인으로 전환하기

**원문**: [Turn buying signals into pipeline with Sendoso gifts in Genie One](https://www.databricks.com/blog/turn-buying-signals-pipeline-sendoso-gifts-genie-one) · **게시일**: 2026-11-09

## 개요

Databricks는 Genie One을 비즈니스 팀이 거버넌스가 적용된 데이터에 자연어로 질문하는 공간으로 설명하는데, 빠져 있던 나머지 절반은 그 답에 따라 실제로 행동하는 일이었다. 목록을 내려받아 다른 도구에 로그인하고 맥락을 손으로 다시 맞추는 과정에서 후속 조치가 끊겼다. 선물이 도착할 무렵에는 구매자가 이미 관심을 접은 경우가 많았고, 발송을 파이프라인과 연결하려면 스프레드시트 작업이 필요했다. Databricks Marketplace의 파트너 MCP 서버가 이 간극을 메우며, Sendoso가 그 실제 사례다. 관리자가 한 번 연결하면 모든 Sendoso 도구가 데이터가 있는 곳에서 바로 사용할 수 있게 된다.

Sendoso는 eGift, 브랜드 키트, 맞춤 굿즈, 실물 선물 등 수만 가지 옵션을 갖춘 선물·다이렉트 메일 플랫폼이다. 자체 AI가 선물을 추천하고 수령자를 조사하며 메모 초안까지 작성한다. 글은 다른 채널이 이미 포화 상태라는 점을 근거로 이 채널의 가치를 설명한다. Sendoso의 2026년 디지털 피로도 보고서에 따르면 구매자의 84%가 콜드콜에, 83%가 마케팅 이메일에 피로를 느낀다. 누구에게 선물을 보낼지 알려 주는 신호는 대개 의도 점수, 참여도, CRM 데이터, 헬스 스코어 형태로 이미 Databricks 안에 있다.

신호와 발송, 발송 이력이 모두 같은 거버넌스 작업 공간에 있기 때문에 팀은 당일에 행동할 수 있고, 자체 기여 모델로 어떤 선물이 성과에 영향을 주었는지 보고할 수 있으며, Sendoso의 예산과 승인 체계도 그대로 유지된다. 또한 모든 도구는 로그인한 Sendoso 사용자 권한으로 실행되므로 에이전트는 그 사용자가 볼 수 있는 것만 보고 그 역할이 허용하는 일만 할 수 있다.

## 핵심 내용

- Sendoso MCP 서버는 Databricks Marketplace에서 Unity Catalog의 거버넌스형 MCP 서비스로 설치되므로 기존 Unity Catalog 권한이 사용 가능 대상을 결정한다. 이후 사용자는 Genie One 안에서 커넥터를 직접 추가한다.
- Unity Gateway는 에이전트가 호출할 수 있는 범위를 정하고, 위험도가 높은 작업에는 승인을 요구할 수 있으며, 모든 호출을 감사용으로 기록한다. 여기에 Sendoso 자체의 예산과 지출 한도, 캠페인 승인 절차가 더해진다.
- 시연은 작업 공간의 의도 테이블에서 시작한다. Genie One이 Northwest Robotics를 최상위 결과로 반환하고, 이 계정은 선물 자동화에 대한 의도가 3배 상승했으며 매출 운영 담당 부사장이 가격 페이지를 세 번 열람한 상태다. 이 계정 맥락이 Sendoso로 전달된다.
- 제안 단계에서는 아무것도 청구되지 않는다. Sendoso가 선물 후보와 계정이 급상승한 이유를 담은 메모를 제안하고, 사용자가 수령자와 선물, 메모를 확인한 뒤 승인한다.
- 발송 후에는 발송 ID가 포함된 확인 정보가 오며, 이 ID로 Sendoso에서 선물을 추적하고 발송 전까지 취소할 수 있다. 발송 이력은 같은 작업 공간의 테이블에 저장되므로 Genie One에 요청해 경영진용 요약을 받을 수 있다.
- Databricks는 타기팅 선물 캠페인을 이미 운영한 기업으로 Samsara, Procore, Talkdesk를 언급하며, 여러 플레이를 한꺼번에 도입하기보다 하나를 골라 실행한 뒤 다음 팀으로 확장할 것을 권한다.

## 상세

설정은 의도적으로 관리자 전용이다. Databricks Marketplace에서 Sendoso MCP 서버를 Unity Catalog의 거버넌스형 MCP 서비스로 설치한 다음, Unity Catalog 권한과 Unity Gateway 정책으로 통제한다. Gateway 정책은 각 호출에 승인이 필요한지 결정하고 이를 기록한다. 준비 조건은 의도, 참여도, CRM, 헬스 스코어 같은 신호가 Databricks에 있어야 하고 관리자가 Marketplace에서 커넥터를 설치해야 한다는 것이며, 단계별 구성은 별도 설정 가이드를 참고한다.

시연의 다섯 단계는 다음과 같다. 먼저 이번 주에 의도가 급상승했고 선물 이력이 없는 대상 계정을 Genie One에 묻는다. 다음으로 그 답에 따라 행동하도록 Sendoso에 요청하면, Sendoso가 카탈로그에서 적합한 선물을 찾고 계정이 급상승한 이유를 바탕으로 메모를 작성한다. 그다음 미리보기와 승인을 거치는데, 이 시점에는 비용이 청구되지 않는다. 발송 후에는 발송 ID가 담긴 확인 정보를 받고 발송 전까지 취소할 수 있다. 마지막으로 같은 작업 공간의 테이블에 있는 발송 이력을 Genie One에 요약해 달라고 요청해 경영진 보고에 쓴다.

글의 FAQ는 운영상의 질문에 답한다. ROI는 발송 이력이 파이프라인·갱신·참여 데이터 옆에 있으므로 팀의 기여 모델을 적용해 측정하며, 선물이 영향을 준 미팅과 파이프라인, 갱신을 지출과 비교한다. MCP 서버는 외부 시스템의 도구를 에이전트에 노출하는 것으로, Databricks에서는 거버넌스형 MCP 서비스로 설치되고 Unity Gateway로 제약된다. 대상 독자는 선물이나 다이렉트 메일을 보내는 모든 팀, 즉 세일즈와 고객 성공, RevOps, 수요 창출, 필드 마케팅, 고객·파트너 마케팅이며 코드 없이 자연어로 작업한다. 에이전트는 로그인한 사용자의 권한을 넘지 않고, 승인 전에는 어떤 비용도 청구되지 않는다.

## 참고 자료

- 원문: [Turn buying signals into pipeline with Sendoso gifts in Genie One](https://www.databricks.com/blog/turn-buying-signals-pipeline-sendoso-gifts-genie-one)
