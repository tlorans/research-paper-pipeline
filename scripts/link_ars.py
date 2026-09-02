#!/usr/bin/env python3
"""Clone Academic Research Skills and expose them to Grok / Claude.

Works on Windows, macOS, and Linux. Run with:

    uv run python scripts/link_ars.py
    python scripts/link_ars.py

On Windows, directory junctions are used when creating a symlink needs
Administrator / Developer Mode. Files fall back to a copy.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_DEFAULT = "https://github.com/Imbad0202/academic-research-skills.git"
SKILLS = ("deep-research", "academic-paper", "academic-paper-reviewer")


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def ensure_git() -> None:
    if shutil.which("git") is None:
        sys.exit("git is not on PATH. Install Git for Windows: https://git-scm.com/download/win")


def clone_or_update(vendor: Path, repo: str, update: bool) -> None:
    vendor.parent.mkdir(parents=True, exist_ok=True)
    if not (vendor / ".git").is_dir():
        if vendor.exists():
            shutil.rmtree(vendor)
        run(["git", "clone", "--depth", "1", repo, str(vendor)])
        return
    print(f"ARS already present at {vendor}")
    if update:
        run(["git", "pull", "--ff-only"], cwd=vendor)


def _unlink(dest: Path) -> None:
    if not dest.exists() and not dest.is_symlink():
        return
    if dest.is_symlink() or dest.is_file():
        dest.unlink()
        return
    if dest.is_dir():
        try:
            dest.rmdir()
        except OSError:
            shutil.rmtree(dest)


def _junction(src: Path, dest: Path) -> bool:
    if os.name != "nt":
        return False
    completed = subprocess.run(
        ["cmd", "/c", "mklink", "/J", str(dest), str(src)],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode == 0:
        return True
    print(completed.stdout)
    print(completed.stderr, file=sys.stderr)
    return False


def link(src: Path, dest: Path) -> None:
    if not src.exists():
        sys.exit(f"missing source: {src} (clone failed?)")
    dest.parent.mkdir(parents=True, exist_ok=True)
    _unlink(dest)
    try:
        os.symlink(src, dest, target_is_directory=src.is_dir())
        kind = "symlink"
    except OSError:
        if src.is_dir() and _junction(src, dest):
            kind = "junction"
        elif src.is_dir():
            shutil.copytree(src, dest)
            kind = "copy-tree"
        else:
            shutil.copy2(src, dest)
            kind = "copy"
    print(f"{kind:10} {dest} -> {src}")


def sync_repo_runtime_files(root: Path) -> None:
    """Copy this repo's dispatchers and skills next to the ARS links."""
    agents_src = root / "agents"
    skills_src = root / "skills"
    for runtime in (root / ".grok", root / ".claude"):
        dest_agents = runtime / "agents"
        dest_agents.mkdir(parents=True, exist_ok=True)
        if agents_src.is_dir():
            for agent in sorted(agents_src.glob("*.md")):
                dest = dest_agents / agent.name
                dest.write_text(agent.read_text(encoding="utf-8"), encoding="utf-8")
                print(f"{'copied':10} {dest}")
        dest_skills = runtime / "skills"
        dest_skills.mkdir(parents=True, exist_ok=True)
        if skills_src.is_dir():
            for skill in sorted(skills_src.iterdir()):
                if (skill / "SKILL.md").is_file():
                    link(skill, dest_skills / skill.name)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo",
        default=os.environ.get("ARS_REPO", REPO_DEFAULT),
        help="ARS git URL",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="git pull if vendor/academic-research-skills already exists",
    )
    args = parser.parse_args()

    ensure_git()
    root = Path(__file__).resolve().parent.parent
    vendor = root / "vendor" / "academic-research-skills"
    clone_or_update(vendor, args.repo, args.update)

    for runtime in (root / ".grok", root / ".claude"):
        (runtime / "skills").mkdir(parents=True, exist_ok=True)
        (runtime / "agents").mkdir(parents=True, exist_ok=True)
        for skill in SKILLS:
            link(vendor / skill, runtime / "skills" / skill)
        integrity = vendor / "academic-pipeline" / "agents" / "integrity_verification_agent.md"
        link(integrity, runtime / "skills" / "integrity-verification" / "SKILL.md")
        link(integrity, runtime / "agents" / "integrity_verification_agent.md")
        link(vendor / "academic-pipeline", runtime / "skills" / "academic-pipeline")

    sync_repo_runtime_files(root)

    print()
    print("ARS skills are on disk. The brief stage fills brief.md with you:")
    print("  uv sync")
    print("  uv run mdharness launch grok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
