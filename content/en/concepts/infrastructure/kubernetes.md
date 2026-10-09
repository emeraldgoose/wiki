---
title: Kubernetes
description: "Seminar-level concept: Kubernetes architecture, scheduling, networking, storage, operators"
tags: [concept, infrastructure, kubernetes, orchestration, operators]
locale: en
---

# Kubernetes

**Read from**: Netflix Kueue, AWS MSK, Databricks Pantheon, Uber, LinkedIn, Twitter

## Architecture

### Control Plane
| Component | Role |
|-----------|------|
| API Server | REST/gRPC gateway; auth, validation, admission |
| Scheduler | Pod → Node assignment (predicates + priorities) |
| Controller Manager | Reconciliation loops (ReplicaSet, Service, Node, etc.) |
| etcd | Key-value store; cluster state (raft consensus) |

### Worker Node
| Component | Role |
|-----------|------|
| kubelet | Pod lifecycle; container runtime interface (CRI) |
| kube-proxy | Service load balancing (iptables/IPVS) |
| Container Runtime | containerd, CRI-O (pull, run, stop) |
| CNI Plugin | Pod networking (Calico, Cilium, Flannel) |

## Scheduling

### Pod Scheduling Flow
1. **Filter** (predicates): Node resources, taints/tolerations, affinity, topology spread
2. **Score** (priorities): Resource balance, image locality, inter-pod affinity
3. **Bind**: Assign pod to node

### Advanced Scheduling
- **Pod Topology Spread**: Even distribution across zones
- **Priority/Preemption**: High-priority pods preempt low-priority
- **Gang Scheduling** (Kueue): All-or-nothing for distributed jobs
- **Custom Schedulers**: For ML/AI workloads (Volcano, YuniKorn)

## Networking

### Service Types
- **ClusterIP**: Internal only
- **NodePort**: External via node port
- **LoadBalancer**: Cloud LB integration
- **ExternalName**: DNS CNAME

### CNI (Container Network Interface)
- **Calico**: BGP, network policy, eBPF datapath
- **Cilium**: eBPF-native, L7 policy, service mesh
- **Flannel**: Simple VXLAN overlay

## Storage

### CSI (Container Storage Interface)
- Volume lifecycle: Provision → Bind → Mount → Unmount → Delete
- **Dynamic Provisioning**: StorageClass → PVC → PV
- **Snapshots**: VolumeSnapshot / VolumeSnapshotContent

### Patterns
- **StatefulSet**: Stable network ID, persistent storage, ordered deployment
- **Operator**: Custom controller for stateful apps (Postgres, Kafka, Redis)

## Operators (from Sources)

### Databricks Pantheon
- **Rollout Operator**: Coordinated StatefulSet updates (quorum preserved)
- **Hashring Controller**: Traffic management decoupled from pod lifecycle
- **Autoscaling/Self-Healing Controller**: Scale on ingestion pressure; heal bad hosts/corrupted WAL

### Netflix Kueue
- **Kueue Operator**: Cohort/ClusterQueue/LocalQueue hierarchy
- Multi-tenant batch scheduling with preemption/fair sharing

### AWS MSK
- Custom domain configuration operator
- Two-phase rollout: networking first, then advertised listener

## Key Seminar Points

1. **Control plane HA**: etcd quorum (3/5 nodes); API server load balanced
2. **Scheduler extensibility**: Plugins for ML workloads (gang, bin-packing)
3. **Stateful workloads**: Operators encapsulate domain knowledge
4. **Multi-tenancy**: Namespaces + quotas + network policies + admission
5. **GitOps**: ArgoCD/Flux for declarative cluster management

## Related Sources
- `sources/articles/netflix-techblog.md` (Kueue batch orchestration)
- `sources/articles/databricks-engineering.md` (Pantheon operators)
- `sources/articles/aws-bigdata.md` (MSK custom domain)
- `sources/articles/uber-engineering.md` (K8s at scale)

## Related Guides
- `guides/infrastructure/deploy-kubernetes.md`
