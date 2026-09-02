"""Idle pipeline starts at brief; dispatchers and the define-brief skill exist."""

from __future__ import annotations

import unittest
from pathlib import Path

from mdharness.io import load_spec, load_state

ROOT = Path(__file__).resolve().parents[1]


class PipelineContract(unittest.TestCase):
    def test_brief_is_first_stage(self) -> None:
        spec = load_spec(ROOT)
        first = spec.first()
        self.assertEqual(first.id, "brief")
        self.assertEqual(first.agent, "briefer")
        self.assertIn("artifacts/00-brief/HANDOFF.md", first.produces)
        self.assertEqual(spec.next_after("brief").id, "research")

    def test_idle_state_matches_first_stage(self) -> None:
        state = load_state(ROOT)
        if state.status == "idle" and not state.history:
            self.assertEqual(state.stage, "brief")

    def test_briefer_files_exist(self) -> None:
        for rel in (
            "agents/briefer.md",
            ".grok/agents/briefer.md",
            ".claude/agents/briefer.md",
            "skills/define-brief/SKILL.md",
            "skills/define-brief/templates/research-plan.md",
            ".grok/skills/define-brief/SKILL.md",
        ):
            path = ROOT / rel
            self.assertTrue(path.is_file(), f"missing {rel}")

    def test_runtime_briefer_matches_source(self) -> None:
        src = (ROOT / "agents" / "briefer.md").read_text(encoding="utf-8")
        for rel in (".grok/agents/briefer.md", ".claude/agents/briefer.md"):
            self.assertEqual((ROOT / rel).read_text(encoding="utf-8"), src, rel)

    def test_brief_md_keeps_required_headings(self) -> None:
        text = (ROOT / "brief.md").read_text(encoding="utf-8")
        for heading in (
            "## Topic",
            "## Working question",
            "## Target",
            "## Discipline and style",
            "## ARS modes",
            "## Constraints",
        ):
            self.assertIn(heading, text)


if __name__ == "__main__":
    unittest.main()
