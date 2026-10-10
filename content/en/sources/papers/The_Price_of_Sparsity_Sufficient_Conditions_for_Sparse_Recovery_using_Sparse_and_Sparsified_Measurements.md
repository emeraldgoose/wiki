---
title: "The Price of Sparsity: Sufficient Conditions for Sparse Recovery using Sparse and Sparsified Measurements"
description: "Sufficient sample-size conditions for ML support recovery from sparse Gaussian measurements"
arxiv_id: 2509.01809
HF_URL: https://huggingface.co/papers/2509.01809
published: 2026-09-08
authors: Youssef Chaabouni, David Gamarnik
locale: en
tags: [source, paper, computer-science]
---

# The Price of Sparsity: Sufficient Conditions for Sparse Recovery using Sparse and Sparsified Measurements

**Authors**: Youssef Chaabouni, David Gamarnik · **Published**: Sep 8, 2026 · **arXiv**: [2509.01809](https://arxiv.org/abs/2509.01809) · **HuggingFace**: [https://huggingface.co/papers/2509.01809](https://huggingface.co/papers/2509.01809)

## Abstract

We consider the problem of support recovery for sparse binary signals from noisy linear measurements. For sparse Gaussian measurement matrices we identify sufficient conditions on the minimal sample size for maximum-likelihood recovery in the high-SNR regime $\frac{d s}{p} \to \infty$, where $p$ denotes the signal dimension, $s$ the number of non-zero components of the signal, and $d$ the expected number of non-zero components per row of measurement. Combined with known lower bounds, this yields an information-theoretic threshold of order $\frac{s \log(p/s)}{\log(d s / p)}$, making explicit the price of measurement sparsity. In particular, we highlight a regime where the sample-complexity loss from measurement sparsity is logarithmic while the computational gain is nearly linear. Second, we study recovery after sparsifying an originally dense Gaussian design: the observations are generated from the dense design, while estimation uses an independently sparsified design and a rescaled response. In the proportional regime $s = \alpha p$, $d = \psi p$, we prove that, for every fixed target error level $\delta$ and every slack $\varepsilon > 0$, a sample size of order $p / \psi^2$ is sufficient for support recovery for arbitrarily small $\psi$.

## Background and Problem Setup

The problem of support recovery arises in many machine learning and statistical settings where we observe linear measurements of a sparse signal and need to identify which components are non-zero. Formally, we observe:

$$y = A x^* + \ noise$$

where $x^* \in \mathbb{R}^p$ is a $s$-sparse signal (only $s$ out of $p$ components are non-zero), $A \in \mathbb{R}^{d \times p}$ is the measurement matrix, and $y \in \mathbb{R}^d$ are the observations. The goal is to recover the support $\text{supp}(x^*) = \{i : x^*_i \neq 0\}$ from the measurements $y$.

When the measurement matrix $A$ has i.i.d. Gaussian entries (sparse Gaussian measurement matrix), the recovery performance depends on the relationship between the sample size $d$, the signal dimension $p$, the sparsity level $s$, and the structure of the measurement matrix.

## Problem: Support Recovery for Sparse Binary Signals

In the support recovery problem, we're given $d$ linear measurements of an unknown $s$-sparse signal in $\mathbb{R}^p$, and we need to determine exactly which $s$ components are non-zero. This is fundamental to many applications including compressed sensing, sparse identification, and feature selection.

The difficulty of support recovery depends on several factors:

- **SNR (Signal-to-Noise Ratio)**: Higher SNR makes recovery easier.
- **Measurement ratio**: The ratio $d/p$ (number of measurements per dimension) is a key parameter.
- **Sparsity ratio**: The ratio $s/p$ (fraction of non-zero components) affects how hard recovery is.
- **Measurement matrix structure**: Whether the measurements are dense or sparse.

## Sparse Gaussian Measurement Matrices

When $A$ has i.i.d. $\mathcal{N}(0, 1/d)$ entries (sparse Gaussian measurements), the recovery performance is characterized by the high-SNR regime where the noise becomes negligible compared to the signal. In this regime, we can identify sufficient conditions on the minimal sample size $d$ for maximum-likelihood support recovery.

The key result identifies that the sample complexity depends on the term $\frac{d s}{p}$. When this term goes to infinity ($\frac{d s}{p} \to \infty$), maximum-likelihood recovery becomes possible. The precise threshold is:

$$\text{Sample complexity} \asymp \frac{s \log(p/s)}{\log(d s / p)}$$

This formula reveals the "price of measurement sparsity": compared to dense measurements (where $d$ can be smaller), sparse measurements require more samples to achieve the same recovery performance, but the additional cost is only logarithmic in the measurement ratio.

## Information-Theoretic Threshold

Combined with known lower bounds, the sufficient conditions yield an information-theoretic threshold for support recovery. This means that no algorithm can recover the support with high probability if the sample size is below this threshold, and the sufficient conditions show that this threshold is achievable by maximum-likelihood decoding.

The threshold of order $\frac{s \log(p/s)}{\log(d s / p)}$ makes explicit three distinct factors:

1. **$s \log(p/s)$**: The fundamental term from information theory — this is the number of bits needed to specify which $s$ components out of $p$ are non-zero, up to constant factors. This captures the "information cost" of support recovery.

2. **$\log(d s / p)$**: The "measurement sparsity penalty" — this logarithmic term accounts for the fact that sparse measurements provide less information per measurement than dense ones. As $d s / p$ grows, this penalty diminishes.

The ratio of these two terms gives the minimal sample size needed. When $d s / p$ is large (many measurements relative to the effective sparsity), the penalty is small, and the sample complexity approaches the information-theoretic lower bound $s \log(p/s)$.

## Proportional Regime Analysis

In the proportional regime where $s = \alpha p$ and $d = \psi p$ for constants $\alpha, \psi > 0$, the analysis simplifies significantly. In this regime:

- The signal occupies a fixed fraction $\alpha$ of all components.
- The measurement matrix has a fixed oversampling ratio $\psi$.

Under these conditions, the sufficient condition for support recovery becomes: a sample size of order $p / \psi^2$ is sufficient for support recovery for arbitrarily small $\psi > 0$ and fixed target error level $\delta$.

This result has several important implications:

1. **Sample efficiency**: The $p / \psi^2$ scaling shows that the sample complexity depends on the inverse square of the measurement ratio. Doubling the oversampling ratio ($\psi$) reduces the required samples by a factor of 4.

2. **Logarithmic loss**: The loss from measurement sparsity is logarithmic, meaning that even significant sparsity (small $\psi$) only incurs a logarithmic penalty in sample complexity.

3. **Computational gain**: In regimes where $\psi$ is small (few measurements relative to dimension), the computational gain from using sparse measurements can be nearly linear while the sample-complexity loss is only logarithmic.

## Sparsified Dense Design

The paper also studies a practical scenario: the observations are generated from a dense Gaussian design, but estimation uses an independently sparsified design with a rescaled response. This is a "best of both worlds" scenario:

- **Generation**: Observations $y = A_{\text{dense}} x^* + \text{noise}$ where $A_{\text{dense}}$ has i.i.d. Gaussian entries.
- **Estimation**: Use a sparsified measurement matrix $A_{\text{sparse}}$ for recovery, with appropriate rescaling to correct for the sparsification.

The analysis proves that support recovery is still possible with a sample size of order $p / \psi^2$, even though the measurements were generated densely but recovered using sparse measurements. This provides a theoretical justification for hybrid approaches that use dense measurements for generation but sparse measurements for recovery.

## Key Results Summary

| Regime | Sample Complexity | Key Insight |
|---|---|---|
| High-SNR, sparse Gaussian | $\frac{s \log(p/s)}{\log(d s / p)}$ | Logarithmic penalty from measurement sparsity |
| Proportional regime ($s=\alpha p, d=\psi p$) | $\frac{p}{\psi^2}$ | Sample efficiency depends on inverse-squared measurement ratio |
| Sparsified dense design | $\frac{p}{\psi^2}$ | Hybrid dense-generation/sparse-recovery works |

## Limitations and Open Questions

- **Extension to other measurement distributions**: The analysis is specific to Gaussian measurement matrices. Extension to sub-Gaussian, Rademacher, or other structured matrices would broaden the applicability.
- **Robustness to model mismatch**: The sufficient conditions assume the measurement matrix exactly matches the theoretical model. Real-world measurements may have structured deviations that affect recovery guarantees.
- **Beyond support recovery**: The analysis focuses on support recovery (identifying which components are non-zero). Recovery of the actual non-zero values, or more general estimation tasks, may have different sample complexity.
- **Finite-SNR effects**: The high-SNR regime analysis may not accurately capture performance at moderate SNR, which is more common in practice.
- **Algorithmic considerations**: The sufficient conditions are for maximum-likelihood recovery. Practical algorithms (e.g., Lasso, greedy methods) may require different or additional conditions.
- **Multiple measurement vectors**: The analysis assumes a single measurement vector. Extension to multiple measurement vectors (MMV) could improve recovery via joint sparsity exploitation.

## Relevance to Software Engineers

For software engineers working with sparse recovery, compressed sensing, or feature selection algorithms, this paper offers several concrete takeaways:

1. **Logarithmic sparsity penalty**: When designing or selecting sparse measurement systems, the sample-complexity cost of using sparse measurements versus dense ones is only logarithmic. This means you can use significantly sparser measurements with modest sample complexity overhead.

2. **$p / \psi^2$ scaling rule**: The sample complexity scales as $p / \psi^2$, where $\psi$ is the measurement oversampling ratio. If you need to support $p$-dimensional signals, plan for approximately $p / \psi^2$ measurements. For example, to support a 10,000-dimensional signal with 2x oversampling ($\psi = 2$), you'd need about 25,000 measurements.

3. **Proportional regime practicality**: In the proportional regime where both sparsity and dimension scale together, the $p / \psi^2$ rule provides a simple planning formula. This is directly applicable to large-scale machine learning systems where both the model dimension and the number of measurements grow together.

4. **Sparsified dense design pattern**: The ability to generate measurements densely but recover using sparse measurements enables hybrid architectures. If your system already has dense measurement infrastructure but you want recovery efficiency, you can sparsify the measurement matrix at recovery time with the rescaling correction.

5. **Information-theoretic bounds**: The $\frac{s \log(p/s)}{\log(d s / p)}$ threshold provides a benchmark for evaluating any support recovery algorithm. If an algorithm requires significantly more samples than this threshold, there may be room for optimization.

6. **Computational vs. sample trade-off**: The paper highlights that sparse measurements can offer nearly linear computational gains while incurring only a logarithmic sample complexity loss. For real-time or resource-constrained systems, this trade-off may be highly favorable.

7. **Rescaling for sparsified designs**: When using a sparsified measurement matrix for recovery (with a dense generation model), the rescaling of the response variable is critical. Forgetting the rescaling factor can lead to poor recovery performance, so implementers must ensure the correction is applied correctly.

## Related Concepts

- `concepts/data-engineering/sparse-recovery.md`, `concepts/data-engineering/compressed-sensing.md`, `concepts/data-engineering/feature-selection.md`