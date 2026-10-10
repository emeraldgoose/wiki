---
title: "Harness-of-Harness: Multi-Day Autonomous Software Development with Continual Improvement"
description: '하네스 위 하네스 — 3 반복 +52.25%, 70+ 반복 FPS 게임'
tags: [source, paper, huggingface, ai-engineering, ko]
locale: ko
source_url: "https://arxiv.org/abs/2609.01481"
arxiv_id: 2609.01481
---

# Harness-of-Harness: Multi-Day Autonomous Software Development with Continual Improvement

**arXiv**: 2609.01481 | **게시일**: 2026-09-01 | **기관**: 

**저자**: Haoyang Yan, Min-le Su, Hangfan Zhang, Zhanhao Li, Chen Zhang, Shao Zhang, Yang Chen, Lei Bai, Shuyue Hu

## 핵심 기여

- **Harness-of-Harness (HoH)**: 기존 코딩 에이전트 하네스 위에서 계획-코딩-테스트 반복 루프를 돌려 복구와 역량 성장을 균형
- **설계 규칙**: 작고 검증 가능한 증분, 구현 테스트와 독립 평가의 분리, 워크플로 강제 대신 검증 가능한 산출물 제약, 산출물·도구·스킬 점진 노출, 재생성보다 재사용, 버전 관리 프로젝트 기록
- **수일 자율 데모**: 70+ 반복으로 플레이 가능한 FPS 게임 구축 (스토리·메커닉·비주얼·오디오)

## 방법론

3종 하네스-모델 쌍(Codex+GPT-5.5, OpenCode+DeepSeek-V4-Pro, Pi+MiniMax-M3)을 GameCraft-Bench·FrontierSWE·ProgramBench에서 HoH 루프 vs 단독 하네스로 비교.

## 결과

| 발견 | 수치 |
|---|---|
| 단독 하네스 대비 평균 상대 이득 | 3 반복 후 **+52.25%** |
| 최대 이득 | **+82.86%** |
| 일관성 | 3쌍 전부 이득 |
| 지구력 | 70+ 자율 반복으로 일관 FPS 게임 |

## SW 엔지니어를 위한 시사점

코딩 에이전트에 버전 기록·분리 평가 게이트·작은 증분의 바깥 루프를 씌우세요 — 단발 생성이 아니라 하네스 단위 반복이 이깁니다. 워크플로가 아니라 *산출물*을 제약(검증 가능)하세요. 논문 링크: https://github.com/Flesymeb/HarnessOfHarness, https://flesymeb.github.io/HarnessOfHarness/

## 관련 개념

- [에이전트](../../concepts/ai-engineering/agent.md)
- [LLM 훈련](../../concepts/ai-engineering/llm-training.md)

## 참고

- 원문: https://arxiv.org/abs/2609.01481
- HF Daily Papers: https://huggingface.co/papers/2609.01481
- 범위: 초록 기반. 벤치별 표는 전문에서 확인
