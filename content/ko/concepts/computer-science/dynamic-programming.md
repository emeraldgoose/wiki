---
title: 동적 프로그래밍 (Dynamic Programming)
description: "세미나 수준 개념: 겹치는 부분문제, 최적 부분구조, 메모이제이션 대 타뷸레이션"
tags: [concept, computer-science, algorithms, dynamic-programming, optimization, ko]
locale: ko
published: 2026-09-06
---

# 동적 프로그래밍 (Dynamic Programming)

[English version](/en/concepts/computer-science/dynamic-programming.md)

> 동적 프로그래밍은 겹치는 부분문제로 문제를 나눠 푼다. 서로 다른 부분문제마다 한 번씩만 풀어 저장하고 재사용함으로써 지수 전수 탐색을 다항 시간으로 바꾼다.

## 정의

**동적 프로그래밍(DP)**은 두 성질을 가진 문제에 쓰는 기법이다:

1. **겹치는 부분문제**: 순진한 재귀가 같은 부분문제를 반복해서 푼다 (부분문제가 서로 겹치지 않는 분할 정복과 반대).
2. **최적 부분구조**: 최적해가 부분문제의 최적해들로 구성된다 (예: C를 거쳐 D로 가는 최단 경로는 C까지의 최단 경로를 포함한다).

두 가지 구현 스타일:

- **메모이제이션 (top-down)**: 자연스러운 재귀를 쓰고 결과를 테이블(보통 [[concepts/computer-science/hash-tables|해시 테이블]]이나 배열)에 캐시하여 각 부분문제를 한 번씩만 계산.
- **타뷸레이션 (bottom-up)**: 기저 사례부터 답까지 테이블을 반복적으로 채움 — 재귀 없음, 보통 메모리 오버헤드 감소.

## 왜 중요한가

- **지수 → 다항**: 순진한 피보나치는 O(2ⁿ), 메모이제이션하면 O(n). 같은 도약이 서열 정렬, 음성 인식, 자원 할당을 떠받친다.
- **인터뷰 핵심**: 배낭, 동전 거스름, 최장 증가/공통 부분수열, 편집 거리가 DP 정석 문제다.
- **실제 시스템**: Unix `diff`(최장 공통 부분수열), 통신의 Viterbi 디코딩, 라우팅의 Floyd-Warshall·벨만-포드([[concepts/computer-science/graphs|그래프]] 참조), 작업 스케줄링, 재고 최적화.
- **사고 도구**: "상태를 정의하고 점화식을 쓰라"는 훈련은 강화학습으로 이어진다 (Bellman 방정식은 MDP 위의 DP다).

## 동작 원리

### 정석 예제: 피보나치

순진한 재귀는 같은 값을 지수 번으로 재계산한다 (`fib(5)`는 `fib(3)`을 두 번, `fib(2)`를 세 번 호출 …):

```python
# O(2^n) — 부분문제 재계산
def fib_naive(n):
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)
```

메모이제이션 (top-down) — 각 `fib(k)`를 한 번씩만 계산:

```python
# 시간 O(n), 공간 O(n)
def fib_memo(n, memo=None):
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]
```

타뷸레이션 (bottom-up) — 기저부터 쌓기:

