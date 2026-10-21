---
title: "Lakeflow Designer 2026년 10월 업데이트: 새로운 기능 총정리"
description: "Lakeflow Designer에 데이터 정리(Prepare), 중복 제거(Unique), 품질 검사(Guardrails)용 새 노코드 오퍼레이터 추가, 출력 옵션 확장(머티리얼라이즈드 뷰, 테이블 병합, 파일 내보내기), 캔버스 개선(시각적 버전 히스토리, 실시간 커서 공존)."
tags: [source, databricks, lakeflow-designer, no-code, data-preparation, ko, ko]
locale: ko
source_url: "https://www.databricks.com/blog/whats-new-lakeflow-designer-october-2026-roundup"
blog: databricks
published: "2026-10-13"
---

# Lakeflow Designer 2026년 10월 업데이트: 새로운 기능 총정리

**Source**: Databricks Blog, 2026-10-13

**핵심**: 2026년 6월 GA 이후 3,000개 이상 고객이 Lakeflow Designer를 노코드 데이터 준비에 채택. 10월 업데이트가 정리, 중복 제거, 품질 검사용 새 오퍼레이터와 확장된 출력 옵션, 캔버스 개선 제공.

## 새로운 노코드 오퍼레이터

### Prepare 오퍼레이터: 데이터 정리 및 표준화
일반 변환을 단일 오퍼레이터로: 텍스트 대소문자 변경, 데이터 타입 변환, 값 치환, 공식 적용.

### Unique 오퍼레이터: 중복 레코드 제거
전체 데이터셋 또는 선택한 컬럼 전반에서 중복 제거. 어떤 레코드 유지할지 순서로 제어(예: 고객당 최신 업데이트 레코드 유지).

### Guardrails 오퍼레이터: 데이터 품질 검사 추가
워크플로에 직접 검사 추가: 누락 값, 중복, 예상치 못한 값 등. 실패한 행은 격리하거나 리뷰용으로 라우팅.

## 확장된 출력 옵션

- **머티리얼라이즈드 뷰**: 변환된 결과 영구 저장으로 빠른 다운스트림 읽기
- **테이블 병합**: SQL 작성 없이 업서트 패턴(SCD Type 1/2)
- **파일 내보내기**: 결과를 클라우드 스토리지에 기록(Parquet, CSV, JSON)
- **기존**: Delta 테이블, 뷰, 스트리밍 싱크

## 캔버스 개선

- **시각적 버전 히스토리**: 워크플로 진화 그래픽으로 확인
- **실시간 커서 공존**: 협업자 커서를 실시간으로 봄
- **파라미터화된 입력/출력**: 재사용 가능한 워크플로 템플릿

## 예정된 기능

- **Databricks Apps 통합**: Designer 워크플로를 앱에 임베드
- **전체 출력 데이터 프로파일링**: 샘플 아닌 전체 데이터셋 통계
- **Custom Report 오퍼레이터**: 워크플로에서 포맷된 리포트 생성
- **Lakebridge와 네이티브 마이그레이션 툴링**: 레거시 툴에서 마이그레이션

## 고객 임팩트

- 사용량 기반 과금, 사용자당 라이선스 없음
- 다수 고객이 레거시 노코드 툴 대비 **90% 비용 절감** 보고
- 간소화된 거버넌스, 단순화된 데이터 스택, 프로덕션까지 경로 가속화

## 소프트웨어 엔지니어를 위한 시사점

**분석가와 도메인 전문가를 위한 데이터 준비 파이프라인 구축**하는 팀에게: Lakeflow Designer가 기술 장벽 낮춤. 분석가는 드래그-앤-드롭; 엔지니어는 Unity Catalog로 거버넌스. 새 오퍼레이터가 "SQL/Python으로 드롭" 이스케이프 해치 줄여 더 많은 로직을 거버닝된 시각적 레이어에 유지.

## 참고문헌

- 원문: [https://www.databricks.com/blog/whats-new-lakeflow-designer-october-2026-roundup](https://www.databricks.com/blog/whats-new-lakeflow-designer-october-2026-roundup)
- Lakeflow Designer GA: [Databricks Blog](https://www.databricks.com/blog/lakeflow-designer-general-availability)