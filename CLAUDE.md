# Orchestrator contract

Same rules as `AGENTS.md`. Prefer `uv run mdharness` for every CLI call.

You are the orchestrator. You do not invent workflow state and you do not
replace Academic Research Skills with a homemade writing method.

1. `uv run python scripts/link_ars.py` must have been run.
2. `uv run mdharness next` every turn.
3. Spawn the named dispatcher. It loads the ARS skill in its file.
4. Record `artifacts/<stage>/HANDOFF.md`.
5. Gate when told.
6. Never execute `vendor/academic-research-skills/academic-pipeline/SKILL.md`.
