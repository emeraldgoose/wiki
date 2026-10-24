# Arkive Wiki

Bilingual (en/ko) static knowledge archive. Markdown in `content/` builds to
plain HTML in `static/` with stdlib-only Python scripts — no dependencies.

## Build & preview

```bash
python3 scripts/wiki_builder.py   # content/ → static/en, static/ko
python3 scripts/make_index.py     # portal index, landing, 404, _redirects, _headers
python3 scripts/serve_wiki.py 8900  # local check: http://localhost:8900/
```

Look for `Build verified` at the end of the builder output. `static/` is
generated output (git-ignored); Cloudflare Pages rebuilds it from source.

## Authoring gate

A stub or a `fetch_drafts.py` skeleton is not a finished document. Before
committing, the loop must pass:

```bash
python3 scripts/gate_promote_check.py --next --worktree  # next item in this batch
python3 scripts/gate_promote_check.py --worktree         # this batch
python3 scripts/gate_promote_check.py                    # full repo audit
git config core.hooksPath .githooks                      # once per clone
```

`.githooks/pre-commit` and `pre-push` block stubs, unexpanded skeletons, and
new English docs without a Korean pair. See `AGENTS.md` for the contract and
`AUTHORING.md` §5.0 for the full loop.

## Docs

- `AUTHORING.md` — authoring guide: file layout, frontmatter, collecting
  articles/papers, common mistakes.
- `scripts/` — `site_css.py` + `portal.js` + `zoom.js` are the sources of
  truth for styling and portal interactivity; never edit the built copies
  under `static/`.
