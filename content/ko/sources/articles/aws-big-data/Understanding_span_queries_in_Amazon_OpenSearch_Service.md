---
title: "Amazon OpenSearch Service의 스팬 쿼리 이해하기"
description: "Amazon OpenSearch Service의 스팬 쿼리는 아홉 가지 스팬 쿼리 유형을 조합해, slop을 쓴 구문 쿼리로는 표현할 수 없는 정확한 단어 순서, 필드 내 위치, 포함 관계를 강제합니다. 법률·규제 준수·특허·계약 검색에 필요한 정밀도를 다룹니다."
tags: [source, aws-big-data, opensearch, search-queries, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/understanding-span-queries-in-amazon-opensearch-service"
blog: aws-big-data
published_date: 2026-11-14
---

# Amazon OpenSearch Service의 스팬 쿼리 이해하기

**원문**: [AWS 빅데이터 블로그](https://aws.amazon.com/blogs/big-data/understanding-span-queries-in-amazon-opensearch-service) · **게시일**: 2026-11-13

## 개요

Amazon OpenSearch Service는 OpenSearch를 클라우드에서 배포, 확장, 운영하는 완전관리형 서비스입니다. OpenSearch는 검색, 분석, 관측 가능성을 위한 Apache License V2.0 라이선스의 오픈소스 소프트웨어 모음입니다. OpenSearch의 여러 쿼리 유형 가운데 스팬 쿼리는 단어가 문서에서 어디에 나타나는지, 그리고 단어들끼리 어떤 관계인지를 정밀하게 제어합니다. 대부분의 애플리케이션은 match와 phrase 쿼리만으로도 좋은 결과를 얻지만, 법률 검색, 규제 준수, 과학·특허 검색, 계약 분석처럼 더 단순한 쿼리로는 표현할 수 없는 정확한 단어 배치가 필요한 워크로드도 있습니다. 스팬 쿼리가 바로 이 간격을 메웁니다.

글은 먼저 구문 쿼리가 어디서 한계를 보이는지 보여 줍니다. match_phrase 쿼리는 순서대로 이어진 단어열을 찾고, slop 파라미터는 단어 위치를 몇 번까지 바꿔도 되게 함으로써 이 제약을 느슨하게 합니다. 제목 필드에서 "star wars iv"를 검색하면 단어 "Episode"가 가운데 끼어 있어 정확한 제목과는 일치하지 않지만, slop을 1로 하면 위치 하나를 바꿔 찾아 냅니다. 문제는 이 해법이 양날의 검이라는 점입니다. slop을 4로 하면 "star wars hope" 쿼리가 단어 순서가 다른 두 번째 문서까지 의외로 일치시키는데, 구문 slop은 편집 거리 방식으로 편집 창 안에서 순서와 무관하게 단어를 맞바꾸기 때문입니다. 단어 순서, 필드 내 위치, 단어 사이의 구조적 관계를 강제해야 한다면 구문 쿼리로는 표현력이 부족합니다.

스팬 쿼리는 이 간격을 채웁니다. 스팬 쿼리는 다른 스팬 쿼리만으로 구성되는 복합 쿼리이며, 글은 스팬 쿼리의 동작 방식, 구문 쿼리 대신 언제 써야 하는지, 정밀한 구조적 제약을 표현하기 위해 어떻게 조합하는지를 다룹니다.

## 핵심 내용

- 스팬 쿼리는 단어들의 상대적 위치를 제어하는 복합 쿼리입니다. 다른 스팬 쿼리만 포함할 수 있어, 같은 복합 식 안에서 스팬이 아닌 쿼리와 섞을 수 없습니다.
- OpenSearch는 아홉 가지 스팬 쿼리 유형을 지원합니다. span_term(단일 단어, 보통 리프), span_multi(prefix, regex, wildcard 다중 단어 쿼리를 감쌈), span_first(필드 시작 부분에서 지정 위치 수 안의 스팬), span_near(slop 안에서 절들을 일치, 구문 쿼리의 스팬판), span_not(특정 단어 제외), span_or(절들의 합집합), span_field_masking(다른 필드의 span_term을 주 필드처럼 위장), span_containing, span_within입니다.
- 모든 스팬 쿼리는 in_order 파라미터를 받아, 하위 스팬이 쿼리 절의 순서대로 나타나야 하는지 제어합니다.
- span_containing과 span_within은 둘 다 big과 little 절을 받아 little 스팬이 big 스팬 안에 포함되도록 요구합니다. span_containing은 big 일치를, span_within은 little 일치를 돌려주며, span_within은 span_containing의 거울입니다.
- "A New Hope"를 찾는 예제는 span_first로 "star"를 제목의 처음 두 위치(end 2)에 고정하고, span_near에 in_order true로 "hope"가 12 위치 안에 오도록 요구합니다. 이 쿼리는 "star"가 제목 처음에 없는 문서를 걸러 내고 에피소드 4 제목만 일치시킵니다.
- span_containing 예제는 정확한 구문 "episode iv"(slop 0, in_order true)가 "star"와 "hope"를 12 단어 안에 담는 big 스팬 안에 들어가도록 요구하며, 두 제약을 모두 만족하는 문서는 에피소드 4 제목 하나뿐입니다.
- 구문 slop은 편집 거리 일치입니다. 편집 창 안에서 순서와 무관하게 단어를 맞바꾸므로, slop 4가 단어 순서가 다른 문서까지 일치시킨 이유가 여기에 있습니다.
- 대표 활용 사례는 "force majeure"가 "termination"의 다섯 단어 안에 나오는 문서 찾기이며, 구조적 단어 위치가 중요한 특허·과학 검색, 규제 정의를 만족시키려 정확한 배치를 강제하는 준수·감사 워크플로, 데이터 재구성 대신 쿼리 시점에 제약을 거는 방법이 이어집니다.
- 대가도 분명합니다. 스팬 쿼리는 구문 쿼리보다 장황하고 신중한 조합이 필요하지만, 그 대가로 구문 쿼리로는 불가능한 정확한 순서, 필드 내 위치, 포함 관계를 표현합니다.

## 세부 사항

### 구문 쿼리가 부족한 순간

실습은 title이라는 text 필드 하나를 가진 term_order 인덱스를 만들고, 두 문서를 색인하는 것에서 시작합니다. 하나는 스타워즈 에피소드 4 제목이고 다른 하나는 단어 순서가 뒤섞인 두 번째 제목입니다. "star wars iv"에 대한 match_phrase 쿼리는 slop을 1로 하면 첫 문서와 일치합니다. slop 1이 단어 위치 하나를 바꿔 가운데 낀 "Episode"를 수용하게 해 주기 때문입니다. 쿼리를 "star wars hope"으로 바꾸고 slop을 4로 하면 두 문서가 모두 일치하는데, 여기에는 단어 순서가 쿼리와 다른 의외의 두 번째 문서도 포함됩니다. 구문 slop은 편집 거리 방식으로 편집 창 안에서 순서와 무관하게 단어를 맞바꾸기 때문에, 단어가 특정 순서로, 특정 위치에, 구조적 관계로 나타나야 한다는 요구는 표현할 수 없습니다. 단어 배치가 의미를 갖는 워크로드를 위한 표현력 격차가 바로 스팬 쿼리가 메우는 부분입니다.

### 스팬 조합: 단어를 위치에 고정하기

스팬 쿼리는 다른 스팬 쿼리만 포함하며, 각 유형이 하나의 구조적 제약을 더합니다. 첫 번째 조합은 span_first로 "star"를 제목 시작부에 고정합니다(span_term "star"를 match로, end 2, 즉 처음 두 위치 안) 그리고 이 절을 span_near의 절로 감싸 "hope"에 대한 일반 span_term과 함께 slop 12, in_order true를 둡니다. 이 쿼리는 에피소드 4 제목만 일치시키고, "star"가 제목 처음에 없는 두 번째 문서는 실패합니다. 이 예제는 구문 쿼리 위에 스팬 쿼리가 더하는 두 가지 메커니즘, 즉 필드 안 위치 고정과 스팬 위의 순서 있는 근접성을 보여 줍니다.

### 스팬 안의 스팬: 포함 제약

span_containing과 span_within은 한 스팬을 다른 스팬 안에서 일치시켜 구조적 제약을 표현합니다. 둘 다 big과 little 절을 받고 little 스팬이 big 스팬 안에 포함되기를 요구하지만, 어느 쪽 일치를 돌려주는지가 다릅니다. 글의 예제는 정확한 구문 "episode iv"가 "star"와 "hope"를 모두 담는 스팬 안에 나타나는 문서를 찾습니다. little 절은 "episode"와 "iv"를 slop 0, in_order true로 잇는 span_near, 즉 정확한 구문이고, big 절은 "star"와 "hope"를 slop 12, in_order false로 잇는 span_near, 즉 순서 무관 12 위치 안의 근접 스팬입니다. 쿼리는 little 구문이 big 일치 안에 들어가도록 요구하며, 두 제약을 모두 만족하는 문서는 에피소드 4 제목 하나뿐입니다.

### 스팬 쿼리를 선택해야 할 때

스팬 쿼리는 구문 쿼리가 표현하지 못하는 제약이 필요한 순간마다 값어치를 합니다. 법률·규제 검색에서 법조문과 계약서는 특정 구문이 근접해야 함을 요구하는 경우가 많습니다. "force majeure"가 "termination"의 다섯 단어 안에 나오는 문서를 찾는 것이 그 예입니다. 특허·과학 검색에서는 청구항과 논문이 단어들이 서로에 대해 특정 구조적 위치에 오도록 요구합니다. 규제 정의를 만족시키려 정확한 단어 배치를 강제해야 하는 준수·감사 워크플로도 같은 정밀도의 이점을 받습니다. 더 일반적으로, 텍스트에 명시적인 구조 모델이 없지만 필드 안 단어 위치에 대한 제약이 필요하다면, 데이터를 재구성하는 대신 스팬 쿼리가 쿼리 시점 대안을 제공합니다. 결론은 단순함을 정밀함과 바꾸는 거래입니다. 스팬 쿼리는 더 장롱하고 신중한 조합이 필요하지만, 정확한 순서·필드 내 위치·포함 관계를 표현할 수 있고, 단어 배치가 의미를 갖는 애플리케이션에는 옳은 도구입니다.
