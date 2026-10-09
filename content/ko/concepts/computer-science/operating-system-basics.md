---
title: 운영체제 기초
description: "세미나 수준 개념: 프로세스, 스케줄링, 가상 메모리, 시스템 콜, 파일시스템, IPC, 동시성 기본 요소"
tags: [concept, computer-science, operating-systems, kernel, scheduling, virtual-memory, processes, filesystems, ko]
published: 2026-09-06
locale: ko
---

# 운영체제 기초

> [English version](/en/concepts/computer-science/operating-system-basics)

**운영체제**는 하드웨어를 프로그램들 사이에 다중화하면서 각자에게 자기 기계인 환상을 준다. 자기 CPU(프로세스/스레드), 자기 메모리(가상 주소 공간), 자기 디스크(파일). 커널은 가운데의 신뢰 중재자다. 모든 추상은 오버헤드 조금과 격리·공정·이식성을 맞바꾸는 거래다.

## 정의

- **커널 대 사용자 공간**: 커널은 특권 모드(ring 0)로 하드웨어와 페이지 테이블을 소유하고, 프로세스는 비특권 모드(ring 3)로 **시스템 콜**(`read`, `mmap`, `fork`, `epoll_wait`)로 요청해야 한다. 시스템 콜 경계가 곧 보안 경계다.
- **프로세스**: 주소 공간 + 자원(fd, 스레드, 자격)의 묶음 — 격리의 단위. **스레드**: 프로세스 메모리를 공유하는 스케줄 가능 스택 + 레지스터 — 실행의 단위. fork는 공간을 복사하고 exec은 프로그램을 바꾼다.
- **가상 메모리**: MMU와 페이지 테이블이 프로세스별 주소 공간을 물리 RAM에 매핑하고, 넘치면 디스크로 페이징한다. 프로그램은 연속 메모리를 보고, 파편화된 현실은 OS가 처리한다.
- **스케줄러**: 어느 실행 가능 스레드를 어느 코어에 얼마나 올릴지 정한다(Linux CFS — Completely Fair Scheduler — 가상 실행 시간을 추적해 가장 덜 받은 태스크를 고른다).
- **파일시스템 + IPC**: 권한·저널링을 갖춘 영속 명명 바이트(ext4, APFS, NTFS), 그리고 프로세스 간 통신로 — 파이프, 소켓, 공유 메모리, 시그널, 메시지 큐.

## 왜 중요한가

- **모든 성능 상한은 OS 상한이다**: 페이지 폴트, 컨텍스트 스위치(~1–10 us), TLB 빗나감, 시스템 콜 횟수가 애플리케이션 한계를 묶는다. `perf`, `strace`, `/proc`를 읽는 엔지니어는 남들이 며칠 추측할 것을 수 분에 진단한다.
- **격리가 곧 보안 모델이다**: 컨테이너(네임스페이스 + cgroup), 샌드박스, 모바일 앱 경계는 모두 OS 기본 요소의 조합이지 새 발명이 아니다. uid/capability 의미를 오해하면 탈출이 나온다.
- **동시성 의미는 커널에서 온다**: 뮤텍스, futex, 조건 변수, `epoll`/`io_uring`이 "동시"의 뜻을 정한다. 언어 런타임(Go 스케줄러, Tokio)은 커널 스케줄러와 협상하는 사용자 공간 스케줄러다.
- **자원 고갈이 흔한 장애다**: fd 누수, OOM kill, 가득 찬 디스크 저널, 좀비 누적. 한계·쿼터·백프레셔의 용량 사고가 곧 위쪽에 적용된 OS 사고다.

## 동작 원리

### 프로세스, 스레드, 스케줄러

```
fork() → 자식이 복사된 주소 공간을 받음(CoW) → exec()이 이미지 교체
clone() → 스레드가 mm·파일·fs 공유 → 스케줄러가 vruntime 순으로 다음 태스크 선택(CFS)
블로킹 시스템 콜 → 태스크 수면 → 이벤트에 깨어남 → 실행 큐 복귀
```

- **Copy-on-write**가 `fork`를 싸게 한다. 부모와 자식은 누군가 쓰기 전까지 페이지를 읽기 전용 공유하므로, 스폰 비용은 메모리 복사가 아니라 페이지 테이블 작업이다.
- **CFS 공정성**: 각 태스크는 nice 가중 가상 실행 시간을 쌓고, 레드블랙 트리 맨 왼쪽(가장 덜 받은 놈)이 다음에 돈다. 고정 타임슬라이스가 아니라 지연 목표(`sched_latency_ns`)를 실행 태스크 수로 나눈다.
- **선점 + 친화도**: 타이머 틱과 웨이크업이 선점하고, `sched_setaffinity`와 NUMA 정책이 뜨거운 스레드를 메모리 곁에 둔다. 스레드를 소켓 너머로 옮기면 캐시가 무효화된다. 지역성이 곧 성능이다.

