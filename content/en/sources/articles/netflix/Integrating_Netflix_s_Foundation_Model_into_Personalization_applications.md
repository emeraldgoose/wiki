---
title: "Integrating Netflix’s Foundation Model into Personalization applications"
description: "The motivation for building the Netflix Foundation Model for personalization was laid out in this previous blog post."
tags: [source, netflix, data-engineering, en]
locale: en
source_url: "https://netflixtechblog.com/integrating-netflixs-foundation-model-into-personalization-applications-cf176b5860eb"
blog: netflix
published_date: 2026-10-14
---

# Integrating Netflix’s Foundation Model into Personalization applications

**Source**: [netflix](https://netflixtechblog.com/integrating-netflixs-foundation-model-into-personalization-applications-cf176b5860eb) · **Published**: 2026-10-14

## Overview

The motivation for building the Netflix Foundation Model for personalization was laid out in this previous blog post. The Netflix homepage is powered by several specialized models and it requires significant time and resources to maintain and continue innovating on these individual models. Therefore, we decided to centralize member preference learning and have one powerful model learned from comprehensive user interaction histories and content data at a large scale and have this model distribute its learnings to other models. The previous two blog posts(1, 2) focus on the development of the Foundation Model and here we talk about how we integrate the Foundation Model into various applications. We found that there is extensive literature focused on the training and inference of large-scale

## Key points

- In this blog, we go over the 3 approaches we experimented with and which are now used in production for different use cases. Each integration approach has its own set of motivations, tradeoffs, complexities and learnings
- Transformer style foundation models naturally lend themselves to generating comprehensive user profile and item representations. Our approach for generating embeddings includes getting the hidden state of the last user e
- Netflix has an elaborate set up for refreshing the embeddings every day. First, the Foundation Model is pre-trained from scratch every month. Then, the monthly pre-trained model is fine-tuned everyday based on the latest

## References

- Original article: [https://netflixtechblog.com/integrating-netflixs-foundation-model-into-personalization-applications-cf176b5860eb](https://netflixtechblog.com/integrating-netflixs-foundation-model-into-personalization-applications-cf176b5860eb)
