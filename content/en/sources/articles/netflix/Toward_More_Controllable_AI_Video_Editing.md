---
title: "Toward More Controllable AI Video Editing"
description: Vera layered video diffusion and VOID physically-plausible inpainting for artist-controlled generative editing of promotional assets
tags: [source, article, netflix, generative-models, video, diffusion, computer-vision]
locale: en
source_url: "https://netflixtechblog.com/toward-more-controllable-ai-video-editing-an-early-research-exploration-at-netflix-eb8160ed60a2"
blog: netflix
published: 2026-06-23
---

# Toward More Controllable AI Video Editing

Authors: Zhuoning Yuan, Ta-Ying Cheng, Benjamin Klein, Bahareh Azarnoush. Netflix produces trailers, teasers, and social shorts from original footage — edits (adding elements, replacing backgrounds, removing objects) that take hours of specialist manual work. Generative video editors promise help but regenerate every pixel: unintended edits to identity/performance/details and physically implausible removals (a deleted object's collision partner keeps moving wrongly). Research goal: AI serving creative intent with precise artist control — what changes and how. Two explorations with public papers: Vera (layered diffusion) and VOID (interaction-aware inpainting).

## Background: the control gap

Text prompts + spatial masks + motion trajectories + style references as control signals over video-diffusion backbones with ControlNet-style adapters face three professional-use blockers: temporal consistency, fine-grained control, compute cost. Regenerating full frames couples intended edits with regions that must stay untouched.

## Methodology

**Vera: layered video diffusion.** Given source video + text instruction, jointly generate an edit layer + alpha matte, composited over the original footage — pixels outside edited regions stay perfectly intact. Supports object addition and background replacement. Training data (no public layered dataset existed): self-built 486k-frame corpus at 832×480 in three tiers — synthetic composites (foreground mattes over generated backgrounds, strong alpha supervision), realistic single-object (segmentation → matting → inpaint/generation → human filtering), realistic multi-object with effects (isolated objects with shadows/reflections). Architecture: Mixture-of-Transformers — three separate DiTs (edit, alpha, composite branches with own QKV/FFN, joint self-attention over concatenated tokens), initialized from one pretrained T2V base plus patch-embedding layers for video/mask inputs, shared RoPE, zero-initialized layer-distinguishing embeddings. Two variants: 1.3B and 14B.

**VOID: object and interaction deletion.** Beyond "behind-object" inpainting and shadow/reflection cleanup: a VLM reasoning pipeline identifies causally-affected regions (objects that would fall/collide/change trajectory), encoded into a quadmask guiding a two-pass diffusion pipeline that synthesizes the counterfactual "as if the object was never there".

**Evaluation.** Vera benchmark: 72 object-addition + 69 background-change video-prompt pairs across motion/camera/scene difficulty; three axes — content preservation (pixel + perceptual), instruction compliance, video quality. Human study: 19 creative reviewers, 512 side-by-side trials vs five baselines.

## Results

- Vera-1.3B and 14B significantly beat baselines on content preservation with comparable video quality and instruction compliance; humans preferred Vera-1.3B over all baselines on preservation and compliance, with clear video-quality edge on object addition.
- Status: early research, not in any production pipeline — prototypes with disclaimers.

## Limitations / open questions

- Compute cost of diffusion video editing remains unaddressed for production use.
- Temporal consistency under fast/complex motion and multi-object dynamics is still benchmark-limited (141 pairs).
- Artist-control UX (mask authoring, trajectory specification) outside this post's scope.

## Relevance to SW engineers

- Decouple edits from preservation architecturally (layers + mattes), not as a loss term — guarantees beat penalties for "don't touch" regions.
- When no dataset exists, build tiered synthetic→realistic corpora with explicit complexity staging.
- Distributionally different outputs deserve separate capacity (MoT branches) with shared interaction (joint attention).
- Pair automated metrics with domain-expert human studies; reviewers catch what pixel metrics miss.

## Related concepts

- `concepts/machine-learning/diffusion.md` (video diffusion, ControlNet adapters)
- `concepts/machine-learning/attention.md` (DiT, RoPE, joint attention)
