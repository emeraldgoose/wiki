---
title: "DramaChain Bench: An End-to-End Benchmark for Short-Drama Generation"
description: '숏드라마 전 단계 벤치마크 — 5,785 아이템, 에이전틱 심판 PLCC 0.918'
tags: [source, paper, huggingface, ai-engineering, ko]
locale: ko
source_url: "https://arxiv.org/abs/2609.00646"
arxiv_id: 2609.00646
---

# DramaChain Bench: An End-to-End Benchmark for Short-Drama Generation

**arXiv**: 2609.00646 | **게시일**: 2026-09-01 | **기관**: Tencent Hunyuan

**저자**: Haoyuan Shi, Mingtao Chen, Shuo Jiang, Ziyan Chen, Xuyi Sheng, Yiming Liu, Ying Zhang, Miao Wang, Jianxiang Lu, Fanyang Lu, Songyuanyi Lu, Xiele Wu, Zhichao Hu, Yuhong Liu, Richeng Xuan

## 핵심 기여

- **최초 종단 숏드라마 벤치마크**: 비디오 생성 단계만 미리 쓴 입력으로 보는 게 아니라 전 5단계(대본→스토리보드→키프레임→숏 비디오→완성본)를 평가
- **DramaChain Dimensions**: 단계마다 5개 평가축, 63개 리프 차원으로 전개. 상용 플랫폼에 보정한 DramaChain Agent로 단계별 공정 비교
- **라벨링 시스템**: 5,785 아이템 × 전문 어노테이터 3인 → 17,488 유효 점수 + 255,925 추적 귀속 기록. 결함을 시공간 국소화·사전 정의 목록에서 선택
- **Agentic Judge**: 체크리스트 대비 다라운드 근거 수집 후 판정. 인간 순위와 평균 PLCC 0.918로 재현 — 신규 모델을 주석비 0에 진입

## 방법론

각 단계에 실제 상류 파이프라인 산출을 투입(미리 쓴 입력 아님). 원본 대본 의도 준수와 멀티에피소드 조립 후 숏 일관성이라는 두 질문에 답. 인간 주석을 기준으로 에이전틱 심판의 순위 상관을 검증.

## 결과

| 발견 | 수치 |
|---|---|
| 주석 규모 | 5,785 아이템, 17,488 점수, 255,925 귀속 |
| 핵심 실증 | 상류 결함이 파이프라인으로 전파 — 최종 품질은 비디오 생성 단독이 아님 |
| 에이전틱 심판 충실도 | 인간 순위 대비 평균 PLCC **0.918** |

## SW 엔지니어를 위한 시사점

생성 파이프라인은 단계별 즉시 프롬프트가 아니라 원본 의도 기준으로 단계별 평가하세요 — 상류 드리프트가 최종 품질을 지배합니다. 체크리스트+다라운드 근거 심판(PLCC 0.918)은 신규 모델 저비용 신뢰 평가의 재사용 레시피입니다.

## 관련 개념

- [에이전트 평가](../../concepts/ai-engineering/agent-evaluation.md)
- [에이전트](../../concepts/ai-engineering/agent.md)

## 참고

- 원문: https://arxiv.org/abs/2609.00646
- HF Daily Papers: https://huggingface.co/papers/2609.00646
- 범위: 초록 기반. 차원 정의는 전문에서 확인
