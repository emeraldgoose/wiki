---
title: "Portal by Spotify cut my Claude Code token usage by 90%"
description: "Routing Claude Code's I/O-heavy reads and boilerplate writes to cheap worker models via Portal AiKA Modes and the shunt plugin — mean 90% token savings on bulk reads"
tags: [source, article, en, en]
locale: en
source_url: "https://engineering.atspotify.com/2026/9/portal-by-spotify-cut-my-claude-code-token-usage-by-90"
blog: spotify
published_date: 2026-09-03
---

# Portal by Spotify cut my Claude Code token usage by 90%

**Author**: Dimitri Mazmanov, Principal Product Manager
**Source**: [Spotify Engineering](https://engineering.atspotify.com/2026/9/portal-by-spotify-cut-my-claude-code-token-usage-by-90)
**Date**: Sep 3, 2026

## Overview

Most of what a coding agent burns tokens on is I/O, not reasoning: reading five files to answer one question, generating a test file that mirrors twenty neighbors. With token spend per developer already reaching hundreds to thousands of dollars monthly, the post shows a practical fix — route grunt work to a cheaper model via two declarative Portal AiKA Modes, enforced by a Claude Code plugin called shunt. Benchmarked on a Java monorepo, bulk reads averaged about 90% token savings.

## Two AiKA Modes

Modes are declarative agents on an ephemeral runtime (Lambda-style): instructions, model, parameters, and MCP tools defined up front, callable from the Portal CLI or API, public or private. The author created two, both using Gemini 2.5 Flash as the worker:

- **bulk-reader** — answers a question over provided files with structured bullets only, no prose. Offloads the "read N large files to answer one thing" pattern.
- **code-writer** — generates code from a spec plus a reference file, matching existing patterns exactly and emitting code only (no markdown fences or explanations that Claude would have to re-parse).

The design principle: modes decide *how* to respond, while the router decides *when* to delegate — so swapping models or prompts never touches the plugin.

## The shunt plugin: hooks, scripts, skills

An early approach (routing rules in `CLAUDE.md`) failed because it was advisory and per-project. The shunt plugin enforces routing in three layers:

- **Hooks** — `check-file-size` blocks Reads over a configurable line threshold (default 350, via `SHUNT_MIN_LINES`) and redirects to the bulk-reader skill; `check-bash-read` catches `cat`/`head`/`tail`/`less`/`more` on large files while letting piped targeted reads through.
- **Scripts** — `bulk-read` wraps files in XML boundaries and sends one-shot ephemeral invocations (nothing stored server-side); `code-write` sends spec plus a required reference file and can write straight to disk so Claude never sees the generated tokens.
- **Skills** — markdown usage files triggered when a hook blocks a read. The system degrades gracefully: even unread skills still save tokens because the hook blocks the expensive read.

## Limits and results

Four benchmark scenarios on a Java monorepo showed mean bulk-read savings near 90%; code-write savings are harder to quantify since output tokens bypass Claude entirely. What doesn't work: delegating edits (worker summaries lack reliable line numbers — targeted reads with offset/limit still go to Claude), delegating reasoning (the worker missed a subtle thread-safety bug Claude caught), and small tasks where 10–30s delegation latency exceeds the savings — hence the line threshold. The broader point: AiKA Modes turn model routing from a systems-engineering problem into a configuration problem, and the same modes are reusable, shareable, and composable (doc-writer, reviewer, translator) across projects.

## References

- [Portal by Spotify cut my Claude Code token usage — original article](https://engineering.atspotify.com/2026/9/portal-by-spotify-cut-my-claude-code-token-usage-by-90)
- [AiKA Modes documentation](https://backstage.spotify.com/docs/portal/core-features-and-plugins/aika/modes) (referenced in the post)
- [spotify/portal-ai-plugins marketplace](https://github.com/spotify/portal-ai-plugins) (referenced in the post)
