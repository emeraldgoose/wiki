---
title: "Amazon EMR에서 Apache HBase 가용성 최적화, Part 2: 컴팩션 진단 및 튜닝"
description: "결정 흐름, 웹 UI 점검, 로그, canary 도구로 Amazon EMR HBase의 컴팩션 압박을 진단하고, 처리량 상한, 오프피크 시간대, S3A 읽기 정책, major compaction 일정 조정을 다룬 뒤 AWS Support 에스컬레이션 기준을 정리했다."
tags: [source, aws-big-data, apache-hbase, amazon-emr, compaction, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/optimizing-apache-hbase-availability-on-amazon-emr-part-2-diagnose-and-tune-compaction"
blog: aws-big-data
published_date: 2026-11-14
---

# Amazon EMR에서 Apache HBase 가용성 최적화, Part 2: 컴팩션 진단 및 튜닝

**원문**: [AWS 빅데이터 블로그](https://aws.amazon.com/blogs/big-data/optimizing-apache-hbase-availability-on-amazon-emr-part-2-diagnose-and-tune-compaction) · **게시일**: 2026-11-11

## 개요

컴팩션은 store 파일을 병합하는 Apache HBase 백그라운드 프로세스다. 피크 시간대에 워크로드와 경쟁하면 읽기·쓰기 지연 상승, 쓰기 정체, RegionTooBusyException 오류가 나타난다. Amazon S3 저장소를 쓰는 Amazon EMR에서는 컴팩션이 클러스터의 S3 요청 비율까지 끌어올려 503 Slow Down 응답이 늘어난다. 두 편으로 된 시리즈의 두 번째 글은 가용성에서 성능으로 주제를 옮긴다. 1부는 3단계 문제 해결 모델과 코디네이터 시작, RegionServer 비정상 종료, 전환 중 region을 다뤘고, 이번 편은 컴팩션이 원인인지 확인하는 방법, 먼저 조정할 파라미터, AWS Support에 연락할 시점을 다룬다.

파라미터를 바꾸기 전에 결정 흐름을 따른다. 지연이 높으면 해당 RegionServer에서 컴팩션이 실제로 실행 중인지 확인하고, 아니라면 가비지 컬렉션, 디스크, 네트워크를 조사한다. 컴팩션이 실행 중이고 큐가 늘어난다면 S3A 읽기 정책, 처리량 상한, 컴팩션 빈도 파라미터, 오프피크 시간대, 마지막으로 수동 major compaction 일정 조정 순서로 진행한다.

명령어를 다루려면 용어가 중요하다. Amazon EMR은 HMaster를 primary 노드에서 구동하며 이 글은 이를 HBase 코디네이터라고 부르고, master가 들어간 이름은 명령어와 로그 파일에서만 등장한다. HBase 웹 UI는 코디네이터가 16010, RegionServer가 16030 포트에서 듣고, primary와 core 노드에 대한 SSH 접근과 클러스터의 저장소 모드(HDFS 또는 Amazon S3) 파악이 사전 조건이다.

## 핵심 내용

- 기본값으로 HBase는 대략 7일(604800000밀리초)마다 major compaction을 실행하고, 지터 계수 0.5로 시작 시각을 흩뿌려 region이 한꺼번에 컴팩션되지 않게 한다. major compaction은 region의 모든 store 파일을 읽어 재작성하므로 읽기 성능을 개선하고 삭제·만료된 셀을 제거하지만 클라이언트 요청과 경쟁한다.
- 쓰기 정체는 연쇄로 온다. store가 hbase.hstore.blockingStoreFiles 개수에 도달하면 HBase는 최대 hbase.hstore.blockingWaitTime(기본 90초)까지 MemStore 플러시를 늦춘다. 그 사이 MemStore가 flush.size에 block.multiplier를 곱한 값을 넘으면 HBase는 해당 region의 업데이트를 막는다.
- Amazon S3 기반 HBase에서 컴팩션은 S3의 store 파일을 읽고 재작성하므로, 요청 비율이 높으면 클러스터에 속도를 줄이라는 503 Slow Down 응답이 더 많이 온다.
- 1단계(웹 UI) 진단: RegionServer를 요청 수와 store 파일 수로 정렬해 특이 서버를 찾고, 컴팩션 큐 길이와 region별 store 파일 수를 확인하고, BlockCache 적중률을 본다. S3 기반 HBase는 캐시 미스 시 로컬 읽기보다 느린 Amazon S3 읽기가 발생하기 때문이다.
- 2단계(로그와 OS) 진단: RegionServer 로그에서 Starting compaction, Completed compaction, too many store files를 grep하고, JvmPauseMonitor 항목으로 GC를 배제하고, free, top, df로 메모리·CPU·디스크를 점검하며, canary 도구(sudo -u hbase hbase canary my_table)를 실행해 region별 읽기 지연 기준선을 /var/log/hbase/hbase.log에 남긴다.
- Amazon S3 기반 HBase에 Amazon EMR 7.10~7.13을 쓴다면 컴팩션 파라미터를 만지기 전에 hbase-site 분류에서 fs.s3a.experimental.input.fadvise를 sequential로 설정하라. EMR 7.10부터 S3A 클라이언트가 normal을 기본값으로 하며, 이 모드에서는 HBase가 순차 읽기를 계속해도 무작위 읽기 정책으로 전환돼 컴팩션, 스캔, 벌크 로드가 느려질 수 있다. 이 변경은 HBase 재시작이 필요한 3단계 조치이고, 개별 명령에만 설정해서는 효과가 없다.
- 주요 기본값: hbase.hstore.compaction.throughput.higher.bound 104857600(초당 100MB), lower.bound 52428800(초당 50MB), compaction.min 3, compaction.max 10, compaction.min.size 134217728(128MB), ratio 1.2. hbase.hstore.blockingStoreFiles는 Apache HBase 2.x에서 16이지만 Amazon EMR은 S3 기반 HBase에 10으로 설정한다. MemStore 플러시 크기 128MB, block multiplier 4, 최대 region 크기 10737418240(10GB), 오프피크 컴팩션 비율 5.0, EMR의 hbase.bucketcache.size는 8,192MB다.
- 자동 major compaction을 끄면(hbase.hregion.majorcompaction=0) 책임이 사용자에게 옮겨진다. 유지 관리 창에 테이블별로 major_compact를 직접 예약하되 읽기 전용 복제본 클러스터에서는 수동 컴팩션을 실행하지 않아야 하고, EMR 7.4.0 미만에서는 복제본의 hbase.regionserver.compaction.enabled도 false로 설정한다. store 파일 수가 blockingStoreFiles의 약 80퍼센트에 접근하면 알람을 걸어 일정이 밀리기 전에 인지한다.
- 컴팩션 부담을 줄이는 관행: region 크기 제한(S3 기반 HBase에서 hbase.hregion.max.filesize 기본 10GB에 도달하면 분할), SPLITS 옵션이나 RegionSplitter 도구로 사전 분할, 키에 salt, hash, reverse를 적용해 row key 핫스팟 해소, 잦은 소형 MemStore 플러시 축소, 로컬 인스턴스 스토어와 EBS에 더 많은 데이터를 담도록 BucketCache 크기 조정, primary 노드를 여러 개 두어 코디네이터 생존 보장.
- AWS Support에 에스컬레이션할 때: 다음 단계가 HBCK2 bypass나 setRegionState일 때, znode를 삭제해야 할 때, 스레드 덤프 세 번 후에도 프로시저가 멈춰 있을 때, 여러 RegionServer가 동시에 멈출 때, 두 차례 튜닝에도 지연이 개선되지 않을 때, 스택 트레이스의 예외가 낯설을 때다.
- 지원 케이스에는 첫 ERROR 주변의 코디네이터 로그 발췌, 해당 core 노드의 RegionServer 로그 발췌, jstack으로 30초 간격으로 세 번 찍은 스레드 덤프, list_procedures나 Procedures and Locks 페이지의 멈춘 프로시저 식별자, 관련 region의 인코딩된 이름을 준비한다.

## 세부 사항

### 튜닝 전에 진단한다

결정 흐름은 설정 변경 전에 증상을 행동으로 연결한다. hbase-site 분류로 적용하는 설정 변경은 3단계 조치이고 EMR HBase 재시작이 필요하므로, 상호작용하는 파라미터가 여럿인 만큼 한 번에 하나씩 바꾸고 canary 기준선과 비교하라는 것이 이 글의 요지다.

### S3A 읽기 정책 수정

EMR 7.10~7.13에서 HFile 수는 계속 늘어나는데 컴팩션, 스캔, 벌크 로드가 예상보다 느리다면 원인은 컴팩션 압박이 아니라 S3A 클라이언트일 수 있다. 릴리스 라벨과 현재 fadvise 설정을 확인한 뒤 속성을 sequential로 바꾸고 HBase 코디네이터와 RegionServer 프로세스를 재시작한다. EMR 7.4 이상의 S3 기반 HBase는 디렉터리 목록 대신 store 디렉터리마다 메타 파일로 store 파일을 추적하므로, RegionServer 웹 UI의 파일 수가 활성 파일 개수다.

### 파라미터 튜닝과 일정 조정

파라미터 표는 처리량 상한, 소형 컴팩션 선정(min, max, min.size, ratio), 차단 임계값, MemStore 크기, region 크기, 오프피크 시간대, major compaction 간격과 지터, BucketCache 크기를 다룬다. 문서에 기본값이 없으면 /etc/hbase/conf/hbase-site.xml의 유효값을 확인한다. 오프피크 시간대에는 기본 5.0의 더 큰 offpeak 비율이 적용되고 별도의 offpeak 처리량 상한을 두지 않았다면 처리량 제한이 풀린다.

### 컴팩션 부담을 줄이고 멈출 줄 알기

예측 가능한 키 분포의 사전 분할, 핫스팟 분산, 플러시와 캐시 크기 조정은 애초에 클러스터가 해야 할 컴팩션 양 자체를 줄인다. 일부 복구 조작은 되돌리기 어렵다. HBCK2 bypass는 프로시저나 region을 불일치 상태로 남길 수 있고, ZooKeeper znode 삭제는 hbase:meta 위치, RegionServer 등록, store 파일 추적 상태를 버리므로, 이런 경로는 첫수단이 아니라 AWS Support와 함께 다뤄야 한다.
