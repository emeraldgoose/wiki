---
title: 정렬 알고리즘 (Sorting Algorithms)
description: "세미나 수준 개념: 비교·비비교 정렬, 복잡도 비교표, 안정성, 선택 기준"
tags: [concept, computer-science, algorithms, sorting, ko]
locale: ko
published: 2026-09-06
---

# 정렬 알고리즘 (Sorting Algorithms)

[English version](/en/concepts/computer-science/sorting-algorithms.md)

> 정렬은 항목을 순서대로 배열하는 가장 많이 연구된 알고리즘 분야다. 비교 정렬은 최악의 경우 Ω(n log n)이 들고, 비비교 정렬은 키의 구조를 이용해 O(n)에 도달한다.

## 정의

**정렬 알고리즘**은 수열을 키 기준으로 오름차순(또는 내림차순)이 되도록 재배열한다. 두 계열이 있다:

- **비교 정렬**: 쌍별 비교(`<`, `>`)만으로 순서를 정한다. 병합 정렬, 퀵소트, 힙 정렬, 삽입 정렬, 버블 정렬이 여기에 속한다.
- **비비교 정렬**: 키의 구조(범위 내 정수, 자릿수, 비트)를 이용한다. 계수 정렬, 기수 정렬, 버킷 정렬이 여기에 속하며 n log n 장벽을 넘을 수 있다.

**안정(stable)** 정렬은 같은 키의 원래 상대 순서를 유지한다. 한 키로 정렬한 뒤 다른 키로 정렬할 때 중요하다.

## 왜 중요한가

