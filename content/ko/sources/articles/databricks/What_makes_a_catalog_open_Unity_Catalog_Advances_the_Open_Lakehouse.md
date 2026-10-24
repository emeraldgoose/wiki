---
title: "오픈 카탈로그란 무엇인가? Unity Catalog가 여는 오픈 레이크하우스"
description: "데이터 이동 없이 테이블을 등록·해제할 수 있는 Iceberg REST 카탈로그 표준과 Unity Catalog의 의미를 설명합니다."
tags: [source, databricks, data-engineering, unity-catalog, ko]
locale: ko
source_url: "https://www.databricks.com/blog/what-makes-catalog-open-unity-catalog-advances-open-lakehouse"
blog: databricks
published_date: 2026-10-19
---

# 오픈 카탈로그란 무엇인가? Unity Catalog가 여는 오픈 레이크하우스

**원문**: [databricks](https://www.databricks.com/blog/what-makes-catalog-open-unity-catalog-advances-open-lakehouse) · **게시일**: 2026-10-19

## 개요

거의 모든 플랫폼이 오픈 포맷을 지원하지만, 카탈로그가 진짜 오픈이라는 것은 무엇일까요? 오픈 카탈로그는 데이터를 고객이 소유한 스토리지에 두고, 그곳에서 최고의 기능을 제공하며, 데이터 이동 없이 테이블을 다른 카탈로그로 옮길 수 있는 이식성을 갖춥니다. 이식성은 오픈 레이크하우스의 핵심이지만 대부분의 카탈로그가 부족한 부분입니다.

Unity Catalog는 Apache Iceberg REST 카탈로그 사양의 REGISTER와 UNREGISTER를 모두 지원하는 첫 카탈로그입니다. 기존 Iceberg 테이블을 데이터 이동 없이 안팎으로 옮길 수 있습니다.

## 핵심 내용

- 고객 소유 스토리지에 있는 관리형 테이블은 데이터 복사 없이 이식할 수 있습니다.
- Unity Catalog는 Iceberg REST 사양의 REGISTER·UNREGISTER를 지원해 카탈로그 간 테이블 이동을 가능하게 합니다.
- 고객이 소유한 테이블에도 고급 테이블 기능을 제공합니다.
- 공급자 스토리지에 있는 테이블에만 복구 기능을 주는 다른 플랫폼과 달리, 고객 소유 스토리지에서도 데이터 복구를 지원합니다.
- 자동 최적화와 유지보수를 고객 소유 스토리지에서 적용합니다.

## 참고 자료

- 원문: https://www.databricks.com/blog/what-makes-catalog-open-unity-catalog-advances-open-lakehouse
