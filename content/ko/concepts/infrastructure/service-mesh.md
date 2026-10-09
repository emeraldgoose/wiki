---
title: 서비스 메시 (Service Mesh)
description: en/concepts/infrastructure/service-mesh.md 한국어 번역 요약
tags: [concept, infrastructure, service-mesh, istio, linkerd, observability, ko]
locale: ko
---

# 서비스 메시 (Service Mesh)

**참고 소스**: Netflix 서비스 토폴로지, Databricks 모니터링, Uber 마이크로서비스, LinkedIn 인프라

## 정의
서비스 간 통신을 위한 전용 인프라 레이어. 애플리케이션에 투명하게 다음을 처리: 트래픽 관리, 보안, 관찰성.

## 아키텍처

### 데이터 플레인 (사이드카 프록시)
| 프록시 | 언어 | 기능 |
|-------|----------|----------|
| Envoy | C++ | L7 라우팅, TLS, rate limit, WASM |
| Linkerd2-proxy | Rust | 경량, 안전성, 단순성 |

**배포 방식**: 파드당 사이드카 (또는 CNI 경유로 VM당 배포)

### 컨트롤 플레인
- **설정**: 서비스 디스커버리, 인증서, 정책
- **배포**: xDS (Envoy) / 인프로세스 (Linkerd)
- **HA**: 다중 레플리카, 리더 선출

## 트래픽 관리

### 라우팅
```yaml
# VirtualService (Istio) / HTTPRoute (Gateway API)
- match: {headers: {x-canary: "true"}}
  route: [{destination: {host: mysvc, subset: v2}, weight: 10}]
- route: [{destination: {host: mysvc, subset: v1}, weight: 90}]
```

### 복원력
| 패턴 | 설정 |
|---------|---------------|
| Retry | `retries: 3, perTryTimeout: 2s` |
| Timeout | `timeout: 10s` |
| Circuit Breaker | `consecutive5xxErrors: 5, interval: 30s` |
| Rate Limit | `requestsPerUnit: 100, unit: MINUTE` |
| Fault Injection | `abort: {httpStatus: 500, percentage: 10}` |

### 트래픽 분할
- 카나리 / 블루-그린 / A/B 테스트
- 섀도 테스트용 트래픽 미러링

## 보안

### mTLS (상호 TLS)
- **자동**: 인증서 순환 (기본 24시간)
- **모드**: PERMISSIVE → STRICT
- **인증 정책**: JWT, OIDC, 커스텀

### 인가
```yaml
# AuthorizationPolicy
rules:
- from: [{source: {principals: ["cluster.local/ns/frontend/sa/app"]}}]
  to: [{operation: {methods: ["GET"], paths: ["/api/*"]}}]
```

## 관찰성 (골든 시그널)

### 메트릭 (Prometheus)
- **지연시간**: `istio_requests_duration_seconds_bucket`
- **트래픽**: `istio_requests_total`
- **에러**: `istio_requests_total{response_code=~"5.."}`
- **포화도**: 프록시 CPU/메모리, 커넥션 풀

### 분산 트레이싱
- **W3C Trace Context** 전파
- **샘플링**: 헤드 기반 / 테일 기반
- **백엔드**: Jaeger, Zipkin, Tempo, Datadog

### 액세스 로그
- 구조화된 JSON (Envoy)
- WASM / Lua를 통한 커스텀 필드

## 소스에서

### Netflix (대규모 서비스 토폴로지 구축)
- 다층 구조: 네트워크 (eBPF), IPC 메트릭, 분산 트레이싱
- 물리적으로 분리된 그래프 레이어
- Kafka 컨슈머 지연 → 해시 기반 재분배
- 불변 데이터 구조 → 초당 수백만 레코드에서 GC 압박
- 실시간 업데이트 (수십 분) vs 한 시간 된 배치

### Databricks (Pantheon 모니터링)
- Grafana용 PromQL-to-SQL
- Hydra: Lakehouse의 고카디널리티 메트릭

### Uber (Software Factory)
- 마이크로서비스에 걸친 3,600개 이상의 에이전트 스킬
- 에이전트 간 통신용 서비스 메시

## Istio vs Linkerd vs Cilium

| 측면 | Istio | Linkerd | Cilium |
|--------|-------|---------|--------|
| 복잡도 | 높음 | 낮음 | 중간 |
| 기능 | 전체 | 핵심 | 네트워크 + 보안 |
| 리소스 사용량 | 높음 | 낮음 | 중간 |
| WASM | ✅ | 제한적 | ✅ |
| Gateway API | ✅ | ✅ | ✅ |
| 멀티클러스터 | ✅ | ✅ | ✅ |

## 핵심 세미나 포인트

1. **사이드카 오버헤드**: 약 10-50ms 지연, 파드당 약 50-100MB RAM
2. **Linkerd부터 시작** (단순함); 기능이 필요하면 Istio로 졸업
3. **mTLS 우선** (보안), 다음 트래픽 관리, 다음 관찰성
4. **Gateway API** = 미래 표준 인그레스
5. **관찰성** = 메트릭 + 트레이스 + 로그 (세 가지 모두)

## 관련 소스
- `sources/articles/netflix-techblog.md` (서비스 토폴로지)
- `sources/articles/databricks-engineering.md` (모니터링)
- `sources/articles/uber-engineering.md` (마이크로서비스)

## 관련 가이드
- `guides/infrastructure/deploy-kubernetes.md`
