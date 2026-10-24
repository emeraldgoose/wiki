# Wiki authoring contract (AGENTS.md)

이 저장소에서 `content/`를 만지는 모든 에이전트에 적용된다.
상세 규칙의 원본은 **`AUTHORING.md` §5**이고, 이 파일은 그 루프의 **중단 조건**을 강제한다.

## 한 줄 규칙

**stub 생성은 작업 완료가 아니다. `gate_promote_check.py`가 통과할 때만 완료다.**

## 필수 루프 (건너뛰기 금지)

수집 대상이 N건이면 N건 각각에 대해 아래를 완주한다. "일단 stub만 만들어 두고
다음 세션"은 허용되지 않는다.

1. **수집** — `collect_articles.py ... --stubs`
   - 이 단계의 산출물은 `status: pending` stub이다. **deliverable이 아니다.**
2. **초안 채우기** — `fetch_drafts.py --kind ... --lang en --limit N --write`
   - `Draft summary auto-extracted` 스켈레톤도 **deliverable이 아니다.**
   - `--full`은 `status: pending`을 유지하므로 여전히 미완성이다.
3. **승격** — `AUTHORING.md` §5.3 1→7
   - en 스켈레톤을 실제 요약으로 다시 쓴다.
   - 주제 태그를 넣고 frontmatter를 확정한다.
   - 같은 상대 경로에 ko를 번역·요약해 쓴다. en 단독 완성은 금지.
4. **검증** — 아래 명령이 **exit 0**이 될 때까지 1~3을 반복한다.

```bash
python3 scripts/gate_promote_check.py --next --worktree  # 이번 배치의 다음 1건
python3 scripts/gate_promote_check.py --worktree         # 이번 배치 검사
python3 scripts/gate_promote_check.py --staged           # 커밋 전 검사 (hook 자동)
python3 scripts/gate_promote_check.py                    # 저장소 전체 감사
```

`--next --worktree`가 항목을 출력하는 동안에는 **작업을 끝내지 않는다.**
그 1건을 처리하고 다시 실행한다. "blocking items left: 0"이 될 때까지 반복한다.
`--worktree`는 **이번 세션에서 생성·수정한 파일만** 본다. 전체 backlog를 보려면
`--next`(플래그 없이)를 쓴다.

## 완료 정의

**이번 배치 완료** (all of):

- `python3 scripts/gate_promote_check.py --worktree` → `Gate: OK`
- `python3 scripts/gate_promote_check.py --staged` → `Gate: OK`
- `python3 scripts/check_ko_papers.py` → `errors: 0`
- `python3 scripts/wiki_builder.py` → `Build verified`
- `python3 scripts/make_index.py` → `Index generation complete`
- `git status`에 의도하지 않은 stub/untracked 문서가 없음

**저장소 전체 완료**는 `python3 scripts/gate_promote_check.py` → `Gate: OK`다.
전체 감사에 남은 레거시 항목은 숨기지 말고 경로와 개수를 보고한다.

하나라도 실패하면 완료라고 보고하지 않는다. 실패한 파일 경로와 이유를 그대로 보고한다.

## 금지

- `status: pending`, `[Content pending]`, `Draft summary auto-extracted`,
  `RAW DRAFT`가 남은 파일을 커밋·푸시하는 것.
- en만 쓰고 ko를 나중으로 미루는 것.
- `git commit --no-verify` / `git push --no-verify`로 게이트를 우회하는 것.
- fetch 실패·`extract: too few blocks`를 조용히 건너뛰고 "완료"라고 보고하는 것.
  → 해당 경로를 남기고 실패 이유를 보고한다.

## Hook

저장소에는 `.githooks/pre-commit`과 `.githooks/pre-push`가 있고,
로컬 설정은 `core.hooksPath=.githooks`다. 새 clone에서는 한 번 설치한다:

```bash
git config core.hooksPath .githooks
```

hook은 다음을 차단한다.

- 새 stub / 스켈레톤 커밋
- en 신규 문서에 ko 짝이 없는 커밋
- 승격 중인 문서의 frontmatter·태그·본문 정책 위반

## 작업 순서 (권장)

```bash
python3 scripts/gate_promote_check.py --next --worktree
# 출력된 1건을 §5.3까지 완주
python3 scripts/gate_promote_check.py --next --worktree
# ... blocking 0이 될 때까지
python3 scripts/gate_promote_check.py --worktree
python3 scripts/gate_promote_check.py --staged
python3 scripts/check_ko_papers.py
python3 scripts/wiki_builder.py
python3 scripts/make_index.py
git add -A && git commit && git push
```
