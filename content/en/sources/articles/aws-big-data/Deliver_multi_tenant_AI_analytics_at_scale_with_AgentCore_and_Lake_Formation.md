---
title: "Deliver multi-tenant AI analytics at scale with AgentCore and Lake Formation"
description: "How to apply Cognito and Lake Formation on AgentCore Gateway so a data agent enforces row- and column-level security per external tenant."
tags: [source, aws-big-data, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/deliver-multi-tenant-ai-analytics-at-scale-with-agentcore-and-lake-formation"
blog: aws-big-data
published_date: 2026-11-06
---

# Deliver multi-tenant AI analytics at scale with AgentCore and Lake Formation

**Source**: [aws-big-data](https://aws.amazon.com/blogs/big-data/deliver-multi-tenant-ai-analytics-at-scale-with-agentcore-and-lake-formation) · **Published**: 2026-11-05

## Overview

Governed, multi-tenant data access is a critical requirement for software and business-to-consumer (B2C) products that embed AI-powered analytics. A data agent can answer natural-language queries over structured data, but when it serves external users the hardest problem is not translating natural language into SQL. It is ensuring that each tenant can access only their authorized rows, columns, tables, or cells.

The post contrasts identity models for different audiences. AWS IAM Identity Center with Trusted Identity Propagation is designed for workforce identity and enterprise federation through SAML 2.0 and SCIM, so it suits enterprise users. For external-facing B2C or multi-tenant applications, Amazon Cognito is a better fit because it offers mobile and single-page application integration through OIDC, social identity federation, and self-service user management for large external user bases. The post then shows how to apply the traditional Cognito and Lake Formation pattern on AgentCore Gateway, a capability of Amazon Bedrock AgentCore, resulting in a data agent that enforces row- and column-level security from the authenticated user's identity.

The end-to-end architecture propagates identity through the whole call chain. A user signs in through the Cognito Hosted UI and receives OAuth tokens, where the ID token carries a custom:team claim. The frontend invokes AgentCore runtime with the access token and ID token, which forwards both through the agent code to the MCP Gateway. The gateway validates the access token with a JWT authorizer and passes the ID token to a minimally privileged Lambda target. The Lambda uses Cognito Identity Pool's GetCredentialsForIdentity to exchange the ID token for temporary AWS credentials scoped to an IAM role selected by rules-based mapping. Athena then runs the query with those user-scoped credentials, and Lake Formation evaluates the IAM role's LF-Tag permissions and data cell filters so the user receives only authorized data.

Permissions are expressed declaratively rather than in application filtering logic. Each user is tagged with custom:team in the Cognito User Pool, the team claim maps to an IAM role through the Identity Pool rules, and the role is granted Lake Formation permission to resources associated with an LF-Tag such as team with values TeamA, TeamB, and shared. This lets tagged tables and rows be exposed or withheld per tenant without writing per-tenant SQL predicates in the application.

## Key points

- Multi-tenant analytics agents need fine-grained authorization, not just natural-language-to-SQL translation.
- Amazon Cognito fits external B2C and SaaS tenants, while IAM Identity Center with Trusted Identity Propagation fits workforce federation.
- A Cognito User Pool custom:team attribute becomes the identity signal carried in the ID token.
- Rules-based mapping in Cognito Identity Pool exchanges that claim for tenant-scoped AWS credentials.
- Lake Formation LF-Tags and data cell filters enforce row- and column-level access at query time.
- AgentCore Gateway connects the agent to the data tools while propagating identity tokens end to end.

## Details

The architecture sends the ID token from the frontend through AgentCore runtime and the MCP Gateway's JWT authorizer to the Lambda target, which performs the credential exchange and runs Athena with temporary credentials. A separate Lake Formation tag with key team and values such as TeamA, TeamB, and shared is applied to data assets, and each role receives SELECT and DESCRIBE permissions through tag-based policies. The intended audiences include SaaS application architects building customer-facing analytics, B2C data product teams serving hundreds of thousands of external users, partner portal developers, and ISVs migrating to AWS who need agentic data capabilities with tenant isolation. Full deployment configuration, including CloudFormation or CDK snippets and the exact console steps, is in the linked source.

## References

- Source: [aws-big-data](https://aws.amazon.com/blogs/big-data/deliver-multi-tenant-ai-analytics-at-scale-with-agentcore-and-lake-formation)
