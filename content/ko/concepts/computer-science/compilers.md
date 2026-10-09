---
title: 컴파일러
description: "세미나 수준 개념: 렉싱, 파싱, 의미 분석, IR, 최적화, 코드 생성, JIT 대 AOT, LLVM"
tags: [concept, computer-science, compilers, llvm, parsing, jit, optimization, programming-languages, ko]
published: 2026-09-06
locale: ko
---

# 컴파일러

> [English version](/en/concepts/computer-science/compilers)

**컴파일러**는 소스 코드를 실행 가능한 형태(기계어, 바이트코드, 다른 언어)로 번역한다. 렉싱, 파싱, 의미 분석, 중간 표현, 최적화, 코드 생성의 파이프라인을 거친다. 이 파이프라인 구조가 언어를 이식 가능하게 한다. 프론트엔드는 문법을 알고, 백엔드는 기계를 알며, 공유 IR 덕분에 M개 언어가 N개 아키텍처를 M×N이 아니라 M+N개 부품으로 노린다.

## 정의

- **렉서(스캐너)**: 문자를 토큰(`if`, 식별자, 리터럴)으로 바꾼다. 정규 규칙으로 동작하고, 깨진 입력은 정확한 위치와 함께 일찍 거부한다.
- **파서**: 토큰을 문법(LL, LR, PEG)으로 추상 구문 트리(AST)로 바꾼다. 우선순위와 결합 법칙을 인코딩한다. `1 + 2 * 3`은 `1 + (2 * 3)`이어야 한다.
- **의미 분석**: 문법을 넘는 의미를 검사한다. 타입 일치, 이름 해석, 소유권/borrow 규칙(rustc). 출력은 타입이 붙은 주석 트리다.
- **중간 표현(IR)**: 소스와 기계 사이의 이식 가능·분석 가능한 형태(LLVM IR, JVM 바이트코드, MIR). 최적화는 여기서 목표 기계와 무관하게 돈다.
- **옵티마이저 + 백엔드**: IR을 변환(인라이닝, 루프 최적화, 죽은 코드 제거, 레지스터 할당, 명령 선택)하고 특정 ISA(x86-64, ARM64)의 기계어를 낸다.

## 왜 중요한가

- **성능이 여기 산다**: `-O0`와 `-O3` 차이는 흔히 2–10배다. 인라이닝, 벡터화, 탈출 분석이 깔끔한 고급 코드를 손튜닝 C처럼 돌릴지 인터프리터처럼 돌릴지 가른다.
- **이식성은 컴파일러 트릭이다**: C, C++, Rust, Swift, Julia가 모두 LLVM 백엔드를 탄다. 프론트엔드 하나를 쓰면 타깃은 열두 개가 따라온다. IR 경계는 시스템 소프트웨어에서 가장 성공한 인터페이스다.
- **오류는 UX 표면이다**: borrow 검사기 진단, TypeScript의 즉시 피드백, Elm의 유명한 메시지는 의미 분석 설계 선택이다. 컴파일러는 모든 언어의 첫 스승이다.
- **보안은 여기서 강제된다**: 스택 카나리, CFI, 새니타이저(ASan/UBSan), WASM 샌드박싱은 컴파일러가 삽입한다. 최신 툴체인이 취약점 완화의 절반이다.

## 동작 원리

### 처음부터 끝까지 파이프라인

```
소스 → 렉서 → 토큰 → 파서 → AST → 의미 분석 → 타입 트리
  → 저하(lowering) → IR (SSA) → 최적화 패스 → 선택/할당 → 기계어 → 링커 → 바이너리
```

- **저하**는 풍부한 구조(async/await, 패턴 매칭, 클로저)를 단계별로 단순 IR 노드로 풀어낸다(Rust: AST → HIR → MIR, Swift: AST → SIL → LLVM IR).
- **SSA(정적 단일 할당)**: 각 변수는 정확히 한 번 할당된다(`x1`, `x2`, …). 제어 흐름 합류는 파이 노드가 잇는다. 거의 모든 데이터 흐름 분석(상수 전파, 활성, CSE)이 SSA 위에서 더 단순하고 빠르다.
- **대표 패스**: 작고 뜨거운 호출을 인라인, 셀 수 있는 루프를 풀고 벡터화, 죽은 코드·중복 로드 제거(GVN/CSE), 루프 불변 끌어올리기, 그래프 채색(Chaitin)이나 선형 스캔(JIT)으로 레지스터 할당.

