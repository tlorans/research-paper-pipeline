---
name: write-verdict
description: Format an integrity or peer-review verdict markdown file with an explicit numeric score for mdharness gate.
---

Write the owned verdict file completely. First line of the score section must
be `score: N` with N in 0–10. Then one paragraph of notes the orchestrator
can paste into `uv run mdharness gate --score N --notes "..."`.
