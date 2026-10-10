---
published: true
title: "공통 기반에 대한 증거로서의 시선: MapTask와 MUNDEX의 교차 코퍼스 분석"
arxiv_id: "2609.18011"
url: "https://arxiv.org/abs/2609.18011"
authors: ["Nan Li", "Albert Gatt", "Massimo Poesio"]
tags: [source, paper, machine-learning, ko]
---
published: true

# 공통 기반에 대한 증거로서의 시선: MapTask와 MUNDEX의 교차 코퍼스 분석

[EN version](../en/sources/papers/Gaze_as_Evidence_for_Common_Grounding.md)

## 초록

정보가 비대칭적인 협업 과제에서 참가자들은 상호작용을 통해 이해를 조율한다. 본 논문은 두 가지 협업 과제에서 시선(gaze)이 그라운딩(grounding)에 대한 증거를 제공하는지 묻는다. 이산 행동 어노테이션에서 출발해 HCRC MapTask (Anderson et al., 1991)와 MUNDEX (Türk et al., 2023)를 공유 partner/task/away 어휘로 매핑하고, 과제 관련 발화 단위 주변의 시선 특징을 계산한다. 두 코퍼스 모두에서 정렬된 지시 해석(aligned reference interpretation, MapTask)과 UND(understood) 판정(MUNDEX)은 과제 지향 시선이 많고, 상대 지향 시선이 적으며, 시선 엔트로피가 낮고, 시선 전환이 적은 것과 연관된다. 연관성은 과제를 주도하는 참가자에서 가장 뚜렷하다: giver가 생성한 지시 표현에서, 그리고 explainer 판정에서 나타나며, 이는 explainee의 시선과도 공변한다. 동일 화자의 MapTask 지시 연쇄에서는, 이전에 정렬되지 않았던 지시 대상이 정렬되는 언급 지점에서 화자의 시선 엔트로피가 낮아진다. 그룹 교차검증 하에서 최적 시선 특징군은 대조군 대비 소폭 개선에 그친다: MapTask에서는 시간적 특징이, MUNDEX에서는 원시 비율 특징이 가장 좋다. 효과가 작고 여럿이 추론 단위를 대화(dialogue)에서 반복 참가자로 바꾸면 약해지므로, 시선은 과제·대화 맥락과 함께 해석해야 하는 하나의 기여 단서로 취급한다.

## 배경 및 문제 설정

참가자들이 서로 다른 사적 정보를 갖고 있을 때 상호 이해(공통 기반, common ground)는 가정할 수 없고 상호작용을 통해 구축해야 한다(Clark and Wilkes-Gibbs 1986; Clark and Brennan 1991). 시선은 관측 가능한 단서다: 사람들은 지시를 하거나 이해를 확인할 때 과제 자료를 보거나, 서로를 보거나, 다른 곳을 본다. 많은 코퍼스가 비디오에서 시선을 시선추적 좌표가 아니라 이산 범주로 어노테이션하지만, 온톨로지가 코퍼스마다 달라 과제 간 비교를 막는다.

본 논문은 두 가지 비대칭 대면 과제를 연구한다. HCRC MapTask: giver가 의도적으로 랜드마크가 다르게 그려진 지도를 들고 follower를 경로로 안내한다. 관점주의(perspectivist) 라벨이 각 참가자의 해석을 따로 기록하므로, 화자와 청자가 같은 랜드마크로 해소할 때만 해당 지시가 정렬된 것으로 본다. MUNDEX: explainer가 독일어로 보드게임을 explainee에게 가르치고, 이후 양쪽이 소급적으로 explainee의 이해도를 UND / PART_UND / NON_UND / MISUND 척도로 판정한다. 코퍼스 내 선행 연구들은 상대 지향 시선과 난이도의 연결(Boyle et al. 1994; Nakano et al. 2003; Murat and Vogel 2026), 청자 시선 엔트로피와 자기보고 이해도의 연결(Wang et al. 2026)을 보고했다. 남은 열린 질문은 시선-그라운딩 연관성이 서로 다른 과제와 그라운딩 측정치에 걸쳐 수렴하는지, 그리고 대조 조건을 넘어선 예측 신호를 갖는지다.

## 방법론

