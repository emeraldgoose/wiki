---
title: "Weight-Space Programming Doesn't Need Transformers"
description: "Hyunjong Ok and Jaeho Lee show that when an LLM writes the weights of a separate model, sparse associative-memory tables beat Transformers written by the same LLM: three frontier writers (Claude Opus 5.5, GPT-6.1 Sol, GPT-6 Astra) converge on the same structure for the 3,530-question ARC benchmark, reaching 54.4% (well above the 25% chance rate) with about 1,800x fewer parameters than the writer's best released architecture and up to 17x faster inference on one RTX 3090."
tags: [source, paper, alphaxiv, weight-space-programming, llm, en]
locale: en
source_url: "https://www.alphaxiv.org/abs/2611.weight-space-programming-associative-memory"
authors: ["Hyunjong Ok", "Jaeho Lee"]
blog: alphaxiv
published_date: 2026-11-17
---

# Weight-Space Programming Doesn't Need Transformers

**Source**: [alphaxiv](https://www.alphaxiv.org/abs/2611.weight-space-programming-associative-memory) · **Published**: not stated on the source page · **Authors**: Hyunjong Ok, Jaeho Lee (POSTECH)

## Overview

A Transformer's dense weight matrix is a poor target for an LLM that has to write the weights by hand. Its entries suit gradient training and GPU matrix multiplication, but a line of text can name a fact while a dense array gives the writer little structure to assign meaning to, inspect, or edit. Weight-space programming (WSP) is the setting in which an LLM writes the weights of a separate model directly — no gradient-based training, no data fitting, no iterative learning loop. The paper's move is twofold: first let the LLM choose the model structure rather than constrain it to a fixed architecture, then design a fixed reader that retrieves the written facts efficiently.

The setup gives the writer ten labeled ARC (ARC-Easy and ARC-Challenge) examples and a sandbox, with minimal guidance. Three writers — Claude Opus 5.5, GPT-6.1 Sol, and GPT-6 Astra — independently converge on the same structure: a sparse fact table, i.e., an associative memory in which a small set of question concepts (the key) retrieves a written fact or recalled concept (the value). The writer groups related word forms ("bird," "birds," "bird's") into one concept, writes declarative fact lines, and compiles each line into a sparse table row. The model matches question and option concepts against rows, ranks the options, and applies written rules such as handling negation. The three LLMs differ mainly in how they divide a row: Claude uses one sentence as both key and value; GPT-6.1 Sol uses a clue side and an answer side; GPT-6 Astra uses rows split into supported and contradicted answers.

## Results

ARC here means the 3,530 four-option ARC-Easy and ARC-Challenge test questions combined, where chance is 25%.

The LLM-designed models (writing the released architecture is the given baseline; LLM-designed is the model the writer designs itself):

| Writer | Released architectures (written) | Written two-layer Transformer | LLM-designed (first / last generation) | Ours, associative-memory model (first / last generation) |
|---|---|---|---|---|
| Claude Opus 5.5 | 43.1 | 36.1 | 50.8 / 54.4 | 49.6 / 52.4 |
| GPT-6.1 Sol | 35.0 | 36.3 | 44.6 / 47.4 | 41.2 / 45.6 |
| GPT-6 Astra | 34.4 | 32.6 | 42.7 / 46.2 | 42.5 / 47.4 |

The LLM-designed lineages run 5, 7, and 5 generations for Claude, Sol, and Astra respectively; the associative-memory lineages run 5, 5, and 8. Chance is 25%.

- Claude Opus 5.5's first-generation LLM-designed model reaches 50.8% on ARC with 0.94 million parameters. The most accurate released architecture the same writer wrote is Qwen3-1.7B at 48.7% with 1.72 billion parameters, so the table model is about 1,800× smaller. These are WSP-written models, not pretrained Qwen performance. This ratio belongs to the first generation; the generation-five model reaches 54.4% but has 3.35 million parameters.
- The associative-memory-based model folds written facts into a pair table read at computed addresses. It keeps the line-by-line writing approach and runs up to 17× faster on one RTX 3090 than a same-sized Transformer.

## Traceability and line removal

Keeping only the best-matching fact for each option changes Claude's first-generation model from 50.8% to 49.1% ARC accuracy, so most of its performance can be traced to single written lines. Removing a written line changes 0.5–1.8 answers on average in the two tested table models, compared with 4.8 in one written Transformer. The line-removal test sampled 40 lines per model, and in one table model most of the 1.8 figure came from vocabulary lines that also alter the vocabulary. Locality is therefore a measured pattern in these models, not a universal property of tables. As a control, BM25 keyword search over each model's own written text is evaluated as well: for Claude, the written two-layer Transformer scores 36.1% on ARC versus 44.1% for BM25 over its text, so the Transformer fails to use its own facts as well as plain search; the first-generation table scores 50.7% versus 47.0% for BM25 over that model's text. The authors read this as consistent with interference among dense, overlapping Transformer keys. They note, however, that the results cannot separate a structure that suits writing from one an LLM favors because retrieval is familiar.

## The fixed reader

The LLM-designed tables have a speed problem: they score every stored fact against every question, so work grows with the fact inventory, and their many GPU kernel launches make most of them slower than a same-sized Transformer. Across 46 LLM-designed variants, only one beat its same-sized Transformer at the fastest measured input, and the median was 9.4× slower.

The authors' remedy is a fixed reader. It maps words to concepts, takes the 16 strongest question concepts, forms their 120 pairs, computes addresses for those pairs, and reads 120 rows from a pair table. Those recalled concepts are combined with a first-order concept table, and the model scores the concepts present in each option but absent from the question. A build script still compiles the lines the LLM wrote; what is fixed is the reader, not the facts. Per-question reading is independent of the number of fact entries at a fixed concept vocabulary, although cost still grows with vocabulary size.

On one RTX 3090, the generation-five model answers all 3,530 ARC test questions in 18 ms, versus 302 ms for a Transformer matched by non-zero value count at its fastest input — 17× faster. These are inference times, not writing cost or fewer LLM attempts. The timed Transformer has random weights; the accuracy comparison instead uses Transformers written by the same LLM. There is also a limit: with dense concept-table storage the advantage fades at roughly 15,000–32,000 concepts, and a row-list variant extends that to about 100,000.

## Scope and limitations

The claim concerns current LLMs writing models from random initialization without running them on benchmark data, mainly for multiple-choice recall. It does not show that WSP generally beats Transformers, and a fine-tuned Qwen3.5-0.8B reaches 82.1% ARC accuracy. The written tables recall facts a writer can state; they are not shown to learn representations or chain facts beyond them. What the work does show is that when an LLM writes the weights, a structure whose entries can be named and edited — paired with a reader that controls retrieval cost — can reach and exceed the accuracy of much larger written Transformers. The paper builds on the weight-space programming setting introduced by Takehi et al. (2026), the MIT CSAIL demonstrations of LLMs reading, writing, and editing network weights.

## Resources

- Paper page (alphaxiv): [Weight-Space Programming Doesn't Need Transformers](https://www.alphaxiv.org/abs/2611.weight-space-programming-associative-memory)
- Project repository: [github.com/effl-lab/Weight-Space-Programming](https://github.com/effl-lab/Weight-Space-Programming)
