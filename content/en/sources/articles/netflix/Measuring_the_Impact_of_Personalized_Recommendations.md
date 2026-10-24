---
title: "Measuring the Impact of Personalized Recommendations"
description: "By Kevin Zielnicki, Guy Aridor, Aurélien Bibaut, Allen Tran, Winston Chou, and Nathan Kallus Personalization is everywhere on the internet."
tags: [source, netflix, data-engineering, en]
locale: en
source_url: "https://netflixtechblog.com/measuring-the-impact-of-personalized-recommendations-4c26be3a4d96"
blog: netflix
published_date: 2026-10-14
---

# Measuring the Impact of Personalized Recommendations

**Source**: [netflix](https://netflixtechblog.com/measuring-the-impact-of-personalized-recommendations-4c26be3a4d96) · **Published**: 2026-10-14

## Overview

By Kevin Zielnicki, Guy Aridor, Aurélien Bibaut, Allen Tran, Winston Chou, and Nathan Kallus Personalization is everywhere on the internet. It shapes the products we discover, the stories we read, the music we hear, and the movies and TV shows we watch. At Netflix, personalization has been central to the member experience for decades — from the Netflix Prize to our modern recommender system that helps members navigate a large and constantly changing catalog.

## Key points

- The first is random recommendations: every member receives titles selected uniformly at random from the catalog. This is not intended as a realistic product experience, but it helps isolate the value of having recommenda
- The second is popularity-based recommendations: every member receives broadly popular titles. This is a natural non-personalized benchmark.
- The third is a basic matrix factorization model, a classic personalized recommendation approach and a useful baseline for older generations of recommender systems.
- The first is exposure: simply showing a title to a member can increase the probability that the member watches it. This captures the basic value of surfacing a title that may otherwise have been hard to find.
- The second is selection: recommended titles are shown to members who already have a relatively high baseline probability of watching them. This channel doesn’t lead to incremental engagement, but it can smooth the discov
- The third is targeting: the recommender system may identify members for whom the recommendation itself is especially effective, meaning members who are much more likely to watch the title when it is recommended than when

## References

- Original article: [https://netflixtechblog.com/measuring-the-impact-of-personalized-recommendations-4c26be3a4d96](https://netflixtechblog.com/measuring-the-impact-of-personalized-recommendations-4c26be3a4d96)
