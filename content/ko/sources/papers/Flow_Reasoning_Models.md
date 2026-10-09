---
title: "Flow Reasoning Models: Turning Flows Into Efficient Recurrent Reasoners"
description: "Flow Reasoning Models는 discrete flow 언어 모델을 self-conditioning으로 recurrent reasoner로 바꾸고 Fixed-Point Forcing으로 안정화; Sudoku-Extreme 99.5퍼센트, 44배 적은 FLOPs"
tags: [source, paper, arxiv, flow-models, reasoning, diffusion, test-time-scaling]
locale: ko
arxiv_id: 2606.29150
published: 2026-08-28
---

# Flow Reasoning Models: Turning Flows Into Efficient Recurrent Reasoners

**arXiv**: [2606.29150](https://arxiv.org/abs/2606.29150) (v2 기준 작성; v3는 제목만 변경, 내용 동등) | **HuggingFace**: [papers/2606.29150](https://huggingface.co/papers/2606.29150) | **발표**: 2026-08-28 (v1: 2026-06-28) | **저자**: Alec Helbling*, Andrey Bryutkin* (공동 제1저자), Mauro Martino, Duen Horng (Polo) Chau, Nima Dehmamy, Hendrik Strobelt — MIT-IBM Computing Research Lab, IBM Research, Georgia Tech, MIT | **라이선스**: CC BY 4.0

## 리드 요약

구조적 추론(Sudoku, Zebra 퍼즐, 미로)은 전역적으로 일관된 해에 도달할 때까지 상호 의존적인 결정을 만들고 고쳐야 한다. 자기회귀 모델은 고정된 순서로 토큰을 확정해서 번복이 안 되고, 마스크드 디퓨전 모델은 병렬 예측은 되지만 같은 스텝의 업데이트끼리 서로를 조건으로 삼지 못한다. Flow Reasoning Models(FRM)는 세 번째 길을 택한다. 모든 토큰을 함께 디노이징하는 discrete flow 언어 모델에서 출발해, 디노이저를 자신의 과거 출력에 self-conditioning함으로써 **recurrent refinement 축**을 추가한다. 핵심 기술 기여인 **Fixed-Point Forcing(FPF)**은 recurrence를 망치는 exposure bias를 고친다. 모델 자신의 rollout dynamics가 만든 상태(carry)로 학습하되 표준 flow-matching 목적식은 그대로 두므로 시간 역전파(BPTT)가 필요 없다. 결과는 Sudoku-Extreme 99.5%, Zebra 100.0%, Maze-Unique 99.9%이며, 차선책의 최고 기록과 동률을 **44배 적은 inference FLOPs**으로 달성한다. 수렴 자체가 정답의 거의 완벽한 예측자가 된다(AUROC 1.00).

## 초록 (전체 범위)

논문은 구조적 추론을 조건부 생성으로 정식화한다. 문제 명세 $c$(Sudoku 단서, 미로 배치)가 주어지면 이산 해 $y$를 생성한다. 소박한 discrete flow(저자들의 FLM 베이스라인)는 Sudoku-Extreme의 약 13%만 푼다. FRM은 매 clean 예측을 다음 스텝에서 다듬을 상태로 되먹임해서, 현재 후보 해로 직접 디코딩되는 해석 가능한 recurrent state를 만든다. 학습 효율적인 recurrence라 BPTT 없이 정식 flow-matching 손실이 유지된다. Self-conditioning만으로 Sudoku-Extreme이 약 13%에서 약 33%로 오르지만 대부분은 여전히 못 푼다. 역학계 관점에서 이유가 드러난다. recurrence는 학습된 fixed-point iteration인데, 기존 self-conditioning은 **spurious fixed point**(자신감 있고 자기 일관적이지만 틀린 상태)에 수렴한다. FPF는 rollout에서 얻은 conditioning 상태로 학습해서 모델이 자신의 dynamics가 만든 상태를 고치도록 가르친다. FPF 하에서는 정답이 안정 attractors가 되고, 오답 상태는 일시적으로 머물다 떠난다. 수렴이 정답을 예측한다.

## 배경

- **자기회귀 모델**은 teacher forcing으로 왼쪽에서 오른쪽으로 토큰을 확정한다. 한번 확정된 앞 토큰은 전역적 귀결이 드러나도 고칠 수 없다. 논문의 plain causal decoder 베이스라인은 이 대비용이다.
- **마스크드 디퓨전 언어 모델**(MDLM, Sahoo et al. 2024; ReMDM; Adaptive MDLM)은 유연한 순서로 병렬 디노이징하지만, 같은 스텝에 갱신되는 토큰들은 현재 상태가 주어지면 조건부 독립이라 공격적인 병렬 업데이트는 불일치를 부른다. 어려운 문제는 보수적인 스텝을 많이 밟고 remasking 같은 추가 장치가 필요하다.
- **Discrete flow 모델**(Flow Language Models / FLM, Flow Map LM, Embedded Language Flows)은 모든 토큰과 상호의존을 동시에 모델링한다. Gaussian-to-one-hot 확률 경로로 비조건부 생성에는 강하지만 구조적 추론 능력은 거의 미탐사였다. 저자들의 FLM 베이스라인도 Sudoku-Extreme 13.9%, Zebra 67.9%에 그친다.
- **Recurrent reasoner**(HRM, TRM, FPRM, Equilibrium Reasoners/EqR)는 가중치 공유 recurrence로 테스트 타임 계산량을 늘린다. FRM은 attractor 직관을 공유하지만 표준 non-causal [Transformer](../../concepts/machine-learning/transformer.md) 기반 DiT와 표준 flow 목적식을 유지한다. 전용 아키텍처가 아니라 큰 모델·덜 특수한 도메인으로 가는 길을 열어두려는 의도적 선택이다.
- **Self-conditioning**(Analog Bits, Chen et al. 2023)은 원래 비조건부 생성 개선용이었다. FPF가 겨냥한 exposure bias 문제의 고전적 참고문헌은 **scheduled sampling**(Bengio et al. 2015)과 autoregressive video diffusion의 **Self Forcing**(Huang et al. 2025)이다.

## 방법론

### 조건부 추론을 위한 Discrete Flow

노이즈를 태우고 생성하는 것은 해 $y = (y_1, \dots, y_L)$뿐이다. 문제 $c$는 고정 조건 입력이다. 해는 one-hot endpoint $x_1 \in \{0,1\}^{L \times |\mathcal{V}|}$로 인코딩하고 positionwise argmax로 디코드한다. Flow matching은 노이즈 $\varepsilon \sim \mathcal{N}(0,I)$와 endpoint를 선형 interpolant로 잇는다.

$$x_t = (1-t)\varepsilon + t x_1, \qquad t \in [0,1] \tag{1}$$

디노이저 $D_\theta^t(x_t \mid c)$는 categorical clean-prediction 파라미터화를 쓴다. 위치마다 clean 토큰 분포를 예측하고, 이 출력이 후보 해 디코딩과 probability-flow velocity 결정에 동시에 쓰인다.

$$v_\theta^t(x_t \mid c) = (D_\theta^t(x_t \mid c) - x_t)/(1-t) \tag{2}$$

학습은 tokenwise cross-entropy다.

$$\mathcal{L}_{\mathrm{CE}}(\theta) = \mathbb{E}_{t,c,y,\varepsilon}\left[-\sum_{i=1}^{L}\log D_\theta^t(x_t \mid c)_{i,y_i}\right] \tag{3}$$

이 바닐라 모델이 논문의 FLM 베이스라인이며, FRM은 여기에 recurrent 축을 덧붙인다.

### Recurrence로서의 Self-conditioning

디노이저에 carry 입력이 추가된다. $D_\theta^t(x_t \mid c, s)$에서 $s$는 이전 clean-solution 예측을 담는다($s = \emptyset$은 null carry). 학습은 두 패스다. null-carry 패스로 detached carry $\tilde{s} = \mathrm{stopgrad}[D_\theta^t(x_t \mid c, \emptyset)]$를 만들고, 지도 패스는 $\tilde{s}$나 null을 조건으로 받는다. 경로와 손실은 그대로이며 carry로 그래디언트가 흐르지 않는다. 추론 때는 $(x_t, t)$를 고정한 채 recurrent refinement를 반복한다.

$$s_t^{(0)} = \emptyset, \qquad s_t^{(k+1)} = D_\theta^t(x_t \mid c, s_t^{(k)}) \tag{4}$$

추론 깊이 $k$는 flow 시간 $t$와 별개의 이산 축이다. 샘플러는 flow 상태 $x_t$ 전진과 현재 flow 시간에서의 recurrent 업데이트를 번갈아 수행한다. 매 업데이트가 같은 clean 해를 직접 추정하므로 BPTT 없는 detached 학습이 가능하다.

### Fixed-point 관점과 Exposure Bias

$(x_t, c, t)$를 고정하면 식 (4)는 후보 해 위의 fixed-point iteration이다. 바람직한 동작은 정답 $y^\star$가 attracting하는 것이다.

$$s_t^{(k)} \longrightarrow s_t^\star, \quad D_\theta^t(x_t \mid c, s_t^\star) = s_t^\star, \quad \mathrm{decode}(s_t^\star) = y^\star \tag{5}$$

반면 무효 상태는 일시적이어야 한다. 기존 학습은 이를 깨뜨린다. carry가 정답 유도 interpolant 위의 one-pass 예측에서 오는데, 추론 carry는 모델 자신의 closed loop에서 오기 때문이다.

$$p_{\mathrm{train}}(s \mid x_t, c, t) \neq p_{\mathrm{infer}}^{(k)}(s \mid \hat{x}_t, c, t) \tag{6}$$

불일치는 깊이와 함께 커진다. 두 효과가 결합한다. 디노이저가 자신의 과신 오답을 신뢰할 증거로 되먹임해 오차를 증폭하고 spurious fixed point에 안착한다. 수렴 근처에 남는 미묘한 low-residual 오차를 학습 때 거의 보지 못하므로 막판 교정을 배우지 못한다. 실제로 깊이가 깊어지면 정답率は 정체하는데 gold-target cross-entropy는 *오른다*.

### Fixed-Point Forcing (FPF)

FPF는 one-pass carry를 모델 자신의 다중 스텝 추론 dynamics에서 나온 detached carry로 바꾼다. 지도 시간 $t$와 rollout 시작 $t_{\mathrm{start}} \sim \mathcal{U}(0,t)$를 뽑고, 추론용 self-conditioned integrator를 $t_{\mathrm{start}}$부터 $t$까지 돌려 최종 예측 $s_{\mathrm{FPF}}$를 detach한 뒤 $D_\theta^t(x_t \mid c, \mathrm{stopgrad}(s_{\mathrm{FPF}}))$를 지도한다. 핵심은 손실 부담 입력이 정식 interpolant $x_t = (1-t)\varepsilon + ty$에, 타깃이 $y$에 그대로 있다는 점이다. FPF는 디노이저가 조건으로 삼는 것의 *분포*만 바꾸고, 지도 상태와 목적식은 손대지 않는다. 깊은 rollout 상태는 수렴 근처의 작고 미묘한 잔차 오차를 노출해서 fixed point 주변의 국소 교정을 가르친다. 학습은 2단계다. Stage A는 self-conditioning을 처음부터 학습하고, Stage B는 Stage-A 가중치에서 optimizer/EMA를 새로 시작해 FPF를 적용한다. 전부 non-causal DiT, AdamW, 상수 LR, EMA 0.9999을 공유한다(데이터셋별 크기는 Sudoku/Zebra/Maze에 7M/25M/8M 파라미터).

## 결과

최고 exact-solve율(Table 1): **Sudoku-Extreme 99.5% (7M), Zebra 100.0% (25M), Maze-Unique 99.9% (8M)**. flow 베이스라인 최고치(Adaptive MDLM 19.1%/98.3%/100.0%)와 전용 recurrent reasoner 최고치(EqR Sudoku-Extreme 98.7%)를 모두 넘는다. Sudoku-Extreme에서 EqR의 98.7%와 동률을 **44배 적은 inference FLOPs**으로 달성한다(operator-level 프로파일, batch-one forward pass × 실제 NFE). 세 태스크 전부 정확도-계산량 frontier를 선도한다.

학습법 ablation, 3 seed 평균(Table 2):

| 변형 | Sudoku-Extreme | Zebra | Maze-Unique |
|---|---|---|---|
| Base flow | 13.1 ± 0.7% | 62.3 ± 29.1% | 77.6 ± 16.7% |
| + Self-conditioning | 32.6 ± 3.7% | 36.9 ± 18.0% | 96.2 ± 3.0% |
| + Fixed-Point Forcing | **99.2 ± 0.3%** | **99.9 ± 0.2%** | **98.0 ± 1.8%** |

Zebra의 seed 분산이 FPF 하에서 붕괴한다(29.1 → 0.2). 쉬운 Sudoku-Shah 변형에서는 self-conditioning만으로 충분하고(30% → 99%), FPF는 어려운 제약 문제에서 진가를 발휘한다.

Dynamics 진단: 기존 self-conditioning에서 인접 상태 residual(token-averaged symmetric KL)의 정답 예측력은 우연 수준(AUROC 0.50)이지만, FPF 하에서는 **AUROC 1.00**이다. 수렴이 성공적 추론의 관측 가능한 시그니처가 된다(형식적 보증은 아니다). FPF는 깊이를 늘려도 계속 추가 평가를 정답 교정으로 전환하지만 베이스라인은 포화한다.

## 한계와 열린 질문

- 수렴-정답 대응은 경험적 시그니처이며 정답의 형식적 인증이 아니다.
- Solved-puzzle 평균 NFE는 정답을 알아야 멈출 시점을 아는 oracle 진단이라 그대로 배포 가능한 early stopping이 아니다. FLOPs도 메모리 트래픽과 오버헤드를 제외한 하한이다.
- 일부 Zebra 베이스라인(MDLM/Adaptive MDLM 발표치)은 저자 파이프라인에서 재현이 안 돼 daggered 참조값으로만 표에 들어간다.
- 7~25M 파라미터의 합성 퍼즐에서 입증됐고, 큰 모델과 덜 구조화된 태스크로의 확장은 향후 과제다.
- Self-conditioning과 preference류 목적식의 결합 학습은 불안정할 수 있다는 점이 언급된다(v1의 FLOWDPO 라인은 현 버전에서 빠짐).

## 소프트웨어 엔지니어 관점

- **패턴**: 반복 정제 샘플러(디퓨전/flow 디코더, self-refine LLM 루프)는 모두 자신의 중간 상태에 대한 train-inference 분포 간극을 겪는다. FPF 처방은 싸고 이식성이 좋다. 지도 목적식은 clean 데이터에 둔 채 정제 채널만 rollout 생성 상태로 학습한다. BPTT 불필요, 코드 변경 최소(carry 구성 교체 한 곳).
- **테스트 타임 스케일링 신호**: 잘 캘리브레이션된 수렴 residual(인접 스텝 symmetric KL ≈ 0 ⟺ 정답일 가능)이 라벨 없는 halting/confidence readout이 된다. 에이전트 루프에서 residual이 높게 머물면 반복 중단이나 큰 모델로 에스컬레이션하는 규칙으로 쓸 수 있다.
- **효율 교훈**: 44배 FLOP 동률은 모델을 키워서가 아니라 dynamics를 고쳐서 나왔다(7M). 스케줄링, 설정 합성, 쿼리 플래닝 같은 제약이 빡센 생성에는 작은 recurrent-refinement 모델이 큰 one-shot 모델을 이길 수 있다.
- **평가 위생**: 정확도-계산량 frontier는 측정된 operating point만(외삽 금지), FLOPs는 프로파일러 × 실제 평가 횟수, 데이터셋 리비전 고정. 그대로 따라 쓸 만하다.

## 참고문헌

- 논문: https://arxiv.org/abs/2606.29150 — HTML: https://arxiv.org/html/2606.29150v2
- Flow map language models (Lee et al. 2026, 2602.16813); Analog Bits (Chen et al. 2023, 2208.04202); Equilibrium Reasoners (Huang et al. 2026, 2605.21488); HRM (Wang et al. 2025a); TRM (Jolicoeur-Martineau 2025); Solve the loop (Fein-Ashley & Rashidinejad 2026, 2605.12466); Self Forcing (Huang et al. 2025); scheduled sampling (Bengio et al. 2015).
- 내부: [트랜스포머](../../concepts/machine-learning/transformer.md) (FRM 백본 계열: non-causal DiT).
