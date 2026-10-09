---
title: "Vector Databases"
description: "Similarity search databases: FAISS, Annoy, Milvus, Pinecone, Qdrant; index types IVF/HNSW; ANN; use cases: RAG, recommendation systems; pitfalls"
tags: [concept, data-engineering, vector-databases, similarity, search]
locale: en
published: 2026-09-09
---

# Vector Databases (벡터 데이터베이스)

## 정의
유사성 검색을 위해 최적화된 데이터베이스입니다. 고차원 벡터 간의 유사도를 효율적으로 찾기 위해 설계되었으며, 주로 검색색(color) 및 추천 시스템에서 활용됩니다.

## 왜 중요한가
- **의미 검색**: 키워드가 아닌 의미 기반 검색 가능
- **추천 시스템**: 사용자 행동 패턴 기반 개인화된 추천
- **RAG(Retrieval-Augmented Generation)**: LLM 응답에 유관 컨텍스트 주입

## 주요 구현체

### FAISS (Facebook AI Similarity Search)
- **특징**: Meta(Facebook) 개발, CPU/GPU 모두 지원
- **인덱스 유형**: 
  - **IVF**: 인덱스 비트 퍼셉트론, 쿼리 시 탐색할 센터 수 설정
  - **HNSW**: 하위 공간 그래프 위상 매핑, 탐색 정확도와 속도의 균형 제공
- **장점**: 라이브러리 매트릭스가 작고 성능 우수
- **단점**: 학습 단계가 필요하며, 고차원 데이터에서는 precision이 낮아질 수 있음

### Annoy (Approximate Nearest Neighbors Oh Yeah)
- **특징**: Netflix 개발, 파일에 인덱스 저장 가능 (데이터 영속성 용이)
- **인덱스 유형**: 
  - **브러트 포스**: 정확한 결과 but 느림
  - **타당성 검색**: 지정된 수의 후보에서 가장 유사한 항목 찾기
- **장점**: 간단하고 직관적, 파일 기반 저장 지원
- **단점**: 고차원 데이터에서는 성능 저하, 실시간 인덱스 업데이트 어려움

### Milvus
- **특징**: 클라우드 네이티브 벡터 데이터베이스, 대규모 배포 용이
- **인덱스 유형**: 
  - **IVF_FLAT**: 정확도 높음 but 느림
  - **HNSW**: 높은 탐색 속도와 적절한 정확도 균형
  - **SCANN**: Scalable Approximate Nearest Neighbor
- **장점**: 분산 스토리지, 쿼리 최적화, 여러 프로토콜 지원
- **단점**: 운영 복잡성, 리소스 소비가 높음

### Pinecone
- **특징**: 완전 관리형 서비스, 인프라 관리 불필요
- **인덱스 유형**: 
  - **HNSW**: 기본값 추천, 탐색 속도와 정확도 균형
  - **SPANN**: 서버측 근사 nearest neighbor
- **장점**: 즉시 사용 가능, 확장성 우수, 고가용성
- **단점**: 비용이 플러그인형, 커스터마이징 제한됨

### Qdrant
- **특징**: vector similarity 검색 엔진, 쿠버네티스 네이티브
- **인덱스 유형**: 
  - **HNSW**: 기본값, 균형된 성능
  - **QTree**: 고차원 데이터 최적화
- **장점**: 필터 기능 강화, 오픈소스, 마이크로서비스에 최적화
- **단점**: 커뮤니티가 상대적으로 작음

## 인덱스 유형 비교

| 인덱스 | 정확도 | 검색 속도 | 메모리 사용량 | 최적의 사용 경우 |
|--------|--------|-----------|---------------|------------------|
| **IVF** | 중간 | 중간 | 낮음 | 대규모 데이터 셋, 대략적 검색 충분할 때 |
| **HNSW** | 높음 | 높음 | 중간 | 고정확도가 필수인 경우, 실시간 검색 필요할 때 |
| **브러트 포스** | 최고 | 가장 느림 | 높음 | 데이터 양이 적고 정확성이 최우선일 때 |

## 일반적인 사용 패턴

### RAG (Retrieval-Augmented Generation)
```python
# 질문에 대한 벡터 검색 및 LLM 컨텍스트 주입
query_vector = embedder.encode(query_text)
results = vector_db.search(query_vector, k=5)
context = "\n".join([r.text for r in results])
prompt = f"Context: {context}\nQuestion: {query_text}\nAnswer:"
llm_response = llm.generate(prompt)
```

### 추천 시스템
```python
# 사용자 임베드와 아이템 임베드 간의 유사도 계산
user_vec = get_user_embedding(user_id)
item_vecs = get_item_embeddings(item_ids)
scores = cosine_similarity(user_vec, item_vecs)
recommendations = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:10]
```

## 일반적인 함정
- **차원 저주**: 차원이 높아질수록 유사도 분포가 수렴하여 구별력이 떨어짐
- **인덱스 파라미터 튜닝 누락**: n_probe(IVF)나 ef(HNSW) 파라미터 기본값 그대로 두면 성능 급감
- **데이터 drift**: 시간이 지남에 따라 벡터 분포가 바뀌어 검색 품질 저하
- **메모리 초과**: 고차원 데이터와 대규모 레코드 수 시 메모리 부족 발생
- **하드웨어 불일치**: CPU 인덱스를 GPU에서 사용하려 하거나 역 경우 성능 저하

## 최적화 가이드라인
1. **데이터 미리 보기**: 실제 데이터 분포 파악 후 인덱스 유형 결정
2. **파라미터 탐색**: ef, n_probe 등 파라미터 그리드 서치로 최적 설정 찾기
3. **하이브리드 접근**: 브러트 포스로 후보 선별 후 HNSW로 정제
4. **지속적 모니터링**: 검색 정확도 및 지연 시간 지속적 모니터링
5. **데이터 재인덱싱**: 시간이 지남에 따라 데이터 분포 변화 감지하고 인덱스 재구성

## 참조
- FAISS 문서 (github.com/facebookresearch/faiss)
- Annoy 프로젝트 (github.com/spotify/annoy)
- Milvus 문서 (milvus.io)
- Pinecone 문서 (docs.pinecone.io)
- Qdrant 문서 (qdrant.tech)
- "Designing Data-Intensive Applications" — Martin Kleppmann, 제11장
