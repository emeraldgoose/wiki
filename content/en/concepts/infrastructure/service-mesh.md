---
title: Service Mesh
description: "Seminar-level concept: Service mesh architecture, Istio/Linkerd, traffic management, security, observability"
tags: [concept, infrastructure, service-mesh, istio, linkerd, observability]
locale: en
---

# Service Mesh

**Read from**: Netflix service topology, Databricks monitoring, Uber microservices, LinkedIn infrastructure

## What It Is
Dedicated infrastructure layer for service-to-service communication. Handles: traffic management, security, observability — transparently to application.

## Architecture

### Data Plane (Sidecar Proxy)
| Proxy | Language | Features |
|-------|----------|----------|
| Envoy | C++ | L7 routing, TLS, rate limit, WASM |
| Linkerd2-proxy | Rust | Lightweight, safety, simplicity |

**Deployment**: Sidecar per pod (or per VM via CNI)

### Control Plane
- **Configuration**: Service discovery, certificates, policies
- **Distribution**: xDS (Envoy) / in-process (Linkerd)
- **HA**: Multi-replica, leader election

## Traffic Management

### Routing
```yaml
# VirtualService (Istio) / HTTPRoute (Gateway API)
- match: {headers: {x-canary: "true"}}
  route: [{destination: {host: mysvc, subset: v2}, weight: 10}]
- route: [{destination: {host: mysvc, subset: v1}, weight: 90}]
```

### Resilience
| Pattern | Configuration |
|---------|---------------|
| Retry | `retries: 3, perTryTimeout: 2s` |
| Timeout | `timeout: 10s` |
| Circuit Breaker | `consecutive5xxErrors: 5, interval: 30s` |
| Rate Limit | `requestsPerUnit: 100, unit: MINUTE` |
| Fault Injection | `abort: {httpStatus: 500, percentage: 10}` |

### Traffic Splitting
- Canary / Blue-green / A/B testing
- Mirror traffic for shadow testing

## Security

### mTLS (Mutual TLS)
- **Automatic**: Certificate rotation (24h default)
- **Modes**: PERMISSIVE → STRICT
- **Auth policies**: JWT, OIDC, custom

### Authorization
```yaml
# AuthorizationPolicy
rules:
- from: [{source: {principals: ["cluster.local/ns/frontend/sa/app"]}}]
  to: [{operation: {methods: ["GET"], paths: ["/api/*"]}}]
```

## Observability (Golden Signals)

### Metrics (Prometheus)
- **Latency**: `istio_requests_duration_seconds_bucket`
- **Traffic**: `istio_requests_total`
- **Errors**: `istio_requests_total{response_code=~"5.."}`
- **Saturation**: Proxy CPU/memory, connection pool

### Distributed Tracing
- **W3C Trace Context** propagation
- **Sampling**: Head-based / Tail-based
- **Backend**: Jaeger, Zipkin, Tempo, Datadog

### Access Logs
- Structured JSON (Envoy)
- Custom fields via WASM / Lua

## From Sources

### Netflix (Building Service Topology at Scale)
- Multi-layer: Network (eBPF), IPC metrics, Distributed tracing
- Physically separate graph layers
- Kafka consumers fell behind → hash-based redistribution
- Immutable data structures → GC pressure at millions records/sec
- Real-time updates (tens of minutes) vs hour-old batch

### Databricks (Pantheon Monitoring)
- PromQL-to-SQL for Grafana
- Hydra: high-cardinality metrics in Lakehouse

### Uber (Software Factory)
- 3,600+ agent skills across microservices
- Service mesh for agent-to-agent communication

## Istio vs Linkerd vs Cilium

| Aspect | Istio | Linkerd | Cilium |
|--------|-------|---------|--------|
| Complexity | High | Low | Medium |
| Features | Full | Core | Network + Security |
| Resource usage | High | Low | Medium |
| WASM | ✅ | Limited | ✅ |
| Gateway API | ✅ | ✅ | ✅ |
| Multi-cluster | ✅ | ✅ | ✅ |

## Key Seminar Points

1. **Sidecar overhead**: ~10-50ms latency, ~50-100MB RAM/pod
2. **Start with Linkerd** for simplicity; graduate to Istio for features
3. **mTLS first** (security), then traffic management, then observability
4. **Gateway API** = future-standard ingress
5. **Observability** = metrics + traces + logs (all three)

## Related Sources
- `sources/articles/netflix-techblog.md` (service topology)
- `sources/articles/databricks-engineering.md` (monitoring)
- `sources/articles/uber-engineering.md` (microservices)

## Related Guides
- `guides/infrastructure/deploy-kubernetes.md`
