---
title: "FLAT - 검색과 생성을 위한 1D 가변 길이 정렬 트랜스모달 토큰으로 이미지·텍스트 리샘플링"
published: 2026-09-15
arxiv_id: "2609.16591"
url: "https://arxiv.org/abs/2609.16591"
authors: ["Guangyu Sun", "Shlok Kumar Mishra", "Wentao Bao", "Robert Zhenheng Yang", "Xiao Wang", "Xiyuan Wang", "Yujunrong Ma", "Chen Yuan", "Max Xiangjun Fan", "Jun Xiao", "Jianpeng Cheng"]
---

# FLAT - 검색과 생성을 위한 1D 가변 길이 정렬 트랜스모달 토큰으로 이미지·텍스트 리샘플링

[EN version](../en/sources/papers/FLAT_Resampling_Image_and_Text_into_1D_Flexible-Length_Aligned_Transmodal_Tokens.md)

## 초록

전통적 멀티모달 파이프라인은 2단계로 쪼개진다: 대조·자기지도 비주얼 인코더를 먼저 학습하고(CLIP, DINO), 그 고정 임베딩에 별도 하류 생성 모델을 조건화한다 — 생성이 고정 표현의 한계에 묶이고 재-정렬이 필요해진다. FLAT (Flexible-Length Aligned Transmodal representations, Meta, 2026년 9월)은 표현 학습과 생성을 공동 최적화해 생성 디코더가 바로 소비할 수 있는 선형 보간 가능한 임베딩을 만든다. 공유 멀티모달 인코더를 텍스트-이미지(T2I)·이미지-텍스트(I2T) 디코더와 함께 최적화하며, 대조 정렬과 양방향 교차 모달 생성 목적함수를 결합해 표현이 판별적 서술자이자 생성 조건으로 동시에 기능하게 한다. 아키텍처적으로 이미지·텍스트를 통합된 연속 1D 토큰 시퀀스로 리샘플링하고 prefix-K 토큰에 nested dropout을 적용해 동적 출력 길이를 지원한다. 단일 사전학습으로 T2I GenEval 71.1, 과제별 미세조정 후 83.1 GenEval, MS-COCO 캡셔닝 40.5 BLEU-4 / 138.6 CIDEr, Recall@5는 COCO 86.8 (I2T) / 75.8 (T2I), Flickr30K 98.3 / 93.6 — 선형 보간·잠재 공간 연산·제로샷 합성 검색은 덤이다.

## 배경 및 문제 설정

두 개의 분리된 전통이 지배적이다: 정렬은 하지만 생성은 못하는 대조 표현 학습(CLIP 계열, SigLIP)과, 학습하지 않은 임베딩의 한계를 물려받는 생성 모델(고정 비주얼 인코더 위의 BLIP-2/LLaVA, 고정 텍스트 인코더 위의 Stable Diffusion/SDXL/SD3/PixArt/Sana). 최신 통합 모델들은 인코더를 생성 백본과 공동 학습하거나 픽셀 공간에서 인코더프리로 간다. FLAT은 중간 경로다 — 명시적·대조적·선형 보간 가능한 임베딩 공간을 유지하되 정렬과 생성을 함께 최적화한다. 통찰(CoCa/BLIP 계열 이후)은 검색과 생성이 서로 강화한다는 것이다: 판별에 좋은 표현은 어느 방향의 합성 조건으로도 좋아야 하고 그 역도 성립한다. 1D 비주얼 토크나이저(TiTok, FlexTok, GigaTok)가 공간 그리드를 compact 시퀀스로 압축한 advances 위에, 여기서는 양 모달리티를 하나의 공유 공간으로 확장하고 탄력적 시퀀스 길이를 위한 nested dropout (Matryoshka 스타일)을 더했다.

## 방법론

**표현 인코더.** 모달리티 m ∈ {img, txt}의 입력 x에 N개의 학습 가능 레지스터 토큰 R을 이어붙여 공유 VLM 인코더 f_enc (Qwen3.5-2B 백본 + LoRA 어댑터, 시스템 프롬프트 "Represent the input")에 통과시키고, 레지스터 위치의 hidden state를 선형 투영한다: z = W_lat · f_enc(x, R) ∈ R^{N×d}. 양 모달리티가 레지스터와 투영을 공유한다.

**Nested dropout.** 학습 스텝마다 keep 길이 K를 기하 사다리 K = {1, 4, 16, 64, 256}에서 한 번 샘플링해 전 rank에 브로드캐스트하고, prefix z_{:K}만을 대조 손실과 양 디코더에 공급한다. 기하 샘플링(정수 균등 아님)은 인지 불가한 길이 차이에 최적화 스텝을 낭비하지 않으며, 직접 truncation이 FlexTok식 null-패딩보다 ablation에서 앞선다.

**디코더.** Prefix z_{:K}를 과제별 MLP + RMSNorm으로 소프트 토큰 e ∈ R^{K×h}에 매핑한다. I2T 디코더는 표준 자기회귀 LM (비주얼 소프트 토큰 + "Describe the input" 프롬프트 → 캡션). T2I 디코더는 rectified-flow 트랜스포머 (SANA-1.6B에서 초기화)로 VAE latent를 디노이징하며, 텍스트 소프트 토큰을 cross-attention 조건으로 사용한다 (flow-matching 손실 ‖v_φ(x̂_t, t, z_{:K}) − (ε − x̂)‖²).

