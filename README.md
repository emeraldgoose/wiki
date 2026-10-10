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

## Docs

- `AUTHORING.md` — authoring guide: file layout, frontmatter, collecting
  articles/papers, common mistakes.
- `scripts/` — `site_css.py` + `portal.js` + `zoom.js` are the sources of
  truth for styling and portal interactivity; never edit the built copies
  under `static/`.
