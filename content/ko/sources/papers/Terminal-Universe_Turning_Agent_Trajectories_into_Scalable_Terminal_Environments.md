---
title: "Terminal-Universe: 에이전트 궤적에서 확장 가능한 터미널 환경으로"
description: "HuggingFace Daily Papers — 2026-09-03 — 에이전트 궤적에서 실행 가능한 터미널 환경을 복원"
tags: [source, paper, huggingface]
locale: ko
arxiv_id: 2609.04148
published: 2026-09-03
---

# Terminal-Universe: 에이전트 궤적에서 확장 가능한 터미널 환경으로



**arXiv**: [2609.04148](https://arxiv.org/abs/2609.04148) | **HuggingFace**: [papers/2609.04148](https://huggingface.co/papers/2609.04148) | **Published**: 2026-09-03 | **제출**: taesiri | **Paper of the day #2 (2026-09-04)**

**저자**: Jie Wu, Zhenru Zhang, Beichen Zhang, Xuwu Wang, Yuhui Su, Mouxiang Chen, Peng Wang, Zhihai Wang, Que Shen, Hao Zhou, An Yang, Fei Huang, Yujiu Yang, Dayiheng Liu (Qwen Team, Alibaba Group; Tsinghua University)

## 초록

터미널 기반 코드 에이전트가 확산되면서 에이전트 궤적(trajectory)은 대규모로 쌓였지만, 사실적이고 실행 가능한 환경(environment)은 여전히 희귀하다. 그런데 에이전트 사후학습(post-training)에 실제로 필요한 것은 환경이다. 하나의 환경은 검증 가능한 많은 태스크로 재질의(re-query)될 수 있고 실행 피드백을 제공하지만, 궤적은 하나의 고정된 시연에 불과하기 때문이다. Terminal-Universe는 통상의 방향을 뒤집는다. 궤적에서 환경을 rollout하는 대신 궤적에서 환경을 복원한다. 궤적에 기록된 도구 실행 이력(읽기·쓰기·편집)이 그 궤적이 실행된 환경의 구조와 내용을 드러낸다는 관찰에 근거한다. 프레임워크는 기록된 파일 연산을 replay하여 각 파일을 에이전트가 수정하기 이전 상태로 되돌리고(부분 workspace), 이어서 completion 에이전트가 누락된 파일과 의존성을 채운다. 복원된 workspace마다 원래 의도 태스크를 복원하고 완전히 새로운 태스크를 합성하며, 두 축으로 확장한다. 넓이(breadth)는 채굴된 의존 관계를 이용한 다중 코드베이스 횡단 질의이고, 깊이(depth)는 사용자 에이전트로 단일턴 질의를 다중 라운드 세션으로 확장한 것이다. 공개 터미널 에이전트 궤적에 적용하여 **37.3k개의 태스크-충분(task-sufficient) 환경**을 얻었으며, 이 코퍼스로 Qwen3.5-27B를 지도 미세조정(SFT)하자 **Terminal-Bench 2.1이 11.9점, EvoCode-Bench v2 MT@4가 13.8점** 향상되었다.

## 배경: 문제 설정 (WHY)

사후학습 관점에서 궤적과 환경은 동등하지 않다. 궤적은 고정된 기록이다. 생성한 정책 모델의 품질에 상한이 묶이고, 코드베이스 변경이 실제로 옳았는지 확인할 방법이 없다. 환경에는 이런 제약이 없다. 같은 태스크를 더 강한 모델로 다시 풀 수 있고, 테스트로 결과를 검증할 수 있으며, 같은 workspace에 더 어려운 태스크를 얹을 수 있다. Terminal-Bench 같은 전문가 벤치마크가 황금 표준을 보여준다(태스크마다 전용 컨테이너 + 지시 + 실행 가능한 verifier). 그러나 그 신뢰성은 수작업에서 오므로 태스크 수에 한계가 있고, 사후학습에 필요한 환경 수는 수작업으로 감당할 수 없다.

기존 연구는 실행 가능한 환경을 세 가지로 확장했으며, 본 논문은 모두와 대비된다(Table 1): (1) **저장소 기반**(SWE-Gym, R2E-Gym) — git으로 과거 수정 이전 상태로 되돌린다. 사실적이지만 가용한 이력에 묶인다. (2) **교란 기반**(SWE-smith, CLI-Gym) — 통과하던 저장소에 버그를 주입한다. 적은 저장소에서 많은 태스크를 얻지만 전부 수정(repair) 태스크이다. (3) **태스크-조건 합성**(Endless Terminal, TMax, CLI-Universe, SkillSynth) — 분류 체계나 시드에서 태스크와 환경을 함께 생성한다. 제어 가능하지만 실제 프로젝트와 무관하므로 작고 정돈된 workspace가 나온다. 기존 보고 규모는 3.2k~37.5k 태스크이며 다중 라운드와 다중 workspace 합성을 모두 갖춘 것은 없다. Terminal-Universe(37.3k 환경, 32.0k 태스크, verifier ✓, multi-round ✓, cross-workspace ✓)가 세 가지를 모두 갖춘 유일한 항목이다.

## 방법론 (HOW)

### 핵심 반전: 궤적–환경 쌍대성

궤적과 환경은 같은 에피소드의 두 관점이다. 기존 연구는 환경 → 궤적(rollout)으로 가지만, Terminal-Universe는 역방향(복원 + 재사용)이다. 도구 호출이 이미 workspace를 드러낸다. `Read`는 파일 내용을, `Write`/`Edit`는 변경 내역을 보여준다. 복원은 본질적으로 손실적이다(건드리지 않은 파일, 암묵적 시스템 의존성, 네트워크 자원은 흔적이 없다). 그래서 세 단계로 복원한다.

### 1단계 — 결정적 replay

궤적의 read·write·edit 연산을 시간순으로 replay하여 경로별 earliest/latest 파일 내용을 복원한다. 재구성된 초기 workspace는 각 기존 파일을 **에이전트의 첫 변경 이전 earliest 관측 버전**으로 모으고, 에이전트가 만든 파일은 제외하며 에이전트의 편집은 이후 검증을 위해 따로 기록한다. 궤적은 건드린 경로만 드러내고(내용이 잘릴 수도 있음) 결과는 **부분 workspace**이다.

### 2단계 — 에이전트 completion

completion 에이전트가 부분 workspace와 복원된 태스크를 받아 누락 파일을 만들고, 부분 파일을 완성하며, 필요한 의존성을 복원한다. **해답을 구현하지는 않는다**. 모든 replay workspace에 적용된다.

### 3단계 — 환경 필터링

복원된 태스크를 뒷받침할 프로젝트 맥락이 충분한 workspace만 유용하다. 읽기 전용 shell/파일 도구를 가진 에이전트 judge가 각 workspace를 복원 태스크 기준으로 sufficient/insufficient으로 판정(소스·설정·데이터·구조)하고, 충분한 것만 이후 태스크 생성에 쓴다. 모든 workspace는 **네트워크 접근이 가능한 표준 Ubuntu 24.04 컨테이너**에서 실행된다. 저장소별 이미지보다 저렴하고 단순하며, resolve율의 소폭 하락이 대가이다(Zeng et al., 2026).

### 재질의: 네 가지 메커니즘

- **Intent Recovery.** 원천 사용자 요청을 자족적 태스크로 통합한다. 단일 라운드 궤적은 유일한 실질 요청을 그대로 쓰고, 다중 라운드 궤적은 첫 실질 요청을 주제로 삼고 이후 요청은 같은 태스크를 명확화·제약·확장할 때만 포함한다. 에이전트 행동과 파일 근거는 해석 보조용이며, 사용자가 명시한 요구사항만 남긴다.
- **Single-WS 합성.** 오프라인 생성기가 각 workspace를 살펴 groundedness·구조적 다양성·검증가능성 제약 하에 **후보 태스크 5개**를 합성하고, 환경당 유효 후보 하나를 rollout·검증에 쓴다.
- **Cross-WS 합성 (넓이).** 에이전트가 각 workspace의 도메인과 구현 역량을 프로파일링하고, **TF-IDF 최근접 이웃 검색**으로 후보 쌍을 찾은 뒤 LLM judge가 target workspace에 없고 reference workspace에 있는 역량의 **방향성 의존 간선**을 판별한다. 쌍당 정확히 하나의 태스크: 쓰기 가능한 target + 별도 경로에 읽기 전용으로 마운트된 reference. 질의는 target의 관측 가능한 동작과 reference 마운트 경로만 주고 reference 내부는 주지 않으므로, solver가 reference 구현을 스스로 탐색·내재화·적응해야 한다(예: 프로젝트 간 기능 이식).
- **Multi-Round 세션 (깊이).** 초기 응답 뒤 사용자 에이전트가 세션을 잇는다. (1) **요구사항 tracker**(active/satisfied/updated)가 라운드마다 제약을 추가·수정·교체하고, (2) **라운드 단위 검증** — 갱신된 명세를 커밋하면 자동 verifier가 코딩 에이전트 행동 전에 승인 테스트를 작성하고, solver는 테스트 스크립트·traceback과 엄격히 격리된다. 사용자 에이전트는 구조화된 실패를 자연스러운 사용자 불만으로 번역하며, 중간 실패는 대화 기록에 남아 오류 진단·복구 감독 신호가 된다.

### 검증

모든 신규 태스크는 컨테이너 안에서 에이전트가 작성한 verifier와 함께 출고되며, **테스트를 전부 통과한 궤적만 남긴다**. 모방 품질이 아니라 실행 피드백이 선택 기준이다.

## 결과

- **규모.** 공개 터미널 에이전트 궤적에서 태스크-충분 환경 37.3k개, 태스크 32.0k개. 이 환경들에 새 질의를 생성하고 **Qwen3.7-Max를 teacher**로 삼아 해답 rollout을 만든다.
- **사후학습 효과.** 코퍼스로 **Qwen3.5-27B**를 SFT하자 동일 베이스 대비 **Terminal-Bench 2.1 단일 라운드 +11.9점, EvoCode-Bench v2 다중 라운드(MT@4) +13.8점**.
- **Ablation.** 각 요소가 기여하며, 특히 **복원 환경에서 태스크를 다시 푸는 것이 원시 궤적 모방을 크게 앞선다**. 즉 가치 있는 자산은 시연이 아니라 환경이다. 궤적 복잡도와 rollout 복잡도가 상관되고(다중 파일 편집·긴 도구 체인이 workspace 상태를 더 드러내면 더 다양하고 어려운 태스크가 나온다), 같은 workspace의 다중 세션을 함께 replay하면 단일 궤적 복원보다 복잡한 환경이 나온다. 즉 더 강한 에이전트가 더 풍부한 궤적을 만들수록 프레임워크가 자연히 확장된다.

## 한계 / 열린 질문

- **범용 컨테이너.** 저장소별 환경(SWE-Factory, RepoLaunch 방식)이 아닌 표준 Ubuntu 24.04 이미지 — 특수 시스템 의존성이나 복잡한 빌드가 필요한 edge case의 재현도가 떨어진다.
- **원천 궤적에 묶인 분포.** 복원 workspace의 도메인·언어·툴체인 분포는 수집된 궤적의 범위를 넘을 수 없다.
- **단일 teacher.** 태스크·해답·verifier를 하나의 teacher(Qwen3.7-Max)가 만든다. 역량 공백이 커버리지를 제한하고 해답 오류가 자체 테스트를 통과할 수 있다. 다중 teacher와 독립 verifier 모델이 향후 과제이다.

## 소프트웨어 엔지니어와의 관련성

- **저장소가 아니라 에이전트 로그를 캐라.** 터미널 코딩 에이전트를 어느 정도 규모로 돌린다면 그 궤적은 잠재적 환경이다. 파일 연산의 시간순 replay → earliest 버전 workspace → 해답 누출 없는 에이전트 completion → 충분성 필터라는 replay 레시피를 내부 사후학습 코퍼스 구축에 그대로 쓸 수 있다.
- **모방이 아니라 검증.** 핵심 ablation의 메시지: 원시 궤적 SFT는 약하고 verifier로 걸러낸 재풀이 rollout이 강하다. 학습 데이터는 teacher 명성이 아니라 실행 가능한 테스트로 걸러라.
- **저장소 횡단 태스크가 사실성 격차이다.** 단일 저장소 벤치마크는 가장 흔한 실제 워크플로(reference 구현 읽기 → 이식·적응)를 과소평가한다. target 쓰기 + reference 읽기 전용 마운트 패턴은 어려운 평가를 만드는 저렴한 틀이다.
- **다중 라운드 하네스 패턴.** 요구사항 tracker + 행동 전 승인 테스트 + solver/테스트 격리 + 실패-불만 번역은 실감 나는 대화형 평가·학습 세션의 구체적 설계이다.
- **쓰지 말아야 할 곳.** 복원 workspace를 빌드 민감 작업의 충실한 저장소 복제로 취급하지 마라. 범용 이미지와 손실 replay 때문에 시스템 단 edge case는 재현되지 않을 수 있다.

## 관련 개념

- `concepts/ai-engineering/agent.md`
- `concepts/ai-engineering/llm-training.md`
- `concepts/machine-learning/transformer.md`

## 참고문헌

- arXiv: https://arxiv.org/abs/2609.04148
- HuggingFace: https://huggingface.co/papers/2609.04148
- 관련: SETA (https://huggingface.co/papers/2607.10891), Endless Terminal / TMax / CLI-Gym / CLI-Universe / SkillSynth (논문 Table 1 참조)
