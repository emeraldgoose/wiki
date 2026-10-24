# 승격 진행 트래킹

이 파일은 더 이상 수동으로 갱신하지 않는다. 승격 상태의 단일 기준은
`scripts/gate_promote_check.py`다.

```bash
python3 scripts/gate_promote_check.py --next --worktree  # 이번 배치의 다음 1건
python3 scripts/gate_promote_check.py                    # 저장소 전체 backlog
```

- `stub` = `status: pending` / `[Content pending]`
- `draft` = `Draft summary auto-extracted` / `RAW DRAFT`
- 둘 다 미완성이며, en/ko 짝이 없어도 미완성이다.
- 자세한 절차는 `AUTHORING.md` §5, 중단 조건은 `AGENTS.md`를 따른다.
