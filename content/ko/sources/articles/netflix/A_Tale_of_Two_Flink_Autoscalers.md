---
title: "A Tale of Two Flink Autoscalers"
description: 3만 개 Flink 잡 함대를 사내 외부 관측 오토스케일러에서 오픈소스 Flink 오토스케일러로 전환한 과정
tags: [source, article, netflix, stream-processing, apache-flink, autoscaling, kubernetes, ko]
locale: ko
source_url: "https://netflixtechblog.com/a-tale-of-two-flink-autoscalers-e9f6a1b1492b"
blog: netflix
published: 2026-08-21
---

# A Tale of Two Flink Autoscalers

넷플릭스는 2017년부터 Flink를 운영하며 2026년 기준 3만 개 이상 잡(대부분 Data Mesh 생성, 일부 상태 저장 커스텀 잡)을 다룬다. 피크 기준 프로비저닝은 낭비, 평균 기준은 서지 시 지연, 상태 저장 잡의 리스케일은 수 분 소요. 사내 1세대 오토스케일러와 오픈소스 2세대를 병행 운영하며 후자로 수렴 중이다.

## 배경: 1세대(사내) 오토스케일러

2019년경 Mantis 기반 구축. Atlas 텔레메트리(클러스터 CPU·네트워크·Kafka 랙 등)로 TaskManager 총수를 조절해 수천 개 파이프라인에서 리소스 25–45% 절감. 한계: 거친 컨테이너 지표로 클러스터 전체를 하나의 노브로 조절해 다중 오퍼레이터 상태 저장 DAG에 부적합했고, 외부 지표가 실제 병목을 놓치는 경우(CPU에 안 잡히는 busy, 네트워크 마이그레이션으로 깨진 지표)가 있었다.

## 방법론: 2세대(오픈소스) 오토스케일러

잡 "내부"에서 추론한다. 핵심은 오퍼레이터별 진짜 처리율(TPR) = 관측 처리량 ÷ busy 비율(예: 700 rec/s @ busy 70% → TPR 1,000 rec/s). 소스부터 그래프를 따라 TPR·입출력 비율·목표 utilization으로 정점별 병렬도를 계산해 병목 없는 크기를 구한다. 상태 저장 다중 오퍼레이터 잡을 정밀 조절하고 잡별 설정이 가능하다.

**넷플릭스 규모 적용.** Flink K8s Operator가 아닌 자체 컨트롤 플레인 위에서 동작하므로, 커뮤니티의 독립 라이브러리 리팩터(컨텍스트·상태 저장소·이벤트 핸들러·realizer)를 연동. Temporal 오케스트레이션의 Spring Boot 서비스가 ~1분마다 폴링하고 잡별 durable 워크플로로 격리(초기 단일 배치 루프의 연쇄 장애 교훈). 세 가지 갭 해소: JobManager 지표 수집 3,000 서브태스크까지(지표명 캐싱·서버사이드 필터링, 일부 업스트림 기여 FLINK-36172), forward 연결 서브그래프 단위 스케일(무시하면 네트워크 셔플로 조용히 전환), 비동기 싱크 배압 감지(포화 싱크로 스케일업 방지). Realizer 안전 검사(리전 대피 중 스케일다운 금지, 체크포인트 디스크 검증, 대기 버퍼).

## 결과

- 커스텀 잡 GA. 예: 텔레메트리/로깅 팀 연간 Flink 비용 ~58% (~110만 달러) 절감 — 일간 사이클 추종, 지속적 라이트사이징, 균일 컨테이너의 촘촘한 빈패킹.
- 안정성 선택: 목표 utilization 0.45(커뮤니티 기본 0.7보다 보수적) — 대형 상태 저장 잡은 적고 차분한 리스케일이 이득.
- 남은 병목은 스케일러 로직이 아니라 Flink 코어 상태 복구. Flink 2.2 분리 상태(disaggregated state) 백엔드 실험 예정.

## 한계·열린 질문

- 상태 저장 잡의 재시작+상태 복구 비용은 여전하고 스케일러 품질의 상한이다.
- Utilization 목표는 워크로드별 경험적 튜닝이 필요하다.
- 사내 스케일러 사용처 전체 이전은 진행 중.

## SW 엔지니어 시사점

- 알고리즘보다 지표 선택이 먼저다. 무엇을 신뢰할지부터 디버깅하라.
- 플랫폼 기본값 + 잡별 오버라이드, 전문 노브는 숨겨라.
- Adopt-then-extend: 신규 워크로드는 커뮤니티 프로젝트로, 수정은 업스트림 기여, 점진 이전.
- 제어 루프는 테넌트별 격리(잡별 워크플로) — 문제 잡 하나가 함대를 멈추지 않게.

## 관련 개념

- `concepts/data-engineering/stream-processing.md`
- `concepts/data-engineering/apache-spark.md`
