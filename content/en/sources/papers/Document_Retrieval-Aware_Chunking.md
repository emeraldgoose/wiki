---
title: "Document Retrieval-Aware Chunking"
description: "D-RAC ingests any enterprise document via PDF normalization plus one multimodal Markdown pass, then plans chunks over IDs — 95.7 percent fewer output tokens at agentic-chunking parity."
published: "2026-09-21"
arxiv_id: "2609.24220"
hf_url: "https://huggingface.co/papers/2609.24220"
authors: "Abhivanth Sivaprakash, Pratik Singh, Aman Manocha, Uday Allu"
organization: "Yellow.ai AI Research Team"
tags: [source, paper, huggingface, rag, chunking, document-ingestion, multimodal]
locale: "en"
---

# Document Retrieval-Aware Chunking

[한국어 버전](../../../ko/sources/papers/Document_Retrieval-Aware_Chunking.md)

**arXiv**: [2609.24220](https://arxiv.org/abs/2609.24220) | **HuggingFace**: [papers/2609.24220](https://huggingface.co/papers/2609.24220) | **Published**: 2026-09-21 | **Organization**: Yellow.ai AI Research Team | **Submitted by**: Uday Allu | **Upvotes**: 51

**Authors**: Abhivanth Sivaprakash, Pratik Singh, Aman Manocha, Uday Allu

## Abstract

Retrieval-Augmented Generation (RAG) systems over enterprise knowledge bases must ingest heterogeneous document formats — PDFs, Word documents, presentations, and scans — whose content is locked inside complex visual layouts, multi-column pages, and dense tables. Rule-based extraction and OCR destroy reading order, flatten tables, and lose heading hierarchy, while fully agentic chunking over extracted text incurs high token costs and hallucination risk. We present Document Retrieval-Aware Chunking (D-RAC), an extension of our Web Retrieval-Aware Chunking (W-RAC) framework to arbitrary document formats. D-RAC first normalizes any input document into PDF, exploiting the fact that virtually every format has a faithful, deterministic PDF rendering. A single multimodal LLM pass then converts rendered pages into retrieval-optimized Markdown — rewriting tables as self-contained prose statements and preserving heading hierarchy — after which chunking proceeds exactly as in W-RAC: deterministic parsing into ID-addressable units followed by lightweight LLM-based chunk planning over identifiers rather than text. Source text is never regenerated during chunking, preserving W-RAC's cost, determinism, and observability benefits while unlocking every renderable format as a first-class input. On the 236-document, 795-page PDF subset of the RAG-Multi-Corpus benchmark spanning five enterprise domains, D-RAC converts and chunks the entire corpus in 72 minutes with zero errors, producing 1,748 retrieval-ready chunks. Compared to agentic chunking with frontier LLMs, D-RAC reduces chunking-stage output tokens by 95.7%, cutting chunking cost by 77.8% (GPT-4.1 pricing) to 85.6% (Gemini 2.5 Pro pricing) and chunking time by 75%. D-RAC scales linearly to documents of 500+ pages.

## Background and Problem Setup

RAG is the dominant pattern for grounding LLMs in enterprise knowledge, and chunking quality decides retrieval quality. The authors' prior system, W-RAC, reframed chunking as semantic planning rather than text generation: deterministically parse a web page into structured ID-addressable units, then have the LLM emit only ordered identifier lists as chunk plans. That cut chunking output tokens by 84.6%, latency by about 60%, and cost by 51.7% while improving precision. But W-RAC assumes recoverable structure (HTML convertible to Markdown), which enterprise PDFs do not offer.

PDFs are a presentation format, not a semantic one, and each classical ingestion route fails in a specific way:

- **Rule-based extraction** (PyMuPDF, pdfminer, pdfplumber): fast and free, but multi-column layouts interleave fragments, headers/footers mix into body text, hyphenation artifacts appear, tables collapse into positionally ambiguous tokens, and heading hierarchy survives only as a font-size heuristic.
- **Layout-analysis / OCR pipelines** (LayoutLM, LayoutLMv2, Docling): recover regions and reading order but need dedicated deployments, break on unusual marketing-style layouts (insurance brochures, product one-pagers), and still emit tables as grids — a cell stripped of row/column context embeds as noise.
- **Agentic chunking over extracted text**: the LLM must simultaneously repair extraction damage and regenerate the full text, maximizing output tokens (about 4x the price of input tokens), latency, and hallucination surface.
- **Vision-guided chunking**: multimodal models reading page images beat extraction pipelines, but using a large vision model for both understanding and chunk generation keeps the full output-token cost.

The paper's question: can a single multimodal pass recover enough structure from rendered pages that the whole W-RAC machinery applies unchanged?

## Methodology

D-RAC inherits W-RAC's principles (no text regeneration during chunking, cost efficiency, determinism/observability) and adds format agnosticism via PDF normalization, a single conversion pass, and retrieval-aware normalization. Four stages; only stages 2 and 4 touch an LLM.

**Stage 1 — PDF normalization and page rendering (deterministic).** Non-PDF inputs convert to PDF with commodity tooling (headless LibreOffice for office formats, print-to-PDF for HTML, image wrapping for scans). No LLM, no per-format parsers. Each page renders to PNG at 200 DPI, downscaled so no dimension exceeds 1,568 px (common vision-encoder limit). Cost: 1–7 s per document, negligible next to inference.

**Stage 2 — Multimodal Markdown conversion (one LLM pass).** Rendered pages go in batches of 5 to a multimodal LLM (evaluated: Gemma-3 27B and 12B via AWS Bedrock, temperature 0.1, up to 8,192 output tokens per batch, 5 batches in parallel) under a retrieval-aware prompt:

- Verbatim preservation: nothing summarized or skipped.
- Table-to-prose normalization: Markdown table syntax is forbidden; every row becomes one self-contained sentence carrying its column headers as context; distinct rows are never merged (a Policy Term 16/PPT 8 row and a 20/10 row stay two sentences, never "16 or 20 years").
- Image suppression: logos, charts, decorative graphics omitted rather than captioned, so hallucinated descriptions never pollute the index.
- Explicit hierarchy: headings emitted as `#`/`##`/`###`, reconstructing the structure PDF extraction destroys.
- Page provenance: an HTML comment `<!-- Page N -->` per page for traceability.

A deterministic post-pass strips code fences and image references and applies a rule-based table-to-prose fallback for anything that escapes. A failed page range becomes an inline error marker, never an aborted document.

**Stage 3 — Deterministic parsing and sectioning.** Converted Markdown parses (as in W-RAC) into ID-addressable elements: headers (`h1`, `h2`, …) with levels, content blocks (`p1`, `p2`, …). Over a 60-element planning budget, a recursive splitter cuts at header boundaries — coarsest level first, descending only where needed, fixed-size fallback for header-free runs — and merges adjacent small sections. Each section carries its parent-header chain (a few dozen input tokens), so the planner sees hierarchy position without resending content.

**Stage 4 — LLM chunk planning and reconstruction.** The planner sees only element IDs, truncated previews (200–400 chars), and hierarchy metadata, and returns chunk plans as ordered ID lists (e.g. `[["h1","h2","p1","p2"],["h1","h3","p3","p4","p5"]]`), grouping 3–8 content blocks per chunk around single topics, reusing header IDs for context, covering every content ID exactly once. Coverage is verified programmatically; missing IDs fall into a fallback chunk with section headers, guaranteeing lossless ingestion. Sections plan in parallel. Final chunks reconstruct locally from verbatim converted text, each prefixed with its full ancestor-heading chain plus a breadcrumb (e.g. *Plan Overview > Eligibility > Age Limits*), then embed and index.

Because converted Markdown and element IDs persist, re-chunking under a new retrieval policy costs only ID-level planning calls — never re-conversion or re-OCR.

## Results

Evaluated on the 236-document / 795-page PDF subset of RAG-Multi-Corpus (five fictional enterprise verticals: automotive, academic, cloud-services, enterprise-technology, banking; product sheets, FAQs, policies, parts catalogs, service guides) plus a 503-page financial prospectus stress test. Embeddings: Titan Text Embeddings V2 (1,024 dims), cosine top-K per organization index; relevance = 60% of a supporting fact's content words in the chunk.

- **Throughput**: full corpus converts in 3,758 s cumulative (62.6 min; 71.7 min wall clock including planning), zero conversion errors across all 236 documents; per-page cost stable at 3.9–5.5 s across domains (API latency dominates, not layout complexity); 503-page prospectus converts in 21.6 min (27B) / 13.4 min (12B) — linear scaling, no super-linear blowup.
- **Planning efficiency**: 542 s for the whole corpus (14% of conversion, 2.3 s/doc); chunk sizes fall naturally into 581–846 characters, the dense-retriever sweet spot, with no hard limits; 1,748 chunks, zero chunking errors; the 5,060-element stress document plans in 68.7 s over 95 parallel section calls (about 5% of its conversion time).
- **Retrieval quality** (762 queries with supporting-fact ground truth, 7 types): D-RAC beats fixed-size-on-PyMuPDF extraction clearly — Recall@6 0.717 to 0.798 (+11.3% relative), MRR 0.602 to 0.690 (+14.6%), NDCG@6 0.764 to 0.801 — and matches or exceeds the agentic-chunking reference on all seven overall metrics despite working from rendered PDF pages (the hardest input) while the reference was built from clean structured sources. Biggest wins on boundary-sensitive queries: temporal (Recall@6 0.85 vs 0.73 fixed), comparative (0.79 vs 0.72), analytical (0.61 vs 0.56); boolean queries are the one category where agentic keeps an edge. Recall@6 varies only 0.022 across organizations (0.790–0.812).
- **Cost**: chunking-stage output tokens 270,454 to 11,714 (−95.7%); at GPT-4.1 ($2/$8 per 1M in/out) −77.8%, at Gemini 2.5 Pro ($1.25/$10) −85.6%; planning input slightly below baseline (265k vs 326k tokens) thanks to truncated previews; measured planning time 541.8 s vs 2,167.5 s agentic (−75.0%). Extrapolated to a 1M-page corpus, one full re-index drops from about $3,540 to about $785 (GPT-4.1). The 11.7k output tokens are pure ID arrays validated against the element table — zero prose hallucination surface during chunking.

## Limitations and Open Questions

- Conversion quality bounds everything: one multimodal pass must get tables, hierarchy, and reading order right; the paper evaluates Gemma-3 12B/27B but does not price frontier vision models per page at production scale.
- Image suppression is deliberate information loss — charts, diagrams, and scanned figures vanish from the index; a corpus where the figure *is* the fact needs a captioning or VQA extension the pipeline currently refuses to pay for.
- Retrieval evaluation uses a fixed judge (60% content-word overlap, Titan embeddings); absolute numbers are benchmark-relative, and boolean-query underperformance hints that row-prose helps recall-style queries more than logic-style ones.
- All benchmark inputs were natively PDF, so Stage 1 normalization was the identity in experiments; DOCX/PPTX/XLSX-to-PDF fidelity at enterprise scale is asserted from tooling, not measured here.

## Relevance to Software Engineers

- If you run RAG over PDFs, this is a concrete blueprint: normalize to PDF, one vision pass to retrieval-optimized Markdown (row-level table prose, explicit headings, provenance comments), then plan chunks over IDs and reconstruct verbatim. The durable artifact (converted Markdown + element IDs) decouples the expensive once-per-document step from cheap re-planning whenever chunking policy changes.
- The cost lever is output tokens: emitting ID arrays instead of rewritten text is what collapses 77–86% of chunking cost and removes the hallucination surface at the same time. Any agentic pipeline that regenerates source text should justify why.
- Two rules worth stealing directly: never merge distinct table rows into disjunctive sentences (a silent precision killer), and always prepend the ancestor-heading chain to each chunk so embeddings carry product/section context.

## Related Concepts

- [RAG](../../concepts/ai-engineering/rag.md)
- [Vector Search](../../concepts/ai-engineering/vector-search.md)
- [Embeddings](../../concepts/machine-learning/embedding.md)

## References

- arXiv: https://arxiv.org/abs/2609.24220
- HuggingFace: https://huggingface.co/papers/2609.24220
- Benchmark: https://github.com/udayallu/RAG-Multi-Corpus
- Predecessor: Web Retrieval-Aware Chunking (W-RAC), arXiv:2604.04936