**공유 표현.** 양쪽 시선 온톨로지를 partner/task/away로 매핑한다: MapTask의 up/down/off가 partner/task/away가 되고, MUNDEX의 EX/EE/TABLE/AWAY도 유사하게 매핑된다(단 up→partner 매핑은 눈맞춤 조건에서만 문자 그대로 성립한다). 양이 아닌 길이의 이벤트는 버리고 참가자 내 겹침을 해소한다. MapTask 윈도우는 지시 표현에 화자 반응을 잡기 위한 1.5초 후행 맥락을 더한 구간이고, MUNDEX 윈도우는 이해도 어노테이션 기준 ±2초다. 어느 한 참가자라도 시선 커버리지가 30% 미만인 윈도우는 제외해, MapTask 지시 윈도우 5,144개(정렬 3,807, 보류 1,261, 오해 76; 대화 46개, 눈맞춤 31 / 비눈맞춤 15)와 MUNDEX 윈도우 807개(UND 360, PART_UND 199, NON_UND 151, MISUND 97; 상호작용 26개, explainer 9명; EX 458 / EE 349 어노테이션을 어노테이션당 1행으로 풀어 합산)가 남는다.

**특징군.** 공유 어휘에서: 원시 비율(참가자별 각 타깃 응시 시간 비율과 상호 응시, 7~8개 특징); 구조적(커버리지·전환 횟수·지속시간 가중 Shannon 엔트로피 추가, 13~14개); 시간 동역학(런 횟수·지속시간·전환율·지연·첫/마지막/지배 지표, 참가자당 21개); 전이 바이그램(task→partner 같은 순서쌍, 참가자당 6개); 협응(약 10Hz 샘플링된 결합 상태: 상호 task/partner 응시, 정렬, 상보성, 결합 엔트로피, 결합도, 6개 결합 특징); 파생 비율(partner/task 비율, 참여도, 과제 지배도, 비대칭, 9개 특징).

**분석.** 이진 대조(정렬 vs. 비정렬; 어노테이터 판정 UND vs. 비UND)에 Mann–Whitney U와 순위-이serial `r`, 역할·눈맞춤 조건별 층화, 클러스터-로버스트 로지스틱 GEE와 Benjamini–Hochberg 보정을 적용하고, 추론 단위를 달리한다(대화 vs. 반복-참가자 그룹). 화자 내 지시 연쇄 분석은 마지막 비정렬 언급과 해소되는 정렬 언급에서 화자 시선을 비교한다(189쌍, 45개 대화). 예측은 표준화된 특징과 균형 가중치를 쓴 로지스틱 회귀를 그룹 교차검증으로 수행하고(MapTask는 대화 기준 10-fold, MUNDEX는 explainer 기준 5-fold), 대조군 전용(조건 + 화자 역할; 어노테이터 역할) 대비 특징군 제거(ablation)를 본다.

## 결과

- **방향적 수렴**: 양 코퍼스에서 긍정 클래스(정렬 / UND)는 과제 지향 시선이 많고, 상대 지향 시선이 적으며, 엔트로피가 낮고, 전환이 적다. 풀링된 최대 `|r|`: MapTask 0.058, MUNDEX 0.181. 상위 연관 모두 Mann–Whitney p < 0.001이며, 엔트로피·전환 특징은 MapTask의 대화-클러스터 GEE에서도, explainer 과제/상대 시선과 explainee 엔트로피/전환은 MUNDEX의 참가자-클러스터 GEE에서도 살아남는다.
- **역할 집중**: 과제 주도자에게서 가장 뚜렷하다. giver 생성 지시는 6개 유의 특징을 갖는(최대 `|r|` 0.086) 반면 follower 생성은 0에 가깝다(최대 0.043). MUNDEX에서는 14개 구조 특징 전부가 EX 판정 층과 EE 자기보고 층에서 부호가 일치하지만, 보정 후 살아남는 것은 EX 판정 층뿐이며, explainee 시선 비율·엔트로피·전환이 포함된다. 특징×역할 상호작용은 보정 후 유의하지 않으므로, 이는 검증된 조절효과가 아니라 층별 차이다.
- **그라운딩 과정**: 정렬률은 첫 언급 0.30에서 두 번째 0.59, 네 번째 이상 0.85로 상승한다. 화자의 상대 응시·엔트로피·전환은 첫 언급보다 두 번째 언급에서 낮다. 화자 내 비교에서는 해소 언급에서 엔트로피가 하락한다(dz = −0.20, q = 0.044). 다만 대화 수준 집계에서는 살아남지 못하고(q = 0.20) 여섯 참가자-공유 그룹 중 두 곳에 집중된다. 연쇄 위치를 맞춘 비교에서는 두 번째 언급의 과제 응시만 보정 후 유의하다(q = 0.01).
- **예측**: 소폭의 분할-민감 개선. MapTask 최적은 구조+시간 특징(macro-F1 0.532 vs. 대조군 전용 0.472, 다수 0.425)이고, MUNDEX 최적은 원시 비율(0.564 vs. 0.544, 다수 0.356)이다. MapTask 개선폭은 30개 reshuffle 분할에서 0.015~0.070(평균 0.038)이고, MUNDEX 개선은 29/30에서 양수이나 최대 0.027이다. 눈맞춤 층은 풀링 데이터보다 큰 `|r|`을 보이지만 조건 상호작용은 유의하지 않으며, 비눈맞춤 층의 효과는 0에 가깝다.
- EMNLP 2026 MINT 워크숍 구두 발표로 채택됐다(16쪽, 표 17개, 그림 2개). 데이터·코드: GMMT 라벨, MUNDEX Zenodo v0.7, 분석 저장소 https://github.com/chnln/gaze-as-grounding-evidence

