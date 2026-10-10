---
title: "Vidu S2: Real-Time Interactive, Editable, and Spatial Video Generation"
published: 2026-09-10
arxiv_id: "2609.11638"
url: "https://arxiv.org/abs/2609.11638"
authors: ["Jintao Zhang", "Kai Jiang", "Jintao Chen", "Xu Wang", "Deyuan Liu", "Jungang Li", "Dechuang Chen", "Ming Lin", "Jingjiang Zhou", "Haopeng Jin", "Qi Jia", "Xiaohang Wang", "Yaole Wang", "Zhanqiang Zhang", "Ran Li", "Zhengkun Huang", "Shuyue Xiong", "Yuji Wang", "Zikun Dai", "Hui He", "Yang Luo", "Mang Ning", "Weiqi Feng", "Chengyang Ye", "Xinyue Lin", "Min Zhao", "Hongzhou Zhu", "Hengkai Tan", "Zeyuan Wang", "Chendong Xiang", "Kaiwen Zheng", "Zhijie Deng", "Fan Bao", "Jianfei Chen", "Jun Zhu"]
tags: [source, paper, machine-learning]
---

# Vidu S2: Real-Time Interactive, Editable, and Spatial Video Generation



## Abstract
We present Vidu S2, which comprises Vidu S2-Avatar, a real-time interactive digital-character model, and Vidu S2-Editing, a real-time video editing model. Moreover, we explore the feasibility of real-time spatial video generation for both Vidu S2-Avatar and Vidu S2-Editing. Compared with Vidu S1, Vidu S2-Avatar supports real-time 720p video generation, generation with dynamic references that can be updated at any moment, and stronger instruction following, such as dancing. Vidu S2-Editing supports editing a video stream in real time, including style rendering, clothing replacement, character replacement, and background replacement. Experiments show that Vidu S2 outperforms all baselines.

## Background & Problem Setup
The demand for real-time interactive video generation is growing, particularly for digital avatars and dynamic video editing. Previous models (like Vidu S1) lacked the speed for real-time 720p output and the flexibility to handle dynamic references or complex instructions (e.g., specific dance moves) in a streaming fashion. There is also a need for consistent spatial video generation that maintains depth and immersion.

## Methodology

### Vidu S2-Avatar
- **Goal**: Real-time interactive digital character generation.
- **Key Features**: Supports 720p output, dynamic reference updates, and improved instruction following.
- **Training Strategy**: Employs bidirectional image- and reference-to-video training.
- **Techniques**: 
    - **Hybrid Teacher and Diffusion Forcing**: Used to stabilize training and improve temporal consistency.
    - **Self-Replay Forcing**: Enhances the model's ability to maintain identity over long sequences.
    - **Super-Resolution Refiner**: ensures high-quality 720p output.

### Vidu S2-Editing
- **Goal**: Real-time video stream editing.
- **Capabilities**: 
    - **Style Transfer**: Changes brushwork and palette (e.g., watercolor, gongbi) while preserving subject identity.
    - **Virtual Try-On**: Replaces garments (e.g., white shirt, denim jumpsuit) while maintaining body motion and occlusion.
    - **Subject Replacement**: Swaps characters while keeping poses and camera trajectories.
    - **Background Replacement**: Changes environments (e.g., Paris cafe, bedroom) while keeping the foreground subject intact.

### Spatial Video Generation
- Vidu S2 explores generating left- and right-eye views to create 3D-like spatial video, improving depth separation between foreground and background.

## Results
- **Quantitative/Qualitative**: Vidu S2 outperforms baselines (e.g., PixVerse, Runway, XMax, Decart) in identity preservation and temporal stability.
- **Avatar Consistency**: Maintains facial identity, hairstyle, and fine-grained geometry without the drift seen in competitors.
- **Editing Precision**: Successfully handles complex tasks like garment deformation during "shirt-pulling" actions, where other models fail.

## Limitations & Relevance
- **Relevance**: For software engineers and ML practitioners, Vidu S2 demonstrates the potential of combining diffusion forcing with efficient inference infrastructure to achieve real-time, high-resolution generative video.
- **Takeaway**: The move toward "streaming" generative AI allows for true interactivity, turning video generation from a batch process into a real-time utility.
