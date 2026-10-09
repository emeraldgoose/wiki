---
title: Twitter의 rasdaemon 활용 하드웨어 신뢰성
description: 수십만 호스트의 하드웨어 오류 텔레메트리를 폐기된 mcelog/edac-utils에서 rasdaemon으로 일원화한 사례
tags: [source, twitter, x, hardware, reliability, linux, rasdaemon, ko]
locale: ko
source_url: "https://blog.x.com/engineering/en_us/topics/infrastructure/2023/how-twitter-uses-rasdaemon-for-hardware-reliability"
blog: twitter
date: '2023-01-06'
---

# Twitter의 rasdaemon 활용 하드웨어 신뢰성

## 요약

Twitter 온프레미스 데이터센터에는 수십만 서버와 수백만 하드웨어 부품이 있다. 일시적·간헐적 하드웨어 결함은 근본 원인 파악이 어려웠다. 서비스 소유자는 느린 머신을 알 수 있어도 어느 부품 문제인지는 몰랐고, 머신은 사이트 운영 수리 루프를 맴돌았다 — 재설치 후 복귀했다가 곧 다시 고장나며 진단 없이 반복됐다. 한편 팀마다 자체 결함 탐지 플러그인을 만들어 신호가 난립했다. 기존 도구 자체도 수명을 다했다. **mcelog는 커널에서 폐기**됐고 **edac-utils는 사실상 유지보수 중단** 상태이며, 커널 변경으로 기존 메트릭의 신뢰도도 떨어졌다. 팀은 표준 Linux 오픈소스 RAS(reliability, availability, serviceability) 유틸리티 **rasdaemon**에 커널 하드웨어 오류 이벤트의 수집·필터·리포트를 일원화했다.

## 커버하는 이벤트

- **MC(Memory Controller) 이벤트** — 정정 가능/불가능/치명적 오류를 상세히 집계·노출
- **MCE(Machine Check Exception)** — 플랫폼 전반의 CPU 감지 하드웨어 결함용으로 mcelog 대체
- **디스크/블록 오류** — EOPNOTSUPP, ETIMEDOUT, ENOSPC, ENOLINK, EREMOTEIO, EBADE, ENODATA, EILSEQ, ENOMEM, EBUSY, EAGAIN, EREMCHG, EIO(S.M.A.R.T. 데이터 보완용)
- **Devlink 오류**, **PCIe AER 이벤트**

부수 효과: CentOS 8/9 마이그레이션 차단 해제, 신호 충실도 향상으로 비실행(non-actionable) 오탐에 따른 팀 간 부담 감소, 적절한 경우 서버 전체 제외 대신 **페이지 오프라이닝**(불량 메모리 페이지만 격리)으로 비용 절감.

## 마이그레이션 규율

- **선구축 후 전환(make-before-break)**: 기존 플러그인 비활성화 전 기능 동등성 확보
- 코드베이스에서 edac-utils/mcelog 언급 전수 검색, 전 서비스 대시보드 검토로 관측 가능성 회귀 방지
- 전사 소통, 충분한 카나리, 느린 플릿 롤아웃
- 결과: 하드웨어 MTTD/MTTR 감소, rasdaemon의 업계 사용 권장

## SW 엔지니어를 위한 시사점

- 커널 인접 폐기 도구(mcelog)는 만료 기한 있는 기술 부채로 다룬다. 정식 폐기 전에 커널 변경이 출력을 조용히 망가뜨린다.
- 팀별 하드웨어 플러그인 N개를 단일 파이프라인으로 통합한다. bespoke 탐지기 N개의 비용은 이후 모든 디버깅 세션에서 지불된다.
- 결함 영역이 허용하면 호스트 전체 제외보다 저하 상태로 계속 서비스(페이지 오프라이닝)를 선호한다.
- "선구축 후 전환" + 대시보드 단위 검증은 플릿 단위 관측 가능성 의존성 마이그레이션의 정석이다.

## 참고

- 원문: https://blog.x.com/engineering/en_us/topics/infrastructure/2023/how-twitter-uses-rasdaemon-for-hardware-reliability (2023-01-06)
- 관련: `concepts/infrastructure/kubernetes.md`