## 한계 및 향후 과제

- 세 가지 시선 범주로는 어느 랜드마크·객체를 보는지 식별할 수 없고, 이름이 같다고 상호작용 기능이 같은 것은 아니다(MapTask의 상대 응시는 지시 확인일 수 있지만 MUNDEX에서는 화제 구조 정리일 수 있다). up→partner 매핑은 눈맞춤 조건에서만 문자 그대로다.
- MUNDEX는 두 관점(explainer 판정 vs. explainee 자기보고)을 풀링한다. 완전히 유지된 연결쌍 135개 중 44개는 이진 라벨에서 불일치하고, 짝지어진 윈도우가 꼭 겹치지 않을 수도 있다(중앙 앵커 간격 4.36초).
- 작고 반복-참가자 표본: MapTask 대화 46개가 24명 참가자의 여섯 연결 그룹에서, MUNDEX 상호작용 26개가 explainer 9명(8명은 각 3회 상호작용)에서 왔다. 참가자/그룹을 클러스터로 하면 MapTask에서는 보정 후 살아남는 특징이 없고, 커버리지 필터링이 MapTask 17개·MUNDEX 149개 윈도우를 불균등하게 탈락시킨다(MUNDEX 탈락 중 139개가 explainer 2명에서 나온다).
- 효과는 작고 추론 단위에 민감하며 예측 개선은 분할 의존적이다. 영어·독일어의 비대칭 대면 과제 두 가지만 검증됐다. 저자들은 시선을 단독 그라운딩 검출기가 아니라 어휘·대화행위·과제 상태 특징과 함께 모델링해야 할 하나의 기여 단서로 취급한다.

## 소프트웨어 엔지니어에의 시사점

회의 비서, 튜터링 에이전트, 인간-로봇 대화(시선 인식 프론트엔드 포함)를 만드는 팀에게 실무적 결론은 보수적이다: 과제 관련 발화 주변에 compact한 partner/task/away 시선 스트림을 로깅하되, 정답 센서가 아니라 보조 특징으로 쓰라. 작고 역할 조건적인 신호를 예상하고 — 과제 주도자의 과제-대-상대 균형, 엔트로피, 전환율을 모니터링하며 — 텍스트·대화행위·과제 상태와 융합하고, 화자 기준 그룹 평가(풀링된 윈도우가 아니라 held-out 화자)로 검증해 개선폭을 과장하지 말라. 부록의 공유-어휘 매핑과 윈도우/특징 정의는 자사 비디오 코딩 시선 로그를 계측해 동일한 Mann–Whitney + 클러스터-로버스트 GEE + 그룹 CV 제거분석을 돌리는 데 바로 재사용할 수 있다. `concepts/machine-learning/embedding.md`, `concepts/ai-engineering/agent-evaluation.md`, `concepts/ai-engineering/agent.md`의 확장이다.

## 참고 자료

- 논문: https://arxiv.org/abs/2609.18011 (HTML: https://arxiv.org/html/2609.18011v1) — HF: https://huggingface.co/papers/2609.18011 — 코드: https://github.com/chnln/gaze-as-grounding-evidence
- MapTask (Anderson et al. 1991); MUNDEX (Türk et al. 2023); GMMT 관점주의 라벨 (Li et al. 2026a); 그라운딩 (Clark and Wilkes-Gibbs 1986; Clark and Brennan 1991); GEE (Liang and Zeger 1986); BH 보정 (Benjamini and Hochberg 1995)