### 메모리: 페이징, 폴트, 회수

- **페이징 경로**: CPU는 VA를 TLB(빠름)나 페이지 테이블 탐색(느림)으로 PA에 번역한다. 빗나가면 폴트 핸들러가 0 페이지 매핑, 파일 페이지 읽기, 스왑인 중 하나를 하고 폴트 난 명령을 투명하게 재개한다.
- **오버커밋 + OOM**: Linux는 `malloc`을 오버커밋하고(VA를 RAM보다 많이 나눠주고), 메모리가 진짜 바닥나면 **OOM killer**가 점수 낮은 프로세스를 희생시킨다. 컨테이너는 이 거래의 범위를 정하는 cgroup 한도다.
- **만능 도구 mmap**: 파일 입출력, 공유 라이브러리, 1 GB 힙 아레나, IPC 공유 구간이 모두 페이지 테이블 매핑이다. `madvise`/`mlock`/`mprotect`가 구간별 동작을 조율한다.

### 파일, 디스크립터, IPC

- **"모든 것은 파일 디스크립터"**: 파일, 소켓, 파이프, epoll 인스턴스, 타이머 — `read/write/poll/close`의 균일 표면에 fd별 플래그(`O_NONBLOCK`, `CLOEXEC`)와 참조 카운트 수명을 얹는다.
- **입출력 모델 사다리**: 블로킹 → 넌블로킹 + `epoll` 준비 → `io_uring` 완료 큐(묶음 시스템 콜, 제로카피 경로). 한 단씩 컨텍스트 스위치나 복사를 덜어낸다. 비동기 런타임은 윗단을 얇게 감싼 것이다.
- **시그널 대 구조적 IPC**: 시그널(`SIGTERM`, `SIGCHLD`)은 손실되는 알림이지 메시지 통로가 아니다. 진짜 조율은 파이프/소켓/공유 메모리 + futex로 한다.

## 흔한 함정

1. **멀티스레드에서 fork만 하고 exec 안 하기**: `fork`에서 살아남는 스레드는 호출 스레드뿐이다. 죽은 스레드가 잡던 락은 자식에서 영원히 잠긴 채다. fork했으면 즉시 exec — 아니면 `posix_spawn`을 쓴다.
2. **파일 디스크립터 한도 무시**: 기본 `ulimit -n`(흔히 1024)에 소켓 누수가 겹치면 새벽 3시 EMFILE 장애다. `CLOEXEC`을 달고 적극 닫으며 fd 개수를 메모리처럼 본다.
3. **OOM 점수 맹목**: RAM 90%짜리 배치 잡 대신 새는 사이드카가 아니라 엉뚱한 놈이 죽는다 — `/proc/<pid>/oom_score_adj`를 보고 cgroup 한도를 의도적으로 건다.
4. **이벤트 루프에서 시스템 콜 블로킹**: 동기 DNS 조회나 버퍼 없는 읽기 하나가 다중화 연결 전부를 멈춘다. 뜨거운 경로는 넌블로킹으로, 막히는 일은 풀로 밀어낸다.
5. **fsync 혼동**: `write()`는 디스크가 아니라 페이지 캐시에 닿으면 돌아온다. 내구성은 `fsync`/`fdatasync`(파일 생성 시 디렉터리 fsync까지)가 줘야 한다. DB 명성은 정확히 이것을 처리해서 얻는다.
6. **좀비·고아 표류**: `wait()` 안 하는 부모는 좀비를 쌓는다. 이중 fork 데몬과 슈퍼바이저(systemd)가 믿음직한 회수를 위해 있다. CPU 말고 프로세스 개수를 본다.

## 관련 개념

- [[concepts/computer-science/processes-and-threads|프로세스와 스레드]] (실행 단위 심화)
- [[concepts/computer-science/virtual-memory|가상 메모리]] (페이징, TLB, 주소 번역)
- [[concepts/computer-science/concurrency-vs-parallelism|동시성 대 병렬성]] (스케줄러가 다중화하는 대상)
- [[concepts/computer-science/caching|캐싱]] (OS 캐시 계층으로서의 페이지 캐시)

## 참고 문헌

- Tanenbaum & Bos — *Modern Operating Systems* (개념, 스케줄링, 메모리, 파일)
- Love — *Linux Kernel Development*, Bovet & Cesati — *Understanding the Linux Kernel*
- Arpaci-Dusseau & Arpaci-Dusseau — *Operating Systems: Three Easy Pieces* (무료, ostep.org)
- Kerrisk — *The Linux Programming Interface* (시스템 콜·시그널·IPC 레퍼런스)
- Corbet, Rubini & Kroah-Hartman — *Linux Device Drivers*, lwn.net 커널 기사