```python
# 시간 O(n), 공간 O(1) (직전 두 값만 필요)
def fib_tab(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

### DP 레시피

1. **상태 정의**: 부분문제 파라미터의 의미는? (예: `dp[i][w]` = 앞의 `i`개 물건·용량 `w`에서의 최적값).
2. **점화식 작성**: 답이 더 작은 답들로 어떻게 조합되는가? (예: `dp[i][w] = max(dp[i-1][w], dp[i-1][w-w_i] + v_i)`).
3. **기저 사례 설정**: `dp[0][*] = dp[*][0] = 0`.
4. **계산 순서 선택**: 의존성이 먼저 계산되도록 반복(bottom-up)하거나 재귀+메모이즈.
5. **복원 (선택)**: 테이블을 역추적하여 최적값뿐 아니라 실제 선택을 복원.

### 고전 문제표

| 문제 | 상태 | 점화식 아이디어 | 복잡도 |
|------|------|-----------------|--------|
| 0/1 배낭 | `dp[i][w]` | 물건 i를 넣거나 빼거나 | O(n·W) |
| 동전 거스름 (최소 개수) | `dp[x]` | 동전 c에 대해 `1 + min(dp[x-c])` | O(금액·동전수) |
| 최장 공통 부분수열 | `dp[i][j]` | 일치 → `dp[i-1][j-1]+1`, 불일치 → 이웃 중 최대 | O(n·m) |
| 편집 거리 | `dp[i][j]` | 삽입/삭제/교체의 최소 | O(n·m) |
| 최장 증가 부분수열 | `dp[i]` | `a[j] < a[i]`인 j에 대해 `1 + max(dp[j])` | O(n²), 최적화 O(n log n) |
| 행렬 체인 곱셈 | `dp[i][j]` | i와 j 사이 최적 분할점 k | O(n³) |

### 미니 예제: 동전 거스름

동전 `[1, 3, 4]`, 금액 6. `dp[x]` = 금액 x의 최소 동전 수:

```
dp[0]=0
dp[1]=1 (1)   dp[2]=2 (1+1)   dp[3]=1 (3)
dp[4]=1 (4)   dp[5]=2 (4+1)   dp[6]=2 (3+3)
```

답은 `dp[6] = 2` (3+3). 탐욕(항상 4 선택)은 4+1+1 = 3개를 내어 틀리며, 바로 그 때문에 DP가 필요하다.

## 흔한 함정

- **최적 부분구조 없는 곳에 DP.** 최적해가 최적 부분해들로 구성되지 않으면(예: 최장 *단순* 경로 — 최적 경로의 부분경로가 최적이 아닐 수 있음) DP는 오답을 낸다. 먼저 성질을 확인하라.
- **겹치지 않는 부분문제에 DP.** 병합 정렬의 부분문제는 서로 겹치지 않으므로 메모이제이션이 무의미하다. DP의 승리는 재사용에서 온다.
- **상태 차원 부족.** 배낭은 물건 인덱스와 남은 용량 둘 다 필요하며, 차원을 빼면 조용히 탐욕이 되어 틀린다. 답이 이상하면 빠진 상태 차원을 먼저 의심하라.
- **타뷸레이션 순서 실수.** `dp[i]`가 `dp[i-1]`에 의존하면 i 오름차순으로 반복해야 하며, 역순은 낡은 값을 읽는다. 2차원 테이블은 현재 행을 읽는지 확인하고 주의 깊게 반복하거나 복사하라.
- **메모이제이션 재귀 깊이.** n = 10⁵의 top-down DP는 10⁵ 깊이로 재귀한다 — Python 기본 한도는 1,000이다. 타뷸레이션으로 바꾸거나 명시적 스택을 써라.
- **유사 다항식 혼동.** O(n·W) 배낭은 *값*에 대해 다항이지만 입력 *비트 수*에 대해 지수다 — 진짜 다항이 아닌 유사 다항(pseudo-polynomial)이며, W가 크면 무너진다.
- **복원 망각.** 많은 과제는 값뿐 아니라 선택(어떤 물건? 어떤 정렬?)이 필요하다 — 부모 포인터를 남기거나 역추적하라.

## 관련 개념

- [[concepts/computer-science/big-o-notation|빅오 표기법]] — 지수→다항의 대가, 유사 다항의 미묘함
- [[concepts/computer-science/graphs|그래프]] — 경로 위의 DP인 벨만-포드와 플로이드-워셜, 가장 단순한 DP인 DAG 최단 경로
- [[concepts/computer-science/hash-tables|해시 테이블]] — 메모이제이션 저장소
- [[concepts/computer-science/trees|트리]] — 겹침 대 독립 부분문제를 보여주는 재귀 트리

## 참고 자료

- Cormen et al. — *Introduction to Algorithms* (CLRS), Ch. 14–15 (DP: 막대 자르기, 행렬 체인, LCS).
- Bellman — *Dynamic Programming* (1957, 원전).
- Kleinberg & Tardos — *Algorithm Design*, Ch. 6 (DP 설계 패턴).
