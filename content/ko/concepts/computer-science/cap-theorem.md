---
title: CAP 정리
description: "세미나 수준 개념: 일관성, 가용성, 분할 내성, 증명 직관, PACELC, CP와 AP 설계"
tags: [concept, computer-science, cap-theorem, distributed-systems, consistency, availability, partition-tolerance, ko]
published: 2026-09-06
locale: ko
---

# CAP 정리

**CAP 정리**는 분산 데이터 저장소가 **일관성(Consistency)**, **가용성(Availability)**, **분할 내성(Partition tolerance)** 세 가지 중 최대 두 가지만 동시에 보장할 수 있다는 정리다. 네트워크 분할은 피할 수 없으므로, 실제 설계 선택은 *분할이 일어났을 때* 어떻게 동작할지로 귀결된다. 일부 요청을 거부하거나(CP), 오래된 데이터라도 내놓거나(AP).

## 정의

- **일관성(C)** — Gilbert–Lynch 정식화에서의 선형화 가능성(linearizability): 모든 읽기는 가장 최근 쓰기나 오류를 받는다. 데이터 사본이 하나인 것처럼 모든 노드가 연산의 단일 전체 순서를 공유한다.
- **가용성(A)** — 고장 나지 않은 노드에 오는 모든 요청이 (오류가 아닌) 응답을 받는다. 가장 신선한 값이라는 보장은 없다. 시스템은 계속 켜져서 답한다.
- **분할 내성(P)** — 노드 사이에서 임의 개수의 메시지가 유실·지연돼도 보장을 유지한다. 분할은 클러스터를 서로 통신할 수 없는 그룹들로 가른다.
- **불가능성의 핵심**: 분할 상태에서 양쪽 노드가 같은 키에 대한 쓰기와 읽기를 각각 받는다. 일관성을 지키려면 분할을 넘어 조율해야 하고(메시지가 안 가니 불가능), 그래서 막거나 오류를 내거나(A 포기), 로컬 상태로 답해야 한다(C 포기). 즉 분할 중에는 CP 아니면 AP다.

## 왜 중요한가

- **분할은 필연적이다**: 스위치 고장, 케이블 절단, 타임아웃을 넘는 GC 멈춤, 클라우드 AZ 격리. 머신을 넘나드는 시스템에 P는 선택이 아니다. 그래서 실무자들은 "셋 중 P는 필수, 선택은 C 대 A"라고 말한다.
- **모든 저장소의 계약을 규정한다**: etcd와 ZooKeeper는 CP(소수 측이 쓰기 거부), Cassandra와 Dynamo 계열은 AP(전 측이 쓰기 수락 후 나중에 조정). 저장소가 어느 쪽인지 알면 장애 동작을 예측할 수 있다.
- **일관성은 지연 비용이다**: 선형화 읽기·쓰기에는 정족수(quorum) 왕복(Raft/Paxos)이 필요하다. AP 읽기는 로컬이라 빠르다. C 대 A 선택은 지연 대 정확성 선택이며 p99에서 보인다.
- **사업 의미가 정한다**: 이중 지불되는 원장은 무가치(C 필요), 분할 때 오류 내는 장바구니는 매출 손실(A 필요). CAP는 공학을 넘어 제품 논의를 강제한다.

## 동작 원리

### Gilbert–Lynch 증명 직관

```
분할:  [노드 A]  ✕ ✕ ✕  [노드 B]   (메시지 차단)
클라이언트 1 → A: WRITE x=1
클라이언트 2 → B: READ x  → ??? (1을 알려면 분할을 넘어야 함. 낡은 0은 C 위반, 오류/타임아웃은 A 위반)
```

- Brewer가 추측했고(PODC 2000 기조), Gilbert와 Lynch가 비동기 네트워크에서 증명했다(2002). 분할 하에서 안전성(원자적 일관성)과 활성(가용성)을 동시에 주는 알고리즘은 없다.
- 증명의 핵심은 *비동기성*이다. 느린 노드와 죽거나 분할된 노드를 구분할 수 없어서 "충분히 기다리기"로는 딜레마가 풀리지 않는다.

### 실전의 CP 대 AP

