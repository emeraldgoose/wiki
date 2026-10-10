---
title: "Atria Dawn: 에이전트 기반 초지능의 서막"
published: 2026-09-14
arxiv_id: "2609.15818"
url: "https://arxiv.org/abs/2609.15818"
authors: ["Honglin Guo", "Tao Gui", "Yicheng Chen", "Guanting Dong", "Qiming Ge", "Yuyang Hu", "Zixian Huang", "Jiajie Jin", "Alexander Lam", "Yining Li", "Jiahang Lin", "Yanjiang Liu", "Xinyu Lu", "Haijun Lv", "Junlin Shang", "Qisheng Su", "Guoqiang Wang", "Rui Wang", "Zhecan Wang", "Hao Xiang", "Xinchen Xie", "Shuhao Xing", "Xiaoyu Xing", "Wanghan Xu", "Xinyu Yang", "Yajie Yang", "Chengfeng Zhao", "Haoran Zhao", "Ruojun Zhou", "Yunhua Zhou", "Yicheng Zou", "Kun Cai", "Qiye Cai", "Xinmeng Che", "Haodong Chen", "Jiabei Chen", "Jiahao Chen", "Jiayi Chen", "Yujia Chen", "Lizhi Cui", "Youheng Dai", "Xin Deng", "Yi Dong", "Shihan Dou", "Chenya Gu", "Xu Guo", "Ding Han", "Feiyang Hao", "Haotan He", "Jie Hou", "Binze Hu", "Zijian Hu", "Junhao Huang", "Huicheng Jiang", "Jiazhen Jiang", "Shufan Jiang", "Jiahao Kuang", "Bowen Lai", "Bo Li", "Jiaqiang Li", "Peng Li", "Qilong Li", "Zhuoqun Li", "Jiaxiang Liu", "Shuainan Liu", "Tong Liu", "Yi Liu", "Zhonghang Lu", "Jianwen Luo", "Yanyi Luo", "Huijie Lv", "Ningsheng Ma", "Zerun Ma", "Houcheng Min", "Chengjun Pan", "Qiyuan Peng", "Xiaoxuan Peng", "Jianmin Qian", "Jiantao Qiu", "Wanying Ren", "Huayu Sha", "Jifei Shan", "Zixin Shang", "Bing Shao", "Zhuohui Sheng", "Jiayang Shi", "Yang Shu", "Aierpanjiang Simayi", "Sirui Song", "Yuxiao Song", "Zhe Sun", "Zhichao Sun", "Wenzhe Tan", "Wenhui Tian", "Zhongbo Tian", "Hanchen Wang", "Pengbo Wang", "Rui Wang", "Yiding Wang", "Yuhui Wang", "Zhiheng Xi", "Caijun Xu", "Chao Xu", "Yongfeng Xu", "Xiaolei Yang", "Zhixiong Yang", "Qian Yao", "Shihong Yi", "Yuankai Ying", "Jia Yu", "Dingbo Yuan", "Hao Yuan", "Junjie Yuan", "Bo Zhang", "Caixian Zhang", "Qiuyinzhe Zhang", "Jiyuan Zhao", "Penghao Zhao", "Ying Zhao", "Pujun Zheng", "Xiaoxue Zhong", "Xiaohao Zhou", "Xinyu Zhou", "Dongsheng Zhu", "Guanru Zhu", "Yulun Zhu", "Yaojie Lu", "Tao Ji", "Hongyu Lin", "Yutao Zhu", "Pengfei Cao", "Guoxiu He", "Xianpei Han", "Ben He", "Zhicheng Dou", "Kang Liu", "Qi Zhang", "Le Sun", "Jun Zhao", "Ji-Rong Wen", "Xuanjing Huang", "Yu-Gang Jiang", "Bowen Zhou"]
tags: [source, paper, ai-engineering, ko]
---

# Atria Dawn: 에이전트 기반 초지능의 서막

[EN version](../en/sources/papers/Atria_Dawn_The_Dawn_of_Agentic_Superintelligence.md)

## 초록
AI 에이전트가 후속 모델의 개발에 직접 참여하게 됨에 따라, 지능의 생산 방식과 인간 연구자의 역할이 재정의되고 있습니다. 본 논문에서는 과학 연구 및 엔지니어링 워크플로우를 위해 설계된 파운데이션 에이전트 언어 모델인 **Atria Dawn Preview**를 소개합니다. 이 모델은 도구 매개 상호작용을 실행 가능한 환경 및 외부 검증 결과와 연결하는 **검증 가능한 경험 파이프라인(Verifiable Experience Pipeline)**을 통해 학습되었습니다. 실제 연구, 엔지니어링, 디지털 작업 등 16개 벤치마크에서 Atria Dawn Preview는 최신 에이전트들과 경쟁 가능한 성능을 보였으며, 그 중 5개 항목에서 최고 점수를 기록했습니다. 성능 외에도, 56명의 참여자와 에이전트 로그를 통해 769개의 작업 기록을 분석하여 인간-AI 협업 사례 연구를 수행했습니다. 그 결과, 참여자들은 완료된 AI 지원 작업의 약 1/3이 AI 없이는 불가능했을 것이라고 평가했습니다. 특히, 에이전트가 방법론을 제안하고 수정을 구현하는 반면, 인간은 최종 결정권을 유지하며 판단과 피드백을 통해 탐색을 가이드하는 경향이 뚜렷했습니다. 이는 작업 단위의 실행에서 프로젝트 단위의 파트너십으로의 전환을 의미하며, 인간의 노력은 '무엇을 추구할 것인가'와 '증거가 연구를 어떻게 가이드해야 하는가'에 집중됩니다. 더 자율적인 AI 연구로 나아가기 위해서는 발견 능력뿐만 아니라 의미 있는 인간 감독 능력을 동시에 발전시켜, 지속적인 개발의 위험과 방향에 대해 인간의 책임 있는 권한을 유지해야 합니다.

