---
title: TCP/IP
description: "세미나 수준 개념: TCP/IP 모델, IP 라우팅, TCP 신뢰성, 핸드셰이크, 혼잡 제어, 포트와 소켓"
tags: [concept, computer-science, tcp-ip, networking, tcp, ip, congestion-control, ko]
published: 2026-09-06
locale: ko
---

# TCP/IP

**TCP/IP**는 인터넷의 프로토콜 묶음이다. **IP**는 호스트 간 패킷을 최선형(best-effort)으로 배달하고, **TCP**는 그 위에 신뢰성·순서·혼잡 제어가 보장되는 바이트 스트림을 구축한다. 분산 시스템의 거의 모든 동작 — 지연, 처리량 붕괴, 연결 설정 비용 — 은 이 두 계층으로 거슬러 올라간다.

## 정의

- **IP(Internet Protocol)**: 출발지에서 목적지 주소로 **데이터그램**을 비신뢰·비연결형으로 배달. IPv4(32비트, 약 43억 주소, NAT로 연명)와 IPv6(128비트). 주소 지정과 **라우팅** 담당. 배달·순서·중복에 대해 보장하는 것은 아무것도 없다.
- **TCP(Transmission Control Protocol)**: IP 위의 신뢰성·순서·연결 지향 바이트 스트림. 순서 번호, 확인 응답, 재전송, 흐름 제어, 혼잡 제어를 추가한다.
- **TCP/IP 모델** (4계층): 링크 → 인터넷(IP) → 전송(TCP/UDP) → 응용(HTTP, DNS, ...). 7계층 OSI는 교육용이고, 실제로 도는 것은 4계층 모델이다.
- **UDP**: 신뢰성 없는 비연결 데이터그램 — 지연이 낮고 head-of-line 블로킹이 없다. DNS, QUIC/HTTP-3, VoIP, 게임에 사용.

## 왜 중요한가

- **신뢰성은 공짜가 아니다**: TCP의 보장은 핸드셰이크(데이터 전 1 RTT), 연결당 상태, head-of-line 블로킹을 대가로 치른다. 대가를 알면 언제 낼지(파일, API)와 언제 내지 말지(실시간 미디어, UDP 위 커스텀 프로토콜)가 보인다.
- **혼잡 붕괴는 실재한다**: 혼잡 제어가 없으면 송신자들이 라우터 버퍼를 집단으로 채워 goodput이 0으로 수렴한다. TCP 알고리즘은 인터넷의 부하 차단 시스템이다.
- **지연 계산은 여기서 시작**: 일반적인 플로우의 전송 시간은 순수 대역폭보다 RTT, 대역폭-지연 곱, 손실 복구가 지배한다.
- **분산 시스템 디버깅**은 대부분 패킷 동작 읽기다: `SYN` 플러드, 재전송, zero window, RST.

## 동작 원리

### IP: 주소 지정, 단편화, 라우팅

```
IPv4 헤더: 버전 | IHL | DSCP | 전체 길이 | 식별자 |
           플래그 + 단편 오프셋 | TTL | 프로토콜 | 체크섬 |
           출발지 IP | 목적지 IP | 옵션...
```

- **라우팅**: 각 라우터는 목적지에 대해 라우팅 테이블 최장 접두어 매칭으로 포워딩한다(AS 간은 BGP, AS 내는 OSPF/IS-IS로 테이블 구성). **TTL**은 홉마다 감소하며 무한 루프를 막는다.
- **단편화**: 링크 MTU(보통 1500 B)보다 큰 패킷은 쪼개져 목적지에서 재조립된다. 실전에서는 피하라: **Path MTU Discovery**와 MSS 클램프를 쓴다. 단편 하나를 잃으면 데이터그램 전체가 죽고(손실 증폭), 방화벽/DDoS의 단골 골칫거리다.
- **NAT**: 사설 → 공인 주소/포트를 재작성해 IPv4를 연명한다. 종단 간 연결성을 깨뜨리므로(P2P용 STUN/TURN/ICE의 존재 이유) 인바운드 연결엔 포트 포워딩이 필요하다.

### TCP: 핸드셰이크, 신뢰성, 종료

```
연결:   SYN → / SYN-ACK ← / ACK →        (데이터 전 1 RTT)
데이터: SEQ=n, len=k → / ACK=n+k ←       (누적 ACK)
종료:   FIN → / ACK ← / FIN ← / ACK →    (또는 RST로 강제 종료)
```

