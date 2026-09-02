# research-paper-pipeline

mdharness control plane for
[Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills).

The existing ARS skills do the research, writing, integrity check, and
review. This repo owns **order, retries, durable state**, and the
pre-research `brief` intake (`skills/define-brief/`).

```
ARS academic-pipeline (dropped)     this repo
------------------------------     -------------------------
detect stage                       pipeline.yaml + state.json
dispatch skill                     agents/*.md (thin)
integrity / review loops           mdharness gates
Material Passport                  state.json + HANDOFF.md
```

```
brief --> research --> write --> integrity --+
                        ^                    | fail
                        +--------------------+
                                             | pass
                                             v
review --> revise --> rereview --+--> final-integrity --> finalize --> summary
              ^                  | fail         | fail
              +------------------+              |
                    ^                           |
                    +---------------------------+
```

## Why the skills are not in this git tree

ARS is licensed **CC BY-NC 4.0**. Copying those files into an MIT repo would
mix licenses. `scripts/link_ars.py` clones ARS next to the pipeline and
links the skills into `.grok/skills/` and `.claude/skills/` (symlink,
Windows junction, or copy — whichever the OS allows).

`academic-pipeline/SKILL.md` is linked for reference only. Do not run it —
it is a second orchestrator.

## Setup

```bash
git clone https://github.com/tlorans/research-paper-pipeline.git
cd research-paper-pipeline
uv run python scripts/link_ars.py
uv sync
```

Same command on Windows (PowerShell or cmd), macOS, and Linux. Optional
wrappers: `scripts/link-ars.ps1`, `scripts/link-ars.sh`. Use
`uv run python scripts/link_ars.py --update` to pull ARS again.

Then:

```bash
uv run mdharness launch grok
```

The first stage interviews you and writes `brief.md`. You can also fill
`brief.md` yourself before starting; the brief stage will confirm it.

## What each dispatcher loads

| stage | dispatcher | skill | mode |
|---|---|---|---|
| brief | briefer | `skills/define-brief/SKILL.md` | interview / confirm |
| research | researcher | `deep-research/SKILL.md` | full / socratic / quick / systematic-review |
| write | writer | `academic-paper/SKILL.md` | full |
| integrity | auditor | `integrity_verification_agent.md` | pre-review |
| review | reviewer | `academic-paper-reviewer/SKILL.md` | full |
| revise | writer | `academic-paper/SKILL.md` | revision |
| rereview | reviewer | `academic-paper-reviewer/SKILL.md` | re-review |
| final-integrity | auditor | `integrity_verification_agent.md` | final-check |
| finalize | writer | `academic-paper/SKILL.md` | format-convert |
| summary | summarizer | (this repo) | process record from `state.json` |

See `references/ars-dispatch.md`.

mdharness only checks that `artifacts/<stage>/HANDOFF.md` exists. The skill
is free to write the rest of that folder (and, for `brief`, the root
`brief.md`) however it specifies.

## License

- This orchestration layer — MIT
- Cloned skills under `vendor/academic-research-skills` — CC BY-NC 4.0,
  © the ARS authors. Non-commercial scholarly use, attribution required.
  Read their `LICENSE` / `POSITIONING.md` before you use the clone.
