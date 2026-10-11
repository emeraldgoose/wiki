---
title: "Leave the Class Path in the Rearview Mirror"
description: Netflix previews ja and its composable CLI tools (jig, jfmt, jist, jdocserver) — module-system-native, agent-friendly Java development with Maven-backed resolution and integrity by default
tags: [source, netflix, java, modules, build-tools, en]
locale: en
source_url: "https://netflixtechblog.com/leave-the-class-path-in-the-rearview-mirror-67a85b15b6be"
blog: netflix
published_date: 2026-09-18
---

# Leave the Class Path in the Rearview Mirror

**Author**: Danny Thomas, JVM Ecosystem Team
**Source**: [Netflix TechBlog](https://netflixtechblog.com/leave-the-class-path-in-the-rearview-mirror-67a85b15b6be)
**Date**: Sep 18, 2026

## Overview

Java's IDE experience is superb, but small composable command-line tools lag behind — a gap that hurts coding agents, which struggle to locate dependencies, documentation, and sources without indexing servers. Netflix's JVM Ecosystem team previews `ja`, a family of module-system-native CLI tools that makes the module descriptor the complete description of a project (dependency versions as comments beside `requires`, metadata as doc tags) and brings other-languages-style command ergonomics to Java.

## Composable tools

`ja` itself is only ergonomics and orchestration; every capability lives in a standalone tool installable in the JDK (all implement `Tool`/`ToolProvider` for in-process execution):

- **jig** — module version resolution, compilation, and assembly, emitting standard module-system arguments; bridges to and from Maven repositories with a module proxy and publishing commands.
- **jfmt** — source formatting per the Java Code Conventions adapted for modern Java; cleans up the whitespace, import-ordering, and over-qualification patterns typical of agent-written code.
- **jist** — source-aware symbol search with a grep-style interface over class files and sources, usable by agents with no indexing, LSP, or MCP.
- **jdocserver** — locally browsable API documentation.

Because tools expose supported module-system options via `OptionChecker`, `ja` can resolve arguments on their behalf, giving a seamless path from source-path modules to `jdeps`, `jlink`, and `jshell`.

## Maven foundation and integrity by default

Only a minority of top Maven Central artifacts declare explicit modules, so `ja` derives canonical module coordinates from Maven's verified reverse-domain namespaces (e.g. `pkg:maven/com.netflix/com.netflix.tools.ja`), with relocation POMs for existing modules and heuristic plus alias fallbacks. On integrity: runtime access needs (final-field mutation, native access, qualified opens) are declared as module metadata that the consuming application must explicitly authorize — otherwise resolution fails — with dependency hashes pinned in `module-info.hash` and annotation processing treated as a visible, reviewable code-generation step rather than hidden build-time execution.

## References

- [Leave the Class Path in the Rearview Mirror — original article](https://netflixtechblog.com/leave-the-class-path-in-the-rearview-mirror-67a85b15b6be)
- [ja on GitHub](https://github.com/Netflix/ja) (referenced in the post)
- [jig on GitHub](https://github.com/Netflix/jig) (referenced in the post)
- [jist project integration wiki](https://github.com/Netflix/jist/wiki/Project-Integration) (referenced in the post)