## 배경 및 문제 설정
LLM이 단순한 '챗봇'에서 '에이전트'로 진화하려면, 다음 토큰을 예측하는 것에서 복잡한 환경에서 목표를 달성하는 것으로 패러다임이 바뀌어야 합니다. 기존의 에이전트 학습은 정적 데이터셋이나 단순한 RLHF에 의존했으나, 과학 연구 및 엔지니어링은 긴 호흡의 작업, 도구 의존성, 그리고 객관적인 검증(예: 코드가 실행되어야 함, 수학적 정답이 명확함)이 필수적입니다. 핵심 문제는 모델이 자율적으로 탐색하고, 실패하고, 환경으로부터 배우며, 이를 검증 가능한 방식으로 반복 개선하도록 학습시키는 방법입니다.

## 방법론: 검증 가능한 경험 파이프라인
핵심 혁신은 **검증 가능한 경험 파이프라인(Verifiable Experience Pipeline)**입니다. 모델은 단순히 정답 궤적(gold-standard trajectories)을 학습하는 것이 아니라, 실제 실행에 기반한 경험을 통해 학습합니다.

1. **도구 매개 상호작용**: 에이전트는 코드 인터프리터, 브라우저, API 커넥터 등 다양한 도구와 상호작용합니다.
2. **실행 가능한 환경**: 결과를 생성하는 모든 작업은 샌드박스에서 실행됩니다. 피드백은 모델이 생성한 '비평'이 아니라, 시스템 출력(예: Python traceback, 유닛 테스트 실패 메시지)이라는 실제 데이터입니다.
3. **외부 검증 결과**: 성공 여부는 환경의 최종 상태(예: 정확한 내용의 파일 생성, Lean/Coq로 검증된 수학적 증명)로 정의됩니다.
4. **경험 루프**: 모델이 여러 궤적을 생성하고, 성공한 궤적은 학습 세트에 추가하며, 실패한 궤적은 대조 학습(contrastive learning)에 사용하거나 프롬프트/정책을 개선하는 데 활용합니다.

## 결과
- **벤치마크 성능**: 16개 벤치마크에서 테스트한 결과, GPT-4o나 Claude 3.5 Sonnet과 같은 최상위 에이전트들과 경쟁 가능했으며, 5개 항목에서 1위를 기록했습니다.
- **인간-AI 협업**: 769개의 작업 기록 분석 결과:
    - 약 33%의 작업이 AI 없이는 "불가능했을 것"으로 평가되었습니다.
    - 노동의 분업: 에이전트는 '제안 및 구현(How)'을 담당하고, 인간은 '판단 및 가이드(What, Why)'를 담당하는 구조로 변화했습니다.
- **생산성 향상**: 복잡한 엔지니어링 작업의 완료 시간이 대폭 단축되었습니다.

## 한계 및 향후 과제
- **감독의 병목**: 에이전트가 제안하는 해결책이 복잡해질수록, 이를 검증하는 인간의 능력이 주된 병목이 됩니다.
- **발산 위험**: 검증 신호가 불완전할 경우, 자율적인 자기 개선 루프가 인간의 의도에서 벗어날 가능성이 있습니다.
- **일반화**: 엔지니어링과 과학 분야에서는 강력하나, 매우 주관적이거나 검증 불가능한 창의적 영역에서의 성능은 아직 충분히 탐색되지 않았습니다.

## 소프트웨어 엔지니어에의 시사점
이는 **프로젝트 레벨의 파트너십(Project-Level Partnership)**으로의 이동을 의미합니다. 엔지니어는 AI를 단순한 '코드 조각 생성기'로 사용하는 것이 아니라, '아키텍처 스티어링(Architectural Steering)' 도구로 활용하게 됩니다. 핵심 교훈은 **검증 가능성(Verifiability)**의 중요성입니다. 테스트, CI/CD, 형식 방법론 등을 통해 작업의 검증을 더 많이 자동화할수록, Atria Dawn과 같은 에이전트 모델에 더 많은 실행 권한을 위임할 수 있습니다.
