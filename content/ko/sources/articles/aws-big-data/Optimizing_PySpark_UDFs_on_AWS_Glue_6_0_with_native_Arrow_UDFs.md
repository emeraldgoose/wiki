---
title: "네이티브 Arrow UDF로 AWS Glue 6.0의 PySpark UDF 최적화하기"
description: "1,000만~1억 행 규모의 AWS Glue 6.0 벤치마크에서 네이티브 Arrow UDF(arrow_udf, Apache Spark 4.1)가 가장 빠른 UDF 방식으로 확인되었습니다. 연산 위주 워크로드에서 표준 Python UDF보다 약 4.4배 빠르며, Arrow의 이득은 전송이 아니라 벡터화된 DataFrame 실행 경로에서 나옵니다."
tags: [source, aws-big-data, glue, pyspark, performance, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/optimizing-pyspark-udfs-on-aws-glue-6-0-with-native-arrow-udfs"
blog: aws-big-data
published_date: 2026-11-14
---

# 네이티브 Arrow UDF로 AWS Glue 6.0의 PySpark UDF 최적화하기

**원문**: [AWS 빅데이터 블로그](https://aws.amazon.com/blogs/big-data/optimizing-pyspark-udfs-on-aws-glue-6-0-with-native-arrow-udfs) · **게시일**: 2026-11-13

## 개요

PySpark의 Python UDF는 JVM과 Python 런타임 사이에서 데이터를 직렬화해야 하므로 성능을 떨어뜨릴 수 있습니다. AWS Prescriptive Guidance는 해결책을 선호 순으로 정리합니다. 내장 Spark SQL 함수를 먼저 쓰고, 다음으로 Scala나 Java로 UDF를 구현하고, 벡터화가 가능한 워크로드에는 Apache Arrow 기반 UDF(벡터화, pandas UDF)를 쓰라는 것입니다. 이 지침은 1,000만 행에 대한 a + b 연산으로 표준 Python UDF, 벡터화 UDF, Spark SQL을 비교한 간단한 예제에 근거합니다. 이 글은 여기에 고객들이 실제로 묻는 질문을 더합니다. 행 수가 1,000만에서 1억으로 늘어도 순위가 유지되는지, a + b가 아니라 연산량이 많은 연산에서도 유지되는지, 그리고 AWS Glue 6.0(Apache Spark 4.1.1)의 두 가지 새 선택지, 즉 Arrow 최적화 Python UDF(useArrow=True)와 네이티브 Arrow UDF(arrow_udf, Apache Spark 4.1.0에서 도입)가 어디에 자리 잡는지입니다.

저자들은 AWS Glue 6.0 작업으로 파라미터화된 벤치마크 하네스를 실행했습니다. Parquet 데이터셋을 한 번 생성해 Amazon S3에 쓴 뒤, 모든 UDF 변형이 같은 파일을 읽도록 각 변형을 동일 데이터에 실행합니다. 측정은 1,000만, 5,000만, 1억 행의 세 가지 규모와, 행당 비용이 점점 커지는 세 가지 워크로드에 대해 이뤄졌습니다. 각 워크로드는 두 가지 쿼리 형태로 실행되었습니다. 행당 비용만 분리해 보는 스트리밍 형태(sum(op(a, b)))와, 약 100만 개 그룹으로 GROUP BY하여 셔플과 해시 집계를 더하는 상태 유지형입니다.

결론은 규모와 형태 모두에서 일관됩니다. 순위는 AWS Prescriptive Guidance 권고와 일치하고, 로직이 PyArrow 커널로 표현될 수 있는 한 UDF 중에서는 네이티브 Arrow UDF가 가장 빠릅니다. 2×2 통제 실험이 핵심 이유를 밝혀 줍니다. 이득은 Arrow 전송 자체가 아니라, 벡터화된 DataFrame 실행 경로에 통합된 Apache Arrow에서 나옵니다.

## 핵심 내용

- AWS Glue 6.0은 Apache Spark 4.1.1에 Python 3.13과 Scala 2.13을 실행합니다. 벤치마크는 미국 동부(버지니아 북부) 리전(us-east-1)에서 G.1X 익스큐터 10개와 드라이버로 bigint 컬럼 두 개짜리 Parquet 데이터셋을 사용했습니다.
- 다섯 가지 방식을 비교했습니다. 표준 Python UDF(Pickle 전송, 행별 Python), Arrow 최적화 Python UDF(Arrow 전송, 행별 Python), 벡터화 pandas UDF(Arrow 전송, pandas 변환을 거쳐 배치별 NumPy), 네이티브 Arrow UDF(arrow_udf, Arrow 전송, pandas 변환 없이 배치별 PyArrow 연산), 그리고 경계를 넘지 않고 JVM에서 실행되는 Spark SQL입니다.
- 연산 위주 워크로드(sqrt(x² + y²) · sin(x) + ln(y))의 1억 행에서 Spark SQL 1.22초, 네이티브 Arrow UDF 3.13초, 벡터화 UDF 3.83초, Arrow 최적화 Python UDF 11.01초, 표준 Python UDF 13.82초였고, 네이티브 Arrow UDF는 벡터화 UDF보다 약 18% 빨랐습니다.
- 같은 워크로드에서 가장 빠른 네이티브 Arrow UDF(3.13초)와 표준 Python UDF(13.82초)의 격차는 동일 출력 기준 약 4.4배였고, Glue는 초 단위로 과금하므로 이 차이는 매 실행 비용에 그대로 반영됩니다.
- 단순 연산(a + b)의 1억 행에서는 Spark SQL 0.99초(기준 대비 11.8배), 네이티브 Arrow UDF 2.81초(4.2배), 벡터화 UDF 3.13초(3.7배), Arrow 최적화 Python UDF 8.94초(1.3배), 표준 Python UDF 11.68초(기준)였습니다.
- 벡터화 UDF가 표준 Python UDF보다 빠른 폭은 규모가 커질수록 벌어집니다. 단순 연산에서 1,000만 행 때 약 2.2배에서 1억 행 때 3.7배로 확대되는데, 행별 직렬화 비용이 행 수에 비례해 늘기 때문입니다.
- 반복 루프 워크로드(행당 최대 1,000회로 제한된 콜라츠 방식)에서는 Spark SQL과 네이티브 Arrow UDF가 적용되지 않고, 벡터화 UDF가 최선입니다. 표준 Python UDF 대비 1,000만 행에서 약 2.2배, 1억 행에서 약 3.8배 빠릅니다.
- 상태 유지형 쿼리도 같은 순위를 보였습니다(연산 위주 워크로드 1억 행: Spark SQL 1.59초, 벡터화 4.22초, Arrow 최적화 11.02초, 표준 14.33초). 셔플과 해시 집계 때문에 다소 느리지만 순서는 변하지 않습니다.
- 통제 실험에서 Pickle 전송으로 NumPy 연산을 재현한 RDD.mapPartitions 변형은 전체 중 가장 느렸습니다. 1억 행에서 21.07초로 표준 Python UDF의 13.82초보다 나빴습니다.
- 방법론도 결과를 좌우했습니다. 캐시된 DataFrame을 재사용하면 Spark가 계획을 가지치기해 Spark SQL이 UDF보다 느려 보였고, 캐시를 비우고 매 반복 Parquet을 다시 읽고 sum(...)을 쓰자 예상 순위가 돌아왔습니다. 행 수에 비례해 늘지 않는 UDF 벤치마크는 계산이 아니라 캐시를 측정하고 있을 가능성이 높습니다.
- 재작성은 행당 작업이 무겁고 데이터가 크거나 실행이 잦을 때 값어치가 있습니다. 소량의 드문 데이터에 대한 단순 연산이라면 표준 Python UDF로도 충분할 수 있습니다.

## 세부 사항

### 다섯 가지 방식의 JVM–Python 경계 통과 방식

다섯 방식은 전송과 연산에서 서로 다릅니다. 벡터화 UDF와 Arrow 최적화 Python UDF는 모두 전송에 Apache Arrow를 쓰므로 물리 계획에 ArrowEvalPython이 나타납니다. 차이는 연산입니다. 벡터화 UDF는 pandas.Series 배치를 받아 NumPy로 네이티브 코드에서 계산하고, Arrow 최적화 변형은 여전히 호출당 값 하나를 받는 스칼라 UDF입니다. Apache Spark 4.1의 arrow_udf 데커레이터로 도입되어 AWS Glue 6.0에서 쓸 수 있는 네이티브 Arrow UDF는 pyarrow.Array를 받고 돌려주며 PyArrow 커널로 Arrow 데이터를 직접 계산해 pandas 변환이 없습니다. Spark SQL은 경계를 아예 넘지 않습니다. 코드 모양도 이를 반영해, useArrow=True는 스칼라 람다를 감싸고, pandas_udf는 pandas.Series를 다루는 배치 함수를 감싸며, arrow_udf는 multiply, sqrt, add, sin 같은 PyArrow 커널을 조합합니다.

### 벤치마크 설계: 워크로드 셋과 쿼리 형태 둘

행당 비용이 점점 커지는 세 연산을 일부러 골랐습니다. arith(a + b)는 계산이 사소해 전송 비용만 분리합니다. mathheavy(sqrt(x² + y²) · sin(x) + ln(y))는 SQL, PyArrow 커널, NumPy, 스칼라 Python 어디로도 표현되는 실질 연산을 더해 다섯 방식 모두가 경쟁합니다. pyheavy는 컬럼 a와 b에서 정수를 만들어 짝수면 반으로 나누고 홀수면 3n + 1을 적용하는, 1,000회로 제한된 콜라츠 방식 반복 루프로, SQL이나 PyArrow 커널 어디에도 대응되지 않아 Python 기반 UDF만 비교 대상이 됩니다. 각 워크로드는 스트리밍 형태(전체 스캔을 값 하나로 축약하는 sum(op(a, b)))와 상태 유지형(cast(op(a, b) AS bigint) % 1,000,000 기준 GROUP BY, 약 100만 그룹)으로 모든 방식과 규모에 대해 실행되었고, 워밍업 1회는 버리고 7회 중 최솟값을 보고했습니다.

### 결과와 전송 대비 연산 통제 실험

위 표의 수치가 결과입니다. 실행 시간은 1,000만, 5,000만, 1억 행에서 거의 선형으로 늘고 순위는 모든 규모에서 안정적입니다. 반복 루프 워크로드의 상태 유지형 수치는 스트리밍보다 다소 느리지만(예: 1억 행에서 벡터화 UDF 2.99초 대 3.01초) 순서는 그대로입니다. 벡터화 UDF의 우위가 전송 때문인지 연산 때문인지 확인하기 위해 저자들은 빠진 조합, 즉 RDD.mapPartitions로 Pickle 전송 위에 NumPy 연산을 얹은 변형을 만들었고, 이 변형이 1억 행 21.07초로 전체 중 가장 느렸습니다. Pickle 전송을 강제하려면 DataFrame API를 벗어나야 하고, 그러면 각 행이 NumPy 배열로 만들어지기 전에 Python 객체로 구체화되며 벡터화 UDF가 누리는 최적화된 DataFrame 실행 엔진도 우회됩니다. 결론은 이렇습니다. 이득은 컬럼 기반 전송과 NumPy 연산을 결합한, 벡터화 DataFrame 실행 경로에 통합된 Arrow에서 나오며, 그 경로 밖에서 NumPy 부분만 재현해는 같은 효과가 없으므로 벡터화 로직은 RDD 연산으로 내려가지 말고 DataFrame API 안에 두어야 합니다.

### 실무 지침

UDF가 필요하고 로직이 PyArrow 커널로 표현된다면 네이티브 Arrow UDF를 먼저 고르십시오. 이번 실험에서 가장 빨랐고 AWS Glue 6.0(Apache Spark 4.1)에서 사용할 수 있습니다. 기존 스칼라 UDF를 최소한만 고치고 싶다면 Arrow 최적화 Python UDF(useArrow=True)가 적합하지만, 이는 전송만 개선하고 연산은 그대로이므로 행당 작업이 무거워지면 벡터화나 네이티브 방식이 이깁니다. Arrow의 이득을 유지하려면 DataFrame API 안에 머무십시오. 재작성 비용은 한 번이고, 절감은 행 수와 실행 빈도에 비례해 커집니다. 매일 수억 행을 다루는 연산 위주 변환은 처음 몇 번의 실행만에 재작성 비용을 회수하는 반면, 작고 드문 데이터의 단순 연산은 재작성이 필요 없을 수 있습니다.
