# AGENTS.md

Grok Build / Codex / Cursor: this is the orchestrator contract.

You do **not** invent workflow state. The Python package `mdharness` is the
source of truth. Prefer `uv run mdharness …` when uv is available.

## Every turn

1. Run `uv run mdharness next` (fallback: `mdharness next`).
2. Follow the printed instruction exactly.
3. Spawn the named subagent from `.grok/agents/` (Grok) or `.claude/agents/`.
4. After the subagent writes files, run `uv run mdharness record PATH`.
5. If the instruction says to record a gate, run
   `uv run mdharness gate --score N --notes "one sentence"`.
6. Stop when status is `passed` or `abandoned`. Never restart a finished run.

## Rules

- Read `pipeline.yaml` if you need the map. Do not edit it mid-run.
- Do not hand-edit `state.json`.
- Read `brief.md`. That is the only product requirement.
- `researcher` owns `artifacts/research.md`.
- `writer` owns `artifacts/paper.md` and `artifacts/response.md`.
- `auditor` owns `artifacts/integrity.md` only.
- `reviewer` owns `artifacts/review.md` only.
- `formatter` owns `artifacts/manuscript.md` only.
- Auditor and reviewer never edit the paper.
- Prefer revising over abandoning unless three integrity or review loops fail.
- Pause and ask the human before treating generated numbers or quotations as real.
