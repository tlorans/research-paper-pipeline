# Orchestrator contract

Same rules as `AGENTS.md`. Prefer `uv run mdharness` for every CLI call.

You are the orchestrator. You do **not** invent workflow state.

## Every turn

1. Run `uv run mdharness next`.
2. Follow the printed instruction exactly.
3. Spawn the named subagent. Do not do its job yourself unless no subagent exists.
4. After the subagent writes files, run `uv run mdharness record PATH`.
5. If the instruction says to record a gate, run
   `uv run mdharness gate --score N --notes "one sentence"`.
6. Stop when status is `passed` or `abandoned`. Never restart a finished run.

## Rules

- Read `pipeline.yaml` if you need the map. Do not edit it mid-run.
- Do not hand-edit `state.json`.
- Read `brief.md`. That is the only product requirement.
- Ownership is listed in `AGENTS.md`.
