---
title: TCP/IP
description: "Seminar-level concept: TCP/IP model, IP routing, TCP reliability, handshake, congestion control, ports and sockets"
tags: [concept, computer-science, tcp-ip, networking, tcp, ip, congestion-control]
published: 2026-09-06
locale: en
---

# TCP/IP

> [한국어 버전](/ko/concepts/computer-science/tcp-ip)

**TCP/IP** is the protocol suite of the internet: **IP** provides best-effort delivery of packets between hosts, and **TCP** builds reliable, ordered, congestion-aware byte streams on top. Nearly every distributed system behavior — latency, throughput collapse, connection setup cost — traces back to these two layers.

## Definition

- **Internet Protocol (IP)**: unreliable, connectionless delivery of **datagrams** from source to destination address. IPv4 (32-bit, ~4.3B addresses, NAT-extended) and IPv6 (128-bit). Handles addressing and **routing**; guarantees nothing about delivery, order, or duplication.
- **Transmission Control Protocol (TCP)**: reliable, ordered, connection-oriented byte stream over IP. Adds sequence numbers, acknowledgments, retransmission, flow control, and congestion control.
- **TCP/IP model** (4 layers): Link → Internet (IP) → Transport (TCP/UDP) → Application (HTTP, DNS, ...). Contrast with the 7-layer OSI model, which is pedagogical; the 4-layer model is what runs.
- **UDP**: connectionless datagrams without reliability — lower latency, no head-of-line blocking. Used by DNS, QUIC/HTTP-3, VoIP, games.

## Why It Matters

- **Reliability is not free**: TCP's guarantees cost a handshake (1 RTT before data), per-connection state, and head-of-line blocking. Understanding the price tells you when to pay it (files, APIs) and when not to (live media, custom protocols over UDP).
- **Congestion collapse is real**: without congestion control, senders collectively overfill router buffers and goodput drops toward zero. TCP's algorithms are the internet's load-shedding system.
- **Latency math starts here**: RTT, bandwidth-delay product, and loss recovery dominate transfer times far more than raw bandwidth for typical flows.
- **Debugging distributed systems** is mostly reading packet behavior: `SYN` floods, retransmits, zero windows, RSTs.

## How It Works

### IP: Addressing, Fragmentation, Routing

```
IPv4 header: version | IHL | DSCP | total length | identification |
             flags + fragment offset | TTL | protocol | checksum |
             source IP | destination IP | options...
```

- **Routing**: each router forwards by longest-prefix match on the destination against its routing table (populated by BGP between ASes, OSPF/IS-IS within). **TTL** decrements per hop and prevents infinite loops.
- **Fragmentation**: packets larger than a link MTU (commonly 1500 B) are split and reassembled at the destination. Avoid it in practice: use **Path MTU Discovery** and clamp MSS — fragments amplify loss (losing one fragment kills the whole datagram) and are a classic firewall/DDoS headache.
- **NAT**: rewrites private → public addresses/ports to stretch IPv4. Breaks end-to-end connectivity (hence STUN/TURN/ICE for P2P) and makes inbound connections require port forwarding.

### TCP: Handshake, Reliability, Teardown

```
Handshake:  SYN → / SYN-ACK ← / ACK →        (1 RTT before data)
Data:       SEQ=n, len=k → / ACK=n+k ←       (cumulative ACKs)
Teardown:   FIN → / ACK ← / FIN ← / ACK →    (or abrupt RST)
```

- **Sequence numbers**: every byte is numbered; the receiver ACKs the next expected byte. Duplicates and reordering are absorbed; gaps trigger retransmission.
- **Retransmission**: on timeout (RTO, computed from smoothed RTT + variance) or triple duplicate ACKs (fast retransmit). **SACK** (selective ACK) reports exactly which blocks arrived, avoiding resending what already got through.
- **Flow control**: the receiver advertises `rwnd` (receive window); the sender never exceeds it — protects a slow receiver.
- **Connection state cost**: each socket holds send/receive buffers, timers, and sequence state. `TIME_WAIT` (2×MSL, typically 60 s) after active close prevents delayed segments from corrupting new connections — and exhausts ephemeral ports under high-churn loads.

### Congestion Control

- Core idea: maintain **cwnd** (congestion window); effective window = `min(cwnd, rwnd)`. Probe for capacity, back off on loss.
- **Slow start**: exponential growth (cwnd doubles per RTT) until ssthresh or loss — how new connections ramp.
- **Congestion avoidance**: AIMD — additive increase per RTT, multiplicative decrease on loss (classic Reno: cwnd halves). This sawtooth is the signature shape of TCP throughput.
- **Modern variants**: CUBIC (default Linux; window growth is cubic in time since last loss, scales well on high-BDP paths), BBR (Google; models bottleneck bandwidth + RTT instead of reacting to loss — better on lossy/bufferbloated paths, requires kernel ≥ 4.9).
- **Bandwidth-delay product (BDP)**: `max throughput = window / RTT`. A 100 Mbps link with 100 ms RTT needs a ~1.25 MB window — window scaling (RFC 7323) exists precisely because the original 64 KB cap would strangle it.

### Ports and Sockets

- A connection is identified by the 4-tuple (src IP, src port, dst IP, dst port). Ports 0–1023 are well-known (80/HTTP, 443/HTTPS, 22/SSH); 49152–65535 are ephemeral (client side).
- `listen()` backlog, `accept()` queue overflows, and `SYN` cookies (spoof-resistant handshake under SYN flood) are the operational surface of TCP servers.

## Common Pitfalls

1. **Chatty protocols on high-RTT links**: N sequential request-response rounds cost N×RTT regardless of bandwidth. Pipeline, batch, or multiplex (HTTP/2, QUIC) instead.
2. **Tiny receive/send buffers**: default socket buffers often cap throughput on high-BDP paths. Size buffers ≥ BDP (`SO_RCVBUF`/`SO_SNDBUF`, system `rmem_max`/`wmem_max`).
3. **TIME_WAIT exhaustion**: short-lived connection churn (proxies, crawlers) burns the ~28k ephemeral ports per destination. Fix with keep-alive, connection pooling, or multiple egress IPs — not by recklessly zeroing `tcp_fin_timeout`.
4. **Disabling Nagle blindly**: `TCP_NODELAY` helps latency-sensitive RPC but turns small-write workloads into packet floods (40-byte headers per few bytes of payload). Batch small writes instead of toggling flags reflexively.
5. **Ignoring loss vs delay signals**: classic Reno treats all loss as congestion; on lossy links (Wi-Fi, intercontinental) it underutilizes badly. Prefer CUBIC/BBR and measure.
6. **Assuming in-order, exactly-once delivery composes**: TCP gives it per connection only. Application-level retries over TCP can still duplicate *requests* (the response may have been lost, not the request) — idempotency keys remain necessary.

## Related Concepts

- [[concepts/computer-science/http|HTTP]] (application layer over TCP/TLS; HTTP/3 over QUIC/UDP)
- [[concepts/computer-science/processes-and-threads|Processes and Threads]] (thread-per-connection costs, socket handling)

## References

- RFC 791 (IPv4), RFC 8200 (IPv6), RFC 9293 (TCP, obsoletes 793), RFC 7323 (window scaling), RFC 8985 (BBR overview via draft-cardwell)
- Stevens — *TCP/IP Illustrated, Vol. 1*; Stevens/Fenner/Rudoff — *UNIX Network Programming, Vol. 1*
- Linux man pages: `tcp(7)`, `ip(7)`, `socket(7)`, `ss(8)`
- Van Jacobson (1988) — "Congestion Avoidance and Control" (foundational paper)
