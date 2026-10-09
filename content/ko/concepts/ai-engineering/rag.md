---
title: 검색 증강 생성 (RAG)
description: en/concepts/ai-engineering/rag.md 한국어 번역 요약
tags: [concept, ai-engineering, rag, ko]
locale: ko
---

# 검색 증강 생성 (RAG)

**원전**: Netflix GenRec (context engineering), Databricks Hydra (PromQL-to-SQL), Uber software factory (agent skills), PonderPounce (System2 reasoning), JIT-Agent (harness intelligence)

## 핵심 RAG 파이프라인
```
Query → Retrieval (vector/keyword/hybrid) → Top-K Context → Generation (LLM) → Answer
```
질의 → 검색(벡터/키워드/하이브리드) → 상위 K개 컨텍스트 → LLM 생성 → 답변의 흐름이다. 사실 정확도는 생성보다 검색 품질에 더 크게 좌우된다.

## 검색 전략

### 밀집 검색 (Dense Retrieval, 벡터 검색)
- 질의 → 임베딩 → ANN 탐색 (HNSW/DiskANN) → 상위 K개 패시지
- 적합: 의미 유사성, 바꿔 말하기(paraphrase) 내성

### 희소 검색 (Sparse Retrieval, BM25/키워드)
- 질의 → 토큰 가중치 → 역인덱스 → 상위 K개 패시지
- 적합: 정확한 일치, 개체명, 기술 용어

### 하이브리드 검색 (프로덕션 표준)
```
score = α × dense_score + β × sparse_score + γ × metadata_filters
```
- α, β는 도메인별로 튜닝하며, 메타데이터 필터(날짜, 출처, 카테고리)는 검색 전에 적용한다

### 다단계 검색
1. **후보 생성**: 넓은 재현율 확보 (BM25 + dense, k=100-1000)
2. **리랭킹**: 크로스 인코더 / LLM 리랭커 (k=10-20)
3. **중복 제거**: near-duplicate 패시지 제거
4. **컨텍스트 조립**: 토큰 예산에 맞게 구성 (context engineering)

## 생성

### 프롬프트 구성
```
System: You are a helpful assistant. Use only provided context.
Context: [passage_1] [passage_2] ... [passage_k]
Query: {user_query}
Answer:
```

### 컨텍스트 엔지니어링 (Netflix GenRec에서 차용)
- **토큰 예산 관리**: 고신호는 유지하고, 저신호는 생략하며, 반복은 요약한다
- **순서**: 가장 관련 높은 것을 앞에(초두 효과) 또는 뒤에(최신 효과) 둔다
- **인용**: 검증 가능성을 위해 인라인 인용 [1], [2]를 요구한다

### 생성 패턴
| 패턴 | 설명 | 용도 |
|---------|-------------|----------|
| Single-pass | LLM 1회 호출 | 단순 QA |
| Iterative | 검색 → 생성 → 정교화 | 복잡한 추론 |
| Self-RAG | LLM이 검색 시점을 스스로 결정 | 적응형 |
| Corrective RAG | 검증 → 교정 → 재생성 | 고정확도 |

## 평가 (세미나 수준)

### 검색 지표
- **Recall@K**: 상위 K개에 관련 문서가 든 비율
- **MRR**: Mean Reciprocal Rank (평균 역순위)
- **nDCG**: Normalized Discounted Cumulative Gain

### 생성 지표
- **Faithfulness(충실도)**: 답변이 컨텍스트로 뒷받침되는가? (LLM-as-judge)
- **Answer Relevance(답변 관련성)**: 질의에 답하는가?
- **Hallucination Rate(환각률)**: 전체 주장 중 근거 없는 주장의 비율

### 종단 간 평가
- **RAGAS**: 검색 + 생성을 결합한 평가
- **Human eval**: 나란히 비교하는 사람 평가

## 프로덕션 패턴 (원전에서 차용)

### Netflix GenRec
- 피처 엔지니어링이 아닌 **컨텍스트 엔지니어링**
- 언어화된 사용자 히스토리 + 아이템 메타데이터를 컨텍스트로 사용
- 비용 효율을 위한 Prefill-only vLLM

### Databricks Hydra
- PromQL-to-SQL 변환 (검색 = SQL 생성)
- 심층 분석을 위한 Delta 테이블 직접 접근
- TSDB + Lakehouse 경로에 걸친 통일된 메트릭 의미 체계

### Uber Software Factory
- 3,600개 이상의 에이전트 스킬 = 검색 + 생성 패턴
- 스킬별 벤치마크 기반 모델 선택
- 비용 방정식 최적화

### PonderPounce
- System2 (Ponder)가 전체 에피소드 컨텍스트를 검색·추론한다
- System1 (Pounce)은 압축된 인지 토큰을 전달받는다

### JIT-Agent
- 하네스 합성 = 관련 스킬 모듈의 검색이다
- (task, harness, performance) 튜플 아카이브로 스스로 진화한다

## 핵심 세미나 포인트

1. 사실 정확도에는 **검색 품질이 생성 품질보다 중요**하다
2. **하이브리드 검색 + 리랭킹**이 프로덕션 기준선이다
3. **컨텍스트 엔지니어링**(토큰 예산, 순서, 인용)이 결정적이다
4. 평가는 **검색 + 생성 양쪽**을 다뤄야 한다 (RAGAS)
5. **에이전틱 RAG**: 검색을 에이전트 하네스의 도구/스킬로 둔다

## 관련 원전
- `sources/articles/netflix-techblog.md` (GenRec context engineering)
- `sources/articles/databricks-engineering.md` (Hydra PromQL-to-SQL)
- `sources/papers/PonderPounce.md` (System2 context)
- `sources/papers/JIT-Agent.md` (harness as retrieval)

## 관련 가이드
- `guides/ai-engineering/build-rag.md`
- `guides/ai-engineering/vector-search.md`
