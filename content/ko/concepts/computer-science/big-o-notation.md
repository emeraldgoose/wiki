---
title: 빅오 표기법 (Big-O Notation)
description: "세미나 수준 개념: 점근 복잡도 분석, Big-O, Big-Omega, Big-Theta와 주요 복잡도 클래스"
tags: [concept, computer-science, algorithms, complexity, big-o, ko]
locale: ko
published: 2026-09-06
---

# 빅오 표기법 (Big-O Notation)

[English version](/en/concepts/computer-science/big-o-notation.md)

> 빅오 표기법은 입력 크기가 커질 때 알고리즘의 실행 시간이나 메모리 사용량이 어떻게 증가하는지를 나타내는 점근적 상한으로, 하드웨어와 무관하게 알고리즘을 비교할 수 있게 한다.

## 정의

빅오 표기법은 함수의 **점근적 상한(asymptotic upper bound)** 증가율을 나타낸다. 양의 상수 `c`와 `n0`가 존재하여 모든 `n >= n0`에 대해 `f(n) <= c * g(n)`이면 `f(n) = O(g(n))`이라 한다. 쉽게 말하면, 입력이 충분히 크면 비용이 상수 배율을 제외하고 `g(n)`보다 빠르게 증가하지 않는다는 뜻이다.

관련 표기법은 다음과 같다:

| 표기법 | 의미 | 비유 |
|--------|------|------|
| `O(g(n))` (Big-O) | 점근적 **상한** (최악 경우) | `<=` |
| `Ω(g(n))` (Big-Omega) | 점근적 **하한** (최선 경우) | `>=` |
| `Θ(g(n))` (Big-Theta) | **긴밀한** 상·하한 | `==` |
| `o(g(n))` (little-o) | 엄격히 느리게 증가하는 상한 | `<` |

실무에서 "퀵소트의 복잡도는 O(n log n)"이라 하면 평균 경우를 말하며, 최악 경우는 O(n²)이다.

## 왜 중요한가

- **알고리즘 선택**: n = 10⁶에서는 언어·CPU와 무관하게 O(n log n) 정렬이 O(n²) 정렬을 압도한다. 규모가 커지면 상수 차이로 복잡도 클래스 격차를 뒤집을 수 없다.
- **설계 인터뷰와 코드 리뷰**: 복잡도 분석은 설계의 확장 가능성을 논증하는 공통 언어다.
- **용량 계획**: 어떤 API가 팔로워 수에 대해 O(n²)이라면, 어떤 고객이 첫 장애를 유발할지 정확히 예측할 수 있다.
- **소통**: 하드웨어·컴파일러·언어를 추상화하므로 두 엔지니어가 접근법을 정밀하게 비교할 수 있다.

## 동작 원리

### 주요 복잡도 클래스

증가가 느린 순에서 빠른 순으로 나열하면 다음과 같다:

| 클래스 | 이름 | 예시 |
|--------|------|------|
| O(1) | 상수 | 해시 테이블 조회, 배열 인덱스 접근 |
| O(log n) | 로그 | 이진 탐색, 균형 트리 연산 |
| O(n) | 선형 | 배열 1회 순회 |
| O(n log n) | 선형로그 | 병합 정렬, 힙 정렬 등 효율적 정렬 |
| O(n²) | 2차 | 버블 정렬, 쌍에 대한 단순 중첩 루프 |
| O(n³) | 3차 | 단순 행렬 곱셈 |
| O(2ⁿ) | 지수 | 단순 재귀 피보나치, 부분집합 전수 탐색 |
| O(n!) | 팩토리얼 | 순열 전수 탐색 외판원 문제 |

### 예제

**O(1) — 상수.** `arr[i]` 접근은 배열 크기가 10이든 1,000만이든 비용이 같다.

**O(n) — 선형.** 한 번의 순회로 최댓값 찾기:

```python
def find_max(xs):
    best = xs[0]
    for x in xs[1:]:      # n - 1회 반복
        if x > best:
            best = x
    return best           # 시간 O(n), 추가 공간 O(1)
```

**O(log n) — 로그.** 이진 탐색은 매 단계 탐색 공간을 절반으로 줄이므로 n = 10⁶에도 약 20번 비교면 충분하다 (2²⁰ ≈ 10⁶).

**O(n²) — 2차.** 모든 쌍 검사:

```python
def has_duplicate(xs):
    for i in range(len(xs)):
        for j in range(i + 1, len(xs)):  # 약 n²/2번 비교
            if xs[i] == xs[j]:
                return True
    return False
```

**상각 분석(amortized analysis).** 동적 배열 append는 상각 O(1)이다. 대부분은 O(1)이고 가끔 O(n) 재할당이 발생하지만, 그 비용이 많은 append에 분산되기 때문이다.

### 분석 요령

1. **상수 제거**: O(2n) → O(n). 상수는 하드웨어에 따라 달라진다.
2. **낮은 차수 항 제거**: O(n² + n) → O(n²). n이 커지면 최고차 항이 지배한다.
3. **중첩 루프는 곱, 순차 단계는 합**: n 루프 2중 중첩 → O(n²), 연속된 n 루프 2개 → O(n).
4. **시간과 공간을 분리해서 기술**: 제자리 뒤집기처럼 시간 O(n)·공간 O(1)인 알고리즘이 있다.

## 흔한 함정

- **최악과 평균의 혼동.** 해시 테이블 조회는 평균 O(1)이지만 최악 O(n)(모든 키 충돌)이다. 퀵소트는 평균 O(n log n), 최악 O(n²)이다. 어느 경우인지 항상 밝혀야 한다.
- **숨은 상수 무시.** n이 작으면 상수가 작은 O(n²) 알고리즘이 상수가 큰 O(n log n)보다 빠를 수 있다. 복잡도는 점근적으로만 우세하며, 그래서 병합 정렬 구현도 작은 부분 배열에는 삽입 정렬을 쓴다.
- **n의 기준 불일치.** n이 "비트 수"인지 "수치"인지에 따라 O(n)의 의미가 달라진다. 소수 판별의 trial division은 수치 기준 O(√n)이지만 비트 수 기준 지수 시간이므로 다항 시간 소수 판별법이 아니다.
- **공간 복잡도 망각.** 메모이제이션처럼 시간 O(n)·공간 O(n)인 해법은 메모리 제약 하에서 못 쓸 수 있으며, 시간 O(n)·공간 O(1)인 대안이 필요할 수 있다.
- **최선 경우로 지연시간 판단.** 사용자는 꼬리 지연시간을 체감하므로, 최선이 아니라 최악(또는 상각 최악) 기준으로 분석해야 한다.

## 관련 개념

- [[concepts/computer-science/sorting-algorithms|정렬 알고리즘]] — O(n log n) 대 O(n²)가 실제 성능을 가르는 영역
- [[concepts/computer-science/hash-tables|해시 테이블]] — 평균 O(1), 최악 O(n) 조회
- [[concepts/computer-science/dynamic-programming|동적 프로그래밍]] — 공간을 써서 지수 시간을 다항 시간으로 바꾸는 기법

## 참고 자료

- Cormen, Leiserson, Rivest, Stein — *Introduction to Algorithms* (CLRS), Ch. 3: Growth of Functions.
- Knuth — *The Art of Computer Programming*, Vol. 1 (점근 분석의 기초).
- Sedgewick & Wayne — *Algorithms*, 4th ed., Ch. 1.4: Analysis of Algorithms.
