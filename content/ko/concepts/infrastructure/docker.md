---
title: Docker
description: en/concepts/infrastructure/docker.md 한국어 번역 요약
tags: [concept, infrastructure, docker, container, buildkit, ko]
locale: ko
---

# Docker

**참고 소스**: Netflix Kueue, AWS MSK, Databricks Pantheon, Uber, Twitter

## 핵심 개념

### 이미지 vs 컨테이너
- **이미지(Image)**: 읽기 전용 템플릿 (레이어 + 매니페스트 + 설정)
- **컨테이너(Container)**: 실행 중인 인스턴스 (쓰기 가능 레이어 + 네임스페이스 + cgroups)

### 레이어 아키텍처
```
Base OS → System deps → App deps → App code → Config
```
- 각 레이어 = 이전 레이어와의 diff
- **콘텐츠 주소 지정(Content-addressable)**: 레이어 tarball의 SHA256
- **공유**: 공통 베이스 레이어를 이미지 간에 재사용

### 빌드 프로세스
```
Dockerfile → BuildKit → Layers → Registry → Pull → Run
```

## 빌드 최적화 (세미나 체크리스트)

### 레이어 캐싱
```dockerfile
# 나쁜 예: 파일 하나만 바뀌어도 캐시가 무효화됨
COPY . .

# 좋은 예: 의존성 파일부터 먼저 복사
COPY package*.json ./
RUN npm ci --only=production
COPY . .
```

### 멀티스테이지 빌드
```dockerfile
# 빌드 스테이지
FROM node:20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# 런타임 스테이지 (더 작음)
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

### BuildKit 기능
- `--cache-from`: 원격 캐시 (레지스트리)
- `--target`: 특정 스테이지 빌드
- `--secret`: 빌드 시점 시크릿 (이미지에 남지 않음)
- `--ssh`: 프라이빗 저장소 접근용 SSH 에이전트 포워딩

## 보안

### 이미지 스캐닝
```bash
# Trivy
trivy image myapp:latest

# Grype
grype myapp:latest

# Syft (SBOM)
syft myapp:latest
```

### 런타임 보안
- **Non-root 사용자**: Dockerfile에 `USER appuser` 지정
- **읽기 전용 rootfs**: `--read-only` + 쓰기 가능 디렉터리는 tmpfs 사용
- **Capabilities**: 전부 제거 후 필요한 것만 추가 (`--cap-drop=ALL --cap-add=CAP_NET_BIND_SERVICE`)
- **Seccomp/AppArmor**: 기본 프로파일 또는 커스텀 프로파일 사용

### 공급망
- **SBOM** (Software Bill of Materials): Syft, SPDX, CycloneDX
- **서명**: cosign (keyless + 키페어)
- **검증**: cosign verify, 정책 컨트롤러 (Kyverno, Gatekeeper)

## 컨테이너 런타임

### containerd vs Docker Engine
| 측면 | containerd | Docker Engine |
|--------|------------|---------------|
| 범위 | 컨테이너 생명주기 전용 | 풀 플랫폼 |
| CRI | 네이티브 | cri-dockerd 경유 |
| 이미지 관리 | nerdctl / ctr | docker CLI |
| K8s | 기본값 | Deprecated |

### CRI-O
- OCI 호환, Kubernetes 전용
- 경량, 데몬 없음

## 레지스트리

### 배포
- **Harbor**: 엔터프라이즈 레지스트리 (복제, 스캐닝, RBAC)
- **GHCR/ECR/GCR/ACR**: 클라우드 관리형
- **Distribution** (CNCF): 레퍼런스 구현

### 최적화
- **Referrers API**: 서명, SBOM, 스캔 결과를 이미지에 첨부
- **OCI Artifacts**: 비이미지 아티팩트 저장 (Helm 차트, 정책)
- **Zstd 압축**: `docker buildx build --compression=zstd`

## 소스에서

### Netflix Kueue
- 배치 워크로드용 컨테이너 이미지
- Kueue가 파드 생명주기 관리; 컨테이너 런타임 = containerd

### AWS MSK
- 브로커가 컨테이너에서 실행 (Amazon Linux 2023)
- NLB를 통한 커스텀 도메인 → 컨테이너 네트워킹

### Databricks Pantheon
- Thanos 컴포넌트를 StatefulSet의 컨테이너로 실행
- Rollout Operator를 통한 롤링 업데이트

### Uber
- Kueue를 통한 수백만 개의 배치 컨테이너
- 컨테이너 수준의 프리엠션/공정 공유

## 핵심 세미나 포인트

1. **레이어 캐싱** = 빌드 속도 최적화의 핵심
2. **멀티스테이지** = 작은 런타임 이미지
3. **BuildKit** = 모던 빌드 기능 (캐시, 시크릿, SSH)
4. **보안**: Non-root, 읽기 전용, capabilities, 스캐닝, 서명
4. **containerd/CRI-O**는 K8s용; Docker Engine은 개발용

## 관련 소스
- `sources/articles/netflix-techblog.md` (Kueue)
- `sources/articles/databricks-engineering.md` (Pantheon 컨테이너)
- `concepts/infrastructure/kubernetes.md` (CRI, 스케줄링)

## 관련 가이드
- `guides/infrastructure/deploy-kubernetes.md`
