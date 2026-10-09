---
title: Docker
description: "Seminar-level concept: Docker/container fundamentals, images, layers, build optimization, security"
tags: [concept, infrastructure, docker, container, buildkit]
locale: en
---

# Docker

**Read from**: Netflix Kueue, AWS MSK, Databricks Pantheon, Uber, Twitter

## Core Concepts

### Image vs Container
- **Image**: Read-only template (layers + manifest + config)
- **Container**: Running instance (writable layer + namespaces + cgroups)

### Layer Architecture
```
Base OS → System deps → App deps → App code → Config
```
- Each layer = diff from previous
- **Content-addressable**: SHA256 of layer tarball
- **Sharing**: Common base layers reused across images

### Build Process
```
Dockerfile → BuildKit → Layers → Registry → Pull → Run
```

## Build Optimization (Seminar Checklist)

### Layer Caching
```dockerfile
# Bad: COPY . . invalidates cache on any file change
COPY . .

# Good: Copy dependency files first
COPY package*.json ./
RUN npm ci --only=production
COPY . .
```

### Multi-Stage Builds
```dockerfile
# Build stage
FROM node:20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Runtime stage (smaller)
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

### BuildKit Features
- `--cache-from`: Remote cache (registry)
- `--target`: Build specific stage
- `--secret`: Build-time secrets (not in image)
- `--ssh`: SSH agent forwarding for private repos

## Security

### Image Scanning
```bash
# Trivy
trivy image myapp:latest

# Grype
grype myapp:latest

# Syft (SBOM)
syft myapp:latest
```

### Runtime Security
- **Non-root user**: `USER appuser` in Dockerfile
- **Read-only rootfs**: `--read-only` + tmpfs for writable dirs
- **Capabilities**: Drop all, add only needed (`--cap-drop=ALL --cap-add=CAP_NET_BIND_SERVICE`)
- **Seccomp/AppArmor**: Default profiles or custom

### Supply Chain
- **SBOM** (Software Bill of Materials): Syft, SPDX, CycloneDX
- **Signing**: cosign (keyless + keypair)
- **Verification**: cosign verify, policy controllers (Kyverno, Gatekeeper)

## Container Runtime

### containerd vs Docker Engine
| Aspect | containerd | Docker Engine |
|--------|------------|---------------|
| Scope | Container lifecycle only | Full platform |
| CRI | Native | Via cri-dockerd |
| Image mgmt | nerdctl / ctr | docker CLI |
| K8s | Default | Deprecated |

### CRI-O
- OCI-compliant, Kubernetes-focused
- Lightweight, no daemon

## Registry

### Distribution
- **Harbor**: Enterprise registry (replication, scanning, RBAC)
- **GHCR/ECR/GCR/ACR**: Cloud-managed
- **Distribution** (CNCF): Reference implementation

### Optimization
- **Referrers API**: Attach signatures, SBOMs, scan results to image
- **OCI Artifacts**: Store non-image artifacts (Helm charts, policies)
- **Zstd compression**: `docker buildx build --compression=zstd`

## From Sources

### Netflix Kueue
- Container images for batch workloads
- Kueue manages pod lifecycle; container runtime = containerd

### AWS MSK
- Broker runs in container (Amazon Linux 2023)
- Custom domain via NLB → container networking

### Databricks Pantheon
- Thanos components as containers in StatefulSets
- Rolling updates via Rollout Operator

### Uber
- Millions of batch containers via Kueue
- Preemption/fair sharing at container level

## Key Seminar Points

1. **Layer caching** = #1 build speed optimization
2. **Multi-stage** = small runtime images
3. **BuildKit** = modern build features (cache, secrets, SSH)
4. **Security**: Non-root, read-only, capabilities, scanning, signing
4. **containerd/CRI-O** for K8s; Docker Engine for dev

## Related Sources
- `sources/articles/netflix-techblog.md` (Kueue)
- `sources/articles/databricks-engineering.md` (Pantheon containers)
- `concepts/infrastructure/kubernetes.md` (CRI, scheduling)

## Related Guides
- `guides/infrastructure/deploy-kubernetes.md`
