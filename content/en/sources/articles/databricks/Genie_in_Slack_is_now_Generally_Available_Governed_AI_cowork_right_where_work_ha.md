---
title: "Genie in Slack is now Generally Available: Governed AI cowork, right where work happens"
description: "Databricks ships the Genie app for Slack to general availability: DM or @mention Genie for governed answers grounded in Unity Catalog context, act through approval-gated MCP connectors, schedule recurring analyses, and keep every question running under the asker's permissions."
tags: [source, databricks, ai-agents, governance, en]
locale: en
source_url: "https://www.databricks.com/blog/genie-slack-now-generally-available-governed-ai-cowork-right-where-work-happens"
blog: databricks
published_date: 2026-11-14
---

# Genie in Slack is now Generally Available: Governed AI cowork, right where work happens

**Source**: [Databricks Blog](https://www.databricks.com/blog/genie-slack-now-generally-available-governed-ai-cowork-right-where-work-happens) · **Published**: 2026-11-12

## Overview

Many business questions cannot be started and answered inside one conversation. The article's running example: a manager asks in Slack why revenue growth slowed last month across active customers. Someone must find the right dashboard, check it against the number finance reported, and search last week's meeting notes for the explanation — the revenue numbers live in the data platform, the explanation lives in documents and tickets, the definition of "active customer" varies across teams, and the decision happens in Slack. By the time findings are pasted back into the thread, the conversation has moved on. Databricks's answer, announced at general availability by Toussaint Webb and Sydney Sundell, is the Databricks Genie app for Slack: Genie answers in the channel, thread, or DM where the question was asked, with the same governed context and permissions it uses inside Databricks.

The product shape is deliberate about collaboration versus privacy. Anyone who has connected their Databricks account can @Genie in a channel the app has been added to; Genie replies in the thread, follow-up questions keep their context, and responses are visible to the whole channel by default so the team shares context for decisions — with an admin option to make private responses the workspace default. Every answer cites its sources, and clicking a source opens the deeper context in Genie One. Channels are configured individually: each picks the Databricks workspace it connects to and whether questions route to Genie One (the default, which spreads a question across Genie Search, Genie Agents, and more for an estate-wide view) or to a pinned, curated Genie Agent for domain-specific channels such as "Product FAQs" or "Employee Benefits", with pinned questions sent through the Genie Agentic API. In a DM, the same capabilities run privately: questions over your data, search across connected enterprise knowledge sources, tables and charts, file uploads for analysis, and actions in other tools.

Beyond answering, the release turns answers into work without leaving Slack. Through MCP connectors Genie can create or update documents, comment on tickets, and update records using the user's own credentials, with every change prepared for approval before it runs. Analyses can be scheduled ("Run this analysis on a schedule" under an answer, or phrased naturally, for example "Send me this analysis every Monday at 9 AM"), files can be attached for analysis and documents like PDFs returned into the thread, and charts land directly in the conversation. The same capabilities work inside Genie One, so workflows can be orchestrated from either system.

## Key points

- General availability of the Databricks Genie app for Slack: DM Genie or @mention it in a channel for governed answers grounded in your business context, without leaving Slack.
- Governance model: every question runs with the identity of the person who asked it across Unity Catalog and each connected source, so Genie only uses information that person is allowed to see — in DMs and channels alike.
- Channel behavior: Genie only reads channels it has been invited to, answers within the context of the channel it was asked in, and keeps follow-ups in-thread; responses are shared by default, and admins can set private responses as the workspace default.
- Per-channel configuration: choose the connected Databricks workspace and the routing — Genie One by default (routes across Genie Search, Genie Agents, and more) or a pinned curated Genie Agent whose scope stays limited to that agent's data and instructions (questions delivered via the Genie Agentic API).
- Answers cite their sources inline; clicking a source opens it deeper in Genie One.
- Action through MCP connectors: create or update documents, comment on tickets, update records with the user's own credentials; each change is staged for the user's approval before it executes.
- Recurring analyses: "Run this analysis on a schedule" under an answer, or a natural-language request like "Send me this analysis every Monday at 9 AM"; results arrive in the Genie DM. Alternatively, create a scheduled task in Genie One and choose Slack as the delivery target. A one-time sign-in to the Genie app from a DM is required before results can be delivered.
- Files and charts: attach files for Genie to analyze and receive documents such as PDFs back in the thread; visualizations are returned directly in the conversation.
- Central admin control: Unity Gateway governs AI usage, including MCP policies that decide which MCP servers and tools Genie can use, which users can access them, and which actions require human approval; cost controls and monitoring are included, and traces record what Genie did and who asked.
- Security posture: questions are processed inside the Databricks workspace, and the service routing messages between Slack and Databricks does not store questions or answers. Workspaces using Private Link are supported through context-based ingress policies created by a Databricks account admin.
- Getting started: admins install the Databricks Genie app from the Slack Marketplace and configure channels and response visibility; users DM or @mention Genie and sign in to Databricks, picking a workspace on first use. Databricks platform notifications can also be received in Slack, and answers can be rated with thumbs up/down.

## Details

### Why answer in the conversation

Databricks frames the problem as fragmentation rather than difficulty: the data needed for an answer is split across the warehouse, documents, tickets, and tribal definitions, while the decision happens in Slack. Embedding Genie where the question is asked removes the copy-out-and-paste-back round trip, and because the same governed context applies as in Databricks, the answer does not lose its permission boundary when it moves into a chat thread.

### Governance and security mechanics

The governance story has three layers. Identity: every question executes as the asker across Unity Catalog and connected sources, so there is no separate permissions model to manage for Slack. Visibility: channel responses are shared or private per channel, with a workspace-wide default settable by admins. Central control: Unity Gateway hosts MCP policies (which servers and tools Genie may use, which users may access them, which actions need human approval) plus cost controls and monitoring, with traces recording both actions and requesters. On the network side, Private Link workspaces connect through context-based ingress policies, and message routing between Slack and Databricks is stateless with respect to question and answer content — questions are processed inside the workspace.

### Recurring insights, both directions

Scheduled insights can be created from either end: in Slack, via the button under an answer or a natural-language cadence request; in Databricks, by creating a scheduled task in Genie One and selecting Slack as the delivery channel. Either way results land in the user's Genie DM, after a one-time sign-in from that DM.
