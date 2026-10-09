---
title: 그래프 (Graphs)
description: "세미나 수준 개념: 그래프 표현, BFS, DFS, 최단 경로와 고전 그래프 알고리즘"
tags: [concept, computer-science, data-structures, graphs, bfs, dfs, shortest-path, ko]
locale: ko
published: 2026-09-06
---

# 그래프 (Graphs)

> 그래프는 개체를 정점, 관계를 간선으로 모델링한다. 너비 우선·깊이 우선 탐색 두 가지 순회가 네트워크·지도·의존성 시스템의 최단 경로, 연결성, 위상 순서, 사이클 검출을 풀어낸다.

## 정의

**그래프** G = (V, E)는 **정점**(노드)과 **간선**(정점 쌍 사이의 링크)으로 구성된다. 핵심 구분:

- **방향 vs. 무방향**: 간선에 방향이 있다(팔로우 → 팔로이, 의존 → 피의존) 또는 없다(친구, 도로).
- **가중 vs. 비가중**: 간선에 비용(거리, 지연, 가격)이 있다 또는 균일하다.
- **순환 vs. 비순환**: **DAG**(방향성 비순환 그래프)는 방향 간선은 있지만 방향성 사이클은 없다 — 빌드 의존성, 작업 스케줄, 버전 히스토리의 형태다.
- **연결 vs. 비연결**: 모든 정점 쌍 사이에 경로가 존재하는지 여부.
- **차수**: 정점에 접속한 간선 수 (방향 그래프에서는 진입/진출 차수).

## 왜 중요한가

- **세상은 그래프다**: 소셜 네트워크, 도로 지도, 웹 링크 그래프, 패키지 의존성, 회로 배치, ML 계산 그래프.
- **두 순회, 수십 응용**: BFS는 비가중 최단 경로를, DFS는 위상 순서·사이클 검출·연결 요소를 제공한다.
- **라우팅과 계획**: 최단 경로 알고리즘(다익스트라, 벨만-포드, A\*)이 내비게이션·네트워크 라우팅·물류를 돌린다.
- **스케줄링**: DAG 위의 위상 정렬이 빌드, 선수과목, 작업 파이프라인의 순서를 정한다.

## 동작 원리

### 표현 방법

| 표현 | 공간 | 간선 조회 | 이웃 순회 | 적합한 경우 |
|------|------|-----------|-----------|--------------|
| 인접 리스트 | O(V + E) | O(차수) | O(차수) | 희소 그래프(대부분의 실제 그래프), 기본 선택 |
| 인접 행렬 | O(V²) | O(1) | O(V) | 밀집 그래프, 간선 존재 검사의 고속화 |
| 간선 리스트 | O(E) | O(E) | O(E) | 크루스칼, 단순 직렬화 |

```python
# 인접 리스트 (방향, 비가중)
graph = {
    "a": ["b", "c"],
    "b": ["d"],
    "c": ["d"],
    "d": [],
}
```

### BFS 대 DFS

```python
from collections import deque

def bfs(graph, start):
    seen = {start}
    queue = deque([start])
    order = []
    while queue:
        v = queue.popleft()          # FIFO → 레벨별 탐색
        order.append(v)
        for w in graph[v]:
            if w not in seen:
                seen.add(w)
                queue.append(w)
    return order                     # O(V + E)

def dfs(graph, start, seen=None, order=None):
    if seen is None:
        seen, order = set(), []
    seen.add(start)
    order.append(start)
    for w in graph[start]:           # LIFO (재귀) → 깊이 우선
        if w not in seen:
            dfs(graph, w, seen, order)
    return order                     # O(V + E)
```

| 측면 | BFS (큐) | DFS (스택/재귀) |
|------|----------|-----------------|
| 탐색 | 레벨별 | 한 경로를 끝까지 먼저 |
| 최단 경로 (비가중) | 예 | 아니오 |
| 메모리 | O(V), 프론티어가 넓을 수 있음 | O(V), 보통 더 얇음 |
| 대표 용도 | 최단 경로, 최근접 이웃, 이분 판정 | 위상 정렬, 사이클 검출, 컴포넌트 |

