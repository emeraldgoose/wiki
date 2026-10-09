---
title: "Trading a Cloud Identity for Your Own: Workload Attestation on Managed Compute"
description: Netflix closes the gap between AWS IAM identities and its private Metatron PKI for Spark on EMR — using AWS STS pre-signed URLs plus control-plane metadata signatures as two independent, mutually corroborating claims
tags: [source, rss, netflix, workload-identity, attestation, security, mTLS, PKI, aws-emr, apache-spark]
locale: en
source_url: "https://netflixtechblog.com/trading-a-cloud-identity-for-your-own-workload-attestation-on-managed-compute-516d5a29b252"
blog: netflix
published_date: 2026-09-25
---

# Trading a Cloud Identity for Your Own: Workload Attestation on Managed Compute

Source: Dhruv Pratap, Netflix Technology Blog, Sep 25, 2026.

**Lead**: Netflix's internal service-to-service auth runs on a private PKI (Metatron) issuing short-lived X.509 certificates — but workloads on managed compute like Amazon EMR start with only an AWS identity. The post describes how a Spark job that boots holding nothing but an IAM role ends up holding a first-class internal identity: the plugin sends one attestation request carrying a pre-signed STS URL *and* a control-plane-signed metadata document, the Identity service verifies both, and the Data Project service holds the authoritative 1:1 identity-to-role mapping that makes the translation possible at all. The interesting part is not the cryptography — it is that neither the provider, the control plane, nor the workload ever issues an identity alone.

> **Coverage note.** This summary is based on the publicly reachable sections of the original. Several middle sections of the post (the full Data Project / Identity service protocol, the exact attestation-request schema, and the fan-out capacity numbers) sit behind Medium's paywall and are not reproduced here. Everything below is drawn from text present in the source.

## Two identity systems, one gap

Most mature organizations run two identity systems side by side. One belongs to the cloud provider — IAM roles, instance profiles, execution roles. The other is the organization's own, and it is the one internal services actually consult when deciding whether to answer a request.

On self-managed infrastructure you can bootstrap your own identity however you like. On managed compute you cannot: the provider hands your process a cloud identity and nothing else. The exchange itself is straightforward — converting a cloud credential into an internal one is a plumbing problem. Making that exchange *trustworthy* is where the design work goes.

## Why a mapping is the whole game

The identity-to-role mapping is what makes translation possible. It lets a statement in the provider's vocabulary — "this process is running as role R" — become a statement in Netflix's — "this process is workload W". Without that mapping there is nothing to translate into, and no amount of cryptography helps.

The hard part of bridging two identity systems is rarely the protocol. It is **committing to a mapping and then keeping it authoritative**. A mapping nobody maintains is worse than no mapping, because it looks like a trust story while quietly drifting from reality.

## Two claims, corroborated

Netflix's design deliberately refuses to trust a single source. The attestation carries two independent artifacts and requires both to verify:

1. **The provider's claim** — a pre-signed AWS STS URL. Unforgeable, but under-specified: it proves *a* role signed this, without saying which logical workload that role stands for.
2. **The platform's claim** — signed metadata describing the specific dispatch. Well-specified, but replayable: on its own, it is just a statement by something the workload could also have produced.

The Identity service fetches the pre-signed URL against AWS STS, reads back the role that actually signed it, verifies the metadata signature against the key issued to the control plane, and then **corroborates the two against the authoritative mapping**. Neither party has to take the workload's own account of itself at face value.

This is not a novel pattern — it is the same shape behind AWS IAM authentication in HashiCorp Vault and in AWS's own function-attestation flows. The generalisation: any environment that gives a process cloud credentials and nothing else can still produce a verifiable statement about its own identity.

## Components

- **Data Project service** — the authority for the identity-to-role mapping. It is what the corroboration step checks against.
- **Identity service** — receives attestation requests, verifies them against both claims, and issues the internal certificate.
- **The plugin** — lives in the Spark runtime and issues the single attestation request carrying both artifacts.

## The fan-out problem

Distributed engines multiply every per-process operation by their parallelism. A Spark job runs many executors, each needing its own attestation and certificate; at Netflix's scale that becomes a capacity question against the Identity service. Netflix chose to keep the signer scarce — exactly one service is able to make the platform's claim — partly so the trust story stays auditable, and partly so the load has a single, deliberately sized answer rather than an incident.

The general lesson the post draws: **identity amplification is a capacity question, and it is better to answer it on purpose than to have it answered for you during an outage.**

## Why the design generalises

1. **Anchor on one exchangeable primitive.** A single authoritative 1:1 mapping between your identity and a provider identity is what makes translation possible. The rest is plumbing.
2. **Require two independent claims and corroborate them.** One from the provider — unforgeable but under-specified. One from your control plane — well-specified but replayable. Trust the intersection, never either alone.
3. **Keep the signer scarce.** If exactly one service can make the platform's claim, the trust story fits in a sentence.
4. **Hook the layer you still own.** On managed compute you rarely control the host or its init system, but you almost always control the runtime: a plugin, an agent, an entrypoint. Attestation belongs there.
5. **Decide the amplification policy on purpose.** Distributed engines multiply every per-process operation by their parallelism — capacity has to be planned, not discovered.
6. **Make attestation repeatable and credentials short-lived.** Renewal is a requirement, not a follow-up.

The property that makes the result trustworthy: **no single participant issues an identity by itself** — not the workload, not the control plane, not the provider. And the workload, which is the party in the weakest position to be trusted, is never asked to vouch for itself.

## Relevance to SW engineers

- If you run on managed compute and need an internal identity, look for a layer you actually control — the runtime plugin is usually the only place left.
- Design attestation as *corroboration of two weak-ish claims*, not as a single strong claim. Both halves are individually insufficient; that is the point.
- Keep the identity-to-role mapping authoritative and maintained. It is the actual trust anchor; everything else is transport.
- Plan certificate issuance for executor fan-out before you need it.
- Related: `concepts/computer-science/operating-system-basics.md`, `concepts/infrastructure/service-mesh.md`, `concepts/data-engineering/apache-spark.md`.

## References

- Source article: https://netflixtechblog.com/trading-a-cloud-identity-for-your-own-workload-attestation-on-managed-compute-516d5a29b252
