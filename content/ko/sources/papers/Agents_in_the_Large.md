---
title: "Agents in the Large: Perception-Centered Architecture for Persistent Agents"
description: '장수 에이전트용 Pera 아키텍처 — 지각에서 수명주기 태스크로. 수치 없는 프레임워크 논문'
tags: [source, paper, huggingface, ko]
locale: ko
source_url: "https://arxiv.org/abs/2608.30478"
arxiv_id: 2608.30478
---

# Agents in the Large: Perception-Centered Architecture for Persistent Agents

**arXiv**: 2608.30478 | **게시일**: 2026-08-31 | **기관**: Fudan University

**저자**: Shihan Dou, Haoxiang Jia, Shichun Liu, Feng Chen, Chenhao Huang, Yujiong Shen, Shaofan Liu, Jiayi Chen, Jiahang Lin, Honglin Guo, Qianyu He, Minghao Guo, Ziyi Ye, Pluto Zhou, Tao Gui, Qi Zhang, Xuanjing Huang

## 핵심 기여

- **Pera(지속 에이전트용 지각 중심 아키텍처)**: 에피소드 실행·내부 컨텍스트·환경 변화에서 서비스 관련 신호를 지속 지각하는 지각/제어 컴포넌트 중심 조직. 신호에서 수명주기 태스크를 만들어 서비스 절차의 운영·적응을 주도
- Pera 렌즈로 기존 연구를 회고 정리 + 상세 사례 연구 + 향후 구축 지침
- 프레이밍: 소프트웨어 공학이 small→large 프로그래밍으로 갔듯, 언어 에이전트도 장수·적응 지능으로 같은 전이를 겪는 중

## 방법론

개념 아키텍처 논문(벤치 표 없음). 지속 지원을 목표 설정로 정의(요구·컨텍스트·절차가 유지·변화)하고, 지각 신호에서 수명주기 태스크를 도출해 기존 시스템과 사례를 재서술.

## 결과

정량 결과 없음 — 프레임워크/포지션 기여입니다. 검증 가능한 내용은 Pera 분해(지각→수명주기 태스크→서비스 절차 적응)의 사례·기존 연구 적용입니다.

## SW 엔지니어를 위한 시사점

세션 넘나드는 에이전트(메모리·변화 절차·반복 사용자)를 운영한다면 Pera 체크리스트: 무엇을 지각하는지, 무슨 수명주기 태스크를 만드는지, 서비스 절차가 어떻게 적응하는지. 지각 루프를 먼저 설계하세요. bounded-task 하네스는 저절로 지속 지원이 되지 않습니다.

## 관련 개념

- [에이전트](../../concepts/ai-engineering/agent.md)
- [LLM 훈련](../../concepts/ai-engineering/llm-training.md)

## 참고

- 원문: https://arxiv.org/abs/2608.30478
- HF Daily Papers: https://huggingface.co/papers/2608.30478
- 범위: 프레임워크 논문. 인용 수치는 없음
