---
title: "LLaDA-Image: Building Strong Image Generators with Fully Open Training Recipes"
description: "HuggingFace Daily Papers — 2026-09-03 — 6B unified image generator with image-only pre-training and TwinFlow distillation"
tags: [source, paper, huggingface, machine-learning]
locale: en
arxiv_id: 2609.03796
published: 2026-09-03
---

# LLaDA-Image: Building Strong Image Generators with Fully Open Training Recipes



**arXiv**: [2609.03796](https://arxiv.org/abs/2609.03796) | **HuggingFace**: [papers/2609.03796](https://huggingface.co/papers/2609.03796) | **Published**: 2026-09-03 | **Submitted by**: Haoxing Chen (Inclusion AI) | **Paper of the day #3 (2026-09-04)**

**Authors**: Chuyan Chen, Haoxing Chen, Kun Chen, Zhenglin Cheng, Long Cui, Ruishan Fang, Zhangxuan Gu, Zhicheng Huang, Zhenzhong Lan, Yuanting Lei, Haoquan Li, Jianguo Li, Rongchuan Li, Sidu Li, Tao Lin, Deyuan Liu, Jiacheng Liu, Lin Liu, Yuxuan Lou, Zhisheng Lu, Yuxin Ma, Shuheng Shen, et al. (AGI Research Center, Inclusion AI)

## Abstract

LLaDA-Image is a unified framework pairing a **6B Diffusion Transformer (DiT) trained from scratch** with a **frozen vision-language understanding module** built on the LLaDA2.0-Mini diffusion-language-model backbone. Instead of leaning on paired image–text data from the start, it first builds a strong visual generative prior through **image-only pre-training and mid-training**; the full generation pipeline processes ~**220M samples, 98% real images**, with image-only training accounting for over 90% of the total. Optimization uses **parameter-free RMSNorm throughout the DiT plus the Muon optimizer** for stability at scale. The unified model produces photorealistic images while following fine-grained editing instructions, and is distilled into **LLaDA-Image-Turbo** for **2–4-step** inference. On Qwen-Image-Bench it scores **53.53 (English) and 53.38 (Chinese)** — open-source SOTA on both tracks. Weights, training code, and detailed recipes are fully released (Base, Turbo, plus FP8 variants of each).

## Background: Problem Setup (WHY)

Image systems are shifting from single-purpose text-to-image models to general visual-creation systems that must understand complex multilingual instructions, render photorealistic content, preserve reference evidence during edits, render text accurately, and still run within practical inference budgets. Proprietary systems lead, but their data, models, and recipes are closed. For open models the goal is therefore not quality alone: capability must come with an attainable data budget, stable large-scale training, and efficient deployment.

The prevailing paradigm couples visual-prior learning with language alignment from step one, demanding paired captions during the most compute-intensive stages — yet captions are expensive and lossy (details in a caption can vanish after downsampling at low training resolutions), and synthetic-heavy mixtures converge fast early but propagate artifacts and cap long-run realism. Two further linked problems: connecting multimodal understanding to generation while preserving reference-image evidence for editing, and compressing long diffusion trajectories for deployment. LLaDA-Image co-designs data, architecture, and deployment against all three.

## Methodology (HOW)

### Architecture: three components, one checkpoint

- **dLLM-based VLM (frozen).** Understanding module on the LLaDA2.0-Mini backbone with SigLIP-VQ vision encoder. Unlike static text encoders, it jointly reasons over text, visual context, and structured reasoning traces. Crucially, during editing the **reference image bypasses the VLM entirely** and is injected straight into the DiT — the VLM sees only the editing instruction.
- **Understanding-to-generation connector.** Two generation-specific modules bridge the representation gap: a **Residual Query Adapter (RQA)** — learnable queries cross-attend to the multimodal input, are appended to it, and prompt the frozen VLM in a single prefill pass to expose generation-useful context — followed by a shallow **Transformer connector** projecting VLM hidden states into DiT conditioning space.
- **Single-stream DiT (6B).** Image and condition tokens are embedded into one shared sequence and processed jointly through the same blocks, so every block models condition↔visual interactions via joint self-attention (no separate streams). It predicts the flow-matching velocity. **Recipe #1: every normalization layer is parameter-free RMSNorm**, which the authors credit for long-horizon optimization stability.

### Training pipeline: visual prior first, language later

1. **CoT SFT** prepares the frozen understanding backbone.
2. **Image-only pre-training (256²).** The frozen dLLM-VLM derives the condition from the *same image region* the DiT learns to generate — condition–target compatibility with no external caption — so mildly-resized informative crops of high-res images can be used directly.
3. **Image-only mid-training (512², aspect-ratio buckets).**
4. **Supervised fine-tuning (512² → 1024²)** for text-to-image, then **joint generation–editing** training (T2I + I2I), with targeted refinement on text-rich and portrait data and checkpoint merging. The **real-image share stays above 70% throughout SFT** — slower early benchmark gains than synthetic-heavy recipes, but stronger realism at convergence and a higher long-horizon ceiling.
5. **TwinFlow few-step distillation.** Building on distribution-matching distillation (DMD) and self-adversarial flow training: one shared DiT backbone plays both roles via **signed time** — positive +t updates the generator, negative −t trains the fake-score estimator (no separate score network). Two output heads ("one-input, dual-output"): a fake-score head and a DMD head; at inference only the DMD head is kept and the fake-score head discarded. Result: **LLaDA-Image-Turbo in 2–4 sampling steps**.

## Results

- **Qwen-Image-Bench.** 53.53 overall (English) and 53.38 (Chinese) — **new open-source SOTA on both tracks**, ordered against rivals including Qwen-Image, GPT-Image 2, and Gemini Flash Image in the paper's qualitative grids (photoreal portraits, Chinese landscape painting with calligraphy, bilingual text rendering).
- **Breadth.** Competitive instruction-guided editing (style transfer, text replacement, object removal/addition, background swap, gesture edits) on GEdit-Bench, plus LongText-Bench and CVTG-2K — all from one checkpoint, no task-specific backbones.
- **Deployment profiles.** Base (multi-step, quality) vs. Turbo (2–4-step, cost); four released checkpoints total (Base, Turbo, FP8 of each) plus training/inference code and data-construction recipes.
- **Qualitative hook.** The report opens with a reader challenge — a grid of apparent photographs the reader must classify as real or generated — then reveals **every image was generated**, spanning T2I synthesis and bilingual text rendering (presented as demonstration, not a controlled study).

## Limitations / Open Questions

- **Scope disclaimer is explicit.** The authors do not claim universal optimality of each component nor an exhaustive architecture/data-mixture comparison — the contribution is an inspectable, reusable recipe.
- **Real-data patience required.** The real-dominant mixture improves more slowly on early benchmarks; teams optimizing for fast leaderboard movement may find synthetic-heavy recipes tempting despite the realism ceiling.
- **Single-model editing bounds.** Reference-preserving edits route around the VLM by design; failures in fine-grained identity preservation and complex multi-instruction edits remain the practical frontier.
- **6B operating point.** The recipe is demonstrated at one scale; scaling laws for the image-only-prior approach beyond 6B are untested.

## Relevance to Software Engineers

- **Decouple prior from alignment in your own pipelines.** The image-only self-conditioning trick (condition derived from the generation target's own region, no captions) is transferable anywhere paired data is the bottleneck — a way to burn cheap unlabeled images into a prior before spending caption budget.
- **Stability recipe worth copying.** Parameter-free RMSNorm everywhere + Muon optimizer is a concrete, small-diff intervention for long-horizon generative training instability.
- **Distill with TwinFlow's signed-time pattern.** One backbone, two heads, role-by-timestep-sign avoids a separate fake-score network — applicable to any flow-matching model you need to compress for serving.
- **Ship two profiles from one lineage.** Base for quality, Turbo for cost, FP8 variants for memory — a release matrix to copy for any generative model serving path.
- **Where not to use it.** Don't expect SOTA motion/video or guaranteed text-rendering accuracy in production rendering pipelines without your own eval harness — run Qwen-Image-Bench/LongText-Bench-style checks on your own prompt distribution first.

## Related Concepts

- `concepts/machine-learning/transformer.md`
- `concepts/ai-engineering/llm-training.md`

## References

- arXiv: https://arxiv.org/abs/2609.03796
- HuggingFace: https://huggingface.co/papers/2609.03796
- Code + weights: https://github.com/inclusionAI/LLaDA-Image and https://huggingface.co/collections/inclusionAI/llada-image
