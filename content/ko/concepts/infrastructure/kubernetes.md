---
title: Kubernetes
description: en/concepts/infrastructure/kubernetes.md 한국어 번역 요약
tags: [concept, infrastructure, kubernetes, orchestration, operators, ko]
locale: ko
---

# Kubernetes

**참고 소스**: Netflix Kueue, AWS MSK, Databricks Pantheon, Uber, LinkedIn, Twitter

## 아키텍처

### 컨트롤 플레인
| 컴포넌트 | 역할 |
|-----------|------|
| API Server | REST/gRPC 게이트웨이; 인증, 검증, 어드미션 |
| Scheduler | 파드 → 노드 할당 (predicates + priorities) |
| Controller Manager | 리컨실리에이션 루프 (ReplicaSet, Service, Node 등) |
| etcd | 키-값 저장소; 클러스터 상태 (raft 합의) |

### 워커 노드
| 컴포넌트 | 역할 |
|-----------|------|
| kubelet | 파드 생명주기; 컨테이너 런타임 인터페이스 (CRI) |
| kube-proxy | 서비스 로드밸런싱 (iptables/IPVS) |
| Container Runtime | containerd, CRI-O (pull, run, stop) |
| CNI Plugin | 파드 네트워킹 (Calico, Cilium, Flannel) |

## 스케줄링

### 파드 스케줄링 흐름
1. **Filter** (predicates): 노드 리소스, taints/tolerations, affinity, topology spread
2. **Score** (priorities): 리소스 균형, 이미지 지역성, inter-pod affinity
3. **Bind**: 파드를 노드에 할당

### 고급 스케줄링
- **Pod Topology Spread**: 존 간 균등 분산
- **Priority/Preemption**: 고우선순위 파드가 저우선순위 파드를 선점
- **Gang Scheduling** (Kueue): 분산 잡의 all-or-nothing 실행
- **Custom Schedulers**: ML/AI 워크로드용 (Volcano, YuniKorn)

## 네트워킹

### 서비스 타입
- **ClusterIP**: 내부 전용
- **NodePort**: 노드 포트를 통한 외부 노출
- **LoadBalancer**: 클라우드 LB 연동
- **ExternalName**: DNS CNAME

### CNI (Container Network Interface)
- **Calico**: BGP, 네트워크 정책, eBPF 데이터패스
- **Cilium**: eBPF 네이티브, L7 정책, 서비스 메시
- **Flannel**: 단순한 VXLAN 오버레이

## 스토리지

### CSI (Container Storage Interface)
- 볼륨 생명주기: Provision → Bind → Mount → Unmount → Delete
- **동적 프로비저닝**: StorageClass → PVC → PV
- **스냅샷**: VolumeSnapshot / VolumeSnapshotContent

### 패턴
- **StatefulSet**: 안정적인 네트워크 ID, 영속 스토리지, 순서 있는 배포
- **Operator**: 스테이트풀 앱용 커스텀 컨트롤러 (Postgres, Kafka, Redis)

## 오퍼레이터 (소스에서)

### Databricks Pantheon
- **Rollout Operator**: StatefulSet의 조율된 업데이트 (쿼럼 유지)
- **Hashring Controller**: 파드 생명주기와 분리된 트래픽 관리
- **Autoscaling/Self-Healing Controller**: 인제스천 압력에 따른 스케일링; 불량 호스트/손상된 WAL 자가 치유

### Netflix Kueue
- **Kueue Operator**: Cohort/ClusterQueue/LocalQueue 계층 구조
- 프리엠션/공정 공유를 갖춘 멀티테넌트 배치 스케줄링

### AWS MSK
- 커스텀 도메인 설정 오퍼레이터
- 2단계 롤아웃: 네트워킹 먼저, 그 다음 advertised listener

## 핵심 세미나 포인트

1. **컨트롤 플레인 HA**: etcd 쿼럼 (3/5 노드); API 서버 로드밸런싱
2. **스케줄러 확장성**: ML 워크로드용 플러그인 (gang, bin-packing)
3. **스테이트풀 워크로드**: 도메인 지식을 캡슐화한 오퍼레이터
4. **멀티테넌시**: 네임스페이스 + 쿼터 + 네트워크 정책 + 어드미션
5. **GitOps**: 선언적 클러스터 관리를 위한 ArgoCD/Flux

## 관련 소스
- `sources/articles/netflix-techblog.md` (Kueue 배치 오케스트레이션)
- `sources/articles/databricks-engineering.md` (Pantheon 오퍼레이터)
- `sources/articles/aws-bigdata.md` (MSK 커스텀 도메인)
- `sources/articles/uber-engineering.md` (대규모 K8s)

## 관련 가이드
- `guides/infrastructure/deploy-kubernetes.md`
