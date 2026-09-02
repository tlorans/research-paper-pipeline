#!/usr/bin/env bash
# Clone Academic Research Skills and expose its skills to Grok / Claude.
# ARS stays upstream (CC BY-NC 4.0). This repo does not vendor the files.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENDOR="$ROOT/vendor/academic-research-skills"
REPO="${ARS_REPO:-https://github.com/Imbad0202/academic-research-skills.git}"

mkdir -p "$ROOT/vendor" "$ROOT/.grok/skills" "$ROOT/.claude/skills" \
  "$ROOT/.grok/agents" "$ROOT/.claude/agents"

if [[ ! -d "$VENDOR/.git" ]]; then
  echo "cloning $REPO"
  git clone --depth 1 "$REPO" "$VENDOR"
else
  echo "ARS already present at $VENDOR"
fi

link() {
  local src="$1" dest="$2"
  mkdir -p "$(dirname "$dest")"
  ln -sfn "$src" "$dest"
  echo "linked $dest -> $src"
}

for skill in deep-research academic-paper academic-paper-reviewer; do
  link "$VENDOR/$skill" "$ROOT/.grok/skills/$skill"
  link "$VENDOR/$skill" "$ROOT/.claude/skills/$skill"
done

# integrity lives as an agent file inside academic-pipeline, not a skill root
link "$VENDOR/academic-pipeline/agents/integrity_verification_agent.md" \
  "$ROOT/.grok/skills/integrity-verification/SKILL.md"
link "$VENDOR/academic-pipeline/agents/integrity_verification_agent.md" \
  "$ROOT/.claude/skills/integrity-verification/SKILL.md"
link "$VENDOR/academic-pipeline/agents/integrity_verification_agent.md" \
  "$ROOT/.grok/agents/integrity_verification_agent.md"
link "$VENDOR/academic-pipeline/agents/integrity_verification_agent.md" \
  "$ROOT/.claude/agents/integrity_verification_agent.md"

# reference only — do not run this skill; mdharness replaced it
link "$VENDOR/academic-pipeline" "$ROOT/.grok/skills/academic-pipeline"
link "$VENDOR/academic-pipeline" "$ROOT/.claude/skills/academic-pipeline"

echo
echo "ARS skills are on disk. Fill brief.md, then:"
echo "  uv sync"
echo "  uv run mdharness launch grok"
