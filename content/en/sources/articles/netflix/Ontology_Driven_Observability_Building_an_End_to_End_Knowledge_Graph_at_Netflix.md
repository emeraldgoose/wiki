---
title: "Ontology-Driven Observability: Building an End-to-End Knowledge Graph at Netflix Scale"
description: "When Jake Paul and Mike Tyson stepped into the ring in November 2024, we delivered the fight to roughly 65 million concurrent streams."
tags: [source, netflix, data-engineering, en]
locale: en
source_url: "https://netflixtechblog.com/ontology-driven-observability-building-an-end-to-end-knowledge-graph-at-netflix-scale-421392cf5adf"
blog: netflix
published_date: 2026-10-16
---

# Ontology-Driven Observability: Building an End-to-End Knowledge Graph at Netflix Scale

**Source**: [netflix](https://netflixtechblog.com/ontology-driven-observability-building-an-end-to-end-knowledge-graph-at-netflix-scale-421392cf5adf) · **Published**: 2026-10-16

## Overview

When Jake Paul and Mike Tyson stepped into the ring in November 2024, we delivered the fight to roughly 65 million concurrent streams. On an ordinary day our infrastructure takes in more than 2 billion requests and handles upwards of 38 million real-time logging events every second. At that scale, the whole picture doesn’t fit into a single engineering team’s head or onto a single dashboard. With more Live content, Podcasts and real-time streams, our need to understand and update our systems as quickly as possible becomes imperative to provide a good user experience. Understanding the system a Consider a regression of the kind we see in a given week. The home screen where you see the list of lists of movies, starts taking about 1.5 seconds longer to render. An alert fires. And then we go l

## Key points

- every URI follows a single naming scheme, and
- the catalog gates every ops:Application.
- Model identity before anything else. Choose one authoritative catalog per entity kind and validate against it before creating an entity.
- Treat the ontology as code. Version it, review it, test it, and let changes arrive as pull requests. Treating the ontology as code lends itself to agentic development and lets teams scale and contribute to it.
- Separate concepts from instances. Concepts change on a human timescale and instances change continuously, conflating them makes both harder to evolve.
- Build on open standards. RDF, OWL, SHACL and SPARQL are specified, implemented many times over, and portable. A bespoke graph model ties a future consumer to one implementation.

## References

- Original article: [https://netflixtechblog.com/ontology-driven-observability-building-an-end-to-end-knowledge-graph-at-netflix-scale-421392cf5adf](https://netflixtechblog.com/ontology-driven-observability-building-an-end-to-end-knowledge-graph-at-netflix-scale-421392cf5adf)
