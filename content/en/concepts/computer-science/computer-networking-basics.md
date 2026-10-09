---
title: Computer Networking Basics
description: "Seminar-level concept: OSI and TCP/IP layers, IP routing, TCP vs UDP, DNS, NAT, congestion control"
tags: [concept, computer-science, networking, tcp-ip, dns, routing, congestion-control, nat]
published: 2026-09-06
locale: en
---

# Computer Networking Basics

**Computer networking** moves bytes between machines through layered protocols: each layer solves one problem — who (addressing), how far (routing), reliably or fast (transport), and what it means (application). The layering is the point: IP routes without caring what TCP guarantees, and HTTP works without knowing which fiber carries it.

## Definition

- **Packet**: the unit of network transmission — headers (source, destination, sequence) plus payload, bounded by the MTU (~1500 bytes on Ethernet). Large messages are fragmented or segmented and reassembled.
- **IP (Internet Protocol)**: best-effort delivery between addresses (IPv4 32-bit, IPv6 128-bit). Routers forward by longest-prefix match toward the destination; no reliability, ordering, or duplicate protection is promised.
- **TCP**: reliable ordered byte stream over IP — handshake, sequence numbers, retransmission, flow and congestion control. **UDP**: thin datagrams with ports and a checksum — no handshake, no retransmission, minimal latency.
- **DNS**: the distributed name-to-address database (`example.com` → A/AAAA records), hierarchical from root to TLD to authoritative servers, with TTL-driven caching at every level.
- **NAT / firewall**: middleboxes that rewrite addresses (letting many private hosts share one public IP) and filter by policy — the reason end-to-end connectivity needs hole-punching or relays.

## Why It Matters

- **Latency is physics plus queues**: light in fiber (~200 km/ms) sets the floor (~130 ms RTT Seoul–Virginia); everything above it — DNS, handshakes, bufferbloat, retransmissions — is negotiable overhead engineers can measure and cut.
- **Reliability is end-to-end**: the network drops, duplicates, and reorders; correctness (retries with idempotency, checksums at the app layer) cannot be fully delegated to TCP. The end-to-end argument still governs API design.
- **Scale is routing + naming**: BGP announces reachability between ~80k autonomous systems; DNS resolves billions of names via caching hierarchies. Both are distributed systems with consistency tradeoffs of their own.
- **Security rides the same layers**: TLS authenticates and encrypts above TCP; DNSSEC signs names; firewalls and security groups filter below. Each layer's threat model differs — defense composes across them.

## How It Works

### Layers: OSI vs TCP/IP Reality

```
7 Application   HTTP, DNS, gRPC          (what it means)
4 Transport     TCP / UDP + ports        (which process, how reliably)
3 Network       IP + routing (BGP/OSPF)  (which host, which path)
2 Link          Ethernet, Wi-Fi, ARP      (which neighbor on the wire)
1 Physical      fiber, radio, copper     (bits as signals)
```

- The famous 7-layer OSI model is pedagogical; the Internet runs the 4-ish-layer TCP/IP stack (link, internet, transport, application). Encapsulation nests them: Ethernet frame → IP packet → TCP segment → HTTP message.
- **Ports** (16-bit) demultiplex to processes: 443/HTTPS, 53/DNS, 22/SSH. A socket is the (IP, port, protocol) tuple; NAT rewrites these tuples to multiplex hosts.

### TCP: Reliability Machinery

- **Handshake**: SYN → SYN-ACK → ACK exchanges sequence numbers and negotiates MSS/window scaling/SACK. Cost: one RTT before any data (TLS 1.3 needs one more; QUIC merges both into ~1 RTT).
- **Sliding window + cumulative ACKs**: sender keeps unacknowledged bytes within the receiver's advertised window; lost segments are retransmitted after duplicate ACKs (fast retransmit) or RTO timeout (exponential backoff).
- **Congestion control**: slow start probes capacity exponentially, then AIMD (additive increase, multiplicative decrease) converges flows to fairness — Reno, CUBIC (Linux default), and BBR (model-based, Google) differ in the signal they track (loss vs RTT vs bottleneck rate).
- **Flow vs congestion**: receiver window protects the peer's buffers; congestion window protects the network. The sender obeys the minimum of the two.

### DNS, Routing, and NAT

- **DNS resolution**: stub → recursive resolver → root → TLD → authoritative, with caching at each hop keyed by TTL. `dig +trace` shows the chain; stale TTLs are why migrations "take time to propagate."
- **Routing**: intra-domain OSPF/IS-IS (link-state, Dijkstra) picks cheapest internal paths; inter-domain **BGP** (path-vector over TCP/179) applies policy between ASes. BGP hijacks/leaks are the Internet's recurring integrity incidents.
- **NAT traversal**: outbound mappings let private hosts initiate; inbound needs port forwarding, STUN hole-punching, or TURN relays (WebRTC's ladder). IPv6 restores end-to-end addressing but firewalls still default-deny inbound.

## Common Pitfalls

1. **Chatty protocols over distance**: dozens of sequential RPCs per page, each paying full RTT — 50 round trips × 130 ms = 6.5 s. Batch, pipeline, cache, and push work near the data (edge, CDN).
2. **No timeouts/retries budget**: default socket timeouts of "forever" turn one slow dependency into thread-pool exhaustion. Set connect/read/deadline timeouts, retry idempotent calls with jittered backoff, circuit-break the rest.
3. **Ignoring MTU/fragmentation**: 9 KB payloads over a 1500-byte path MTU fragment; one lost fragment kills the whole datagram. Prefer path-MTU discovery and segment at the sender.
4. **DNS TTL traps**: 7-day TTLs during a migration mean a week of split traffic; 5-second TTLs everywhere mean resolver load and tail latency. Lower TTLs *before* the move, raise after.
5. **Head-of-line blocking**: one lost TCP packet stalls every multiplexed stream behind it. HTTP/3 over QUIC (UDP-based, per-stream retransmission) exists largely to fix this.
6. **Assuming the LAN in the WAN**: broadcast discovery, unauthenticated plaintext, and "internal = trusted" fail the moment a laptop leaves the office. Zero-trust: authenticate and encrypt every hop (mTLS, WireGuard).

## Related Concepts

- [[concepts/computer-science/tcp-ip|TCP/IP]] (deep dive on the core protocols)
- [[concepts/computer-science/http|HTTP]] (the application layer in practice)
- [[concepts/computer-science/cap-theorem|CAP Theorem]] (partitions: what the network inflicts on systems)
- [[concepts/computer-science/cryptography-basics|Cryptography Basics]] (TLS, authentication, secure channels)

## References

- Kurose & Ross — *Computer Networking: A Top-Down Approach* (layered pedagogy, socket programming)
- Peterson & Davie — *Computer Networks: A Systems Approach* (free online edition)
- Stevens — *TCP/IP Illustrated, Vol. 1*; RFC 9293 (TCP), RFC 1034/1035 (DNS), RFC 9000 (QUIC)
- Jacobson, "Congestion Avoidance and Control" (SIGCOMM 1988); Cardwell et al., BBR (ACM Queue 2016)
- Beej's Guide to Network Programming (practical sockets reference)
