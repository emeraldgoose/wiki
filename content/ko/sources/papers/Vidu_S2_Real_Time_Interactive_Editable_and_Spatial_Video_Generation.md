---
title: "Vidu S2: Real-Time Interactive, Editable, and Spatial Video Generation"
published: 2026-09-10
arxiv_id: "2609.11638"
url: "https://arxiv.org/abs/2609.11638"
authors: ["Jintao Zhang", "Kai Jiang", "Jintao Chen", "Xu Wang", "Deyuan Liu", "Jungang Li", "Dechuang Chen", "Ming Lin", "Jingjiang Zhou", "Haopeng Jin", "Qi Jia", "Xiaohang Wang", "Yaole Wang", "Zhanqiang Zhang", "Ran Li", "Zhengkun Huang", "Shuyue Xiong", "Yuji Wang", "Zikun Dai", "Hui He", "Yang Luo", "Mang Ning", "Weiqi Feng", "Chengyang Ye", "Xinyue Lin", "Min Zhao", "Hongzhou Zhu", "Hengkai Tan", "Zeyuan Wang", "Chendong Xiang", "Kaiwen Zheng", "Zhijie Deng", "Fan Bao", "Jianfei Chen", "Jun Zhu"]
tags: [source, paper, machine-learning, ko]
---

# Vidu S2: 실시간 인터랙티브, 편집 가능 및 공간 비디오 생성



## 초록
본 논문에서는 실시간 인터랙티브 디지털 캐릭터 모델인 Vidu S2-Avatar와 실시간 비디오 편집 모델인 Vidu S2-Editing으로 구성된 Vidu S2를 제시합니다. 또한, Vidu S2-Avatar와 Vidu S2-Editing 모두에 대해 실시간 공간 비디오 생성의 가능성을 탐구합니다. Vidu S1과 비교하여, Vidu S2-Avatar는 실시간 720p 비디오 생성, 언제든지 업데이트 가능한 동적 참조 생성, 그리고 춤과 같은 더 강력한 지침 수행 능력을 지원합니다. Vidu S2-Editing은 스타일 렌더링, 의상 교체, 캐릭터 교체, 배경 교체를 포함하여 비디오 스트림을 실시간으로 편집할 수 있습니다. 실험 결과, Vidu S2는 모든 베이스라인 모델보다 우수한 성능을 보였습니다.

## 배경 및 문제 설정
실시간 인터랙티브 비디오 생성, 특히 디지털 아바타와 동적 비디오 편집에 대한 수요가 증가하고 있습니다. 기존 모델(Vidu S1 등)은 실시간 720p 출력을 위한 속도가 부족했고, 동적 참조나 복잡한 지침(예: 특정 춤 동작)을 스트리밍 방식으로 처리하는 유연성이 부족했습니다. 또한, 깊이감과 몰입감을 유지하는 일관된 공간 비디오 생성의 필요성이 있었습니다.

## 방법론

### Vidu S2-Avatar
- **목표**: 실시간 인터랙티브 디지털 캐릭터 생성.
- **주요 특징**: 720p 출력 지원, 동적 참조 업데이트 가능, 개선된 지침 수행 능력.
- **훈련 전략**: 양방향 이미지 및 참조-비디오 훈련 방식을 사용합니다.
- **기술적 세부사항**:
    - **Hybrid Teacher 및 Diffusion Forcing**: 훈련을 안정화하고 시간적 일관성을 개선하는 데 사용됩니다.
    - **Self-Replay Forcing**: 긴 시퀀스에서도 정체성을 유지하는 능력을 향상시킵니다.
    - **Super-Resolution Refiner**: 고품질 720p 출력을 보장합니다.

### Vidu S2-Editing
- **목표**: 실시간 비디오 스트림 편집.
- **기능**:
    - **스타일 전이**: 대상의 정체성을 유지하면서 붓터치와 색상 팔레트를 변경합니다 (예: 수채화, 공필화).
    - **가상 시착 (Virtual Try-On)**: 신체 움직임과 폐색 관계를 유지하면서 의상을 교체합니다 (예: 흰 셔츠, 데님 점프수트).
    - **대상 교체**: 포즈와 카메라 궤적을 유지하면서 캐릭터를 교체합니다.
    - **배경 교체**: 전경의 대상과 동작을 유지하면서 환경을 변경합니다 (예: 파리 카페, 침실).

### 공간 비디오 생성
- Vidu S2는 좌우 안구 뷰를 생성하여 3D와 같은 공간 비디오를 구현함으로써, 전경과 배경을 명확히 분리하고 몰입감을 높입니다.

## 결과
- **정량적/정성적 평가**: Vidu S2는 정체성 보존과 시간적 안정성 면에서 PixVerse, Runway, XMax, Decart와 같은 베이스라인 모델보다 뛰어난 성능을 보였습니다.
- **아바타 일관성**: 경쟁 모델에서 나타나는 얼굴 표정의 표류(drift) 없이 정체성, 헤어스타일, 세부 기하학적 구조를 유지합니다.
- **편집 정밀도**: 다른 모델들이 실패하는 "셔츠를 당기는" 동작 중의 의상 변형까지 정확하게 처리합니다.

## 한계 및 시사점
- **관련성**: 소프트웨어 엔지니어 및 ML 실무자에게 Vidu S2는 효율적인 추론 인프라와 diffusion forcing을 결합하여 실시간 고해상도 생성 비디오를 구현하는 방법을 보여줍니다.
- **핵심 교훈**: "스트리밍" 생성 AI로의 전환은 진정한 인터랙티브성을 가능하게 하며, 비디오 생성을 일괄 처리 과정에서 실시간 유틸리티로 변화시킵니다.
