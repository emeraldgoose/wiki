---
title: "GA: 본인-대신-사용자 인증으로 권한 인지 Databricks 앱 만들기"
description: "GA된 OBO 인증으로 Databricks 앱이 로그인 사용자 신분으로 동작하며, 좁은 API 스코프와 함께 Unity Catalog 권한을 강제한다."
tags: [source, databricks, databricks-apps, unity-catalog, authorization, ko, ko]
locale: ko
source_url: "https://www.databricks.com/blog/now-ga-building-permission-aware-databricks-apps-behalf-user-authorization"
blog: databricks
published_date: 2026-10-07
---

# GA: 본인-대신-사용자 인증으로 권한 인지 Databricks 앱 만들기

## 개요

Databricks Apps의 OBO(on-behalf-of-user) 인증이 GA되었다. 지원 API 호출 시 로그인 사용자의 신분으로 동작하므로, 앱이 거버넌스를 재구현하지 않아도 Unity Catalog가 해당 사용자의 데이터 권한(행 필터·컬럼 마스크 포함)을 강제한다. 공유 설정 읽기나 백그라운드 작업 같은 앱 소유 업무에는 기존 서비스 주체를 그대로 쓴다.

## 두 가지 신분: 연산마다 선택

설계 질문은 각 연산이 누구의 권한을 따라야 하는가이다. 사용자별 조회와 거버넌스 데이터에 대한 행위는 사용자 인증(예: 각 영업사원이 볼 수 있는 계정만 보여주는 영업 어시스턴트), 공통 경험과 백그라운드 유지보수는 앱 인증이 맞다. 운영 앱 대부분은 둘을 섞어 쓰되, 자격 증명을 재활용하지 말고 클라이언트를 분리하고 경계를 명시한다.

## 좁은 스코프와 설정

API 스코프는 사용자 신분으로 앱이 할 수 있는 일의 상한이다. 읽기 전용 분석이면 넓은 `sql`이 아닌 `sql:restricted-query`를, Genie·AI Gateway를 쓸 때만 해당 스코프를 요청한다. 스코프는 상한일 뿐 데이터 허가가 아니므로, 사용자는 여전히 웨어하우스·Unity Catalog 권한이 있어야 한다. 개발자는 UI나 번들로 스코프를 선언하고, 사용자는 첫 접근 시 동의하며, 워크스페이스 관리자는 허용 목록(설정 > Development > Apps)으로 상한을 통제하고 좁히거나 끌 수 있다.

## 구현: 토큰 흐름과 보안 수칙

플랫폼은 요청별 단기 사용자 토큰을 `x-forwarded-access-token` 헤더로 전달한다. 앱은 요청마다 읽어 SQL 커넥터(또는 AppKit의 사용자 컨텍스트 클라이언트)에 넘기고, 저장·로깅·세션 재사용을 절대 하지 않는다. 토큰이 없으면 서비스 주체로 조용히 대체하지 말고 실패로 닫는다(fail closed). 커스텀 에이전트도 동일 패턴이다. 시작 시점이 아닌 요청 시점 핸들러 안에서 사용자 클라이언트를 초기화한다. 권한이 다른 사용자로 테스트하고 정책 변경 후 반복한다.

## References

- 원문: [Now GA: Building permission-aware Databricks Apps with on-behalf-of-user authorization](https://www.databricks.com/blog/now-ga-building-permission-aware-databricks-apps-behalf-user-authorization)
