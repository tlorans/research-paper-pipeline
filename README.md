# research-paper-pipeline

An [mdharness](https://github.com/tlorans/mdharness) project. Fill `brief.md`,
then let Grok Build (or Claude Code) walk a paper through a gated stage machine.

```
research ──▶ draft ──▶ integrity ──┐
              ▲                    │ fail (score < 8)
              └───────────────────┘
                                   │ pass
                                   ▼
                 ┐────────▶ review ──▶ finalize ──▶ done
                 │              │
                 │              │ fail (score < 7)
                 └── revise ◀───┘
```

Built with the [mdharness-pipeline](https://github.com/tlorans/mdharness-skill)
skill. Stage names follow the public map in
[Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills)
(research → write → integrity → review → revise → finalize). This repo is
**not** a port of that suite and does not vendor its files (that project is
CC BY-NC 4.0). Prompts here are original.

## Setup

```bash
git clone https://github.com/tlorans/research-paper-pipeline.git
cd research-paper-pipeline
uv sync
```

Edit `brief.md` with the topic and working question.

## Run with Grok

```bash
uv run mdharness launch grok
```

Headless:

```bash
uv run mdharness launch grok --headless --always-approve
```

The orchestrator only runs `uv run mdharness next` / `record` / `gate`.
Subagents live in `agents/` and are mirrored under `.grok/agents/` and
`.claude/agents/`.

## Agents and artifacts

| stage | agent | writes | gate |
|---|---|---|---|
| research | researcher | `artifacts/research.md` | — |
| draft | writer | `artifacts/paper.md` | — |
| integrity | auditor | `artifacts/integrity.md` | score ≥ 8 or back to draft |
| review | reviewer | `artifacts/review.md` | score ≥ 7 or back to revise |
| revise | writer | `artifacts/paper.md`, `artifacts/response.md` | then back to review |
| finalize | formatter | `artifacts/manuscript.md` | — |

Auditor and reviewer never edit the paper. The writer may not cite sources
absent from the research map. Unverified items stay tagged `[UNVERIFIED]`.

## What this will not do

- search paywalled literature for you unless the runtime has network tools
- compile a journal PDF
- replace a human author or a real peer reviewer
- guarantee that a citation exists

Treat every bibliography row as a claim to check.

## Related

- Control plane — https://github.com/tlorans/mdharness
- Factory skill — https://github.com/tlorans/mdharness-skill
- Inspiration (not a dependency) — https://github.com/Imbad0202/academic-research-skills
