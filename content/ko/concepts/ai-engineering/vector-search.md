---
title: 벡터 검색 (Vector Search)
description: en/concepts/ai-engineering/vector-search.md 한국어 번역 요약
tags: [concept, ai-engineering, vector-search, ko]
locale: ko
---

# 벡터 검색 (Vector Search)

**원전**: Netflix Embedding Store, Databricks monitoring, Uber Hudi, PonderPounce, JIT-Agent

## 문제 정의
질의 벡터 q ∈ ℝ^d가 주어졌을 때, 데이터셋 X ∈ ℝ^(N×d)에서 상위 K개 최근접 이웃을 찾는다. N은 수백만~수십억 규모다.

## 알고리즘 계열

### 그래프 기반 (HNSW, NSW)
- **NSW**: Navigable Small World 그래프, 탐욕적 탐색(greedy walk)
- **HNSW**: 계층적 NSW, 다층 구조 (고속 경로 + 국소 탐색)
- **복잡도**: 탐색 O(log N), 구축 O(N log N)
- **메모리**: 큼 (그래프 간선 + 벡터를 RAM에 보관)

### 디스크 기반 (DiskANN, SPANN, FreshDiskANN)
- **핵심 아이디어**: 그래프는 RAM에, 벡터는 SSD에 둔다
- **PQ (Product Quantization)**: 벡터를 압축해 RAM에 두고, SSD에서 정교화(refine)한다
- **복잡도**: 탐색 O(log N), HNSW 대비 RAM 약 10분의 1
- **적합**: 일반 하드웨어에서의 10억 규모

### 양자화(Quantization)
| 방법 | 압축률 | 재현율 손실 | 탐색 속도 |
|--------|-------------|-------------|--------------|
| None (FP32) | 1× | 0% | 기준 |
| FP16 / BF16 | 2× | ~0% | 2× |
| PQ (8-bit) | 4× | 1-3% | 4-8× |
| PQ (4-bit) | 8× | 3-8% | 8-16× |
| Scalar Quantization | 4× | 0.5-2% | 4× |

### 필터링 + 하이브리드
- 메타데이터로 사전 필터링(카테고리, 날짜, 테넌트) → 후보 집합 축소
- 정확한 제약 조건은 사후 필터링

## 프로덕션 아키텍처 (원전에서 차용)

### Netflix Embedding Store
- 분리된 스토어: 학습과 서빙에서 동일한 임베딩 사용
- 크로스 모달: CLIP (아트워크), SeqCLIP/MediaFM (비디오)
- crop/resize에 불변 → 모든 캔버스에 단일 모델

### Databricks Hydra
- 고카디널리티 메트릭 → Delta 테이블
- Grafana용 PromQL-to-SQL (순수 벡터 검색이 아님)

### Uber Hudi
- 메타데이터 테이블의 컬럼 통계 → 파일 프루닝
- 벡터 검색은 아니지만 유사한 원칙: 메타데이터 우선, 데이터는 그 다음

## 세미나 수준 설계 결정

### 규모 → 인덱스 선택
| 규모 | 벡터 수 | 권장 |
|-------|---------|-------------|
| < 1M | 소규모 | HNSW (RAM) |
| 1M - 100M | 중규모 | HNSW + PQ 또는 DiskANN |
| 100M - 1B+ | 대규모 | DiskANN / SPANN + PQ |

### 지연 시간 요구사항
| 지연 예산 | 접근법 |
|----------------|----------|
| < 10ms (p99) | HNSW (RAM) |
| < 50ms (p99) | DiskANN + PQ |
| < 200ms (p99) | DiskANN + 공격적 PQ |

### 업데이트 빈도
| 업데이트율 | 전략 |
|-------------|----------|
| 정적 / 배치 | 주기적으로 인덱스 리빌드 |
| 낮음 (< 1%/day) | 증분 HNSW 삽입 |
| 높음 (> 1%/hour) | DiskANN (증분에 강함) + 병합 |

## 핵심 세미나 포인트

1. **HNSW = RAM의 정석**, **DiskANN = 디스크의 정석**이다
2. **PQ (Product Quantization)**는 10억 규모의 필수 요소다 (4-8× 압축)
3. 프로덕션 품질에는 **하이브리드 검색**(벡터 + 키워드 + 필터)이 필수다
4. 업데이트율에 따라 **인덱스 리빌드 vs 증분**을 선택한다
5. **관측 가능성**: recall@K, 지연 p50/p99, 인덱스 크기, 빌드 시간

## 관련 원전
- `sources/articles/netflix-techblog.md` (Embedding Store)
- `concepts/machine-learning/embedding.md` (embedding types)
- `concepts/ai-engineering/rag.md` (retrieval in RAG)

## 관련 가이드
- `guides/ai-engineering/vector-search.md`
