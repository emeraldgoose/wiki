---
title: Real-World Knowledge-Guided Change Data Synthesis for Remote Sensing
arxiv_id: 2608.24263
HF_URL: https://huggingface.co/papers/2608.24263
published: 2026-08-25
authors: Yaoyi Qi, Xingxing Weng, Chao Pang, Yongkang Cui, Xiangyu Hao, Xiaokang Zhang, Guibo Zhu, Gui-Song Xia
locale: en
tags: [source, paper, machine-learning]
---

# Real-World Knowledge-Guided Change Data Synthesis for Remote Sensing

**Authors**: Yaoyi Qi, Xingxing Weng, Chao Pang, Yongkang Cui, Xiangyu Hao, Xiaokang Zhang, Guibo Zhu, Gui-Song Xia · **Published**: Aug 25, 2026 · **arXiv**: [2608.24263](https://arxiv.org/abs/2608.24263) · **HuggingFace**: [https://huggingface.co/papers/2608.24263](https://huggingface.co/papers/2608.24263)

## Abstract

Change data synthesis provides a cost-effective solution for expanding training data and improving the performance of change detection models. However, existing synthesis methods typically rely on handcrafted rules to simulate changes, where limited coverage of class transitions restricts the diversity of synthesized data, while predefined transition designs limit their flexibility in accommodating varied change types. In this work, we introduce KnowChange, a knowledge-guided change data synthesis framework that leverages pretrained vision-language models as knowledge sources to reason about plausible change locations and class transitions from pre-change scenes and desired change types. By integrating knowledge-guided change simulation with generalizable synthesis models, KnowChange enables flexible synthesis of diverse change types within a unified framework. Extensive experiments demonstrate that KnowChange-generated data consistently outperforms existing synthetic datasets in both synthetic-to-real transfer and synthetic data augmentation, despite being generated at a compact scale. Further analyses show that the knowledge-guided change simulation can be seamlessly integrated into existing synthesis pipelines and enhance the downstream utility of synthesized data.

## Background and Problem Setup

Change detection in remote sensing identifies differences between two temporal images of the same area, typically taken at different times. The goal is to produce a binary (or multi-class) mask indicating where changes have occurred. This is fundamental to applications such as urban growth monitoring, disaster damage assessment, agricultural change tracking, and deforestation detection.

A major challenge in training change detection models is the lack of labeled data. Collecting and annotating change pairs is expensive because:
- Change events are inherently rare (most of the image area is unchanged between two timestamps).
- Annotating the exact changed pixels requires expert knowledge.
- Changes vary widely in type (construction, flooding, deforestation, etc.) and scale (from small potholes to city-wide expansion).

Synthetic data generation has been explored as a cost-effective alternative, but existing methods face two key limitations:

1. **Limited class transition coverage**: Handcrafted rules can only simulate a small subset of possible change types. Rules like "add a building" or "remove a vehicle" don't cover the full spectrum of real-world changes.

2. **Rigid transition designs**: Predefined designs limit flexibility. Once the design pattern is set, it's difficult to adapt to new change types without extensive re-engineering.

These limitations restrict the diversity of synthesized data, leading to models that generalize poorly to real-world change types.

## KnowChange Framework

KnowChange addresses these limitations by leveraging pretrained vision-language models as knowledge sources to guide the change synthesis process. The framework has two integrated components:

### Knowledge-Guided Change Simulation

This component uses pretrained vision-language models (such as CLIP, Flamingo, or other multimodal models) as knowledge sources to reason about:

- **Plausible change locations**: Given a pre-change scene, what locations are likely to experience changes? The vision-language model provides semantic understanding of what objects or structures might be added, removed, or modified.
- **Class transitions**: What class of change is occurring? (e.g., "building added", "road destroyed", "vegetation cleared", "flooded"). The vision-language model can classify the type of change and generate appropriate synthetic labels.

The key insight is that vision-language models have broad world knowledge from pre-training on vast image-text pairs, allowing them to reason about plausible changes even for change types they've never seen specifically for remote sensing.

### Generalizable Synthesis Models

KnowChange integrates generalizable synthesis models that can generate realistic change given the guidance from the knowledge-guided component. These models:

- Take as input the pre-change scene and the desired change type/location.
- Generate a post-change scene that looks realistic and consistent.
- Produce pixel-level change masks for supervision.

The synthesis models are trained on a diverse set of change types but can generalize to new types thanks to the knowledge guidance.

### Integrated Pipeline

The KnowChange pipeline operates as follows:

1. **Input**: A pre-change remote sensing image and a desired change type (e.g., "flood", "construction", "vegetation loss").
2. **Knowledge reasoning**: The vision-language model analyzes the pre-change image and generates:
   - A set of plausible change locations (pixel-level or region-level).
   - The change class/category and relevant attributes (e.g., water depth for floods, building height for construction).
3. **Synthetic generation**: The synthesis model generates the post-change image and change mask, guided by the reasoning output from step 2.
4. **Output**: A synthetic change pair (pre-change, post-change) with ground-truth change mask, plus metadata about the change type and attributes.

## Integration with Existing Pipelines

One of KnowChange's key contributions is that the knowledge-guided change simulation can be seamlessly integrated into existing synthesis pipelines. Rather than replacing the entire pipeline, KnowChange adds a knowledge reasoning layer that enhances whatever synthesis model is already in use:

- **Plugin architecture**: The vision-language model reasoning can be plugged in as a pre-processing step before any synthesis model.
- **Compatibility**: Works with both image-to-image translation models (e.g., GAN-based, diffusion-based) and explicit change mask generation models.
- **Incremental improvement**: Adding the knowledge-guided step improves downstream utility even with the same base synthesis model.

## Experimental Results

KnowChange was evaluated extensively on change detection benchmarks:

### Synthetic-to-Real Transfer

KnowChange-generated data, despite being generated at a compact scale, consistently outperforms existing synthetic datasets in synthetic-to-real transfer. This means that models trained on KnowChange synthetic data generalize better to real remote sensing imagery than models trained on other synthetic data. The key finding is that knowledge-guided synthesis produces more realistic and diverse changes, leading to better transfer performance.

### Synthetic Data Augmentation

In addition to synthetic-to-real transfer, KnowChange also improves models trained with synthetic data augmentation. Models trained with KnowChange-generated data show improved performance on real-world change detection tasks compared to those trained with other synthetic datasets.

### Analytic Findings

Further analyses demonstrate that:

- The knowledge-guided change simulation can be seamlessly integrated into existing synthesis pipelines.
- The enhanced synthetic data improves downstream task performance even when the base synthesis model is unchanged.
- The diversity of synthesized change types is significantly broader than handcrafted rule-based approaches.

## Limitations and Open Questions

- **Vision-language model dependence**: KnowChange's effectiveness depends on the quality and coverage of the vision-language model used for knowledge reasoning. Models with better remote sensing understanding will produce more accurate guidance.
- **Change type coverage**: While KnowChange broadens the range of synthesizable change types, extremely rare or novel change types may still be challenging.
- **Spatial coherence**: The synthesized changes must maintain spatial coherence with the pre-change scene (e.g., flooded areas should be consistent with terrain elevation, buildings should follow existing street patterns). Ensuring this coherence remains an open research question.
- **Real-time synthesis**: The vision-language model reasoning step may add latency, which could be a constraint for real-time or near real-time change detection applications.
- **Generalization to other remote sensing modalities**: KnowChange has been primarily evaluated on optical satellite imagery. Extension to radar (SAR), multispectral, or hyperspectral imagery would broaden its applicability.
- **Ethical and interpretability concerns**: Using vision-language models as knowledge sources raises questions about bias propagation, interpretability of change decisions, and the ethical implications of synthetic change data in sensitive applications.

## Relevance to Software Engineers

For software engineers working on remote sensing, change detection, or synthetic data generation, KnowChange offers several concrete takeaways:

1. **Vision-language model as knowledge source**: If you're building a change detection training pipeline, consider using a pretrained vision-language model (CLIP, ALIGN, or other multimodal model) as a knowledge reasoner to guide data synthesis. The broad semantic understanding of these models can help generate more plausible and diverse synthetic changes.

2. **Plugin architecture for synthesis enhancement**: KnowChange's integration pattern is a plugin architecture — add a knowledge reasoning step before your existing synthesis model. This means you can improve your synthetic data quality without replacing your entire pipeline.

3. **Diversity over realism alone**: The experiments show that knowledge-guided synthesis outperforms existing methods even at a "compact scale." Focus on generating diverse change types rather than just making individual images more realistic. Diversity across change types leads to better model generalization.

4. **Mask-aware synthesis**: Generate both the post-change image and the change mask simultaneously. The change mask provides ground-truth supervision for training change detection models, and generating it alongside the image ensures consistency.

5. **Incremental improvement**: Adding the knowledge-guided reasoning step improves performance even with the same base synthesis model. If you're resources-constrained, enhancing your pipeline with a knowledge reasoning layer can yield significant gains without needing a new synthesis model.

6. **Compact-scale effectiveness**: KnowChange produces strong results despite being generated at a compact scale. This is important for practical deployment: you don't need massive computational resources to produce high-quality synthetic change data.

7. **Spatial coherence awareness**: When implementing your own knowledge-guided synthesis, pay attention to spatial coherence between the synthesized changes and the pre-change scene. Synthetic changes that respect terrain, lighting, and existing structures will produce more realistic and useful training data.

8. **Rescaling for hybrid approaches**: The paper's analysis of sparsified dense designs has an analogy here: you may have existing generation infrastructure (e.g., GAN-based synthesis) and can add a knowledge reasoning layer on top without replacing the generator. Design your pipeline to support this hybrid approach.

9. **Evaluation across transfer settings**: When evaluating change detection models, include synthetic-to-real transfer tests. Models trained on synthetic data that generalizes well to real imagery (like those trained on KnowChange data) are more valuable than those that only perform well on in-distribution synthetic data.

10. **Synthesis metadata**: The change type and attributes generated by the knowledge-guided component serve as rich metadata. Use this metadata to organize your training data, enable targeted model training for specific change types, and support analysis of model strengths and weaknesses across change categories.

## Related Concepts

- `concepts/data-engineering/remote-sensing-change-detection.md`, `concepts/data-engineering/synthetic-data-generation.md`, `concepts/data-engineering/vision-language-models.md`