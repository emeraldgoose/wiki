---
title: "FLAT - Resampling Image and Text into 1D Flexible-Length Aligned Transmodal Tokens for Retrieval and Generation"
published: 2026-09-15
arxiv_id: "2609.16591"
url: "https://arxiv.org/abs/2609.16591"
authors: ["Guangyu Sun", "Shlok Kumar Mishra", "Wentao Bao", "Robert Zhenheng Yang", "Xiao Wang", "Xiyuan Wang", "Yujunrong Ma", "Chen Yuan", "Max Xiangjun Fan", "Jun Xiao", "Jianpeng Cheng"]
tags: [source, paper, machine-learning]
---

# FLAT - Resampling Image and Text into 1D Flexible-Length Aligned Transmodal Tokens for Retrieval and Generation

[KO version](../ko/sources/papers/FLAT_Resampling_Image_and_Text_into_1D_Flexible-Length_Aligned_Transmodal_Tokens.md)

## Abstract

Traditional multimodal pipelines split into two stages: a contrastive or self-supervised visual encoder is trained first (CLIP, DINO), then a separate downstream generative model is conditioned on its frozen embeddings — bottlenecking generation behind frozen representations that must be re-aligned. FLAT (Flexible-Length Aligned Transmodal representations, Meta, September 2026) revisits joint representation learning and generation to produce linearly interpolatable embeddings directly consumable by generative decoders. A shared multimodal encoder is optimized together with text-to-image (T2I) and image-to-text (I2T) decoders, combining contrastive alignment with bidirectional cross-modal generative objectives so representations serve as both discriminative descriptors and generative conditions. Architecturally, images and text are resampled into a unified continuous 1D token sequence with nested dropout over prefix-K tokens for dynamic output lengths. One pre-training stage yields GenEval 71.1 on T2I; task-specific fine-tuning reaches 83.1 GenEval, 40.5 BLEU-4 / 138.6 CIDEr on MS-COCO captioning, Recall@5 of 86.8 (I2T) / 75.8 (T2I) on COCO and 98.3 / 93.6 on Flickr30K — plus native linear interpolation, latent arithmetic, and zero-shot composed retrieval.

## Background & Problem Setup

Two decoupled traditions dominate: contrastive representation learners (CLIP family, SigLIP) that align but cannot generate, and generative models (BLIP-2/LLaVA on frozen visual encoders; Stable Diffusion/SDXL/SD3/PixArt/Sana on frozen text encoders) that inherit the limits of embeddings they didn't train. Recent unified models either co-train encoders with generative backbones or go encoder-free in pixel space. FLAT takes the middle path — keep an explicit, contrastive, linearly-interpolatable embedding space, but optimize alignment and generation jointly — on the insight (after CoCa/BLIP) that retrieval and generation are mutually reinforcing: a representation good at discriminating should also condition synthesis in either direction, and vice versa. The work builds on 1D visual tokenizers (TiTok, FlexTok, GigaTok) that compress spatial grids into compact sequences, extended here to both modalities in one shared space, plus nested dropout (Matryoshka-style) for elastic sequence length.

## Methodology

**Representation encoder.** Input x of modality m ∈ {img, txt} is concatenated with N learnable register tokens R and passed through a shared VLM encoder f_enc (Qwen3.5-2B backbone with LoRA adapters, system prompt "Represent the input"); hidden states at register positions are linearly projected: z = W_lat · f_enc(x, R) ∈ R^{N×d}. Both modalities share registers and projection.

**Nested dropout.** Per training step a keep-length K is sampled once from the geometric ladder K = {1, 4, 16, 64, 256} and broadcast across ranks; only the prefix z_{:K} feeds the contrastive loss and both decoders. Geometric (not integer-uniform) sampling avoids wasting steps on imperceptible length differences; direct truncation beats FlexTok-style null-padding in their ablations.

**Decoders.** Prefix z_{:K} is mapped via task-specific MLP + RMSNorm into soft tokens e ∈ R^{K×h}. The I2T decoder is a standard autoregressive LM (visual soft tokens + "Describe the input" prompt → caption). The T2I decoder is a rectified-flow transformer (initialized from SANA-1.6B) denoising VAE latents, conditioned on textual soft tokens via cross-attention (flow-matching loss ‖v_φ(x̂_t, t, z_{:K}) − (ε − x̂)‖²).

