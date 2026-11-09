---
title: "UCDataset로 Unity Catalog 테이블에서 GPU 학습 가속하기"
description: "Databricks AI Runtime의 베타 네이티브 PyTorch 데이터 로더 UCDataset은 Unity Catalog 테이블을 모든 GPU로 직접 스트리밍하며, 벤치마크에서 내보낸 Parquet 사본을 읽는 방식보다 학습 시간을 10배 단축했다."
tags: [source, databricks, machine-learning, training, ko]
locale: ko
source_url: "https://www.databricks.com/blog/accelerate-gpu-training-unity-catalog-tables-ucdataset"
blog: databricks
published_date: 2026-11-10
---

# UCDataset로 Unity Catalog 테이블에서 GPU 학습 가속하기

**원문**: [Accelerate GPU training on Unity Catalog tables with UCDataset](https://www.databricks.com/blog/accelerate-gpu-training-unity-catalog-tables-ucdataset) · **게시일**: 2026-11-09

## 개요

GPU는 대개 학습 실행에서 가장 비싼 부분이면서 가장 활용하기 어려운 자원이고, 병목은 좀처럼 모델이 아니다. 데이터가 있는 곳에서 GPU까지 충분히 빠르게 옮기는 일이 문제다. Databricks는 AI Runtime에서 UCDataset(Unity Catalog Dataset)을 베타로 공개했다. Unity Catalog 테이블을 학습 작업의 모든 GPU로 직접 스트리밍하는 네이티브 PyTorch 데이터 로더로, 내보내기와 복사본, 사용자 정의 로더 코드가 필요 없다.

글은 팀들이 빠지는 세 가지 우회책을 짚는다. 매 실행 전에 테이블을 Parquet로 내보내면 사본을 하나 더 저장해야 하고, 새 데이터가 들어오는 순간 낡은 데이터가 되며, Unity Catalog 계보에서 벗어난다. `toPandas()`로 테이블 전체를 pandas로 읽는 방식은 작은 테이블에서만 통하고 모든 데이터를 한 노드에 올리므로 32개 GPU로 학습하는 작업에는 도움이 되지 않는다. 웨어하우스를 통해 스트리밍하는 방식은 느린데, 웨어하우스는 GPU를 먹이도록 설계된 것이 아니라 여러 GPU가 동시에 읽으면 스로틀링이 걸리기 때문이다. 여기에 더해 모든 GPU와 워커가 균형 잡힌 데이터 조각을 가져야 하는데, 이를 손으로 구현하다 보면 중복되거나 누락된 행으로 학습해도 아무도 모르는 미묘한 버그가 생긴다.

UCDataset은 대신 Unity Catalog 테이블을 분산 PyTorch 학습의 일급 데이터 소스로 취급한다. 읽을 대상(테이블, 필요한 컬럼, 행 필터)을 지정하면 학습 준비가 끝난 배치를 스트리밍한다. 테이블의 파일을 클라우드 스토리지에서 직접 읽고, 일치하는 행을 모든 GPU와 데이터 로더 워커에 균등하게 나누며, 데이터를 읽는 시점에 필터와 삭제 벡터를 적용하고, 다음 실행에서는 새로 추가된 행을 자동으로 반영한다. 작업이 실행 주체의 자격으로 데이터를 읽으므로 Unity Catalog 권한도 그대로 적용된다.

## 핵심 내용

- 시뮬레이션된 프로덕션 워크로드 벤치마크에서 UCDataset은 300GB 특징 테이블을 8개의 NVIDIA H100 GPU로 스트리밍해 추천 모델을 학습했고, Parquet에서 직접 읽는 방식보다 학습 시간을 평균 10배 단축했다.
- 표준 PyTorch 학습 루프에 그대로 들어간다. UCDataset이 이미 완성된 배치를 내놓으므로 배치 크기를 지정하지 않은 `DataLoader`로 감싸며, 예시의 16개 GPU가 각자 일치하는 행의 몫을 받으므로 샘플러나 샤딩 코드를 작성할 필요가 없다.
- 행 필터가 읽기 단계로 밀려 들어가므로 조건에 맞지 않는 행은 학습 코드에 도달하지 않고, 살아 있는 테이블을 읽으므로 따로 저장하거나 동기화하거나 보호해야 할 사본이 없다.
- 확장은 설정 변경이다. 작업은 `workload.yaml`에 기술되어 각 노드에서 `torchrun`으로 `train.py`를 실행하며, 더 많은 GPU로 학습하려면 `num_accelerators`만 바꾸면 되고 학습 코드는 그대로다.
- 패키지는 PyPI에서 설치하며(`%pip install databricks-uc-dataset`), 베타는 삭제 벡터가 있는 테이블을 포함해 Unity Catalog에 등록된 Delta 테이블을 읽는다.
- 두 가지 제약이 명시된다. 베타에서는 행 필터나 컬럼 마스크가 있는 테이블을 읽을 수 없고, 정형 테이블에 한정된다. Unity Catalog 볼륨의 비정형 파일은 로컬 캐싱을 사용하는 UCVolumeDataset이 담당하며, FILE 타입을 통한 멀티모달 지원은 준비 중이다.

## 상세

예시는 매일 새 노출이 들어오는 `main.recsys.ctr_features` 테이블로 클릭률 모델을 두 노드에 걸친 16개 GPU에서 학습하는 흐름이다. `train.py`에서 테이블을 고르고 레이블이 있는 학습 행만 남기며 모델에 필요한 컬럼만 투영하고, `workload.yaml`이 AI Runtime CLI를 통해 각 노드에서 `torchrun`으로 스크립트를 실행한다. 전체 `train.py`와 `workload.yaml`, 그리고 바로 시험해 볼 수 있는 샘플 테이블은 Unity Catalog 테이블 기반 클릭률 모델을 다루는 AI Runtime 쿡북 레시피에 공개되어 있다.

거버넌스는 내보내기를 생략한 결과다. 학습 작업이 실행 주체의 자격으로 데이터를 읽고 테이블의 Unity Catalog 권한이 Databricks의 다른 곳과 똑같이 적용되므로, 별도의 접근 제어를 유지해야 하는 내보낸 사본이 존재하지 않는다. Databricks는 베타를 사용해 보고 문서를 읽고 쿡북 레시피에서 시작한 뒤 계정 팀을 통해 피드백을 보내 달라고 요청한다.

## 참고 자료

- 원문: [Accelerate GPU training on Unity Catalog tables with UCDataset](https://www.databricks.com/blog/accelerate-gpu-training-unity-catalog-tables-ucdataset)
