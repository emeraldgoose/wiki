---
title: HTTP
description: "세미나 수준 개념: HTTP 메서드, 상태 코드, 헤더, 캐싱, 버전 1.1부터 3까지, 쿠키, TLS"
tags: [concept, computer-science, http, web, rest, tls, http2, http3, ko]
published: 2026-09-06
locale: ko
---

# HTTP

> [English version](/en/concepts/computer-science/http)

**HTTP**(Hypertext Transfer Protocol)는 웹의 요청-응답 응용 프로토콜이다. 클라이언트가 메서드·대상·헤더·선택적 본문을 보내면, 서버가 상태·헤더·선택적 본문으로 답한다. 모든 API, 페이지 로드, 웹훅은 이 문법의 대화다.

## 정의

- **메시지 모델**: 전송 계층 위의 무상태 요청/응답(1.1/2는 TCP, 3은 QUIC/UDP). 각 요청은 독립적이고, 상태는 그 위에 얹는다(쿠키, 토큰).
- **메서드 + 대상 + 버전**: 예. `GET /users/42 HTTP/1.1`. 메서드는 의도를, 대상은 자원을 나타낸다.
- **상태 코드**(서버의 판결, 첫 자리로 그룹화): 1xx 정보, 2xx 성공, 3xx 리다이렉션, 4xx 클라이언트 오류, 5xx 서버 오류.
- **헤더**: 확장 가능한 `이름: 값` 메타데이터(콘텐츠 협상, 인증, 캐싱, 압축). 본문은 `Content-Type`/`Content-Length`(또는 청크 프레이밍)로 기술되는 불투명 바이트다.

## 왜 중요한가

- **보편적 API 기반**: REST, GraphQL, 웹훅, OAuth 플로우, LLM API가 모두 HTTP 의미론이다. 메서드/상태/헤더 리터러시는 그 무엇을 설계·디버깅하든 전제 조건이다.
- **성능은 프로토콜이 빚는다**: 연결 재사용, 다중화, 헤더 압축, 캐싱 지시어가 서버 코드보다 페이지·API 지연을 더 좌우한다.
- **정확성 계약이 여기 산다**: 메서드의 멱등성, 캐시 가능성 규칙, 상태 코드 의미에 중간자(CDN, 프록시, 브라우저)가 반응한다 — 오용하면 체인 전체가 깨진다.
- **보안 경계**: 쿠키/SameSite/CORS/TLS 동작이 이 계층에서 정의된다. 여기서의 설정 오류가 가장 흔한 웹 취약점이다.

## 동작 원리

### 메서드와 계약

| 메서드 | 안전 | 멱등 | 캐시 가능 | 의미 |
|---|---|---|---|---|
| GET | ✓ | ✓ | ✓ | 표현 조회 |
| HEAD | ✓ | ✓ | ✓ | 본문 없는 GET (존재, 크기 확인) |
| POST | ✗ | ✗ | ✗ (대체로) | 일반 액션/생성 |
| PUT | ✗ | ✓ | ✗ | 대상 URI 자원 교체 |
| DELETE | ✗ | ✓ | ✗ | 자원 삭제 |
| PATCH | ✗ | ✗* | ✗ | 부분 수정 (*설계에 따라 멱등 가능) |
| OPTIONS | ✓ | ✓ | ✗ | CORS 프리플라이트/기능 탐색 |

- **안전** = 상태 변경 없음(읽기 전용). **멱등** = 동일한 요청 N회 ≡ 1회(재시도 안전). 자동 재시도는 멱등 메서드에만 — POST에는 멱등 키를 쓴다.
- PUT vs PATCH vs POST 선택은 취향이 아니라 캐시·재시도 계층과의 계약이다.

### 외워둘 상태 코드

- `200 OK`, `201 Created`(`Location` 반환), `204 No Content`(성공, 빈 본문).
- `301` vs `302` vs `307` vs `308`: 301/302는 역사적으로 메서드 재작성(GET으로)을 허용했고(POST→GET 놀람), 307/308은 메서드를 보존한다. 레거시 동작을 명시적으로 원하지 않으면 307/308을 쓴다.
- `304 Not Modified`(조건부 GET 적중 — 재검증), `400`(형식 오류), `401`(미인증 — "누구요"), `403`(권한 없음 — "알지만 안 돼요"), `404`, `409 Conflict`(상태 충돌, 예. 버전 불일치), `422`(형식은 맞지만 의미상 불가), `429`(호출 제한 — `Retry-After` 준수).
- `500`(버그/크래시), `502`(업스트림 고장), `503`(일시 과부하 — 백오프로 재시도 가능), `504`(업스트림이 너무 느림).

### 웹을 굴리는 헤더들

