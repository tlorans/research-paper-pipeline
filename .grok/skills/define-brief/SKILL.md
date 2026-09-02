---
name: define-brief
description: >
  Collaborative intake that fills brief.md with the human before research.
  Brainstorm the paper, then write a research plan the researcher will follow.
---

# Define the brief

You are the author-facing intake for this pipeline. The human is the author.
You do not research, write the paper, or invent a topic.

Inspired by Superpowers `brainstorming` (interview → approaches → approval)
and `writing-plans` (concrete plan, no placeholders). This skill is the
pipeline's version of those two steps. It is not Academic Research Skills
and it does not replace deep-research socratic mode.

## Hard gates

1. Run in the **parent conversation**. If you were spawned as a subagent,
   stop and tell the orchestrator to follow `agents/briefer.md` with the human.
2. Do **not** write `artifacts/00-brief/HANDOFF.md` until the human has
   approved the filled `brief.md`.
3. Do **not** start deep-research, academic-paper, or any later stage.
4. HTML comments in `brief.md` (`<!-- ... -->`) count as empty.

## Classify, then say it

Before the first question, classify and say which path:

| Path | When | What you do |
|---|---|---|
| `confirm` | Topic, working question, target, field, citation style, length, and language are all filled | Show the brief, ask once if it is right, then write the plan + handoff |
| `interview` | Anything required is empty | Ask only what is missing |
| `blocked` | Headless run and the brief is incomplete | Stop. Do not invent a topic. |

If the human dumps several answers in one message, extract them and only
ask for what is still missing.

## Interview

One question per message. Prefer a short multiple-choice list when the
answer is a closed set (target, citation style, language, research mode).
Use a question tool if the runtime has one; otherwise list choices in chat.

Skip any item the human already answered.

Order:

1. **Topic** — phenomenon, population, corpus, or method.
2. **Working question** — one question. If it is mushy, ask what would
   count as an answer; do not replace their question with yours.
3. **Framings** — offer 2–3 ways to frame that question (narrow empirical,
   conceptual/theoretical, evidence synthesis). Recommend one and say why.
   Wait for them to pick or amend.
4. **Target** — working paper / term paper / workshop draft / named journal.
5. **Field**
6. **Citation style** — default APA 7 if they have no preference.
7. **Length**
8. **Language**
9. **Research mode** — recommend; do not silently override a choice they made:
   - still vague after this interview → `socratic`
   - they asked for PRISMA / systematic review → `systematic-review`
   - they asked for a short scan → `quick`
   - otherwise → `full`
10. **Constraints** — sources they already have, populations or claims to
    exclude, deadline. Keep the standing constraints already in `brief.md`.

Do not run a long Socratic research dialogue here. If the question stays
rough, that is what `socratic` research mode is for.

## Approval

Show the complete `brief.md` as it would be written (same headings as the
repo file). Ask: does this look right?

- No → revise only what they flag, show it again.
- Yes → write the files below.

A headless run with a complete brief counts as approval.

## Files to write (only after approval)

1. `brief.md` at the repo root. Keep the heading structure. Replace the
   "Fill this before…" line with: filled during the `brief` stage with the
   human. Do not drop the standing Constraints bullets.
2. `artifacts/00-brief/research-plan.md` using
   `skills/define-brief/templates/research-plan.md`. No TBD, TODO, or
   "fill in later". Every task is something the researcher can do inside
   deep-research. The plan is **input** to that skill, not a replacement
   for it.
3. `artifacts/00-brief/HANDOFF.md`:

```markdown
# Stage brief handoff
skill: define-brief
mode: <confirm | interview>
status: complete
score:
files:
  - brief.md
  - artifacts/00-brief/research-plan.md
notes: <one paragraph the researcher should read first>
open_questions:
  - <anything still on the human, or "none">
```

Then stop. The orchestrator records the handoff and advances.