### 고전 알고리즘

| 문제 | 알고리즘 | 복잡도 | 비고 |
|------|----------|--------|------|
| 최단 경로, 비가중 | BFS | O(V + E) | 단일 출발점 |
| 최단 경로, 음수 없는 가중치 | 다익스트라 (이진 힙) | O((V + E) log V) | 음수 가중치에 실패 |
| 최단 경로, 음수 허용 | 벨만-포드 | O(V·E) | 음수 사이클 검출 |
| 휴리스틱 최단 경로 | A\* | 보통 O(b^d) | 다익스트라 + 휴리스틱, 게임 길 찾기 |
| 모든 쌍 | 플로이드-워셜 | O(V³) | 단순 DP, 작은 밀집 그래프 |
| 최소 신장 트리 | 크루스칼 / 프림 | O(E log E) / O((V+E) log V) | 전 정점을 최소 비용 연결 |
| 위상 순서 (DAG) | Kahn / DFS 종료 순서 | O(V + E) | 빌드 시스템, 스케줄러 |
| 강연결 요소 | Kosaraju / Tarjan | O(V + E) | 방향 그래프 군집 |

### 위상 정렬 예제

선수과목 `입문 → 알고리즘 → ML`에 대해 DFS 종료 순서(또는 Kahn의 진입차수 제거)는 유효한 수강 순서를 낸다. 사이클이 있으면(A는 B를, B는 A를 요구) 위상 순서는 존재하지 않으며, 그 사이클 자체가 진단이다(교착상태, 순환 의존성).

## 흔한 함정

- **음수 가중치에 다익스트라.** 음수 간선 하나가 탐욕 가정을 깨뜨린다. 벨만-포드를 쓰고 음수 사이클을 검사하라("최단"이 정의되지 않음).
- **방문 집합 망각.** 없으면 순환 그래프에서 무한 루프를 돌거나 공유 서브그래프를 반복 방문해 지수 폭발한다(DAG는 [[concepts/computer-science/trees|트리]]가 아니다 — 부모가 여러 명이다).
- **큰 그래프의 재귀 깊이.** 백만 노드 그래프의 재귀 DFS는 콜 스택 오버플로우를 낸다. 명시적 스택을 써라.
- **희소 그래프의 인접 행렬.** 백만 정점 소셜 그래프를 행렬로 하면 10¹²칸이 필요하다. 실제 희소 그래프는 항상 인접 리스트다.
- **비연결 그래프를 연결로 착각.** 순회는 항상 전 정점에 대해 반복하라(`for v in V: if unseen: search(v)`). 아니면 뒤쪽 컴포넌트를 조용히 놓친다.
- **BFS 순서와 가중 최단 경로 혼동.** BFS 레벨은 *간선 수*를 셀 뿐 비용이 아니다. 가중 그래프에서는 간선이 적어도 비용이 클 수 있다.

## 관련 개념

- [[concepts/computer-science/trees|트리]] — 연결 비순환 그래프이며 BFS/DFS는 둘 다 순회한다
- [[concepts/computer-science/dynamic-programming|동적 프로그래밍]] — 플로이드-워셜과 벨만-포드는 경로 위의 DP다
- [[concepts/computer-science/big-o-notation|빅오 표기법]] — O(V + E) 선형 시간 순회 분석

## 참고 자료

- Cormen et al. — *Introduction to Algorithms* (CLRS), Ch. 22–26 (그래프 알고리즘, MST, 최단 경로).
- Sedgewick & Wayne — *Algorithms*, 4th ed., Ch. 4 (그래프).
- Dijkstra — "A Note on Two Problems in Connexion with Graphs" (1959).
