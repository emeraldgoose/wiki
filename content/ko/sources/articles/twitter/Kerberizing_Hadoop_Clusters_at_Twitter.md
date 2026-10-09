---
title: Twitter Hadoop 클러스터의 Kerberos 적용기
description: 수십 개 Hadoop 클러스터에 HDFS 무중단으로 Kerberos 인증을 도입한 방법
tags: [source, twitter, x, hadoop, kerberos, security, sre, ko]
locale: ko
source_url: "https://blog.x.com/engineering/en_us/topics/infrastructure/2023/kerberizing-hadoop-clusters-at-twitter"
blog: twitter
date: '2023-02-23'
---

# Twitter Hadoop 클러스터의 Kerberos 적용기

## 요약

Twitter는 세계 최대급 Hadoop을 운영한다: 수십 개 클러스터, 수천 노드, 수백 페타바이트 논리 스토리지, 하루 수만 건의 MapReduce/Spark 작업이 검색·AI/ML·광고·스팸 방지를 뒷받침한다. 인가(HDFS Unix식 권한 + LDAP)와 감사(HDFS 감사 로그)는 초기부터 있었지만 강력한 *인증*이 없었다. 이 글은 정석 롤아웃이 불가능한 제약 속에서도 HDFS 무중단으로 전체 클러스터를 Kerberos화한 과정을 설명한다.

## 난관: 4가지 제약

1. **변경의 증폭** — 수백 팀이 쓰는 검증된 플랫폼이라 모든 변경이 고위험이다.
2. **고객 코드 변경이 확장 불가** — 서비스 Kerberos화 전에 수백 팀·수천 일일 작업이 모두 Kerberos 준비를 마쳐야 하는 all-or-none 전환이다(kerberized 서비스는 미인증 클라이언트를 버린다).
3. **내장 클라이언트** — 수천 인스턴스의 마이크로서비스가 Hadoop 클라이언트 라이브러리를 내장하므로, 모든 호스트에 keytab 배포 + 조율된 재시작(며칠 소요 가능)이 필요하다. 단일 "플래그 데이"는 불가능하다.
4. **순환하는 클러스터 간 의존성** — 복제 작업(목적지 클러스터 작업이 원본을 읽음)과 ViewFS 다중 클러스터 경로 때문에 한 클러스터만 Kerberos화하면 교차 작업이 깨진다. 의존성 그래프에 사이클이 있어 안전한 순서가 존재하지 않았다.

기각된 대안: fail-open/화이트리스트(강한 인증 무력화, 우회 조장, Hadoop 기본 기능 아님), Kerberos 클러스터 병렬 구축(마이그레이션 long-tail + CapEx/OpEx, 교차 클러스터 문제는 여전), 모든 Hadoop RPC 프록시 경유(인증 문제를 옮길 뿐, 교차 문제는 여전).

## 빌딩 블록

- **KDC 스케일아웃** — 수만 서비스 principal, 수천 클라이언트 principal, 수백 추가 auth QPS를 마스터 KDC 튜닝 + 레플리카로 흡수.
- **keytab 생성·안전 배포 서비스**를 플랫폼 보안 팀과 구축하고, 호스트별 keytab API와 셀프서비스 웹 UI 제공.
- **NameNode principal 설계** — 폭발 반경 축소를 위해 기본은 호스트별 principal을 쓰되, HA NameNode 쌍은 동일 서비스 principal 공유(예: `namenode/hadoopClusterOne@DOMAIN`). 수천 클라이언트가 연결된 상태의 장애조치(failover)가 KDC를 서비스 티켓 요청으로 범람시키는 것을 방지한다.

## 롤아웃 전략

핵심은 Hadoop 내장 설정 `ipc.client.fallback-to-simple-auth-allowed=true`이다. 클라이언트와 서비스 양쪽에 설정하면 kerberized 클라이언트가 비-kerberized 클러스터와 계속 통신하므로, **한 번에 한 클러스터씩** Kerberos화할 수 있다(kerberized 클러스터에서 실행되어 비-kerberized 원본을 읽는 DistCp는 계속 동작). 반대 방향(비-kerberized 클러스터 작업이 kerberized 데이터를 읽음)은 실패하는데, Kerberos 티켓이 아니라 Task가 KDC 재인증 없이 NameNode를 호출하게 하는 **위임 토큰(delegation token)** — ResourceManager가 갱신 — 을 경계 너머에서 받을 수 없기 때문이다. 팀은 `FileSystem.getTargetFileSystem(Path)` API를 추가해 입출력 파일시스템을 명시적으로 구분하고 올바른 클러스터에서 토큰을 받게 했다.

추가 전술: keytab 자동 로그인 래핑(`UserGroupInformation.loginUserFromKeytab`, 수십만 애플리케이션이 클라이언트 라이브러리 교체만으로 대응), Kerberos화 순서 *클라이언트 → DataNode/NodeManager → NameNode/ResourceManager/History 서버*(역순은 대규모 중단 유발), HDFS 감사 로그로 미전환 잔여 추적(보통 10팀 미만), 항상 롤백 플랜 보유.

## 결과

HDFS 무중단, 최소한의 YARN 중단(ResourceManager 전환 시점의 진행 중 작업은 실패 후 자동 재시도로 성공)으로 전체 Hadoop 클러스터 Kerberos화. 최대 민감 데이터 플랫폼에 강력한 인증 적용.

## SW 엔지니어를 위한 시사점

- 플릿 단위 인증 마이그레이션은 플래그 데이보다 *호환 폴백* 중간 상태를 선호하고, 클라이언트 우선·서버 나중에 롤아웃한다.
- HA 쌍의 공유 서비스 principal은 폭발 반경 확대와 KDC 생존 사이의 의도적·문서화된 트레이드오프다.
- Hadoop에서는 Kerberos 티켓뿐 아니라 위임 토큰이 두 번째 인증 시스템이다. 혼합 모드 롤아웃은 토큰 갱신 경계에서 깨진다.
- 감사 로그는 마이그레이션 트래커로도 쓸 수 있다: 미인증 접속 주체를 조회해 소유자에게 직접 연락한다.

## 참고

- 원문: https://blog.x.com/engineering/en_us/topics/infrastructure/2023/kerberizing-hadoop-clusters-at-twitter (Ashwin Poojary, Sampath Kumar, Santosh Marella, 2023-02-23)
- 관련: `concepts/data-engineering/apache-kafka.md`, `concepts/infrastructure/kubernetes.md`