- **순서 번호**: 모든 바이트에 번호가 붙고, 수신자는 다음 기대 바이트를 ACK한다. 중복·역순은 흡수하고, 빈틈은 재전송을 일으킨다.
- **재전송**: 타임아웃 시(RTO, 평활 RTT + 분산으로 계산) 또는 중복 ACK 3회(fast retransmit). **SACK**(선택적 ACK)은 도착한 블록을 정확히 보고해 이미 도착한 것의 재전송을 피한다.
- **흐름 제어**: 수신자가 `rwnd`(수신 윈도우)를 광고하고 송신자는 이를 초과하지 않는다 — 느린 수신자를 보호한다.
- **연결 상태 비용**: 소켓마다 송수신 버퍼, 타이머, 순서 상태가 있다. 능동 종료 후 **TIME_WAIT**(2×MSL, 보통 60초)은 지연 도착 세그먼트가 새 연결을 오염시키는 것을 막지만, 고회전 부하에서 ephemeral 포트를 고갈시킨다.

### 혼잡 제어

- 핵심 아이디어: **cwnd**(혼잡 윈도우) 유지, 실효 윈도우 = `min(cwnd, rwnd)`. 용량을 탐색하고 손실 시 후퇴한다.
- **Slow start**: 손실이나 ssthresh까지 지수 성장(RTT마다 cwnd 2배) — 새 연결의 ramp-up 방식.
- **혼잡 회피**: AIMD — RTT마다 가산 증가, 손실 시 승산 감소(고전 Reno는 손실 시 cwnd 반감). 이 톱니 파형이 TCP 처리량의 시그니처다.
- **현대 변형**: CUBIC(Linux 기본, 마지막 손실 이후 시간의 3차 함수로 윈도우 성장, high-BDP 경로에 강함), BBR(Google, 손실 반응 대신 병목 대역폭+RTT를 모델링 — 손실 많은/버퍼블로트 경로에 유리, 커널 ≥ 4.9).
- **대역폭-지연 곱(BDP)**: `최대 처리량 = 윈도우 / RTT`. 100 Mbps 링크에 RTT 100 ms면 ~1.25 MB 윈도우가 필요 — 원래 64 KB 상한을 뚫는 윈도우 스케일링(RFC 7323)이 존재하는 이유다.

### 포트와 소켓

- 연결은 4-튜플(출발지 IP, 출발지 포트, 목적지 IP, 목적지 포트)로 식별된다. 0–1023은 well-known(80/HTTP, 443/HTTPS, 22/SSH), 49152–65535는 ephemeral(클라이언트 측).
- `listen()` 백로그, `accept()` 큐 오버플로, `SYN` 쿠키(SYN 플러드 하의 스푸핑 방지 핸드셰이크)가 TCP 서버의 운영 표면이다.

## 흔한 함정

1. **고RTT 링크의 잘게 끊는 프로토콜**: 순차 요청-응답 N회는 대역폭과 무관하게 N×RTT가 든다. 파이프라이닝·배치·다중화(HTTP/2, QUIC)를 쓴다.
2. **너무 작은 송수신 버퍼**: 기본 소켓 버퍼는 high-BDP 경로에서 처리량을 옥죈다. 버퍼를 BDP 이상으로(`SO_RCVBUF`/`SO_SNDBUF`, 시스템 `rmem_max`/`wmem_max`).
3. **TIME_WAIT 고갈**: 단명 연결 회전(프록시, 크롤러)은 목적지당 ~2.8만 개 ephemeral 포트를 태운다. keep-alive, 연결 풀, 다중 egress IP로 해결 — `tcp_fin_timeout`을 무모하게 0으로 만드는 게 아니다.
4. **맹목적인 Nagle 끄기**: `TCP_NODELAY`는 지연 민감 RPC에 좋지만 소량 쓰기 워크로드를 패킷 홍수로 바꾼다(수 바이트 페이로드에 40바이트 헤더). 플래그를 반사적으로 건드리지 말고 작은 쓰기를 배치하라.
5. **손실/지연 신호 무시**: 고전 Reno는 모든 손실을 혼잡으로 취급해서 손실 많은 링크(Wi-Fi, 대륙 간)에서 활용률이 처참하다. CUBIC/BBR을 쓰고 측정하라.
6. **순서·정확히 한 번 배달의 합성 착각**: TCP 보장은 연결당이다. TCP 위 앱 재시도는 여전히 *요청*을 중복시킬 수 있다(잃어버린 게 요청이 아니라 응답일 수 있음) — 멱등 키는 여전히 필요하다.

## 관련 개념

- [[concepts/computer-science/http|HTTP]] (TCP/TLS 위 응용 계층, QUIC/UDP 위 HTTP/3)
- [[concepts/computer-science/processes-and-threads|프로세스와 스레드]] (연결당 스레드 비용, 소켓 처리)

## 참고 문헌

- RFC 791 (IPv4), RFC 8200 (IPv6), RFC 9293 (TCP, 793 대체), RFC 7323 (윈도우 스케일링), RFC 8985 (BBR 개요, draft-cardwell 경유)
- Stevens — *TCP/IP Illustrated, Vol. 1*; Stevens/Fenner/Rudoff — *UNIX Network Programming, Vol. 1*
- Linux man pages: `tcp(7)`, `ip(7)`, `socket(7)`, `ss(8)`
- Van Jacobson (1988) — "Congestion Avoidance and Control" (기초 논문)
