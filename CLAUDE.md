# CLAUDE.md

This file exists only to point at the real documents.

| Read | For |
|---|---|
| **[AGENTS.md](AGENTS.md)** | Conventions, invariants, the required note shape, the research method. **Start here.** |
| **[README.md](README.md)** | The machinery: build, front matter, citations, glossary, math. |

## The short version

Deep research into how solar eclipse computational products are computed.
Markdown in `content/`, built deterministically to `site/` by
`python tools/merge_refs.py && python tools/build.py --clean`. Requires pandoc.

Invariants the build enforces and that you must not work around:

1. Every substantive claim carries a `[@slug]` citation from a `refs.tsv`.
2. Every source carries an evidence grade.
3. Jargon carries a `[?slug]` explainer from a `terms.tsv`.
4. The site states positions, not revisions.
5. Formulas that matter are quoted, with their constants, not paraphrased.
