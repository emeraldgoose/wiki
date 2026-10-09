---
title: Custom Domain Name for Amazon MSK (Technical Deep-dive)
description: OAuth audience-routed broker auth on Amazon MSK — EKS IAM/STS web-identity flow and Keycloak SSO operator flow behind per-provider resource servers over AMQPS.
date: 2026-08-25
tags: [aws, kafka, msk, auth, oauth, iam, kubernetes]
locale: en
blog: aws
---

# Custom Domain Name for Amazon MSK (Technical Deep-dive)

**Published**: Aug 25, 2026 · **Source**: AWS Big Data Blog (original URL no longer listed; split from the legacy aggregate `sources/articles/aws-bigdata.md`)

> Note: no source URL is available for this entry — it predates the current blogwatcher feed. The summary below is preserved from the aggregate file. URLs are never fabricated.

## Companion article

See `Configure_Custom_Domain_Name_for_Amazon_MSK.md` for the networking side (NLB + DNS + ACM, two-phase rollout of advertised listeners on ZooKeeper and KRaft). This file covers the **authentication architecture** behind the custom domain.

## Auth flows

- **Services (EKS workloads)**: EKS pod → IAM role (IRSA) → STS web-identity token with audience `rabbitmq-iam` → broker over AMQPS 5671. The audience claim routes the token to the correct signing keys on the broker's resource server.
- **Operators (humans)**: Keycloak SSO → broker, via a separate OAuth provider binding.
- **Architecture**: one resource server per OAuth provider on the broker; the token's audience claim selects the provider and its signing keys, so machine (STS) and human (Keycloak) identities coexist on the same listener.

## Takeaways for the seminar

- Audience-routed resource servers let two unrelated identity systems share one Kafka endpoint — the custom domain is what makes that single endpoint stable and addressable.
- The machine path (short-lived STS tokens via IRSA) and the human path (SSO) differ only in issuer; the broker-side dispatch on `aud` keeps both working without per-client broker config.

## Related concepts

- `concepts/infrastructure/kubernetes.md`, `concepts/data-engineering/stream-processing.md`
