---
title: Compilers
description: "Seminar-level concept: lexing, parsing, semantic analysis, IR, optimization, codegen, JIT vs AOT, LLVM"
tags: [concept, computer-science, compilers, llvm, parsing, jit, optimization, programming-languages]
published: 2026-09-06
locale: en
---

# Compilers

> [한국어 버전](/ko/concepts/computer-science/compilers)

A **compiler** translates source code into an executable form — machine code, bytecode, or another language — through a pipeline of lexing, parsing, semantic analysis, intermediate representation, optimization, and code generation. The pipeline structure is what makes languages portable: front ends understand syntax, back ends understand machines, and a shared IR lets M languages target N architectures with M+N components instead of M×N.

## Definition

- **Lexer (scanner)**: turns characters into tokens (`if`, identifiers, literals) via regular rules; rejects malformed input early with precise positions.
- **Parser**: turns tokens into an abstract syntax tree (AST) via a grammar (LL, LR, PEG). It encodes precedence and associativity — `1 + 2 * 3` must mean `1 + (2 * 3)`.
- **Semantic analysis**: checks meaning beyond syntax — types match, names resolve, ownership/borrow rules hold (rustc). Output is a typed, annotated tree.
- **Intermediate representation (IR)**: a portable, analyzable form between source and machine (LLVM IR, JVM bytecode, MIR). Optimizations run here, target-independent.
- **Optimizer + backend**: transforms the IR (inlining, loop opts, dead-code elimination, register allocation, instruction selection) and emits machine code for a specific ISA (x86-64, ARM64).

## Why It Matters

- **Performance lives here**: the gap between `-O0` and `-O3` is routinely 2–10x — inlining, vectorization, and escape analysis decide whether clean high-level code runs like hand-tuned C or like an interpreter.
- **Portability is a compiler trick**: C, C++, Rust, Swift, and Julia all ride LLVM's backends; write one front end, get a dozen targets. The IR boundary is the most successful interface in systems software.
- **Errors are a UX surface**: borrow-checker diagnostics, TypeScript's instant feedback, and Elm's famous messages are semantic-analysis design choices — a compiler is the first teacher of every language.
- **Security is enforced here**: stack canaries, CFI, sanitizers (ASan/UBSan), and WASM sandboxing are compiler-inserted. A modern toolchain is half of your exploit mitigation.

## How It Works

### The Pipeline, End to End

```
source → lexer → tokens → parser → AST → semantic analysis → typed tree
  → lowering → IR (SSA) → optimization passes → selection/allocation → machine code → linker → binary
```

- **Lowering** desugars rich constructs (async/await, pattern matching, closures) into simpler IR nodes step by step (Rust: AST → HIR → MIR; Swift: AST → SIL → LLVM IR).
- **SSA (static single assignment)**: each variable is assigned exactly once (`x1`, `x2`, …), with φ-nodes merging control-flow joins. Nearly all dataflow analysis (constant propagation, liveness, CSE) is simpler and faster on SSA.
- **Classic passes**: inline small hot callees; unroll/vectorize counted loops; eliminate dead code and redundant loads (GVN/CSE); hoist loop invariants; allocate registers by graph coloring (Chaitin) or linear scan (JITs).

### Grammars and Parsing Strategies

| Strategy | Direction | Power / use |
|---|---|---|
| Recursive descent / PEG | Top-down, hand-written | Simple, great errors; Go, TypeScript parsers |
| LL(k) | Top-down, table/predictive | ANTLR-generated; needs lookahead-factored grammars |
| LR / LALR | Bottom-up, shift-reduce | yacc/bison heritage; handles left recursion naturally |
| LR(1) / LALR in practice | Bottom-up | Rust's LALRPOP, Go's goyacc lineage |

- Real languages cheat pragmatically: C++ parsing needs name resolution mid-parse (the "lexer hack" lineage), and Rust's grammar is context-sensitive around `<` (generics vs comparison). Production parsers add error recovery so one typo does not cascade into a hundred messages.

### AOT vs JIT

- **AOT (ahead-of-time)**: compiles everything before shipping (rustc, clang, Go). Predictable, maximally optimized, slow builds; required where runtimes are forbidden (kernels, embedded, iOS).
- **JIT (just-in-time)**: compiles hot paths at runtime with live profiling (HotSpot, V8, PyPy). Tiered execution — interpret, baseline-compile, then optimize the hot 1% with speculative inlining and deoptimization guards.
- **Hybrids dominate**: Java AOT caches plus JIT, JavaScript bytecode caching in V8, PGO (profile-guided optimization) feeding production profiles back into AOT builds.

## Common Pitfalls

1. **-O0 benchmarking**: measuring unoptimized builds and concluding "Rust is slow" — always benchmark release/LTO/PGO builds with realistic inputs before judging a language.
2. **Fighting the optimizer with cleverness**: hand-unrolled loops and `volatile` hacks that block vectorization. Write simple countable loops; check the assembly (`cargo asm`, Compiler Explorer) instead of guessing.
3. **Undefined behavior reliance**: signed-overflow tricks and use-after-scope in C/C++ are miscompiled "correctly" at -O2 — the optimizer assumes UB never happens. Run UBSan/ASan in CI.
4. **Stringly build flags**: shipping without `-O2`, LTO, or target-cpu tuning while hand-tuning source. Toolchain flags are the cheapest 2x available; pin them in the build system.
5. **Ignoring compile-time budgets**: 20-minute clean builds kill iteration. Split crates, cache (sccache), and measure with `-ftime-trace` /`-Z self-profile` before blaming the language.
6. **Treating warnings as noise**: `-Wall -Werror` plus Clippy/lints catch the bugs tests miss. A warning-free build is a feature, not vanity.

## Related Concepts

- [[concepts/computer-science/big-o-notation|Big-O Notation]] (cost models optimizers target)
- [[concepts/computer-science/graphs|Graphs]] (control/data-flow as graph problems)
- [[concepts/computer-science/trees|Trees]] (ASTs, parse trees)
- [[concepts/computer-science/processes-and-threads|Processes and Threads]] (what compiled binaries become at runtime)

## References

- Aho, Lam, Sethi & Ullman — *Compilers: Principles, Techniques, and Tools* (the Dragon Book)
- Cooper & Torczon — *Engineering a Compiler* (modern pass structure, SSA)
- Lattner & Adve, "LLVM: A Compilation Framework for Lifelong Program Analysis" (CGO 2004)
- Rustc Guide (rustc-dev-guide); V8 design docs (TurboFan/Ignition tiers); LLVM LangRef
- Appel — *Modern Compiler Implementation* (single-pass and functional perspectives)
