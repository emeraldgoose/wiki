---
title: "PARSER: Read in Parallel, Reason in Depth for Long-Context LLM Agents"
arxiv_id: 2609.06702
HF_URL: https://huggingface.co/papers/2609.06702
published: 2026-09-06
authors: Kun Li, Zexuan Qiu, Tianhua Zhang, Irwin King, Helen Meng
locale: ko
---

# PARSER: Read in Parallel, Reason in Depth for Long-Context LLM Agents

**Authors**: Kun Li, Zexuan Qiu, Tianhua Zhang, Irwin King, Helen Meng · **Published**: 2026년 9월 6일 · **arXiv**: [2609.06702](https://arxiv.org/abs/2609.06702) · **HuggingFace**: [https://huggingface.co/papers/2609.06702](https://huggingface.co/papers/2609.06702)

## Abstract

연속된 메모리 에이전트는_longDocuments를 처리하기 위해 청크를 하나씩 차례대로 읽으며 컴팩트한 메모리 상태를 유지합니다. 이러한 접근 방식에서 문서 탐색과 추론 깊이가 결합되어 있어 증거 위치에 대한 민감도가 발생하고 추론 지연이 문서 길이에 비례하게 됩니다. PARSER는 읽기를 추론에서 분리합니다. 가볍고 하나의 청크에 바운드된 서브에이전트 은행 전체에서 parallel로 전체 문서를 읽으며, 리드 에이전트는 반복적인 scatter-gather 라운드를 통해 깊이 있는 추론을 수행합니다: 각 라운드에서 리드 에이전트는 모든 서브에이전트에게 쿼리를 방송하고, 반환된 증거를 통합하며, 지금까지 발견된 내용에 조건된 더 깊은 후속 쿼리를 수립합니다. 이러한 분리된 설계는 모든 학습 가능한 행동을 리드 에이전트에 집중시키며, 이는 강화학습으로 최적화되며 서브에이전트는 frozen된 off-the-shelf 모델로 남습니다. 7K부터 896K 토큰까지의 컨텍스트를 사용한 multi-hop QA에서 PARSER 4B 백본은 strongest sequential memory baseline보다 평균 5.7포인트, 896K 토큰에서는 12.0포인트 우수한 성적을 기록합니다. 9B 백본으로 확장하면 DeepSeek-V4-Pro를 6.3포인트 앞섭니다. 컨트롤드 실험은 PARSER가 evidence 위치, 순서, 거리의 perturbation에 robust하며, 이러한 요인으로 인해 sequential methods에서 발생하는 큰 정확도 변동에 강건하며, inference latency를 최대 11배까지 감소시킨다는 사실을 확인합니다.

## 배경 및 문제 설정

연속된 메모리 에이전트는 long-context 언어 모델링의 표준 접근 방식으로 문서 청크를 순차적으로 처리하면서 내부 상태(memory)를 유지하여 이전 청크로부터 관련된 정보를 캡처합니다. 이 접근 방식의 핵심 제한 사항은 문서 traversal과 reasoning이 결합되어 있다는 점 — 모델이 문서를 탐색하는 방식이 추론의 품질 directly impact하고, 이 결합은 증거가 문서 어디에 나타날 경우 민감하게 반응한다는 점입니다. 구체적으로:

- **증거 위치 민감도**: 관련 정보가 나중에 있는 청크에 있으면, 순차적 에이전트는 앞에 있는 모든 청크를 읽은 후 reasoning을 시작해야 하므로 오류가累积되고 지연이 발생합니다.
- **Latency proportionality**: 추론 지연이 문서 길이와 선형으로 스케일링됩니다. 각 청크를 순차적으로 읽은 후 reasoning을 진행해야 하기 때문입니다.
- **용량 병목**: 컴팩트한 메모리 상태는 모든 관련 정보를 압축해야 하며, 특히 매우 긴 문서의 경우 세부 사항이 손실됩니다.

이러한 제한 사항은 7K에서 896K 토큰까지의 컨텍스트를 사용하는 multi-hop QA와 같은 애플리케이션에서 비판적입니다. 모델은 문서의 먼 부분에서 증거를 찾아 통합해야 합니다.

PARSER는 reading process를 reasoning process에서 분리하여 parallel 증거 수집과 depth-first 추론을 가능하게 하여 이러한 제한 사항을 해결합니다.

## 방법론

PARSER 아키텍처는 두 가지 구성 요소가 함께 작동하는 구조입니다:

### 서브에이전트 (평행 읽기 은행)

단일 청크에 바운드된 서브에이전트 은행이 전체 문서를 parallel로 읽습니다. 주요 설계 선택 사항은 다음과 같습니다:

- **frozen off-the-shelf 모델**: 서브에이전트는 훈련되지 않으며, PARSER 운영 동안 고정된 사전 훈련된 모델을 사용합니다. 이는 시스템을 가볍고 배포하기 쉽게 만듭니다.
- **single-chunk binding**: 각 서브에이전트는 정확히 하나의 청크에 책임지며, 서브에이전트 수를 늘려 읽기 대역폭을 확장할 수 있습니다.
- **Parallel execution**: 모든 서브에이전트가 동시에 청크를 읽어, 증거를 수집하는 시간을 O(n)에서 O(1)으로(document 길이 n에 대해) reduces reduces.

### 리드 에이전트 (깊이 우선 추론자)

리드 에이전트는 PARSER의 유일한 trainable 구성 요소입니다. 깊은 추론을 수행하기 위해 반복적인 scatter-gather 라운드를 통해 작동합니다:

- **Scatter 라운드**: 각 라운드에서 리드 에이전트는 모든 서브에이전트에게 쿼리를 방송합니다. 쿼리는 현재 추론 상태와 지금까지 수집된 증거를 기반으로 공식화됩니다.
- **Aggregate 라운드**: 리드 에이전트는 모든 서브에이전트로부터 반환된 증거를 통합합니다. 이 증거는 쿼리와 관련된 청크 내용과 이전에 관련된 정보를 찾은 위치에 대한 메타데이터를 포함합니다.
- **Follow-up query formulation**: 통합된 증거를 기반으로 리드 에이전트는 다음 라운드를 위한 더 깊은 후속 쿼리를 공식화합니다. 이 반복 과정은 리드 에이전트가 원래 질문을 답변할 충분한 정보를 갖출 때까지 지속됩니다.

리드 에이전트는 강화학습으로 최적화되며, 서브에이전트는 frozen된 상태로 유지되어 모든 학습 가능한 행동이 단일 구성 요소에 집중되게 됩니다.

### 읽기와 추론의 분리

PARSER의 핵심 혁신은 읽기와 추론의 분리입니다:

1. **증거 수집은 추론 깊이와 독립적**: 모든 청크가 parallel로 읽히므로, 리드 에이전트는 깊은 추론을 시작하기 전에 모든 증거를 기다릴 수 추가 latency 없이 수행됩니다.
2. **증거 위치에 대한 강건성**: 시스템이 모든 청크를 parallel로 읽기 때문에, 관련 증거의 위치가 더 이상 추론 지연에 영향을 주지 않습니다. 이는 순차적 방법과 대비되며, 나중에 있는 증거는 비례하여 지연을 유발합니다.
3. **지연 감소**: parallel로 읽고 aggregated evidence에 대해서만 iterative 추론을 수행함으로써, PARSER는 순차적 방법에 비해 최대 11배의 지연 감소를 달성합니다. 장기 컨텍스트 QA를 실시간 또는 근실시간 설정에서 가능하게 하는 중요한 개선입니다.

## 결과

PARSER는 7K에서 896K 토큰 범위의 컨텍스트를 사용하는 multi-hop QA에서 평가되었습니다:

- **4B 백본**: 평균 5.7포인트, 896K 토큰에서는 12.0포인트 strongest sequential memory baseline을 앞섭니다.
- **9B 백본**: DeepSeek-V4-Pro를 6.3포인트 앞섭니다. 더 큰 백본으로 확장하면 성능이 추가로 향상됨을 보여줍니다.

컨트롤드 실험은 다음에서 PARSER의 robust성을 확인합니다:

- **증거 위치 perturbation**: 문서 내에서 relevant evidence가 어디에 나타나든 성능이 안정적으로 유지됩니다.
- **증거 순서 perturbation**: 청크 재정렬에도 성능이 저하되지 않습니다.
- **증거 거리 perturbation**: 쿼리 초점과 멀리 떨어져 있는 정보라도 성능이 유지됩니다.

11배의 추론 지연 감소는 실용적인 관점에서 중요한 개선입니다. long-context QA를 real-time 또는 near real-time 설정에 가능하게 만듭니다.

## 제한 및 열린 질문

- **서브에이전트 모델 의존성**: PARSER의 효과성은 서브에이전트 모델의 품질에 dependency가 있습니다. 기본 모델이 약하다면, aggregated evidence는 한계가 있으며 리드 에이전트의 추론 능력과 관계없이 성능이 제한됩니다.
- **쿼리 공식화 복잡도**: iterative scatter-gather 접근 방식은 리드 에이전트가 효과적인 후속 쿼리를 공식화하도록 요구합니다. 부족한 쿼리 공식화는 최적치 않은 증거 수집으로 이어질 수 있습니다.
- **강화 학습 훈련**: 리드 에이전트는 RL로 훈련되며, 이는 sample-unstable할 수 있고 모든 문서 유형과 질문 형식에 일반화되지 않을 수 있습니다.
- **메모리 오버헤드**: 서브에이전트는 frozen되었음에도, parallel 읽기 접근 방식은 모든 청크 표현을 동시에 메모리에 보관해야 하므로, 특히 매우 큰 문서의 경우 메모리 오버헤드가 발생할 수 있습니다.
- **다른 작업으로의 일반화**: PARSER는 주로 multi-hop QA에서 평가되었습니다. 다른 long-context 작업(예: summarization, classification)에서의 성능은 아직 탐구되지 않았습니다.

## 소프트웨어 엔지니어에게 미치는 영향

long-context LLM 애플리케이션을 작업하는 소프트웨어 엔지니어에게 PARSER는 다음과 같은 concrete takeaways를 제공합니다:

1. **parallel reading architecture**: long-context QA 시스템을 구축하는 경우, 여러 가벼운 에이전트가 다른 청크를 동시에 읽는 parallel reading architecture를 고려해 보세요. 이는 long 문서에 대해 추론 지연을 크게 감소시킬 수 있습니다.

2. **증거 수집과 추론의 분리**: 시스템을 설계하여 evidence 수집(읽기/모으기)을 reasoning(분석/통합)과 분리하세요. 이렇게 하면 먼저 모든 evidence를 수집한 후 깊은 추론을 수행할 수 있으며, reading 단계 동안 누적되는_latency에 대해 걱정할 필요가 없습니다.

3. **배포 용이성을 위한 frozen 서브에이전트**: reading 구성 요소에 frozen, off-the-shelf 모델을 사용하면 배포가 간소화되고 compute 비용이 줄어들며, 문서 내용 변경에 더 robust해집니다.

4. **리드 에이전트를 위한 강화 학습**: 리드 에이전트의 RL 최적화는 single component에 학습을 집중하면 효과적일 수 있음을 보여줍니다. multi-agent 시스템을 구축하는 경우, "perception"(읽기)과 "cognition"(추론) 컴포넌트를 분리하고 cognition 구성 요소만 훈련하는 것을 고려하세요.

5. **11배 지연 감소**: 입증된 11배 지연 감소는 parallel 아키텍처로 달성할 수 있습니다. response time가 critical한 products(chat assistants, search, real-time QA)의 경우, 이 개선은 usable와 unusable 시스템 간의 차이를 만드는 요인이 될 수 있습니다.

6. **증거 위치에 대한 강건성**: 시스템 설계 시 evidence position가 시스템을 제약하지 않도록 설계하세요. parallel reading은 evidence position가 latency에 중요한 요인이 되는 sequential 병목 현상을 제거합니다.

7. **확장성**: 시스템은 4B에서 9B 백본으로 효과적으로 확장됩니다. prototyping의 경우 더 작은 백본으로 시작하고 필요한 경우 규모를 확장하세요; parallel reading 아키텍처는 모델 규모를 키우기 전에도 즉시 latency 이점을 제공합니다.

8. **관련 개념**:
   - `concepts/data-engineering/llm-context-management.md`, `concepts/data-engineering/agentic-ai.md`, `concepts/data-engineering/retrieval-augmented-generation.md`
