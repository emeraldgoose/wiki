---
title: "How Block powers collaborative AI agents with Buzz and Unity Gateway"
description: "Block's open source Buzz workspace puts employees and AI agents in the same channels, threads, and DMs; through Databricks Unity Gateway each agent can run on a different frontier or open-weight model behind one API, enabling multi-agent teams where a stronger model coordinates smaller ones."
tags: [source, databricks, ai-agents, en]
locale: en
source_url: "https://www.databricks.com/blog/how-block-powers-collaborative-ai-agents-buzz-and-unity-gateway"
blog: databricks
published_date: 2026-11-14
---

# How Block powers collaborative AI agents with Buzz and Unity Gateway

**Source**: [Databricks Blog](https://www.databricks.com/blog/how-block-powers-collaborative-ai-agents-buzz-and-unity-gateway) · **Published**: 2026-11-12

## Overview

As AI agents become part of everyday work, Block's teams wanted to work with agents in the same place they work with each other. The result is Buzz, an open source collaboration space — written up here by Bradley Axen, Brandon Kvarda, Julia Powell, and Kelly Albano — where employees and AI agents share channels, threads, and direct messages. A user creates an agent, chooses the model or coding harness behind it, and brings that agent into a conversation with colleagues; instead of hopping between AI tools, a team can work with several agents in one environment. An employee might ask an agent for help with coding or analysis while colleagues review its work, add information, or ask follow-up questions in the same thread.

Buzz ships with its own built-in agent that incorporates a lightweight version of Goose, Block's coding agent, and supports other coding harnesses and tools. As an open source project it is model-agnostic and can be self-hosted, running privately on an organization's own network or system. At Block, employees use Buzz for coding, analytics, and other day-to-day work, and many bring agents into the conversations where colleagues are already collaborating.

Model access comes from Databricks Unity Gateway. When an employee creates an agent in Buzz, they can select Databricks as the inference provider and pick from the models Unity Gateway exposes — frontier models from OpenAI, Anthropic, and Google plus selected open-weight models — all through a single integration. That separation of model choice from agent creation is the point: a coding task, an analytical question, and a lightweight everyday request may each deserve a different model or harness, so employees can build a collection of specialized agents rather than designing every agent around the same model.

The most interesting experiment is multi-agent. Not every step of a complex task needs the most expensive model, so Block has been exploring configurations in which a more capable model coordinates a team of agents powered by smaller, more efficient models — the coordinator takes the demanding reasoning while the others handle tasks suited to their capabilities, all visible to people inside the same Buzz environment. Block has also built an internal approach to benchmarking these agent teams so engineers can try different configurations. The article frames this as a broader shift: the question is no longer which single model performs best, but how to combine models, harnesses, and agents to complete work effectively.

## Key points

- Buzz is Block's open source collaboration workspace where employees and AI agents work together in channels, threads, and DMs; users create agents, choose their model or coding harness, and collaborate with multiple agents and colleagues in one environment.
- The built-in Buzz agent incorporates a lightweight version of Goose; other coding harnesses and tools are also supported.
- Open source, model-agnostic, and self-hostable — organizations can run it privately on their own network or system.
- Unity Gateway is the model access layer: employees select Databricks as their inference provider and choose from frontier models (OpenAI, Anthropic, Google) and select open-weight models through a single integration.
- Per-task model choice: different tasks benefit from different models or harnesses, so agents can be specialized rather than one-size-fits-all.
- Multi-agent pattern under experimentation: a more capable coordinating model works across a team of agents powered by smaller, more efficient models; people can watch and join the agent-to-agent work inside the same collaborative environment.
- Block uses an internal benchmarking approach for agent teams to compare model-and-harness configurations on performance and cost.
- Framing: AI development is shifting from picking a single best model to combining models, harnesses, and agents to complete work effectively.
- Getting started: explore the Buzz project on GitHub, and use Databricks Unity Gateway to access frontier and open-weight models through a single API for your own applications and agents.

## Details

### One environment for people and agents

Buzz treats agents as participants rather than external tools: they can be created in place, assigned a model and harness, and invited into ongoing work where colleagues already converse. The collaboration modes span group discussions, focused conversations, and one-on-one exchanges, which maps cleanly onto channels, threads, and DMs. Because the workspace is shared, an agent's intermediate work is reviewable by colleagues — the article presents this as a reason agents end up in existing conversations rather than in a separate AI tool.

### The gateway as the model abstraction

Unity Gateway centralizes model access behind one integration, so the Buzz agent-creation flow simply offers "Databricks" as the inference provider with a model list behind it. For an enterprise this decouples agent design from vendor switching: when new models arrive, agents can be re-pointed without changing where work happens. The combination with Buzz's model-agnostic, self-hostable design means the harness layer and the model layer can evolve independently.

### Multi-agent economics

The coordination pattern — strong model orchestrating, small models executing — is presented as a cost-and-performance experiment rather than a finished product, with Block's internal benchmarking approach as the measurement tool. The FAQ reinforces the same idea for enterprises generally: assign models to agents based on task requirements, performance, and cost, and experiment with combinations instead of committing to one model for every workflow.
