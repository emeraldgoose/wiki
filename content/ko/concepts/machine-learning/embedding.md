---
title: 임베딩 (Embedding)
description: "세미나 수준 개념: 임베딩, 벡터 검색, 멀티모달 임베딩, Netflix Embedding Store"
tags: [concept, machine-learning, embedding, vector-search, multimodal, ko]
locale: ko
---

# 임베딩 (Embedding)

**출처**: Netflix MAPS(멀티모달 임베딩), GenRec(verbalization), Databricks 모니터링, Uber Hudi, PonderPounce

## 임베딩이란
의미적 유사성을 포착하는 밀집 벡터 표현. 이산 토큰/이미지를 연속 공간에 매핑하며, 거리 = 의미적 관련성이 된다.

## 종류

### 텍스트 임베딩
| 모델 | 차원 | 사용 사례 |
|-------|-----|----------|
| Word2Vec/GloVe | 300 | 고전적, 정적(static) |
| BERT | 768 | 문맥적, 양방향 |
| Sentence-BERT | 384/768 | 문장 유사도 |
| E5 / BGE | 1024 | 검색 최적화 |
| LLM 히든 스테이트 | 4096+ | 풍부함, 작업 적응적 |

### 이미지/비디오 임베딩 (Netflix MAPS에서)
- **CLIP**: 이미지-텍스트 공동 임베딩 (768차원)
- **SeqCLIP**: 비디오용 순차 프레임 처리
- **MediaFM**: 미디어 임베딩용 파운데이션 모델

### 멀티모달 (Netflix Embedding Store)
- 단일 저장소에 통합: 타이틀 임베딩, 게임 임베딩, 멤버 프로필, 멀티미디어 자산
- **크로스모달 전이**: CLIP 공간을 통해 아트워크 선호도가 신규 타이틀로 전이됨
- **콜드스타트 해결**: 신규 자산은 생성 시점에 임베딩 부여 → 즉시 개인화 가능

## 벡터 검색

### 인덱스 구조
| 인덱스 | 구축 시간 | 쿼리 지연 | 재현율 | 메모리 |
|-------|------------|---------------|--------|--------|
| Flat (전수 탐색) | O(1) | O(N) | 100% | 낮음 |
| IVF (Inverted File) | O(N) | O(√N) | ~95% | 중간 |
| HNSW | O(N log N) | O(log N) | ~99% | 높음 |
| DiskANN / SPANN | O(N log N) | O(log N) | ~99% | 낮음 (디스크) |

### 하이브리드 검색
```sql
-- 벡터 + 키워드(BM25) + 필터
SELECT * FROM items
WHERE vector_search(embedding, query_vec, k=100)
AND category = 'electronics'
ORDER BY hybrid_score(bm25_score, vector_score)
LIMIT 20
```

## Netflix Embedding Store (MAPS에서)
- **파운데이션 모델 업데이트와 개인화 모델 배포를 분리(decouple)**
- 훈련 시점과 온라인 추론 시점에 동일한 임베딩 사용 → 스큐 없음
- 모든 개인화 모델에 정확히 동일한 임베딩 서빙
- 아트워크 임베딩(CLIP)은 자르기/리사이즈에 불변 → 5개 캔버스에 걸친 단일 통합 모델

## 소스에서

### Netflix GenRec
- Verbalization: 사용자 히스토리 + 아이템 메타데이터 → 텍스트 → LLM 임베딩 공간
- 컨텍스트 엔지니어링: 토큰 예산 관리 (고신호 유지, 저신호 생략, 반복 요약)

### Databricks Hydra
- 높은 카디널리티의 메트릭 → 트러블슈팅용 임베딩 유사 표현

### PonderPounce
- 에피소드 메모리 임베딩으로서의 MLLM 인과적 컨텍스트(KV 캐시)

## 핵심 세미나 포인트

1. **재현율에는 인덱스 선택보다 임베딩 품질**이 중요
2. **멀티모달 정렬**(CLIP 방식)이 크로스모달 전이를 가능하게 함
3. **분리된 스토어**(Netflix)가 훈련/서빙 스큐를 방지
4. 프로덕션 품질을 위한 **하이브리드 검색**(벡터 + 키워드 + 필터)
5. 10억 규모에는 **HNSW/DiskANN**, 100만 미만에는 Flat

## 관련 소스
- `sources/articles/netflix-techblog.md` (MAPS, GenRec)
- `sources/papers/PonderPounce.md` (메모리로서의 인과적 컨텍스트)
- `sources/papers/JIT-Agent.md` (하네스 내 도구 임베딩)

## 관련 가이드
- `guides/ai-engineering/build-rag.md` (임베딩 + 검색)
- `guides/ai-engineering/vector-search.md`
