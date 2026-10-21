---
title: "Lakebase와 에이전틱 SDLC: 코딩 에이전트를 위한 브랜칭 데이터베이스"
description: "copy-on-write 브랜칭, Git worktree, CI 자동화로 모든 코딩 에이전트와 PR에 격리된 Lakebase Postgres 브랜치를 제공한다."
tags: [source, databricks, lakebase, coding-agents, cicd, ko, ko]
locale: ko
source_url: "https://www.databricks.com/blog/lakebase-and-agentic-sdlc-branching-databases-coding-agents"
blog: databricks
published_date: 2026-10-08
---

# Lakebase와 에이전틱 SDLC: 코딩 에이전트를 위한 브랜칭 데이터베이스

## 개요

병렬로 동작하는 코딩 에이전트는 모두 스키마 조회·마이그레이션·테스트용 데이터베이스가 필요한데, 공유 개발 DB는 충돌 지대가 되기 쉽다. Lakebase Postgres는 Git식 데이터베이스 브랜칭으로 이를 해결한다. copy-on-write 방식이라 1초 안에 생성되고, 달라진 부분만 저장하며, 유휴 상태에서는 컴퓨트 비용이 들지 않는다.

## 에이전트마다 격리된 데이터베이스

핵심 패턴은 Git worktree(에이전트별 체크아웃 디렉터리로 코드 충돌 방지)와 worktree당 하나의 Lakebase 브랜치를 짝짓는 것이다. worktree 생성 시 post-checkout 훅이 자동으로 전용 DB를 만들고, 저장소의 지침 파일(예: `AGENTS.md`)이 에이전트를 PR 생성으로 이끈다. 작업이 끝나면 worktree와 브랜치를 함께 정리한다. 브랜치는 다시 병합하지 않는다. 부모·자식이 각자 변하므로, 스키마 변경은 마이그레이션 코드(Drizzle, Alembic, Flyway, Liquibase)로 전달하고 배포 자동화가 적용한다.

## PR마다 임시 데이터베이스

PR이 열리면 CI가 프로덕션에서 짧게 사는 브랜치를 만들고, 마이그레이션 도구를 실행한 뒤 해당 연결 문자열을 가리키는 프리뷰 앱을 배포하고, 스키마 diff(바뀐 테이블·컬럼·인덱스)를 PR 댓글로 게시한다. 리뷰어는 실제 데이터 기준으로 코드와 DB 변경을 함께 검증하고, 병합 시 마이그레이션이 승격되며 PR 종료 시 브랜치는 삭제된다. 참조 구현은 GitHub Actions와 Databricks Apps를 쓰지만 어떤 호스팅에도 적용 가능하다.

## 응용: 버그 재현, 마이그레이션 검증, 마스킹 데이터

브랜칭은 특정 시점 버그 재현(장애 직전으로 분기해 실제 데이터로 디버깅 후 정리), 배포 전 마이그레이션 사전 검증, Unity Catalog 마스킹을 적용한 프로덕션 파생 데이터 작업에도 쓸 수 있어 운영 DB를 위험에 빠뜨리지 않는다. 데모는 단일 워크스페이스로 단순화했지만, 환경별 워크스페이스 분리나 민감 데이터 보호용 시드 DB 분기에도 같은 개념이 적용된다.

## References

- 원문: [Lakebase and Agentic SDLC: Branching Databases for Coding Agents](https://www.databricks.com/blog/lakebase-and-agentic-sdlc-branching-databases-coding-agents)
