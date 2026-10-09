---
title: "RRSI: Regularized Recursive Self-Improvement of Agent Harnesses"
description: "RRSI는 에이전트 하네스의 재귀적 자기 개선을 제안·선택 양면에서 정규화하여 evolve 점수를 유지하면서 분포 외 벤치마크에서 최대 4.7점 전이를 달성하고 정책 토큰을 30퍼센트 절감한다."
published: "2026-09-21"
arxiv_id: "2609.24972"
hf_url: "https://huggingface.co/papers/2609.24972"
authors: "Peng Xia, Rujun Han, Zifeng Wang, Yanfei Chen, Yufan Zhang, Yoonho Lee, Chengsong Huang, Han Yu, Zhongying CuiZhu, Yifei Ming, Huaxiu Yao, Burak Gokturk, Tomas Pfister, Chen-Yu Lee"
organization: "Google Cloud AI Research"
tags: [source, paper, huggingface, agents, agent-harness, self-improvement, regularization]
locale: "ko"
---

# RRSI: Regularized Recursive Self-Improvement of Agent Harnesses

[English version](../../../en/sources/papers/RRSI_Regularized_Recursive_Self-Improvement_of_Agent_Harnesses.md)

**arXiv**: [2609.24972](https://arxiv.org/abs/2609.24972) | **HuggingFace**: [papers/2609.24972](https://huggingface.co/papers/2609.24972) | **발행**: 2026-09-21 | **소속**: Google Cloud AI Research | **제출**: Peng Xia | **추천**: 168

**저자**: Peng Xia, Rujun Han, Zifeng Wang, Yanfei Chen, Yufan Zhang, Yoonho Lee (Stanford), Chengsong Huang (WashU), Han Yu, Zhongying CuiZhu, Yifei Ming, Huaxiu Yao (UNC-Chapel Hill), Burak Gokturk, Tomas Pfister, Chen-Yu Lee

**코드**: [github.com/google-research/rrsi](https://github.com/google-research/rrsi) · **프로젝트**: [regularized-rsi.com](https://regularized-rsi.com/)

## 초록

LLM 에이전트의 능력은 고정된 백본 모델을 둘러싼 하네스, 즉 프롬프트, 제어 흐름, 도구, 메모리, 컨텍스트 관리에 의해 크게 증폭된다. 최근 방법들은 에이전트 하네스의 컴포넌트별 편집을 반복적으로 제안·선택하면서 자동화하고 있으며, 이는 사실상 에이전트 시스템 레벨의 재귀적 자기 개선(RSI)을 확립한다. 그러나 이러한 재귀적 진화는 학습 태스크를 암기하며 과적합될 수 있어, 분포 내 큰 향상이 분포 외 벤치마크에서는 줄어들거나 사라지기도 한다. 본 논문은 하네스 자기 개선에 정규화 원리를 도입한 Regularized Recursive Self-Improvement of Agent Harnesses (RRSI)를 제시하며, 진화 후보의 제안과 선택을 제약한다. 제안자는 시간적으로 어닐링되는 예산으로 동작하여 한 후보가 묶을 수 있는 편집 수를 제한하고, 진화 이력 기반 미탐색 궤적을 장려한다. 선택자는 비평가와 가지치기 장치를 갖추어 벤치마크 특화 제안을 걸러내고, 너무 작거나 비싸거나 더 이상 유용하지 않은 변경을 제거한다. 이들 제약이 모여 벤치마크 특화 요소나 노이즈보다 재사용 가능한 에이전트 메커니즘을 선호하게 된다. 코딩, 에이전틱 워크스페이스, 엔지니어링 설계에 걸친 8개 벤치마크에서 RRSI는 진화 대상 분할에서 최대 14.1점, 5개 분포 외 벤치마크에서 최대 4.7점을 얻으면서, 비정규화 진화 대비 정책 토큰을 30% 적게 쓰는 하네스를 만든다.

## 배경과 문제 설정

현대 에이전트는 모델이 아니라 시스템이다: 고정 백본을 감싼 하네스 (시스템·태스크 프롬프트, 계획·행동·성찰·중단의 제어 흐름, 도구 인터페이스와 설명, 메모리·스킬 파일, 정책이 매 스텝 보는 것을 정하는 컨텍스트 관리)가 같은 모델이 올바른 파일을 먼저 읽고, 실패한 명령에서 복구하고, 작업 컨텍스트를 관리하고, 산출물에 결과를 쓰는지 결정한다. 최근 제품 진전은 새 가중치보다 하네스 엔지니어링에서 더 많이 나왔다 — 그러나 수동으로는 엔지니어가 읽을 수 있는 궤적 수에 진전이 묶인다. 이를 자동화하는 흐름 (Meta-Harness, AHE, TTHE, HarnessX 등)은 실용적 RSI를 만든다: 현재 시스템의 피드백으로 다음 행동을 빚는 하네스를 개선한다.

RRSI가 겨냥하는 실패 모드는 적응적 과적합이다. 매 라운드 같은 유한 evolve 집합을 재사용해 편집을 제안·선택하므로, evolve 점수는 세 가지 결합 행태로 오를 수 있다: 벤치마크 특화 피팅 (태스크명·엔티티명·판정자 환심 문구 인코딩), 노이즈 추격 (확률적 승자를 영속 상태로 승격), 복잡도 축적 (메커니즘 없이 토큰·스텝만 늘리는 편집). 선행 방법들이 정확히 이 모습을 보인다: evolve에서 크게 오르고 분포 외에서는 줄거나 사라지며, 시작 하네스 H0 아래로 끝나는 경우도 있다.

RRSI의 입장은 하네스를 완전히 편집 가능하게 두되 (프롬프트, 제어 흐름, 도구, 메모리, 서브에이전트 — 전부), 그 공간을 통과하는 탐색 궤적을 정규화한다는 것이다. 제안 측면 (한 라운드가 쓸 수 있는 적응 용량을 얼마나, 어디에 쓰는지)과 선택 측면 (어떤 측정된 개선이 영속 상태가 될 수 있는지) 모두를 제약한다.

## 방법론

에이전트를 A = (정책, H)로 형식화하고 태스크·샘플 궤적 평균으로 점수 S(H; D)와 정책 토큰 비용 C(H; D)를 측정한다. 매 라운드 t마다 Ht를 evolve 집합에 실행해 피드백 Ft를 요약하고, 후보를 제안해 같은 evolve 집합에서 평가한 뒤 argmax를 유지한다. RRSI는 제안 분포 P와 승인 규칙을 고전적 정규화의 유사체 (L0식 업데이트 희소성, Ridge식 비용 축소, Lasso식 구조 가지치기)로 제약한다.

**제안 측면.**

- *L0식 어닐링 업데이트 희소성.* 한 후보가 묶을 수 있는 독립 귀속 편집 수를 bt개로 제한하며, bt는 T 라운드에 걸쳐 bmax에서 bmin으로 코사인 어닐링한다. 초반에는 협조적 변경을 묶어 메커니즘을 발견하고, 후반에는 희소·귀속 가능하게 하여 측정된 변화가 식별 가능한 메커니즘에 매핑된다.
- *증거 인식 크레딧 할당.* 평가된 모든 후보의 컴포넌트, 가설, diff, 점수·비용 변화, 채택 여부를 기록하고 제안자가 전체 이력에 조건화한다. 기각된 메커니즘은 음성 증거로 남고 성공한 메커니즘은 명시적 크레딧을 유지한다 — 이미 반증된 가설에 용량을 재지출하지 않는다 (적응적 데이터 분석 규율).
- *구조적 탐색.* 최근 w 라운드 진전이 경험적 노이즈 밴드 δ 안에 머물면 예산 일부를 아직 건드리지 않은 컴포넌트에留保한다 (예: 프롬프트 고치기 중단, 제어 흐름·메모리 건드리기). 편집 계열에 대한 다양성·엔트로피 정규화 역할이다.

**선택 측면 (모두 비보상형 — 후보는 모든 게이트를 통과해야 한다).**

- *누출 스크리닝.* 평가 전에 비평가 LLM이 각 diff를 읽고 태스크명, 엔티티명, 태스크 특화 값·정답, 벤치마크 특화 로직, 불활성 장치를 기각한다. 일반 프롬프트·도구 개선은 통과한다. 평가 전 스크리닝이 중요한 이유: 누출 후보는 부풀려진 evolve 점수를 받을 기회조차 없어야 후속 라운드를 유혹하지 않기 때문이다.
- *안정성 인식 승인.* 진화 전 불변 베이스 하네스를 반복 평가해 경험적 노이즈 밴드 δ를 추정한다. 지금까지 최고 evolve 점수 S*가 하한을 만든다: S_hat(H') >= S* − δ를 만족해야 하며, 노이즈 크기로 오인될 만한 작은 후퇴들의 연속 하강을 막는다.
- *Ridge식 복잡도 인식 승인.* 노이즈 밴드를 넘는 향상 (ΔS > δ)에 대해서는 추가 추론 비용을 정당화해야 한다: ΔC <= β0 + β1·ΔS (ΔC는 상대 정책 토큰 변화). β0/β1은 evolve 집합에서 고정한다. 밴드 내 후보는 부록의 더 엄격한 규칙을 따른다. 특정 컴포넌트 제거를 강제하지 않고 총 자원 발자국을 축소한다.
- *Lasso식 구조 가지치기.* 고정 윈도우 동안 엄격히 양의 측정 향상을 내지 못한 컴포넌트는 후속 라운드의 삭제 대상으로 보고한다. 메커니즘은 자리를 계속 벌어야 하며, 점수 전용 진화는 쓸모없어진 것을 절대 제거하지 않기 때문이다.

보고된 실행 설정: 전 도메인 고정 정책 Claude Opus 4.8 (Gemini 3.5 Flash 복제 포함). 제안자·실패 피드백 분석자·누출 비평가 모두 Claude Opus 4.8. 베이스 하네스는 Terminus-2 (코딩), MCP 도구 게이트웨이 위 ReAct + 동적 toolbelt + ReSum식 컨텍스트 관리 (워크스페이스·설계).

## 결과

3개 도메인 8개 벤치마크. 각 하네스는 하나의 스위트에서만 진화하고 변경 없이 모든 곳에서 평가한다. 어떤 held-out 분할도 후퇴하지 않는다.

- **전체 전이.** evolve 분할 향상: Terminal-Bench 2.1 +6.0, EngDesign +4.9, Harvey LAB +1.1. 그 외에서 살아남는 것: SWE-bench Verified +1.8 (진화 중 채점된 적 없음), Harvey LAB 분포 내 held-out +2.3, 3개 분포 외 에이전틱 벤치마크 +3.5~+4.7 (7.2–13.1% 상대), Frontier-Eng +4.3 Medal 점 (+24.3% 상대).
- **에이전틱 워크스페이스 정면 비교** (동일 H0·evolve·후보 예산. H0 = evolve 89.4 / ID held-out 86.9 / JobBench 36.0 / GDPval 48.8 / APEX 34.2): 모든 선행 방법은 evolve에서 이기고 분포 외에서 무너진다 — Meta-Harness 분포 외 평균 +0.9, HarnessX 베이스와 동점, AHE·TTHE는 H0 아래 (TTHE −1.7). RRSI는 evolve 향상이 가장 작고 (90.5) 분포 외 평균이 H0를 1점 넘게 넘는 유일한 방법이다 (43.6 vs 39.7): JobBench 40.7, GDPval 52.3, APEX-Agents 37.9.
- **절제 연구** (JobBench/GDPval/APEX 분포 외 평균): 전체 RRSI 90.5 / 43.6 / 시행당 2.42M 토큰. 제안 정규화 제거 90.7 / 41.9 / 2.69M. 승인 정규화 제거 91.5 / 41.0 / 3.59M. 비정규화 92.8 / 40.3 / 3.80M. 어느 한쪽을 빼도 evolve는 오르고 전이는 떨어진다 — 정규화가 의도한 트레이드다.
- **정책 강건성.** 독립 코딩 진화: Gemini 3.5 Flash는 Terminal-Bench 64.6→78.7 (+14.1, 논문 대표 evolve 수치), SWE-bench Verified로 +2.2 전이 (76.8→79.0). Claude Opus 4.8은 74.2→80.2 (+6.0), +1.8 전이 (82.0→83.8). Gemini 3.5 Flash로 진화한 하네스는 탐색에 참여한 적 없는 약한 Gemini 3.1 Flash Lite에서도 그대로 돕는다 (11.2→14.6, +30.4% 상대) — 정책 특화 피팅이 아니라 메커니즘이라는 뜻이다.
- **효율.** RRSI는 가장 가벼운 진화 하네스다: 시행당 2.42M 정책 토큰 vs 선행 방법 3.59–3.82M (AHE는 +58% 토큰으로 분포 외 −4.4점), 시행당 26.3 스텝 vs 27.3–34.6. 미진화 H0가 여전히 가장 싸다 (1.56M, 21.2 스텝) — 진화는 향상의 일부를 테스트 타임 연산으로 산다. 예산이 얼마를 쓸지 정한다. 대표 수치: 비정규화 진화 대비 정책 토큰 30% 감소.
- **판정자 해킹 아님.** Harvey LAB·JobBench·GDPval은 판정자 채점이지만 EngDesign·Frontier-Eng는 결정적 시뮬레이터·테스트벤치 채점이다 — 향상이 거기서도 그대로 유지된다.

## 한계와 열린 질문

- 백본 가중치는 고정이며, 가중치를 함께 업데이트하는 RSI나 모델·하네스 공진화는 다루지 않는다.
- 유한 evolve 집합과 여러 하이퍼파라미터 (예산, 윈도우, β0/β1, 노이즈 밴드)에 여전히 의존하므로 피드백 신호 품질과 탐색 예산에 따라 효과가 달라질 수 있다.
- 8개 벤치마크·3개 도메인·2–3개 정책 계열에서 전이를 보였지만, существенно 다른 아키텍처·도구 생태계·더 긴 자기 개선 지평에 대한 검증은 더 필요하다.

## 소프트웨어 엔지니어를 위한 시사점

- 고정 평가 집합에 에이전트를 자동 튜닝한다면 게이트를 그대로 베껴라: 채점 전 누출 비평가, 승인 전 노이즈 밴드 하한, 비용 정당화 승인 (ΔC <= β0 + β1·ΔS), 기여를 멈춘 컴포넌트 가지치기. 각각 실제 과적합 행태 (벤치마크 피팅, 노이즈 추격, 복잡도 증가)에 대응한다.
- 라운드에 걸쳐 편집 묶음 크기를 어닐링하라: 초반 넓게 탐색, 후반 희소·귀속 가능하게. 절제 연구에서 제안 조향만으로 evolve는 거의 같은데 분포 외 +1.7점이다.
- evolve 점수가 아니라 전이를 출하하라: 논문에서 evolve 최고 하네스 (92.8)가 전이 최하 (분포 외 40.3)다. 토큰당 held-out·교차 벤치마크 수치가 가장 좋은 하네스를 출하하라 — 여기서는 그것이 가장 싼 진화 하네스이기도 하다.

## 관련 개념

- [Agent](../../concepts/ai-engineering/agent.md)
- [Agent Evaluation](../../concepts/ai-engineering/agent-evaluation.md)
- [LLM Training](../../concepts/ai-engineering/llm-training.md)

## 참고문헌

- arXiv: https://arxiv.org/abs/2609.24972
- HuggingFace: https://huggingface.co/papers/2609.24972
- 코드: https://github.com/google-research/rrsi
- 프로젝트: https://regularized-rsi.com/
