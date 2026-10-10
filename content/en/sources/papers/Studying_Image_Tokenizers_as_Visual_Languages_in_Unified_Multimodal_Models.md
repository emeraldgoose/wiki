---
title: "Studying Image Tokenizers as Visual Languages in Unified Multimodal Models"
description: "Do discrete image tokenizers behave like visual languages inside unified multimodal models — vocabulary, grammar, and compositionality under test"
locale: "en"
source_url: "https://arxiv.org/abs/2609.09143"
arxiv_id: "2609.09143"
authors: ["Siting Li", "Zhengyang Wang", "Simon Shaolei Du", "Xi Chen", "Yang Liu"]
published: "2026-09-08"
tags: [source, paper, machine-learning]
---

# Studying Image Tokenizers as Visual Languages in Unified Multimodal Models

## Abstract

Image tokenizers define the “visual language” of unified multimodal models, yet are commonly studied through isolated metrics or generation-/understanding-only evaluations. These evaluations do not fully capture how visual tokens behave when modeled jointly with text. We build a controlled pure-autoregressive testbed and track task-specific validation losses during multimodal continual pretraining across text, image, text-to-image (T2I), and image-to-text (I2T) prediction. We examine how these losses scale and relate to downstream performance, then use them to study multimodal learnability—how well image and text tokens are jointly modeled—and tokenizer design. We find that (1) losses should be analyzed by task, since they exhibit distinct scaling behavior and rank tokenizers differently. (2) The loss–performance relationship depends on the predicted token space: for a fixed tokenizer, T2I and I2T losses correlate with generation quality, but across tokenizers, the T2I loss–performance relationship shifts with the image-token space, whereas I2T loss, computed over a shared text vocabulary, provides a more consistent signal. I2T loss also correlates with both generation and visual understanding performance after supervised finetuning. Using losses as a lens, we show that (3) better reconstruction does not necessarily yield lower task-specific losses or stronger downstream performance, and that (4) image tokenizer choice can affect text modeling under joint optimization. As case studies, we revisit three tokenizer design axes—the discriminator, semantic supervision, and vocabulary size—to examine their effects on joint modeling and downstream performance. Together, our testbed offers a complementary perspective on image tokenizers as visual languages, highlighting their interplay with text in joint multimodal training.

## Background

In large-scale unified multimodal models, particularly those using autoregressive (AR) modeling, the discrete image tokenizer is a critical component. It converts raw pixels into discrete symbols that are modeled alongside text. Thus, the image tokenizer is more than a preprocessing module; it defines the "visual language" that the language model must learn and align with text.

Current research on tokenizers often relies on isolated metrics (like reconstruction-based rFID) or specific downstream tasks (generation-only or understanding-only). However, these evaluations fail to capture how visual tokens behave when modeled *jointly* with text in a single, shared AR framework. Because joint training can affect both image-token modeling and cross-modal alignment, understanding the interplay between the tokenizer and the text modality is essential for optimizing multimodal models.

## Methodology

The researchers developed a controlled, pure-autoregressive (AR) continual pretraining framework to study these effects.

### Experimental Setup
- **Backbone**: Qwen3 language model.
- **Task Scales**: Three model sizes (0.6B, 1.7B, and 4B parameters).
- **Training Process**: Continual pretraining on a mixture of 60M samples (6.6M pure-text and 53.3M image-text samples from LAION-Aesthetics, JourneyDB, and BLIP3o datasets), followed by supervised finetuning (SFT) on 4.9M multimodal instruction-following samples.
- **Evaluation Metrics**: Task-specific validation losses for four distinct tasks: text, unconditional image, text-to-image (T2I), and image-to-text (I2T).

### Tokenizer Design Axes Investigated
1.  **Discriminator**: Comparing a standard PatchGAN discriminator against a DINO-based discriminator.
2.  **Semantic Supervision**: Evaluating the impact of adding a CLIP-based contrastive loss to encourage higher-level semantic representation.
3.  **Vocabulary Size**: Examining how the number of discrete tokens affects multimodal learnability and downstream performance.

## Results

The study yielded several key findings regarding the role of image tokenizers:

- **Task-Specific Scaling**: Pretraining losses for text, image, T2I, and I2T do not scale identically. Text-modeling quality is largely inherited from the pretrained backbone, while image-related tasks benefit significantly from multimodal continual pretraining. Because they scale differently, an averaged loss is an insufficient metric for evaluating tokenizer performance.
- **Consistency of I2T Loss**: While T2I loss correlates with generation quality for a *fixed* tokenizer, its relationship with performance shifts across different tokenizers due to the differing prediction spaces. Conversely, I2T loss (computed over a shared text vocabulary) provides a consistent cross-tokenizer signal that correlates well with both generation and visual understanding performance.
- **Reconstruction vs. Learnability**: Higher reconstruction fidelity (e.g., lower rFID) does not always guarantee better multimodal learnability or downstream performance. For example, adding a DINO-based discriminator improved reconstruction but did not improve joint modeling performance.
- **Cross-Modal Effects**: The choice of image tokenizer can affect text modeling. Specifically, semantic supervision and certain vocabulary sizes can influence the difficulty of predicting text tokens under joint training.

## Limitations & Open Questions

- The relationship between reconstruction fidelity and multimodal learnability remains complex and not always monotonic.
- The study notes that while reconstruction metrics are useful, they may diverge from the requirements of joint multimodal optimization.
- Further research is needed to understand the optimal balance between compression ratio, reconstruction quality, and cross-modal alignment.

## Relevance to Software Engineers

For engineers building or fine-tuning multimodal AI systems, this paper highlights that:
- **Metric Selection Matters**: Relying solely on image reconstruction metrics (like rFID or PSNR) can be misleading when the goal is unified multimodal performance. 
- **Diagnostic Signals**: I2T (Image-to-Text) loss can serve as a reliable, consistent diagnostic signal for tracking training progress across different tokenizer architectures.
- **Holistic Optimization**: Optimizing a tokenizer for better image reconstruction might not actually improve the model's ability to reason or generate text-aligned visual content.

## References

- [63] Qwen3 language models.
- [18] Heusel et al. (2017) GANs trained by a two time-scale update rule.
- [35] UniTok: a unified tokenizer for visual generation and understanding.
- [62] GigaTok.
