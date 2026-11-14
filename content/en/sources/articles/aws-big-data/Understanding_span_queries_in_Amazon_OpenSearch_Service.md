---
title: "Understanding span queries in Amazon OpenSearch Service"
description: "Span queries in Amazon OpenSearch Service compose nine span query types to enforce exact term order, position within a field, and containment relationships that phrase queries with slop cannot express — the precision legal, regulatory, patent, and contract search workloads need."
tags: [source, aws-big-data, opensearch, search-queries, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/understanding-span-queries-in-amazon-opensearch-service"
blog: aws-big-data
published_date: 2026-11-14
---

# Understanding span queries in Amazon OpenSearch Service

**Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/understanding-span-queries-in-amazon-opensearch-service) · **Published**: 2026-11-13

## Overview

Amazon OpenSearch Service is a fully managed service for deploying, scaling, and operating OpenSearch, the open source suite for search, analytics, and observability licensed under the Apache License V2.0. Among OpenSearch's query types, span queries give precise control over where terms appear in a document and how they relate to one another. Most applications get good results from match and phrase queries, but some workloads require exact term placement that simpler queries cannot express: legal search, regulatory compliance, scientific and patent search, and contract analysis.

The post first shows where phrase queries fall short. A match_phrase query matches a contiguous sequence of terms in order, and its slop parameter loosens that constraint by allowing a number of position swaps between terms. Searching "star wars iv" against a title field does not match "Star Wars: Episode IV - A New Hope" because the word "Episode" intervenes; slop 1 fixes that by swapping one position. But the fix cuts both ways: with slop 4, a query for "star wars hope" also unexpectedly matches "Hope for Star Wars: The Prequel Series", because phrase slop performs an edit-distance match, swapping terms within the edit window regardless of order. When you need to enforce term order, position within a field, or structural relationships between terms, phrase queries lack the expressiveness.

Span queries fill that gap. They are compound queries composed only of other span queries, and the post teaches how they work, when to prefer them over phrase queries, and how to compose them to express precise structural constraints.

## Key points

- Span queries are compound queries that control the position of terms relative to one another; they can only contain other span queries — you cannot mix them with non-span queries inside the same compound expression.
- OpenSearch supports nine span query types: span_term (single term, typically the leaf), span_multi (wraps a prefix, regex, or wildcard multi-term query), span_first (matches spans at the start of a field within a specified number of positions), span_near (matches clauses within a slop, like match_phrase but over spans), span_not (excludes terms), span_or (unions clauses), span_field_masking (uses a span_term from another field masked as the primary field), span_containing, and span_within.
- All span queries accept an in_order parameter that controls whether sub-spans must appear in the order of the query clauses.
- span_containing and span_within both take a big and a little clause and require the little span to be contained by the big span; span_containing returns the big matches while span_within returns the little matches — span_within is the mirror of span_containing.
- To find "A New Hope", the example anchors "star" with span_first (end 2, the first two positions of the title) and requires "hope" within 12 positions via span_near with in_order true — matching only "Star Wars: Episode IV - A New Hope" and rejecting the document where "star" is not at the start.
- A span_containing example requires the exact phrase "episode iv" (slop 0, in_order true) to fall within a big span containing "star" and "hope" within 12 terms in either order; only the Episode IV title satisfies both constraints.
- Phrase slop is an edit-distance match: it swaps terms within the edit window regardless of order, which is why slop 4 matched a document with the words in a different order.
- Typical span use cases include finding documents where "force majeure" appears within five terms of "termination", plus patent and scientific search with structural term positions, compliance and audit workflows enforcing exact placement, and query-time constraints on unstructured text instead of reshaping data.
- The trade: span queries are more verbose than phrase queries and require careful composition; in return they express exact ordering, position within a field, and containment that phrase queries cannot.

## Details

### Where phrase queries fall short

The walkthrough builds a small index named term_order with a single text field, title, and indexes two documents: "Star Wars: Episode IV - A New Hope" and "Hope for Star Wars: The Prequel Series". A match_phrase query for "star wars iv" with slop 1 matches the first document, because slop 1 allows OpenSearch to swap one term position and accommodate the intervening "Episode". Changing the query to "star wars hope" with slop 4 matches both documents — including the unexpected second one, whose term order differs from the query. Phrase slop performs an edit-distance match, swapping terms within the edit window regardless of order, so phrase queries cannot enforce that terms appear in a specific order, at a specific position, or in a structural relationship. That expressiveness gap is exactly what span queries address for workloads where term placement carries meaning.

### Composing spans: anchoring a term to a position

Span queries only contain other span queries, and each type contributes a structural constraint. The first composition anchors "star" to the beginning of the title with span_first (match span_term "star", end 2 — within the first two positions) and wraps it with a second clause in span_near: a plain span_term for "hope", with slop 12 and in_order true. This matches only "Star Wars: Episode IV - A New Hope"; the second document fails because "star" is not at the start of its title. The example demonstrates the two mechanisms span queries add over phrase queries: position anchoring within a field and ordered proximity over spans.

### Spans within spans: containment constraints

span_containing and span_within express structural constraints by matching one span inside another. Both take a big and a little clause; the difference is which matches are returned. The post's example finds documents where the exact phrase "episode iv" appears within a span containing both "star" and "hope": the little clause is a span_near of the terms "episode" and "iv" with slop 0 and in_order true (an exact phrase), and the big clause is a span_near of "star" and "hope" with slop 12 and in_order false (either order, within 12 positions). The query requires the little phrase to fall inside a big match, and only "Star Wars: Episode IV - A New Hope" satisfies both constraints.

### When to choose span queries

Span queries earn their complexity whenever phrase queries cannot express the constraint. In legal and regulatory search, statutes and contracts often require specific phrases in proximity — for example, documents where "force majeure" appears within five terms of "termination". In patent and scientific search, claims and papers require terms in specific structural positions relative to one another. Compliance and audit workflows that must enforce exact term placement to satisfy regulatory definitions benefit from the same precision. More generally, when text has no explicit structured model but you need constraints about where terms appear within a field, span queries provide a query-time alternative to reshaping your data. The conclusion is a trade of simplicity for precision: span queries are more verbose and need careful composition, but they express exact ordering, position within a field, and containment relationships that phrase queries cannot, and for applications where term placement carries meaning they are the right tool.