- **콘텐츠 협상**: `Accept`, `Accept-Encoding: gzip, br`, `Content-Type`, `Content-Length` / `Transfer-Encoding: chunked`.
- **캐싱**: `Cache-Control: max-age=3600, must-revalidate`, `ETag` + `If-None-Match`, `Last-Modified` + `If-Modified-Since`, `Vary: Accept-Encoding`(압축 변형을 내주는 CDN에서 필수).
- **인증**: `Authorization: Bearer <token>`, 401에 대한 `WWW-Authenticate` 챌린지.
- **쿠키/상태**: `Set-Cookie: id=abc; HttpOnly; Secure; SameSite=Lax`, `Cookie:`로 반송. `HttpOnly`는 JS 탈취 차단, `Secure`는 HTTPS 강제, `SameSite`는 크로스사이트 전송 제한(CSRF 방어).
- **CORS**: `Origin` + `Access-Control-Allow-Origin`, 비-단순 요청의 프리플라이트 `OPTIONS`. 서버 측 허용 목록이며 브라우저가 강제한다.

### 버전: 1.1 → 2 → 3

```
1.1: TCP 연결 × N, 순차 요청, HOL 블로킹, 텍스트 헤더
2:   TCP 연결 1개, 이진 프레임, 다중화 스트림, HPACK 헤더 압축,
     서버 푸시(대체로 폐기), 그래도 TCP 수준 HOL 블로킹 잔존
3:   UDP 위 QUIC, TCP HOL 없는 스트림, 0-RTT 재개,
     QPACK, TLS 1.3 필수
```

- **HTTP/1.1**(1997, RFC 9112): 지속 연결(keep-alive) + 파이프라이닝(잘 안 쓰이고 깨지기 쉬움). 실질적으로 연결당 요청 1개 → 브라우저가 오리진당 6개 연결을 열었고 "도메인 샤딩" 시대가 있었다.
- **HTTP/2**(2015, RFC 9113): 다중화가 6-연결 꼼수를 죽임. HPACK이 반복 헤더(쿠키 많은 트래픽)를 줄임. 패킷 하나가 느려지면/잃어버리면 모든 스트림이 멈춤(TCP HOL) — 3의 동기다.
- **HTTP/3**(2022, RFC 9114): QUIC의 스트림별 흐름 제어·손실 복구, IP 변경에도 살아남는 연결 마이그레이션(모바일 핸드오프), 0-RTT로 이전 연결을 빠르게 재개(재전송 위험 — 멱등 요청에만).
- 협상: TLS 핸드셰이크 중 ALPN(`h2`, `h3`). 평문 HTTP/2(h2c)도 있지만 브라우저는 TLS를 요구한다.

### HTTPS/TLS 한 문단 요약

- TLS 1.3 핸드셰이크는 암호 협상, X.509 체인으로 서버 인증, 세션 키 도출(1 RTT, 재개 시 0-RTT). HTTP는 암호 터널 안에서 그대로 돈다. 혼합 콘텐츠(HTTPS 페이지가 HTTP 하위 자원 로드)는 보안 보장을 깨고 브라우저가 차단한다.

## 흔한 함정

1. **부수 효과 있는 GET**: 크롤러·프리페처·재시도 계층은 GET이 안전하다고 가정한다. `GET /delete-account`는 언젠가 의도하지 않은 무언가에 의해 호출된다.
2. **멱등 키 없는 POST 재시도**: 타임아웃된 POST는 서버에서 성공했을 수 있다(잃어버린 건 응답). 재시도는 중복을 만든다 — 결제, 주문, 행. 연산을 멱등하게 만들거나 `Idempotency-Key`를 붙인다.
3. **잘못된 리다이렉트 코드**: 307 자리 302는 일부 클라이언트에서 POST→GET으로 조용히 바뀌고 본문이 증발한다. 의도적으로 선택하라.
4. **콘텐츠 협상 누락된 `Vary`**: `Vary: Accept-Encoding` 없이 gzip과 평문을 한 캐시 키로 내주면 CDN 캐시가 일부 클라이언트에 잘못된 변형을 먹인다(캐시 오염).
5. **인증 응답 캐싱**: 사용자별 응답에 `Cache-Control: public`을 붙이면 공유 캐시를 통해 남의 데이터가 샌다. 개인화 콘텐츠는 기본 `private, no-store`, 진짜 공유 자산에만 `public`.
6. **백오프/지터 없는 5xx 재시도**: 503에 함대가 일제히 재시도하면 자작 DDoS(재시도 폭풍)다. 지수 백오프 + 지터 + 서킷 브레이커가 완전한 답이다.
7. **CORS 프리플라이트 비용 무시**: 크로스 오리진 `PUT`/`DELETE`/JSON POST마다 OPTIONS 1왕복이 추가된다. 가능하면 동일 오리진, 아니면 RTT를 예산에 넣는다.

## 관련 개념

- [[concepts/computer-science/tcp-ip|TCP/IP]] (HTTP 아래 전송 계층, HTTP/3의 QUIC/UDP)
- [[concepts/computer-science/caching|캐싱]] (HTTP 캐시 지시어, CDN 동작, ETag 검증)

## 참고 문헌

- RFC 9110 (HTTP 의미론), RFC 9111 (캐싱), RFC 9112 (HTTP/1.1), RFC 9113 (HTTP/2), RFC 9114 (HTTP/3), RFC 9000 (QUIC)
- Fielding (2000) — "Architectural Styles and the Design of Network-based Software Architectures" (REST 학위논문)
- MDN Web Docs — HTTP 레퍼런스 (메서드, 상태 코드, 헤더, CORS)
