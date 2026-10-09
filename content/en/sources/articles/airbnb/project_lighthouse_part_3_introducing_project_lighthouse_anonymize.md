---
title: "Project Lighthouse — Part 3: Introducing project-lighthouse-anonymize"
description: Airbnb's open-source anonymization library for privacy-preserving disparity measurement; Core Mondrian algorithm and data-quality framework
tags: [source, airbnb, privacy, anonymization, open-source, data-engineering]
locale: en
source_url: "https://medium.com/airbnb-engineering/project-lighthouse-part-3-introducing-project-lighthouse-anonymize-74f8b26653fb"
blog: airbnb
date: 2026-08-25
---

# Project Lighthouse — Part 3: Introducing project-lighthouse-anonymize

**Source**: Airbnb Engineering (Medium) · **Published**: 2026-08-25 · **Author**: Adam Bloomston (Anti-discrimination & Equity team)

## Background: Why Project Lighthouse Exists

In 2020 Airbnb launched Project Lighthouse in partnership with civil-rights and privacy organizations to **measure potential disparities in user experiences** (e.g., discrimination on the platform). The design is privacy-by-design:

- Analyses use **perceived race data never linked to individual accounts**.
- Data is used **only** for measuring disparities; users can opt out via Privacy settings.
- Results were publicly shared in the [2024 Project Lighthouse update](https://news.airbnb.com/2024-project-lighthouse-update/).

The 2020 foundational paper established **p-sensitive k-anonymity** as the technical privacy model (see Part 1 on p-sensitive k-anonymity and Part 2 on measurement with anonymized data). This post announces the **open-sourcing of `project-lighthouse-anonymize`** (PyPI + GitHub) plus **two new arXiv papers** that complete the story: scalable implementation + quality validation.

## Core Mondrian: Scalable Partition-Based Anonymization

Paper: *Core Mondrian: Basic Mondrian beyond k-anonymity* (2025). It extends the classic Mondrian algorithm (LeFevre et al.) with:

1. **Extensible architecture** — Strategy Pattern supporting k-anonymity now, future privacy models later.
2. **Parallel processing** — hybrid recursive-queue execution: immediate recursive processing for small partitions, queue-based parallel processing for large ones.
3. **NaN-pattern pre-partitioning** — principled handling of missing values instead of dropping them.
4. **Dynamic suppression budget management** — controls how many records may be suppressed to satisfy k.

Result: anonymization of **large datasets at scale** while preserving usability for statistical analysis.

## Measuring Data Quality Under Anonymization

Paper: *Measuring Data Quality for Project Lighthouse* (2025). Core question: how do you know anonymized data is "good enough" for your analysis?

**Three primary metrics**:

| Metric | What it measures |
|--------|------------------|
| Pearson correlation | Preservation of linear relationships between original and anonymized values |
| RILM (Revised Information Loss Metric) | How well the geometric "shape"/size of data is preserved (higher = less distortion) |
| NMIv1 (Normalized Mutual Information v1) | Entropy/information-content preservation |

**Validation methodology**: reframes quality assessment as an ML classification problem — synthetic datasets validate that the metrics + thresholds predict when anonymized data yields statistically valid results. The paper ships **default thresholds** (the values Airbnb uses), usable as starting points by others. Analysts without anonymization expertise can thus check `check_dq_meets_minimum_thresholds(dq_metrics)` before trusting results.

## Usage

```python
p, k = 2, 5
# Step 1: k-anonymity
anon_df, dq_metrics, disclosure_metrics = k_anonymize(logger, input_df, qids, k, {}, "row_id")
# Step 2: p-sensitive k-anonymity via perturbation
sensitized_df, _, _ = p_sensitize(logger, anon_df, qids, "race", p, k, sens_attr_value_to_prob)
# Step 3: gate on quality
minimum_dq_met, reasons = check_dq_meets_minimum_thresholds(dq_metrics)
assert minimum_dq_met, str(reasons)
```

The getting-started guide uses the UCI Adult dataset as a runnable example.

## Takeaways for SW Engineers

- **Two-stage privacy**: k-anonymity first, then p-sensitivity via perturbation — the composition is what prevents sensitive-attribute disclosure, not either step alone.
- **Quality gates are part of the pipeline**, not an afterthought: anonymize → measure (correlation/RILM/NMIv1) → assert thresholds → analyze.
- **Parallel Mondrian + NaN pre-partitioning** are the two tricks that make partition-based anonymization practical on real, messy, large tables.

## Related Concepts

- Privacy-preserving data publishing (k-anonymity, differential privacy, t-closeness)
- Open-source data tooling (Spark/Pandas/Polars integration)

## References

- Library: https://github.com/airbnb/project-lighthouse-anonymize
- Core Mondrian paper: https://arxiv.org/abs/2510.09661
- Data Quality paper: https://arxiv.org/abs/2510.06121
- 2020 methodology: https://news.airbnb.com/wp-content/uploads/sites/4/2020/06/Project-Lighthouse-Airbnb-2020-06-12.pdf
