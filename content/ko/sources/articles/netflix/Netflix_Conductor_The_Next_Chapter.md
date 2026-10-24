---
title: "Netflix Conductor: 다음 장"
description: "오픈소스 유지보수를 중단한 뒤에도 내부에서 더 빠르게 성장한 Netflix의 워크플로 오케스트레이션 엔진 Conductor 이야기입니다."
tags: [source, netflix, data-engineering, workflow, conductor, ko]
locale: ko
source_url: "https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649"
blog: netflix
published_date: 2026-10-14
---

# Netflix Conductor: 다음 장

**원문**: [netflix](https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649) · **게시일**: 2026-10-14

## 개요

Conductor는 Netflix가 마이크로서비스를 안정적이고 관측 가능한 비즈니스 프로세스로 엮는 워크플로 오케스트레이션 엔진입니다. 외부에서 Conductor를 지켜봤다면 GitHub 저장소의 "Netflix가 내부 포크에 집중하기 위해 Conductor OSS 유지보수를 중단한다"는 공지를 마지막으로 기억할 수 있습니다.

그 공지는 오픈소스 장의 끝처럼 보였지만 이야기는 끝나지 않았습니다. 내부에서 Conductor는 멈추지 않았고 오히려 더 빠르게 성장했습니다. 이 글은 아키텍처 변화, 성능·확장 작업, 개발자 경험의 도약, 운영 제어를 위한 새 기능을 다룹니다.

## 핵심 내용

- Conductor는 마이크로서비스를 신뢰할 수 있는 워크플로로 연결하는 핵심 엔진입니다.
- 내부 포크로 전환한 뒤에도 사용량과 기능 개발이 계속 확장됐습니다.
- 한 해 10억 건 워크플로 실행이 이정표였던 시절에서, 이제는 분기마다 그 수준을 넘어섭니다.
- 아키텍처와 성능, 확장성을 개선해 더 큰 규모를 감당합니다.
- 개발자 경험과 운영 제어 기능도 함께 발전했습니다.

## 참고 자료

- 원문: https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649
