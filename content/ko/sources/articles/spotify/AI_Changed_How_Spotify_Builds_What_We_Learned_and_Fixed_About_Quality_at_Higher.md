---
title: "AI가 바꾼 Spotify의 개발 방식: 더 빠른 속도에서 품질을 되찾은 과정"
description: AI 시대 품질에 대한 Spotify의 데이터 — 월 병합 변경이 1.7만 건으로 2배가 됐지만 AI발 장애는 없었고, 병목은 코드 작성에서 검증으로 이동했다
tags: [source, spotify, ai-coding, quality, reliability, ko, ko]
locale: ko
source_url: "https://engineering.atspotify.com/2026/9/ai-changed-how-spotify-builds-what-we-learned-and-fixed-about-quality-at-higher-velocity"
blog: spotify
published_date: 2026-09-16
---

# AI가 바꾼 Spotify의 개발 방식: 더 빠른 속도에서 품질을 되찾은 과정

**저자**: Tyson Singer, Head of Technology and Platforms (SVP)
**출처**: [Spotify Engineering](https://engineering.atspotify.com/2026/9/ai-changed-how-spotify-builds-what-we-learned-and-fixed-about-quality-at-higher-velocity)
**날짜**: 2026-09-16

## 개요

Spotify는 약 3,000개의 프로덕션 서비스로 1억 명 안팎의 동시 접속자를 감당한다. AI 보조 개발을 본격화한 뒤 일부 품질이 흔들렸지만, 장애 회고를 분석한 결과 AI가 작성한 코드 특유의 실패 패턴은 발견되지 않았다. 진짜 원인은 속도였다. 변경을 만들어내는 능력이 그 변경을 검증하는 체계를 앞질렀다. 이 글은 압박을 받은 네 영역, 적용한 수정, 그리고 속도-품질 맞교환 가설에 대한 자체 배송 지표의 답을 정리한다.

## 압박을 받은 네 영역

**콘텐츠 처리.** Spotify는 매일 50만 건이 넘는 음원·영상·팟캐스트·오디오북을 처리한다. 조용히 묻히는 처리 실패, 알림 없는 트랜스코딩 대기열 적체라는 잠재 결함에 배치 작업 충돌, 편당 연산량 증가, 스케줄러 버그가 겹쳐 6월 24일 팟캐스트·영상 발행이 몇 시간 지연됐다. 이후 종단 간 모니터링, 스케줄러 수정, 배치 작업 우선순위 하향, 용량 증설, 서비스 등급 재설계, 악성 업로드 우선순위 강등을 적용했다.

**플릿 업데이트.** Fleet Management 프레임워크는 매일 대규모 자동 변경을 적용하며, 에이전트 기반 마이그레이션(백엔드 Java 마이그레이션을 3일 만에 완료)까지 맡는다. 그러나 자동 의존성 업그레이드 하나가 모든 검사를 통과하고도 프로덕션에서 실패했다. 대응책은 안전장치 강화, 롤백 역량 확대, 소유 팀 근무 시간대 배치다.

**연산 용량 부족.** 업계 전반의 AI 수요가 CPU/GPU 여유분을 앗아가면서, 예전엔 무난했던 리전 장애조치가 사용자 체감 장애로 번지기 시작했다. 엣지 예약 용량을 2배로 늘리고, 장애조치 시 하위 등급 서비스는 포기할 수 있음을 받아들였으며, 점진적 트래픽 이동 제어를 엣지로 확장 중이다.

**모바일 앱 경험.** 빨리 출시하고 나중에 다지는 오래된 품질 사이클이 AI로 빨라졌다. 개별 릴리스는 건강해 보여도 관측 지표 밖에 작은 회귀가 쌓인다. 가드레일 지표를 넓히고 릴리스 판단에 장기 추세를 반영했다.

## 배송 데이터가 말하는 것

이제 매월 주요 장애 회고에서 AI 작성 코드의 직접 기여와 변경량 압박 여부를 묻는다. 지금까지 AI 작성 코드가 실질 원인이었다는 결론은 없었지만, 검증 체계가 변경 속도를 못 따라간 사례는 있었다. 상위 파이프라인도 같은 방향이다. 8월 병합 변경은 전년 대비 2배 이상(약 8,100건 → 17,000건)이었고, 코드 품질·최적화 비중은 27%에서 31%로 올라 절대 투자량은 2배를 넘었다. 재작업률(단순 churn이 아닌 연식 가중 지표)은 오르지 않아 업계 churn 급등(FAROS 보고)과 대비된다. 주시 중인 신호는 코드 복잡도와 PR 크기 상승뿐인데, 큰 PR이 인간-에이전트 협업의 결과물일 수 있어 임계값을 서둘러 고치지는 않는다.

## 핵심 정리

AI는 Spotify가 시스템을 바꾸는 속도의 상한을 올렸고, 병목은 리뷰·테스트·배포·관측·롤백·장애조치가 같은 속도로 도는지로 옮겨갔다. 배송 체계와 개발 속도의 정렬은 일회성 수정이 아니라 지속 작업이다.

## 참고 자료

- [AI Changed How Spotify Builds — 원문](https://engineering.atspotify.com/2026/9/ai-changed-how-spotify-builds-what-we-learned-and-fixed-about-quality-at-higher-velocity)
- [콘텐츠 인제스트·팟캐스트 영상 장애 보고서](https://engineering.atspotify.com/2026/7/content-ingestion-and-podcast-video-incident-report) (원문에서 인용)
- [Google Cloud 2025 DORA 보고서](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report) (원문에서 인용)
- [FAROS 2026 AI 가속 보고서](https://www.faros.ai/research/ai-acceleration-whiplash) (원문에서 인용)