**Losses.** (1) Bidirectional contrastive: late-interaction similarity averaged over matching register positions s_{ij}^{(K)}, with InfoNCE both directions (i2t + t2i)/2 over the global batch. (2) Captioning NLL. (3) Flow-matching MSE. Total L = λ_align·L_align + λ_txt·L_txt + λ_img·L_img; fine-tuning optimizes task subsets separately.

## Results

- **T2I generation**: single pre-train → GenEval 71.1; +88k-step decoder fine-tune on 120K clean pairs → **83.1**, above all compared baselines incl. two 7B models with prompt rewriting (evaluated no-rewrite). Complexity needs length: K=1 captures single object/color; relational categories (two objects, position, color binding ≈0.03 at K=1) recover steeply by K=4/16 (0.67).
- **I2T captioning** (COCO Karpathy, 55k-step decoder-LoRA tune): **40.5 BLEU-4 / 138.6 CIDEr**, steady gains with K; even K=1 beats CrossFlow/SCD-Net on CIDEr/METEOR/SPICE. Qualitatively K=1 gives coherent captions, longer prefixes add lexical precision (street→alley).
- **Retrieval** (contrastive-tuned encoder LoRA): COCO R@5 **86.8 I2T / 75.8 T2I**, Flickr30K **98.3 / 93.6** — and remarkably K-invariant: every metric within ~1pp from 64-dim (K=1) to 16K-dim (K=256), unlike MRL/SAE/CSR baselines that collapse at low width. First token carries global semantics.
- **Linear probing/clustering**: frozen K=1 token → 73.3% ImageNet top-1, scaling to **81.8%** at K=64 (above DREAM and all generative latents at matched dim); k-means on one token recovers ImageNet classes unsupervised.
- **Geometry**: FLAT halves CLIP's image-text centroid distance at one token, quarters it at 256 — a near-overlapping space enabling z_α = (1−α)z_1 + αz_2 smooth cross-modal interpolation, zero-shot arithmetic (sunrise − … + moonlit night preserves scene), and zero-shot composed retrieval on CIRR.
- **Ablations (7 loss combos, Shapley decomposition)**: full objective is the only one strong on all five metrics; each task is driven by its matched loss with complementary help from the others — alignment and generation reinforce rather than conflict.
- Project: https://guangyusun.com/flat-website/

## Limitations & Open Questions

- Fine-tuning is still needed per task to match SOTA; the pre-trained checkpoint trails on absolute retrieval/generation numbers (Appendix C/D quantify the gap and the value of FLAT pre-training vs. task-only training).
- Backbone scale is modest (2B encoder + 1.6B image decoder); whether the joint recipe holds at 7B+ with LLM rewriters in the loop is untested.
- Geometry results are qualitative plus centroid statistics; compositional failure modes at K=1 (binding, counting) remain, and multilingual/emoji and multi-frame video transfer (Appendix G) are preliminary.

## Relevance to SW Engineers

For RAG and multimodal product work, FLAT's headline is operational: **one encoder pass serves retrieval and generation at elastic cost** — K=1 (64-dim) already retrieves within a point of full width, so route cheap queries to 1–4 tokens and spend 64–256 only on compositional generations. The shared-space design also collapses two serving stacks (embedding model + generator conditioner) into one representation with arithmetic/composed-retrieval bonuses (e.g., "this image but at night" as vector math). If you maintain separate CLIP + diffusion-conditioner pipelines, this paper is the strongest current evidence for co-training them. Extends `concepts/ai-engineering/rag.md`, `concepts/ai-engineering/embedding.md`, and `concepts/machine-learning/attention.md`.

## References

- Paper: https://arxiv.org/abs/2609.16591 (HTML: https://arxiv.org/html/2609.16591v1) — Project: https://guangyusun.com/flat-website/
- CLIP (Radford et al. 2021); FlexTok/TiTok (Bachmann et al. 2025; Yu et al. 2024); CoCa (Yu et al. 2022); BLIP-2 (Li et al. 2023); SANA (Xie et al. 2025); GenEval (Ghosh et al. 2023)
