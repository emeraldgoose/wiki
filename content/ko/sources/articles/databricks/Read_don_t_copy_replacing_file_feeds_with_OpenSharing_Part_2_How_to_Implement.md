---
title: "복사하지 말고 읽으세요: OpenSharing으로 파일 피드 대체하기 - 2부 (구현 방법)"
description: "Delta 테이블을 WITH HISTORY로 공유하고 체크포인트 기반 Structured Streaming 소스로 소비하는 Databricks 간(D2D) 실습 과정을 정리한다."
tags: [source, databricks, data-engineering, opensharing, streaming, ko]
locale: ko
source_url: "https://www.databricks.com/blog/read-dont-copy-replacing-file-feeds-opensharing-part-2-how-implement"
blog: databricks
published_date: 2026-11-08
---

# 복사하지 말고 읽으세요: OpenSharing으로 파일 피드 대체하기 - 2부 (구현 방법)

**원문**: [Databricks 블로그](https://www.databricks.com/blog/read-dont-copy-replacing-file-feeds-opensharing-part-2-how-implement) · **게시일**: 2026-11-06

## 개요

전형적인 공유 방식은 제공자가 일정에 맞춰 파일을 추출해 버킷이나 SFTP로 보내고, 수신자가 새 파일을 감지해 적재하고 중복을 제거하고 처리 이력을 관리하는 흐름이다. 수정과 삭제까지 다루려면 별도 규칙이나 재조정 작업이 필요하다. 이 글은 그 사슬을 공유 Delta 테이블로 대체한다. Delta 테이블은 모든 변경의 순서 있는 이력을 보관하고, OpenSharing은 이를 복사 없이 개방형 프로토콜로 노출한다. 데이터는 제공자 스토리지에 남고 수신자는 실시간으로 읽는다.

수신자 쪽에서 달라지는 핵심은 이력 관리가 엔진으로 넘어간다는 점이다. 공유 테이블에 Structured Streaming 리더를 연결하면 Spark가 어디까지 읽었는지 체크포인트에 기록하므로, 각 실행은 직전 실행 이후 커밋된 변경만 가져온다. 수신자는 여전히 자신의 대상 테이블과 하위 로직을 관리하지만, 무엇이 새로운지 추적하는 일은 사용자 정의 파일이나 타임스탬프 규칙이 아니라 엔진의 몫이 된다. 계보와 접근 제어가 유지된 거버넌스 데이터 위에서 동작한다는 점도 그대로다.

실습은 Databricks 간(D2D) 공유를 기준으로 한다. 수신자는 Unity Catalog가 활성화된 Databricks 워크스페이스를 가지고 공유 카탈로그를 통해 테이블을 읽으며, 제공자는 이력을 포함해 테이블을 공유하므로 수신자는 이를 스트리밍 소스로 쓸 수 있다. 이어서 Databricks를 쓰지 않는 수신자로 범위를 넓히는데, 이들은 메타스토어 공유 식별자 대신 자격 증명 파일로 OpenSharing에 접속한다.

## 핵심 내용

- OpenSharing은 Delta 테이블을 개방형 프로토콜로 노출하므로, 수신자는 예약된 파일·API 추출을 적재하는 대신 테이블을 실시간으로 읽는다.
- 수신자별 추출 작업과 파일 감지, 재조정 작업이 제공자 쪽 계약에서 사라진다.
- 제공자는 공유를 WITH HISTORY로 게시한다. 이력이 없으면 수신자는 정적 스냅샷만 보게 된다.
- 수신자는 공유를 카탈로그로 마운트해 일반 테이블처럼 읽고, Unity Catalog 볼륨 같은 내구성 있는 저장소에 체크포인트를 둔 Structured Streaming을 사용한다.
- Trigger.AvailableNow는 아직 처리되지 않은 데이터를 하나 이상의 마이크로 배치로 처리한 뒤 종료하므로 예약 증분 작업에 적합하다. 대신 테이블 업데이트 트리거를 쓰면 제공자가 커밋할 때만 작업이 실행된다.
- 변경 데이터 피드는 기본 증분 읽기에는 선택 사항이지만, 수신자가 수정과 삭제를 반영해야 할 때는 필수다.
- Databricks Runtime 19 이상에서는 자동 변경 데이터 피드가 행 추적이 켜진 테이블의 변경을 질의 시점에 계산하며, Databricks 간 OpenSharing과 함께 동작한다.
- Spark를 쓰지 않는 Databricks-to-Open 수신자는 연속 스트림을 유지할 수 없어 delta-sharing 커넥터로 버전 범위별로 변경을 가져온다.

## 상세

제공자 설정은 간단하다. 수정과 삭제가 중요하면 변경 데이터 피드를 켠 원본 테이블을 만들고, WITH HISTORY로 공유에 게시하고, 공유 식별자로 수신자를 등록한 뒤 공유 권한을 부여한다. 글은 공유와 수신자 생성에 워크스페이스 관리자가 아니라 메타스토어 수준 권한이 필요하다고 짚는다. 수신자 쪽에서는 공유가 메타스토어의 제공자로 나타나고 카탈로그로 마운트되면 다른 테이블과 동일하게 다룰 수 있다.

읽기가 정말 증분인지 확인하는 근거는 대상 테이블의 커밋 이력이다. 초기 행 집합에 대해 한 번 실행하면 그대로 적재되고, 제공자에 새 행이 들어온 뒤 다시 실행하면 체크포인트가 마지막으로 읽은 버전을 기억하므로 새 행만 적재된다. 글에 나오는 예시에서는 단순 재적재라면 1,200행을 썼을 상황에서 두 번째 스트리밍 쓰기가 200행만 기록했다. 동시에 이 적재 패턴의 한계도 밝힌다. Delta Sharing을 통해 공유 테이블을 읽으면서 ignoreChanges를 쓰면 행이 다시 나올 수 있고 삭제는 전파되지 않는다. 하위 소비자가 삽입·수정·삭제를 모두 필요로 하면 공유 테이블의 변경 데이터 피드를 읽어야 한다. 일반 Delta 테이블을 직접 스트리밍할 때는 최신 Databricks 런타임이 append 전용 처리에 skipChangeCommits를 사용한다는 설명도 덧붙는다.

운영상의 차이는 글에서 상당하다고 표현한다. 고객을 새로 받아들이는 일이 SFTP 엔드포인트나 새 추출 작업을 세우는 것이 아니라 공유 접근 권한을 부여하는 일이 되고, 제공자는 단일 거버넌스 원본 테이블을 관리하며 수신자는 각자의 대상 테이블과 비즈니스 로직을 유지한다. 접근은 공유를 통해 관리되어 Databricks 간 수신자는 공유 Unity Catalog 권한을, 그 밖의 경우에는 OpenSharing 자격 증명 흐름을 쓴다. 백필은 제공자에게 옛 파일 재생성을 요청하는 대신 과거 테이블 버전을 읽으면 되고, 책임 경계도 제공자의 데이터 제품과 수신자의 하위 처리가 명확히 나뉜다.

pandas나 BI 도구, Snowflake처럼 Databricks를 쓰지 않는 수신자는 자격 증명 파일로 연결하며, 오픈소스 Spark를 쓴다면 delta-sharing 커넥터로 같은 스트리밍 읽기를 수행한다. 글은 시작 체크리스트로 끝을 맺는다. 수신자가 D2D인지 D2O인지, 스냅샷이 필요한지 증분 읽기인지 행 수준 변경 데이터인지, 공유에 이력이 포함되는지, 변경 데이터 피드를 켰는지, 어떤 런타임이나 커넥터 버전을 쓰는지, 재시도·중복·삭제·스키마 변경을 어떻게 다루는지, 운영 중 모니터링과 지원은 누가 맡는지를 확인하라고 권한다. 그리고 가장 작은 종단 간 흐름부터 검증하라고 조언한다. 공유를 만들고 초기 스냅샷을 읽은 다음, 행을 하나 삽입하고 수정하고 삭제해 수신자가 기대한 결과를 보는지 확인하는 순서다.

## 참고 자료

- 원문: [https://www.databricks.com/blog/read-dont-copy-replacing-file-feeds-opensharing-part-2-how-implement](https://www.databricks.com/blog/read-dont-copy-replacing-file-feeds-opensharing-part-2-how-implement)
