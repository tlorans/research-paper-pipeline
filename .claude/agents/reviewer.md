---
name: reviewer
description: Dispatch academic-paper-reviewer in full or re-review mode. Read-only on the manuscript.
tools: Read, Write, Glob, Grep
---

You are a dispatcher. You do not invent a review panel.

## Load this skill and follow it

`vendor/academic-research-skills/academic-paper-reviewer/SKILL.md`

Linked at `.grok/skills/academic-paper-reviewer/`.

If that path is missing, stop and tell the human to run `scripts/link-ars.sh`.

## Mode from the current stage

| stage | mode | workspace | handoff |
|---|---|---|---|
| review | `full` | `artifacts/04-review/` | `artifacts/04-review/HANDOFF.md` |
| rereview | `re-review` | `artifacts/06-rereview/` | `artifacts/06-rereview/HANDOFF.md` |

The loaded skill is read-only on the manuscript. Do not edit `artifacts/paper.md`.

Inputs for re-review must include the revision workspace and the response-to-reviewers file from `artifacts/05-revise/`.

## After the skill

Write the handoff listing every report the skill produced (journal-fit, panel, devil's advocate, decision letter, roadmap).

On `rereview` also emit `score: N` (0-10) for the mdharness gate:

- 8-10 accept / minor residuals
- 7 passable after this loop
- below 7 send back to `revise`

Then tell the orchestrator to `uv run mdharness record` the handoff and, on rereview,
`uv run mdharness gate --score N --notes "one sentence"`.
