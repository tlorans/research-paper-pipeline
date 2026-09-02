# ARS → mdharness dispatch

`academic-pipeline` in Academic Research Skills is an orchestrator. This
project keeps its **skills** and drops its **state machine**.

| ARS stage | mdharness id | skill file | mode | produces |
|---|---|---|---|---|
| 1 RESEARCH | `research` | `deep-research/SKILL.md` | full / socratic / quick / systematic-review | `artifacts/01-research/HANDOFF.md` |
| 2 WRITE | `write` | `academic-paper/SKILL.md` | full | `artifacts/02-write/HANDOFF.md` |
| 2.5 INTEGRITY | `integrity` | `academic-pipeline/agents/integrity_verification_agent.md` | pre-review | `artifacts/03-integrity/HANDOFF.md` |
| 3 REVIEW | `review` | `academic-paper-reviewer/SKILL.md` | full | `artifacts/04-review/HANDOFF.md` |
| 4 REVISE | `revise` | `academic-paper/SKILL.md` | revision | `artifacts/05-revise/HANDOFF.md` |
| 3' RE-REVIEW | `rereview` | `academic-paper-reviewer/SKILL.md` | re-review | `artifacts/06-rereview/HANDOFF.md` |
| 4' RE-REVISE | (retry of `revise`) | `academic-paper/SKILL.md` | revision | same folder |
| 4.5 FINAL INTEGRITY | `final-integrity` | integrity agent | final-check | `artifacts/07-final-integrity/HANDOFF.md` |
| 5 FINALIZE | `finalize` | `academic-paper/SKILL.md` | format-convert | `artifacts/08-finalize/HANDOFF.md` |
| 6 PROCESS SUMMARY | `summary` | this repo `agents/summarizer.md` | — | `artifacts/09-summary/HANDOFF.md` |

Gates (Python):

- integrity score ≥ 8 else back to `write` (max 3)
- rereview score ≥ 7 else back to `revise` (max 3)
- final-integrity score ≥ 8 else back to `revise` (max 3)

Do not run `academic-pipeline/SKILL.md` during a run. It would fight
mdharness for control of the stage pointer.
