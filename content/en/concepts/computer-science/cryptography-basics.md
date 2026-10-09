---
title: Cryptography Basics
description: "Seminar-level concept: symmetric and asymmetric ciphers, hashes, MACs, signatures, key exchange, TLS, common failures"
tags: [concept, computer-science, cryptography, tls, hashing, encryption, signatures, security]
published: 2026-09-06
locale: en
---

# Cryptography Basics

**Cryptography** provides confidentiality, integrity, and authenticity for data in transit and at rest — built from a small set of primitives (ciphers, hashes, MACs, signatures) composed into protocols like TLS. The mathematics is strong; nearly all real failures come from misusing the primitives, not breaking them.

## Definition

- **Confidentiality**: only key holders can read the data (encryption). **Integrity**: tampering is detectable (hashes, MACs). **Authenticity**: the peer is who it claims to be (signatures, certificates). Most protocols need all three at once.
- **Symmetric cipher**: one shared secret key encrypts and decrypts (AES-256-GCM, ChaCha20-Poly1305). Fast (~GB/s), but both sides must already share the key.
- **Asymmetric (public-key) cipher**: a public key encrypts/verifies, a private key decrypts/signs (RSA, ECDH/ECDSA over Curve25519/P-256). Solves key distribution but is ~1000x slower — used to agree on symmetric session keys, not bulk data.
- **Cryptographic hash**: one-way fingerprint with preimage, second-preimage, and collision resistance (SHA-256, SHA-3, BLAKE3). Any input change avalanches the digest; finding two inputs with one digest must be infeasible.
- **MAC / digital signature**: a MAC (HMAC-SHA256) proves integrity to someone holding the shared secret; a signature (Ed25519, ECDSA, RSA-PSS) proves authorship to anyone holding the public key, giving non-repudiation.

## Why It Matters

- **Everything sensitive depends on it**: HTTPS sessions, password stores, API tokens, software updates, disk encryption. A single primitive misuse (ECB mode, static IV) silently voids the whole guarantee.
- **The threat model decides the primitive**: encrypting a disk (symmetric, one key holder) vs proving a software release came from you (signatures, world verifiers) vs storing passwords (slow salted KDF, never reversible encryption). Wrong-primitive choices fail by construction.
- **Performance shapes protocol design**: TLS handshakes use ECDH once to derive a symmetric session key, then bulk-encrypt with AES-GCM/ChaCha20. Hybrid construction is why the web can afford encryption everywhere.
- **Quantum horizon**: Shor's algorithm breaks RSA/ECDSA on a large enough quantum computer; NIST's post-quantum standards (ML-KEM for key exchange, ML-DSA for signatures, 2024) are the migration path systems should plan for now.

## How It Works

### Symmetric Encryption Done Right

- **Use AEAD only**: AES-256-GCM or ChaCha20-Poly1305 bind confidentiality and integrity in one construction — ciphertext that was tampered with fails decryption instead of yielding forged plaintext. Never raw CBC/CTR plus a bolted-on check.
- **Nonces must never repeat** under one key (GCM fails catastrophically on nonce reuse: key recovery). Random 96-bit nonces or counters both work; XChaCha20's 192-bit nonce tolerates random generation at scale.
- **Key derivation**: derive per-purpose keys with HKDF from a master secret; store passwords with Argon2id, scrypt, or bcrypt (slow, salted, memory-hard) — fast hashes like SHA-256 alone let attackers try billions of guesses per second.

### Public-Key Machinery

```
Key exchange (ECDH):   A + B each combine own private key with peer public key → same shared secret
Signatures (Ed25519):  Sign(private, message) → sigma; Verify(public, message, sigma) → yes/no
Certificates (X.509):  CA signature binds "this public key belongs to example.com" → browser trusts via root store
```

- **Forward secrecy**: ECDHE generates ephemeral keys per session, so stealing the server's long-term key does not decrypt past traffic. Modern TLS 1.3 provides it by default; static RSA key transport (removed in 1.3) did not.
- **Signatures vs MACs**: a build server signs releases (anyone verifies, only it can sign); two microservices sharing a secret use HMAC on webhooks (either side could have made it — fine, since both are trusted).

### TLS 1.3 Handshake in Brief

1. ClientHello (supported versions, cipher suites, ephemeral ECDH share) → ServerHello (chosen suite, its ECDH share, certificate).
2. Both derive session keys; server's CertificateVerify proves private-key possession; Finished MACs confirm no tampering.
3. Application data flows under AEAD with per-record nonces; session resumption via PSK tickets avoids a full handshake on reconnect.
4. Trust anchors in root CA stores; Certificate Transparency logs make rogue issuance publicly auditable.

## Common Pitfalls

1. **Rolling your own cipher/protocol**: custom XOR "encryption" or homebrew handshakes fail to Kerckhoffs's principle and peer review. Compose vetted primitives (libsodium, age, TLS) instead.
2. **ECB mode or static IVs**: ECB leaks plaintext patterns (the famous penguin image); CBC with predictable IVs enabled BEAST-style attacks. Use AEAD with unique nonces, always.
3. **Hashing passwords with SHA-256/MD5 unsalted**: rainbow tables and GPUs crack these in minutes. Use Argon2id/scrypt/bcrypt with per-user salts and work factors you raise over time.
4. **Skipping certificate verification**: disabling verification "temporarily" or accepting any cert invites MITM. Pin expectations via the system trust store; use DANE or key pinning only where justified.
5. **Timing side channels**: comparing MACs with `==` leaks prefix length via timing — use constant-time comparison. Likewise, RSA/ECDSA need constant-time and deterministic-nonce (RFC 6979) implementations; prefer Ed25519.
6. **Keys in code, logs, and images**: hardcoded secrets leak via repos and container layers. Keys live in a KMS/HSM or secret manager, rotate on schedule, and every use is logged — never in source.

## Related Concepts

- [[concepts/computer-science/tcp-ip|TCP/IP]] (the layer TLS sits on)
- [[concepts/computer-science/http|HTTP]] (HTTPS semantics, HSTS, certificate checks)
- [[concepts/computer-science/hash-tables|Hash Tables]] (non-cryptographic vs cryptographic hashing)
- [[concepts/computer-science/database-transactions|Database Transactions]] (encryption at rest for stored data)

## References

- Katz & Lindell — *Introduction to Modern Cryptography* (definitions, proof approach)
- Ferguson, Schneier & Kohno — *Cryptography Engineering* (implementation pitfalls, AEAD guidance)
- Dworkin (NIST SP 800-38D) — GCM mode specification; RFC 8446 (TLS 1.3); RFC 8032 (Ed25519)
- NIST FIPS 203/204/205 (2024) — ML-KEM, ML-DSA, SLH-DSA post-quantum standards
- libsodium docs; Latacora "Cryptographic Right Answers" (practical primitive choices)