**손실.** (1) 양방향 대조: 매칭 레지스터 위치 평균의 late-interaction 유사도 s_{ij}^{(K)}에 전역 배치 InfoNCE 양방향 (i2t + t2i)/2. (2) 캡셔닝 NLL. (3) Flow-matching MSE. 전체 L = λ_align·L_align + λ_txt·L_txt + λ_img·L_img이며, 미세조정에서는 과제별 부분집합을 따로 최적화한다.

## 결과

- **T2I 생성**: 단일 사전학습 → GenEval 71.1, 120K 정제 쌍에 디코더 88k 스텝 미세조정 → **83.1**. 프롬프트 리라이팅 없는 평가(no-rewrite)에서 프롬프트 리라이터를 쓰는 7B 모델 2종 포함 비교 대상 전부 상회. 복잡도는 길이를 요구한다: K=1은 단일 객체/색상 포착, 관계형 범주(두 객체, 위치, 색상 바인딩 — K=1에서 ≈0.03)는 K=4/16에서 가파르게 회복 (0.67).
- **I2T 캡셔닝** (COCO Karpathy, 디코더 LoRA 55k 스텝): **40.5 BLEU-4 / 138.6 CIDEr**, K 증가에 따라 전 지표 안정 상승. K=1조차 CrossFlow/SCD-Net을 CIDEr/METEOR/SPICE에서 상회. 정성적으로 K=1은 말이 되는 캡션, 긴 prefix는 어휘 정밀도 추가 (street→alley).
- **검색** (대조학습된 인코더 LoRA): COCO R@5 **86.8 I2T / 75.8 T2I**, Flickr30K **98.3 / 93.6** — 놀랍게도 K-불변: 64차원(K=1)부터 16K차원(K=256)까지 전부 ~1pp 이내, 저폭에서 붕괴하는 MRL/SAE/CSR 베이스라인과 대조적. 첫 토큰이 전역 의미를 담는다.
- **선형 프로빙/클러스터링**: 고정 K=1 토큰 → ImageNet top-1 73.3%, K=64에서 **81.8%** (동일 차원의 DREAM과 모든 생성 latent 상회). 단일 토큰 k-means가 비지도 ImageNet 클래스를 복원.
- **기하**: FLAT은 CLIP의 이미지-텍스트 중심 거리를 1개 토큰에서 절반, 256개에서 1/4로 — 거의 겹치는 공간이 z_α = (1−α)z_1 + αz_2의 매끄러운 교차 모달 보간, 제로샷 연산 (새벽 빼고 달밤 더해도 장면 유지), CIRR 제로샷 합성 검색을 가능케 한다.
- **Ablation (7개 손실 조합, Shapley 분해)**: 전체 목적함수만이 5개 지표 모두에서 강하고, 각 과제는 매칭 손실 주도 + 나머지 보완 — 정렬과 생성은 충돌이 아니라 강화한다.
- 프로젝트: https://guangyusun.com/flat-website/

## 한계 및 향후 과제

- SOTA 일치는 여전히 과제별 미세조정 필요. 사전학습 체크포인트의 절대 검색/생성 수치는 뒤처지며 (부록 C/D가 격차와 FLAT 사전학습의 가치 vs 과제 전용 학습을 정량화).
- 백본 스케일이 중간 규모 (2B 인코더 + 1.6B 이미지 디코더)이며, LLM 리라이터를 곁들인 7B+에서도 joint recipe가 성립하는지는 미검증.
- 기하 결과는 정성 + 중심 통계이며, K=1의 합성 실패 모드(바인딩, 개수 세기)는 남는다. 다국어/이모지·멀티프레임 비디오 전이(부록 G)는 예비 수준.

## 소프트웨어 엔지니어에의 시사점

RAG·멀티모달 제품 관점에서 FLAT의 헤드라인은 운영적이다: **한 번의 인코더 패스가 탄력적 비용으로 검색과 생성을 겸한다** — K=1 (64차원)만으로 전폭 대비 1pp 이내 검색이 되므로, 싼 쿼리는 1–4 토큰으로 라우팅하고 합성적 생성에만 64–256을 쓴다. 공유 공간 설계는 서빙 스택 2개 (임베딩 모델 + 생성 조건기)를 연산·합성검색 보너스를 곁들인 단일 표현으로 합친다 ("이 이미지인데 밤 버전"을 벡터 연산으로). CLIP + diffusion-조건기를 따로 운영하는 팀에게 이 논문은 공동 학습의 가장 강력한 최신 근거다. `concepts/ai-engineering/rag.md`, `concepts/ai-engineering/embedding.md`, `concepts/machine-learning/attention.md`의 확장이다.

## 참고 자료

- 논문: https://arxiv.org/abs/2609.16591 (HTML: https://arxiv.org/html/2609.16591v1) — 프로젝트: https://guangyusun.com/flat-website/
- CLIP (Radford et al. 2021); FlexTok/TiTok (Bachmann et al. 2025; Yu et al. 2024); CoCa (Yu et al. 2022); BLIP-2 (Li et al. 2023); SANA (Xie et al. 2025); GenEval (Ghosh et al. 2023)