### 문법과 파싱 전략

| 전략 | 방향 | 위력 / 용도 |
|---|---|---|
| 재귀 하강 / PEG | 하향식, 손작성 | 단순하고 오류 메시지 우수. Go, TypeScript 파서 |
| LL(k) | 하향식, 표/예측 | ANTLR 생성. 전방주시 정리된 문법 필요 |
| LR / LALR | 상향식, 이동-축소 | yacc/bison 계보. 좌재귀를 자연스럽게 처리 |
| 실전 LR(1) / LALR | 상향식 | Rust LALRPOP, Go goyacc 계보 |

- 실제 언어는 실용적으로 속인다. C++ 파싱은 파싱 도중 이름 해석이 필요하고(lexer hack 계보), Rust 문법은 `<`(제네릭 대 비교) 앞에서 문맥 의존적이다. 상용 파서는 오류 복원을 넣어 오타 하나가 메시지 백 개로 번지지 않게 한다.

### AOT 대 JIT

- **AOT**: 출하 전에 전부 컴파일(rustc, clang, Go). 예측 가능하고 최대 최적화, 빌드는 느리다. 런타임이 금지된 곳(커널, 임베디드, iOS)에 필수다.
- **JIT**: 실행 중 프로파일로 뜨거운 경로만 컴파일(HotSpot, V8, PyPy). 계층 실행 — 인터프리트하고, 기준 컴파일하고, 뜨거운 1%는 추측 인라이닝과 탈최적화 가드로 최적화한다.
- **혼합이 지배한다**: Java AOT 캐시 + JIT, V8의 자바스크립트 바이트코드 캐싱, PGO(프로파일 안내 최적화)로 상용 프로파일을 AOT 빌드에 되먹이기.

## 흔한 함정

1. **-O0 벤치마크**: 최적화 안 된 빌드를 재고 "Rust가 느리다" 결론내기. 언어를 판단하기 전에 릴리스/LTO/PGO 빌드를 현실 입력으로 잰다.
2. **잔꾀로 옵티마이저와 싸우기**: 벡터화를 막는 손풀기 루프와 `volatile` 꼼수. 셀 수 있는 단순 루프를 쓰고 추측 말고 어셈블리를 본다(`cargo asm`, Compiler Explorer).
3. **정의되지 않은 동작 의존**: C/C++의 부호 오버플로 트릭과 범위 밖 사용은 -O2에서 "정확히" 잘못 컴파일된다. 옵티마이저는 UB가 절대 없다고 가정한다. CI에서 UBSan/ASan을 돌린다.
4. **문자열 빌드 플래그**: `-O2`, LTO, target-cpu 조율 없이 출하하면서 소스만 손으로 튜닝하기. 툴체인 플래그가 가장 싼 2배다. 빌드 시스템에 고정한다.
5. **컴파일 시간 예산 무시**: 20분 클린 빌드는 반복을 죽인다. 크레이트 분리, 캐시(sccache), `-ftime-trace`/`-Z self-profile` 측정이 언어 탓보다 먼저다.
6. **경고를 잡음으로 취급**: `-Wall -Werror`와 Clippy/린트가 테스트가 놓치는 버그를 잡는다. 경고 없는 빌드는 허영이 아니라 기능이다.

## 관련 개념

- [[concepts/computer-science/big-o-notation|Big-O 표기법]] (옵티마이저가 노리는 비용 모델)
- [[concepts/computer-science/graphs|그래프]] (제어/데이터 흐름의 그래프 문제)
- [[concepts/computer-science/trees|트리]] (AST, 파스 트리)
- [[concepts/computer-science/processes-and-threads|프로세스와 스레드]] (컴파일된 바이너리의 실행 중 모습)

## 참고 문헌

- Aho, Lam, Sethi & Ullman — *Compilers: Principles, Techniques, and Tools* (드래곤 북)
- Cooper & Torczon — *Engineering a Compiler* (최신 패스 구조, SSA)
- Lattner & Adve, "LLVM: A Compilation Framework for Lifelong Program Analysis" (CGO 2004)
- Rustc Guide (rustc-dev-guide), V8 설계 문서(TurboFan/Ignition 계층), LLVM LangRef
- Appel — *Modern Compiler Implementation* (단일 패스와 함수형 관점)
