---
title: "Now GA: Building permission-aware Databricks Apps with on-behalf-of-user authorization"
description: Promoted on 2026-10-17
tags: [source, article, en]
locale: en
source_url: "https://www.databricks.com/blog/now-ga-building-permission-aware-databricks-apps-behalf-user-authorization"
blog: databricks
published_date: 2026-10-07
published: 2026-10-17
---

# Now GA: Building permission-aware Databricks Apps with on-behalf-of-user authorization

## Overview

Databricks Apps now generally supports on-behalf-of-user (OBO) authorization: an app can call supported APIs using the signed-in user's identity, so Unity Catalog enforces that user's data permissions (including row filters and column masks) without the app reimplementing governance. The app's service principal remains available for app-owned work such as shared configuration reads or background jobs.

## Two identities: choose per operation

The design question is whose permissions should govern each operation. User authorization fits user-specific reads and actions on governed data (e.g., a sales assistant showing only the accounts each viewer may see); app authorization fits uniform experiences and background maintenance. Most production apps mix both, with separate clients and explicit boundaries rather than one reused credential.

## Narrow scopes and configuration

API scopes cap what the app may do with the user's identity — for read-only analytics, `sql:restricted-query` instead of the broader `sql` scope; similarly `genie` or `ai-gateway` only when those services are actually invoked. Scopes are a ceiling, not a data grant: the user must still hold warehouse and Unity Catalog rights. Developers declare scopes in the UI or a bundle, users consent on first access, and workspace admins set the upper boundary via an allowlist (Settings > Development > Apps), which can be narrowed or disabled entirely.

## Implementation: token flow and hardening

The platform forwards a short-lived per-request user token in the `x-forwarded-access-token` header; the app reads it per request, passes it to the SQL connector (or the user-context client in AppKit), and never stores, logs, or reuses it across requests. If the token is missing, fail closed rather than silently falling back to the service principal. The same pattern extends to custom agents — build the user-scoped client inside the request-time handler, not at startup. Test with users holding different Unity Catalog rights and re-test after policy changes.

## References

- Original article: [Now GA: Building permission-aware Databricks Apps with on-behalf-of-user authorization](https://www.databricks.com/blog/now-ga-building-permission-aware-databricks-apps-behalf-user-authorization)
