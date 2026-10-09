---
title: HTTP
description: "Seminar-level concept: HTTP methods, status codes, headers, caching, versions 1.1 through 3, cookies, TLS"
tags: [concept, computer-science, http, web, rest, tls, http2, http3]
published: 2026-09-06
locale: en
---

# HTTP

**HTTP** (Hypertext Transfer Protocol) is the request-response application protocol of the web: a client sends a method, target, headers, and optional body; a server returns a status, headers, and optional body. Every API, page load, and webhook is a conversation in this grammar.

## Definition

- **Message model**: stateless request/response over a transport (TCP for 1.1/2, QUIC/UDP for 3). Each request is independent; state is layered on top (cookies, tokens).
- **Method + target + version**: e.g. `GET /users/42 HTTP/1.1`. Method declares intent; target identifies the resource.
- **Status codes** (server's verdict, grouped by first digit): 1xx informational, 2xx success, 3xx redirection, 4xx client error, 5xx server error.
- **Headers**: extensible `Name: value` metadata (content negotiation, auth, caching, compression). Bodies are opaque bytes described by `Content-Type` / `Content-Length` (or chunked framing).

## Why It Matters

- **The universal API substrate**: REST, GraphQL, webhooks, OAuth flows, and LLM APIs are all HTTP semantics. Method/status/header literacy is prerequisite to designing or debugging any of them.
- **Performance is protocol-shaped**: connection reuse, multiplexing, header compression, and caching directives decide page-load and API latency more than server code does.
- **Correctness contracts live here**: idempotency of methods, cacheability rules, and status-code meanings are what intermediaries (CDNs, proxies, browsers) act on — misuse breaks the whole chain.
- **Security boundaries**: cookies/SameSite/CORS/TLS behavior is defined at this layer; misconfigurations here are the most common web vulnerabilities.

## How It Works

### Methods and Their Contracts

| Method | Safe | Idempotent | Cacheable | Meaning |
|---|---|---|---|---|
| GET | ✓ | ✓ | ✓ | Retrieve representation |
| HEAD | ✓ | ✓ | ✓ | GET without body (existence, size) |
| POST | ✗ | ✗ | ✗ (mostly) | General action / create (subordinate) |
| PUT | ✗ | ✓ | ✗ | Replace resource at target URI |
| DELETE | ✗ | ✓ | ✗ | Remove resource |
| PATCH | ✗ | ✗* | ✗ | Partial update (*idempotent if designed so) |
| OPTIONS | ✓ | ✓ | ✗ | CORS preflight / capability discovery |

- **Safe** = no state change (read-only). **Idempotent** = N identical requests ≡ 1 (safe for retries). Retry logic must only auto-retry idempotent methods — or use idempotency keys for POST.
- Choosing PUT vs PATCH vs POST is a contract with caches and retry layers, not a style preference.

### Status Codes Worth Memorizing

- `200 OK`, `201 Created` (return `Location`), `204 No Content` (success, empty body).
- `301 Moved Permanently` vs `302 Found` vs `307 Temporary Redirect` vs `308 Permanent Redirect`: 301/302 historically allowed method rewriting to GET (POST→GET surprise); 307/308 preserve the method. Use 307/308 unless you explicitly want the legacy behavior.
- `304 Not Modified` (conditional GET hit — revalidation), `400` (malformed), `401` (unauthenticated — "who are you"), `403` (unauthorized — "I know you, no"), `404`, `409 Conflict` (state clash, e.g. version mismatch), `422 Unprocessable Entity` (well-formed but semantically bad), `429 Too Many Requests` (honor `Retry-After`).
- `500` (bug/crash), `502 Bad Gateway` (upstream broken), `503 Service Unavailable` (temporarily overloaded — retryable with backoff), `504 Gateway Timeout` (upstream too slow).

### Headers That Run the Web

- **Content negotiation**: `Accept`, `Accept-Encoding: gzip, br`, `Content-Type`, `Content-Length` / `Transfer-Encoding: chunked`.
- **Caching**: `Cache-Control: max-age=3600, must-revalidate`, `ETag` + `If-None-Match`, `Last-Modified` + `If-Modified-Since`, `Vary: Accept-Encoding` (critical when a CDN serves compressed variants).
- **Auth**: `Authorization: Bearer <token>`, `WWW-Authenticate` challenge on 401.
- **Cookies/state**: `Set-Cookie: id=abc; HttpOnly; Secure; SameSite=Lax`, echoed back as `Cookie:`. `HttpOnly` blocks JS theft; `Secure` requires HTTPS; `SameSite` gates cross-site sending (CSRF defense).
- **CORS**: `Origin` + `Access-Control-Allow-Origin`, preflight `OPTIONS` for non-simple requests. A server-side allowlist, enforced by browsers.

### Versions: 1.1 → 2 → 3

```
1.1: TCP conn × N, sequential requests, head-of-line blocking, text headers
2:   one TCP conn, binary frames, multiplexed streams, HPACK header compression,
     server push (mostly abandoned), still TCP-level HOL blocking
3:   QUIC over UDP, streams without TCP HOL blocking, 0-RTT resumption,
     QPACK, mandatory TLS 1.3
```

- **HTTP/1.1** (1997, RFC 9112): persistent connections (`keep-alive`) + pipelining (rarely used, fragile). One outstanding request per connection in practice → browsers opened 6 connections per origin; the "domain sharding" era.
- **HTTP/2** (2015, RFC 9113): multiplexing kills the 6-connection hack; HPACK shrinks repetitive headers (~cookie-heavy traffic). One slow/lost packet still stalls all streams (TCP HOL blocking) — the motivation for 3.
- **HTTP/3** (2022, RFC 9114): QUIC gives per-stream flow control and loss recovery; connection migration survives IP changes (mobile handoff); 0-RTT repeats prior connections fast (with replay risk — only for idempotent requests).
- Negotiation: ALPN (`h2`, `h3`) during TLS handshake; plaintext HTTP/2 (h2c) exists but browsers require TLS.

### HTTPS/TLS in One Paragraph

- TLS 1.3 handshake negotiates cipher, authenticates the server via X.509 certificate chain, and derives session keys (1 RTT; 0-RTT on resumption). HTTP runs unchanged inside the encrypted tunnel. Mixed-content (HTTPS page loading HTTP subresources) breaks security guarantees and browsers block it.

## Common Pitfalls

1. **GET with side effects**: crawlers, prefetchers, and retry layers assume GET is safe. A `GET /delete-account` will eventually be triggered by something you did not intend.
2. **POST retries without idempotency keys**: a timed-out POST may have succeeded server-side (lost response). Retrying creates duplicates — charges, orders, rows. Make the operation idempotent or attach an `Idempotency-Key`.
3. **Wrong redirect codes**: issuing 302 where 307 was meant silently converts POST→GET at some clients and drops the body. Choose deliberately.
4. **Missing `Vary` with content negotiation**: serving gzip and identity under one cache key without `Vary: Accept-Encoding` poisons CDN caches with the wrong variant for some clients.
5. **Caching authenticated responses**: `Cache-Control: public` on a per-user response leaks one user's data to others via shared caches. Default to `private, no-store` for personalized content; use `public` only for truly shared assets.
6. **Treating 5xx as retryable without backoff/jitter**: a fleet retrying 503s in lockstep is a self-inflicted DDoS (retry storm). Exponential backoff + jitter + circuit breaking is the complete answer.
7. **Ignoring CORS preflight cost**: cross-origin `PUT`/`DELETE`/JSON POSTs each cost an extra OPTIONS round trip. Keep APIs same-origin where possible or budget the RTT.

## Related Concepts

- [[concepts/computer-science/tcp-ip|TCP/IP]] (transport under HTTP; QUIC/UDP for HTTP/3)
- [[concepts/computer-science/caching|Caching]] (HTTP cache directives, CDN behavior, ETag validation)

## References

- RFC 9110 (HTTP Semantics), RFC 9111 (Caching), RFC 9112 (HTTP/1.1), RFC 9113 (HTTP/2), RFC 9114 (HTTP/3), RFC 9000 (QUIC)
- Fielding (2000) — "Architectural Styles and the Design of Network-based Software Architectures" (REST dissertation)
- MDN Web Docs — HTTP reference (methods, status codes, headers, CORS)