- **도처에 존재**: 검색 인덱스, DB의 `ORDER BY`, 피드 랭킹, 모든 표준 라이브러리의 `sort()`가 정렬 위에 있다.
- **복잡도 이론의 구체적 사례**: 비교 정렬의 Ω(n log n) 하한은 증명 가능한 한계와의 첫 만남인 경우가 많다.
- **설계 패턴의 보고**: 분할 정복(병합·퀵), 힙 자료구조(힙 정렬), 점진적 불변식(삽입 정렬)은 알고리즘 설계 전반에 재등장한다.
- **성능 절벽**: 병합 정렬(O(n log n)을 써야 할 곳에 버블 정렬(O(n²))을 쓰는 것은 규모에서 터지는 전형적 실수다.

## 동작 원리

### 복잡도 비교표

| 알고리즘 | 최선 | 평균 | 최악 | 공간 | 안정 | 비고 |
|----------|------|------|------|------|------|------|
| 버블 정렬 | O(n) | O(n²) | O(n²) | O(1) | 예 | 교육용, 실전 사용 금지 |
| 삽입 정렬 | O(n) | O(n²) | O(n²) | O(1) | 예 | 작은/거의 정렬된 입력에 빠름 |
| 선택 정렬 | O(n²) | O(n²) | O(n²) | O(1) | 아니오 | 교환 횟수 최소 (O(n)) |
| 병합 정렬 | O(n log n) | O(n log n) | O(n log n) | O(n) | 예 | 예측 가능, 분할 정복의 정석 |
| 퀵소트 | O(n log n) | O(n log n) | O(n²) | O(log n) | 아니오 | 좋은 피벗이면 실제 최속, 라이브러리 기본(introsort) |
| 힙 정렬 | O(n log n) | O(n log n) | O(n log n) | O(1) | 아니오 | 제자리 + 보장된 상한 |
| 계수 정렬 | O(n+k) | O(n+k) | O(n+k) | O(k) | 예 | 범위 k 내 정수 키 |
| 기수 정렬 | O(d·n) | O(d·n) | O(d·n) | O(n+k) | 예 | d 자릿수, 고정 폭 키에 강함 |
| 버킷 정렬 | O(n+k) | O(n+k) | O(n²) | O(n) | 예 | 균등 분포 키 |

k = 키 범위, d = 자릿수.

### n log n 하한 (개요)

비교 정렬의 결정 과정은 이진 결정 트리다. 각 비교마다 두 갈래로 나뉘고, n!개의 가능한 순열마다 리프가 하나씩 필요하다. 리프가 n!개인 이진 트리의 높이는 Stirling 근사에 의해 최소 log₂(n!) = Θ(n log n)이다. 따라서 **어떤 비교 정렬도 최악 비교 횟수에서 Ω(n log n)을 넘을 수 없으며**, 병합·힙 정렬은 점근적으로 최적이다.

### 주요 알고리즘의 동작

**퀵소트 (분할 정복).** 피벗을 골라 작은 원소는 왼쪽, 큰 원소는 오른쪽으로 분할한 뒤 양쪽을 재귀 정렬한다:

```python
def quicksort(xs):
    if len(xs) <= 1:
        return xs
    pivot = xs[len(xs) // 2]
    left = [x for x in xs if x < pivot]
    mid = [x for x in xs if x == pivot]
    right = [x for x in xs if x > pivot]
    return quicksort(left) + mid + quicksort(right)
```

평균 O(n log n), 피벗이 항상 극단이면(예: 정렬된 입력 + 첫 원소 피벗) 최악 O(n²). 실전 라이브러리는 최악을 피하려고 **introsort**(퀵 + 힙 폴백)와 median-of-three 피벗을 쓴다.

**병합 정렬 (분할 정복).** 절반으로 나누어 각 절반을 정렬한 뒤 정렬된 두 런을 선형 시간에 병합한다. 항상 O(n log n)이지만 O(n) 추가 공간이 필요하다.

**힙 정렬.** O(n)에 최대 힙을 만들고 최대값을 반복 추출한다(회당 O(log n), n회). 제자리·보장된 O(n log n)이지만 캐시 지역성이 나빠 실제로는 퀵소트보다 느리다.

**계수 정렬 (비비교).** `[0, k)` 정수에 대해 빈도를 센 뒤 순서대로 다시 쓴다:

```python
def counting_sort(xs, k):
    counts = [0] * k
    for x in xs:
        counts[x] += 1
    out = []
    for value, c in enumerate(counts):
        out.extend([value] * c)
    return out  # 시간 O(n + k)
```

### 선택 기준

1. **범용**: 표준 라이브러리 정렬을 신뢰할 것 (보통 Timsort·introsort 하이브리드).
2. **거의 정렬됨 또는 tiny (n < ~20)**: 삽입 정렬.
3. **보장된 상한 + O(1) 공간**: 힙 정렬.
4. **안정성 + 보장**: 병합 정렬.
5. **정수 키·작은 범위**: 계수/기수 정렬.

## 흔한 함정

- **"n이 작다"며 측정 없이 O(n²) 정렬 사용.** n은 자란다. 오늘의 100행이 내년의 1,000만 행이다. 기본은 라이브러리 정렬이다.
- **퀵소트 맹신.** 순진한 피벗 + 적대적·정렬된 입력은 O(n²)로 추락하며, 이는 실제 DoS 벡터다 (랜덤 피벗·introsort의 존재 이유).
- **안정성 무시.** 가입일 순으로 정렬한 뒤 국가별 정렬을 불안정 정렬로 하면 첫 순서가 깨진다. 안정 정렬로 뒤에서부터 체인하거나 튜플 키로 한 번에 정렬하라.
- **불필요한 정렬.** 상위 k개는 힙이면 충분(O(n log k)), 포함 여부만이면 [[concepts/computer-science/hash-tables|해시 테이블]](O(1))이면 된다.
- **k가 큰 데 계수/기수 정렬.** k가 n 대비 작을 때만 O(n + k)이 선형이다. 32비트 키 범위에는 계수 정렬이 불가능하다.

## 관련 개념

- [[concepts/computer-science/big-o-notation|빅오 표기법]] — 정렬 비교의 어휘
- [[concepts/computer-science/trees|트리]] — 힙 정렬은 이진 힙 위에서 돌고, BST는 중위 순회로 정렬한다
- [[concepts/computer-science/hash-tables|해시 테이블]] — 순서가 필요 없을 때의 O(1) 대안

## 참고 자료

- Cormen et al. — *Introduction to Algorithms* (CLRS), Ch. 6–8 (힙 정렬, 퀵소트, 선형 시간 정렬).
- Sedgewick & Wayne — *Algorithms*, 4th ed., Ch. 2 (정렬).
- Tim Peters — Timsort 설명 (CPython의 병합/삽입 하이브리드 정렬).
