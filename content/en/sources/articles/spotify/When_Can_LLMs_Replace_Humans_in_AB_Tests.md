---
title: When Can LLMs Replace Humans in A/B Tests?
description: Spotify's statistical framework for when LLM predictions can stand in for human outcomes in A/B tests — surrogate endpoint theory, Upworthy empirical results, and why raw LLM predictions attenuate treatment effects
tags: [source, rss, spotify, ab-testing, llm-eval, statistics, causal-inference]
locale: en
source_url: "https://engineering.atspotify.com/2026/8/when-can-llms-replace-humans-in-a-b-tests"
blog: spotify
published_date: 2026-08-13
---

# When Can LLMs Replace Humans in A/B Tests?

Authors: Sebastian Ankargren (Senior Data Scientist), Joel Persson (Research Scientist, Computational Economics), Mårten Schultzberg (Senior Manager, Staff Data Scientist). Source: Spotify Engineering, Aug 13, 2026.

**Lead**: LLM predictions can stand in for human outcomes in A/B tests, but only by assumption, not by design. Calibrating LLM outputs against human A/B data can recover the human treatment effect — but only when two identification conditions hold, and those conditions cannot be verified for genuinely new treatments. The promise is least justified precisely where it offers the most benefit.

## Background: why the question matters

The pitch is straightforward: run the experiment on a model instead of on users, get results in hours instead of weeks, and skip traffic allocation entirely. But most proposals skip the statistical question that makes experiments valid in the first place: under what conditions does the procedure identify the treatment effect of interest?

Randomized experiments are the gold standard because random assignment causally identifies the treatment effect **by design**. Replacing real user responses with LLM-generated predictions removes that guarantee — identification then holds only **by assumption**. The authors formalize those assumptions using surrogate endpoint theory from biostatistics: if a surrogate outcome captures everything about a treatment that matters for the outcome, experimenting on the surrogate gives the correct result. Clinical trials routinely use lab biomarkers as fast, cheap surrogates for clinical endpoints; LLM predictions are now the analogous candidate surrogate for user responses in digital A/B tests.

## Empirical evidence: raw LLM predictions are biased, not just noisy

The team tested the promise on the Upworthy Research Archive, the largest open-access A/B test dataset available — click-through rates for headline variants across thousands of experiments. They prompted `gpt-4o-mini` to predict a typical user's click-through rate for each headline, separately for treatment and control variants.

- Using raw LLM predictions in a standard experimental analysis recovered only **39% of the observed human treatment effect**.
- The bias is **systematic and directional**: LLM outcomes attenuate treatment effects toward zero, making treatments look less than half as effective as they actually are.
- This is not random noise that averages out — it is structural attenuation. Applied across many product decisions, LLM-based experiments would systematically steer teams away from changes users actually value.

## The framework: surrogacy + comparability, plus calibration

Two conditions must hold for calibrated LLM outputs to recover the human treatment effect:

1. **Surrogacy**: the LLM prediction must capture everything about the treatment that matters for the human outcome — i.e., the treatment affects the outcome only through channels the surrogate reflects. Like all proxy metrics, LLM surrogates work until the relationship between proxy and outcome shifts.
2. **Comparability**: the calibration mapping learned from past experiments must still apply to the new experiment — the new treatment must be comparable to the treatments the calibration was fit on.

When both hold, calibrating LLM outputs on human A/B data recovers the treatment effect. When either fails, the estimate is biased — not from lack of data, but because the procedure identifies something else: with infinite LLM predictions you would recover exactly the effect **on the LLM**, not the effect on users. The framework makes the proxy–outcome relationship explicit and testable, and spells out the consequences when it fails. It cannot guarantee the relationship holds for the experiment you care about most: the one testing something new. The further a new treatment is from past experiments, the less plausible comparability becomes.

## Practical complications

- **Model drift**: any calibration function is fit to a specific model at a specific point in time. Providers update and replace models; a calibration learned today may be invalid six months from now, even for nominally the same model.
- **Temporal bias**: any new calibration function should ideally be fit on new user experiments — otherwise it may be temporally biased.
- **Diminishing promise**: surrogacy and comparability can become more realistic over time (better models, more calibration data), but the method's value proposition — skipping human experiments — is strongest for novel treatments, exactly where the assumptions are weakest.

## Limitations / open questions

- Results are demonstrated on headline click-through (Upworthy); generalization to engagement, retention, or revenue outcomes is untested.
- The paper shows a specific calibration methodology works on this dataset; which methods work in general remains open.
- Surrogacy is fundamentally untestable for a never-before-run treatment — a structural limitation, not a data gap.

## Relevance to SW engineers

- Do not treat LLM judgments as drop-in replacements for user A/B tests; raw LLM evals understate effect sizes by more than half in this study.
- If you use LLM evals as proxy metrics, calibrate them against human data, state the surrogacy/comparability assumptions explicitly, and re-calibrate when models or time periods change.
- Related: `concepts/machine-learning/transformer.md`, `concepts/ai-engineering/agent.md`.

## References

- Source article: https://engineering.atspotify.com/2026/8/when-can-llms-replace-humans-in-a-b-tests
- Companion piece: Better Experiments with LLM Evals — A funnel, not a fork (Spotify Engineering, May 2026)
