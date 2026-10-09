---
title: "In-House LLM Serving at Netflix"
description: vLLM+Triton 자사 LLM 스택 — 엔진 선정, 모델 패키징, OpenAI 호환 API, 버전별 배포, 제약 디코딩
tags: [source, article, netflix, llm, model-serving, platform-engineering, ai-engineering, ko]
locale: ko
source_url: "https://netflixtechblog.com/in-house-llm-serving-at-netflix-a5a8e799ea2c"
blog: netflix
published: 2026-07-17
---

# In-House LLM Serving at Netflix

AI Platform Model Runtime·Inference 팀. 호스티드 API 소비를 넘어 배포부터 추론까지 전체 LLM 스택을 기존 프로덕션 환경 안에서 직접 운영한다. 쟁점이 된 선택 — 엔진 선정, 모델 패키징, API 표면, 배포 전략, 출력 제약 강제 — 과 설계 단계에 안 보이던 프로덕션 교훈이 주제다.

## 배경: 아키텍처

JVM 기반 통합 서빙 시스템이 회원 규모 ML의 앞단: 라우팅/A-B, 후보 생성, 피처 조회, 추론, 후처리, 로깅, 실시간+캐시 배치 경로. 소형 CPU 모델은 인프로세스, 대형은 원격 Model Scoring Service(MSS) — XGBoost/TF/PyTorch/LLM 공용 백엔드, 밑단은 NVIDIA Triton + Java 컨트롤 플레인(배포·버전·헬스·오토스케일·멀티리전).

## 방법론: 의존 순서의 네 가지 결정

**기본 엔진으로 vLLM.** 원래 TensorRT-LLM이었으나 2025년 여름 워크로드(임베딩·프리필 전용 랭킹/검색·자회귀 디코딩·커스텀 제약 로직)와 오픈소스 격차 축소로 재벤치마크. 컴파일 없는 커스텀 아키텍처, 커스텀 디코딩 확장 훅, 디버깅 용이, 연구→프로덕션 이관 비용이 선정 이유.

**패키징: Python 백엔드 대신 vLLM 백엔드.** Python 백엔드는 입출력 텐서 스펙을 패키징 시점에 고정해 프론트엔드 업그레이드마다 협조 변경이 필요하지만, vLLM 백엔드는 가중치+토크나이저 JSON에서 배포 시점에 스펙을 동적 생성 — 모델과 프론트엔드가 독립 진화. 주의: Triton/vLLM 버전 드리프트는 백엔드 로딩 전체 실패로 이어지므로 버전 핀 + 작성자 오버라이드 금지. 커스텀 전후처리 모델은 Python 백엔드의 execute() 제어가 여전히 필요하다.

**생태계 호환 HTTP 프론트엔드.** 모든 모델은 같은 gRPC 호출로 스코어(공유 클라·헬스·파이프라인)하되, 사실상 표준인 OpenAI 호환 API를 병행 노출(NVIDIA Triton OpenAI 프론트엔드 + FastAPI, Java 컨트롤 플레인용 KServe 유지). 호스티드 → 파인튜닝 자사 모델 전환이 거의 매끄럽다. 함정 수정: response_format이 vLLM 도달 전 조용히 누락되어 malformed JSON 무에러 반환 — git-subtree 후 요청 시점에 guided decoding 파라미터로 번역하도록 패치.

**배포: Red-Black vs Versioned.** Red-Black(병렬 배치·단계 전환·원자 롤백)은 I/O 스키마 변경 시 깨진다: 소비자가 모델 완전 활성화 전 설정을 못 바꾸어 구 요청이 신 배포에 닿아 실패. Versioned((modelId, modelVersion)별 독립 배포, 준비 후 소비자 전환, 유휴 후 정리)는 GPU 비용 일시 증가로 갭 해소. 권장: 가변 설정(텐서 형상)을 모델에 내장해 Red-Black 유지, Versioned는 불가피한 breaking 변경에만.

**운영 세부.** 부팅: S3/HF 직접 다운로드 대신 공지 시점에 FSx에 구체화(콜드스타트 bound), 배포별 임베디드/독립 Triton, entry_points 플러그인, 준비 전 gRPC 차단. 관측: Triton 9개뿐인 브리지를 보완하는 경량 HTTP 프록시로 vLLM 멀티프로세스 지표와 합쳐 단일 /metrics.

**규모의 제약 디코딩.** 비즈니스 제약을 디코드 루프 안 상태머신(요청별, 토큰 허용 마스크 방출, vLLM 커스텀 logits 프로세서)으로 강제. V0 순수 Python 요청별 구현은 CPU/GIL 바운드(배치에 선형 증가 — 단일 요청 벤치에 안 보임). V1 배치 단위 처리 + C++ 멀티스레드 핫패스로 배치 증가에 평탄. 경화: 청크 프리필의 부분 프리필 내부 추적, KV 선점 시 토큰 히스토리 비단조 축소 감지 후 상태머신 리셋.

## 결과

실험→프로덕션 고속 경로의 통합 vLLM+Triton 플랫폼. 교훈은 디테일(버전 핀, 조용한 API 갭, 패키징 트레이드오프)에 집중. 다음: 시스템 프롬프트 압축, V1 비동기 스케줄링, GPU 융합 벡터화 logits 프로세서, 저정밀 변형.

## 한계·열린 질문

- Triton↔vLLM 버전 핀은 업그레이드마다 운영 toil이다.
- 선점/프리필 엣지케이스의 상태머신 처리는 미묘하게 틀리기 쉽다.
- GPU 벡터화 프로세서·비동기 스케줄링은 미측정 향후 과제.

## SW 엔지니어 시사점

- LLM을 특별 취급하지 마라: 같은 서빙 경로·클라·배포 파이프라인을 재사용하라.
- 엔진은 범용 리더보드가 아니라 *자신의* 워크로드 믹스로 벤치마크하고 디버깅·이관 비용을 따져라.
- 아티팩트 진화와 프론트엔드 진화를 분리(동적 I/O 스펙)하지 않으면 영원한 협조 릴리스 세금을 낸다.
- 현실 동시성에서 부하 시험하라 — 요청별 직렬 병목은 단일 요청 벤치에 안 보인다.

## 관련 개념

- `concepts/ai-engineering/rag.md`
- `concepts/system-design/scalability.md`
