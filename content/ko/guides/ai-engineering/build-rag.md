---
title: RAG 시스템 구축 — 가이드 (번역)
description: en/guides/ai-engineering/build-rag.md 한국어 번역 요약
tags: [guide, ai-engineering, rag, retrieval, generation, ko]
locale: ko
---

# RAG 시스템 구축 — 실행 가이드

## 아키텍처
```
Query → [하이브리드 검색] → [리랭크] → [컨텍스트 조립] → [LLM 생성] → 답변
         ↑                    ↑              ↑                   ↑
    벡터 + BM25          Cross-encoder   토큰 예산           Prefill-only/
    + 메타데이터                                               인용
```

## 단계별 구현

### 1. 데이터 준비
```python
# 시맨틱 청킹
from langchain.text_splitter import RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64)

# 임베딩
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("BAAI/bge-large-en-v1.5")

# 인덱스 (HNSW <100M, DiskANN >100M)
import faiss
index = faiss.IndexHNSWFlat(1024, 32)
```

### 2. 하이브리드 검색
```python
def hybrid_search(query, top_k=100, alpha=0.7):
    dense_scores, dense_idx = index.search(model.encode([query])[0], top_k)
    sparse_scores, sparse_idx = bm25_search(query, top_k)
    # 가중 결합
```

### 3. 리랭킹
```python
reranker = CrossEncoder("BAAI/bge-reranker-large")
reranked = reranker.predict([[query, c] for c in candidates])
```

### 4. 컨텍스트 조립 (Netflix GenRec 패턴)
- 토큰 예산 내 고신호 우선
- 인라인 인용 [1], [2]

### 5. 평가 (RAGAS)
- Faithfulness, Answer Relevancy, Context Recall/Precision

## 소스 패턴
- **Netflix GenRec**: Prefill-only vLLM, 컨텍스트 엔지니어링
- **Databricks Hydra**: PromQL→SQL, Delta 직접 접근
- **Uber**: 3,600+ 스킬, 벤치마크 기반 모델 선택
