---
title: "Sony LIV, AWS로 실시간 비디오 스트리밍 분석 구축"
description: "Sony LIV가 배치 분석의 한계를 넘어서 AWS 기반 실시간 비디오 스트리밍 분석 아키텍처를 구축하고 비즈니스 영향을 이끈 사례를 요약한다."
tags: [source, article, aws-big-data, streaming, video, analytics, aws, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/how-sony-liv-built-real-time-video-streaming-analytics-with-aws/"
blog: "AWS Big Data"
published: "2026-09-10"
---

# Sony LIV, AWS로 실시간 비디오 스트리밍 분석 구축

**원문**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/how-sony-liv-built-real-time-video-streaming-analytics-with-aws/) · **게시일**: 2026-09-10

## 개요

Sony LIV는 대규모 동영상 스트리밍 서비스에서 사용자 행동과 콘텐츠 성과를 빠르게 이해하기 위해 실시간 분석을 필요로 했다. 기존 배치 처리는 데이터가 발생한 뒤에야 인사이트를 제공했고, 이는 개인화, 장애 탐지, 콘텐츠 의사결정에 제약을 줬다. AWS 기반 스트리밍 분석 아키텍처는 ingest, processing, storage, consumption 단계를 분리하여 이벤트를 실시간으로 수집하고 변환한 뒤 serving layer로 전달함으로써 배치가 갖던 지연을 줄였다. 설계의 핵심은 확장성과 운영 안정성을 simultanously 충족하는 것이었다.

이 사례는 기술 도입만으로 성능이 얻어지지 않는다는 점도 보여준다. Sony LIV는 아키텍처 도입과 함께 운영 지표와 cost-benefit 측면을 모두 고려해야 했고, 단계적 개선을 통해 real-time insights를 비즈니스 의사결정에 활용했다. streaming analytics는 개인화 추천과 시스템 모니터링에 직접 연결되어, 콘텐츠 전략과 운영 안정성 개선에 기여했다.

## 핵심 내용

- Sony LIV는 배치 중심 분석에서 실시간 스트리밍 분석으로 전환했다.
- architecture는 데이터 ingest, processing, storage, consumption을 분리하여 지연을 줄인다.
- real-time analytics는 personalization, incident detection, business decision-making에 활용된다.
- 확장성과 안정성이 설계의 주요 요구사항이다.
- streaming event data는 비용과 운영 복잡도까지 함께 고려해야 한다.
- future innovations는 지속적으로 분석 coverage를 확장하려는 의도를 보여준다.

## 비즈니스 영향과 후속 방향

실시간 분석은 사용자의 시청 패턴을 더 빠르게 반영해 content acquisition과 product experience 결정을 가속했다. streaming pipeline 도입은 legacy batch job과 병행하여 운영 risk를 줄이는 방식으로 추진되었고, 점진적으로 더 많은 use case를 online 분석으로 옮길 수 있는 기반을 만들었다. 지속적으로 analyze, optimize, monitor의 feedback loop을 만들면 analytics maturity가 올라가고 engineering cost도 점차 예측 가능해진다.

## 참고

- Source: [How Sony LIV built real-time video streaming analytics with AWS](https://aws.amazon.com/blogs/big-data/how-sony-liv-built-real-time-video-streaming-analytics-with-aws/)