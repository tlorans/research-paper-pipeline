# AGENTS.md

Grok Build / Codex / Cursor: this is the orchestrator contract.

You do **not** invent workflow state. `mdharness` is the source of truth.
You do **not** invent research/writing/review method. Academic Research
Skills (cloned under `vendor/`) are the source of truth for that work.

Prefer `uv run mdharness …` when uv is available.

## First run

```bash
uv run python scripts/link_ars.py
uv sync
```

If `vendor/academic-research-skills/` is missing, stop and run that command
(Windows, macOS, and Linux).

## Every turn

1. Run `uv run mdharness next`.
2. Follow the printed instruction exactly.
3. Spawn the named dispatcher from `.grok/agents/` (or `.claude/agents/`).
4. That dispatcher **loads the ARS skill named in its file** and follows it.
5. After the dispatcher writes `artifacts/<stage>/HANDOFF.md`, run
   `uv run mdharness record artifacts/<stage>/HANDOFF.md`.
6. If the instruction says to record a gate, run
   `uv run mdharness gate --score N --notes "one sentence"`.
7. After each stage, pause for the human unless they asked for a headless run.
8. Stop when status is `passed` or `abandoned`. Never restart a finished run.
9. Never run `academic-pipeline/SKILL.md`. That skill is a second orchestrator.

## Ownership

- `researcher` → `artifacts/01-research/`
- `writer` → `artifacts/02-write/`, `05-revise/`, `08-finalize/`, plus pointer `artifacts/paper.md`
- `auditor` → `artifacts/03-integrity/`, `07-final-integrity/`
- `reviewer` → `artifacts/04-review/`, `06-rereview/` (read-only on the paper)
- `summarizer` → `artifacts/09-summary/`

Do not hand-edit `state.json` or `pipeline.yaml` mid-run.
Read `brief.md` and `references/ars-dispatch.md`.