| 선택 | 분할 중 동작 | 예 | 조정 |
|---|---|---|---|
| CP | 소수 측이 오류/차단, 다수 측이 선형화 유지 | etcd, ZooKeeper, Consul (Raft), HBase, MongoDB (primary) | 불필요 — 하나의 진실 유지 |
| AP | 전 측이 응답, 값은 갈라짐 | Cassandra, DynamoDB (일부 모드), Riak, CouchDB | 반엔트로피: 벡터 시계, CRDT, last-write-wins, read repair |
| "CA" | 단일 노드나 완전 신뢰 네트워크에서만 가능 | 단일 사이트 RDBMS | 해당 없음 — 분할이 오면 CA는 불가능 |

- **정족수 산술**: 복제 N개에서 R + W > N이면 읽기-쓰기 겹침(CP 쪽 설정), R + W ≤ N이면 오래됨을 감수한 가용성(AP 쪽). 조정 가능 일관성(Cassandra ONE/QUORUM/ALL)은 말 그대로 CAP 슬라이더다.
- **PACELC 확장**(Abadi, 2012): "분할이면 A 아니면 C, 평소(E)에는 지연(L) 아니면 일관성(C)." 분할이 없어도 동기 복제는 지연과 일관성을 맞바꾼다. 선택은 완전히 사라지지 않는다.

### AP 조정 장치

- **벡터 시계 / 버전 벡터**: 인과율을 추적해 동시 쓰기를 조용히 잃지 않고 감지한다(Dynamo 논문, 2007).
- **CRDT**(충돌 없는 복제 자료구조): 병합이 수학적으로 수렴하는 구조(카운터, 집합, 맵) — 애플리케이션 충돌 코드 없이 AP를 낸다.
- **Read repair와 hinted handoff**: 치유 후 복제본을 수렴시키는 백그라운드 장치(Cassandra). 시스템은 *결과적 일관성* — C를 잠시 포기했다가 시간이 지나 회복한다.

## 흔한 함정

1. **"우리는 CA를 택했다"**: AZ·리전을 넘나들면서 CA를 주장하기. 첫 진짜 분할에서 틀렸음이 드러난다 — 보통 조정 장치 없는 split-brain 쓰기로 나타난다.
2. **CAP 일관성과 ACID 혼동**: CAP-C는 단일 레지스터의 선형화 가능성, ACID 직렬화 가능성은 다중 연산 트랜잭션 이야기다. 단일 노드 ACID와 노드 간 AP는 공존할 수 있다.
3. **선택을 전역으로 취급**: 데이터마다 원하는 글자가 다르다 — 인증 세션은 AP(낡은 세션 감내), 결제는 CP(이중 지불 불가). 회사당 독단이 아니라 데이터셋별 조율이 낫다.
4. **지연 절반(ELC) 무시**: 글로벌 저지연 읽기 경로에 선형화를 요구했다가 모든 읽기가 리전 간 왕복을 치르는 것을 뒤늦게 발견한다. CP 데이터는 쓰는 쪽 가까이 두거나 인과적/결과적 읽기로 완화한다.
5. **기본 충돌 정책 last-write-wins**: 물리 시계 LWW는 시계 틀어짐 아래 동시 쓰기를 조용히 버린다. 사용자가 직접 고치는 데이터엔 CRDT나 명시적 애플리케이션 병합을 쓴다.
6. **분할 훈련 없음**: 진짜 분할을 본 적 없는 장애조치 로직은 필요할 때 정확히 실패한다. 방화벽 차단 게임 데이, `iptables` 카오스로 소수 측 동작을 미리 시험한다.

## 관련 개념

- [[concepts/computer-science/distributed-consensus|분산 합의]] (Raft/Paxos: CP 시스템의 합의 방식)
- [[concepts/computer-science/database-transactions|데이터베이스 트랜잭션]] (격리 수준 대 분산 일관성)
- [[concepts/computer-science/tcp-ip|TCP/IP]] (바탕의 타임아웃과 장애 감지)

## 참고 문헌

- Brewer, "Towards Robust Distributed Systems" (PODC 2000 기조 강연)
- Gilbert & Lynch, "Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services" (ACM SIGACT News, 2002)
- Abadi, "Consistency Tradeoffs in Modern Distributed Database System Design" (PACELC, IEEE Computer, 2012)
- DeCandia 외, "Dynamo: Amazon's Highly Available Key-Value Store" (SOSP 2007)
- Kleppmann — *Designing Data-Intensive Applications*, 5장/9장 (복제, 일관성 모델)
