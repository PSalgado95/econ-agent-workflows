#!/usr/bin/env python3
"""Generate the Claude Code package from the canonical Codex sources.

Codex is the single source of truth. Edit skills/, .codex/agents/, and
references/ in their Codex form, then run this script to regenerate the
committed `claude/` tree. Never hand-edit anything under `claude/`.

What it does:
- copies each skill (SKILL.md + references/ + scripts/ + assets/) into
  claude/skills/<name>/, applying the Codex->Claude substitution table to
  Markdown and dropping the Codex-only agents/openai.yaml;
- turns each skill's agents/openai.yaml into a Claude slash command under
  claude/commands/<name>.md;
- turns each .codex/agents/*.toml reviewer into a Claude subagent under
  claude/agents/<name>.md;
- copies shared root references into
  claude/references/econ-agent-workflows/.
"""

from __future__ import annotations

import re
import shutil
import tomllib
from pathlib import Path

# (source path under skills/, installed skill name). Mirrors install.py.
SKILLS = (
    ("econ-plan", "econ-plan"),
    ("econ-work", "econ-work"),
    ("econ-review", "econ-review"),
    ("econ-compound", "econ-compound"),
    ("auxiliary/gpt-pro-handoff", "gpt-pro-handoff"),
)

BANNER = (
    "<!-- GENERATED FROM CODEX SOURCE - DO NOT EDIT. "
    "Edit the Codex sources (skills/, .codex/agents/, references/) "
    "and run build_claude.py. -->"
)

# Reviewers default to Sonnet; promote a run to Opus manually when critical.
REVIEWER_MODEL = "sonnet"
READ_ONLY_TOOLS = "Read, Grep, Glob"


def substitute(text: str) -> str:
    """Rewrite Codex-runtime references to their Claude Code equivalents."""
    # Skill/command invocation syntax: $econ-review -> /econ-review, etc.
    text = re.sub(r"\$(econ-(?:plan|work|review|compound)|gpt-pro-handoff)", r"/\1", text)
    # User-prompt tool.
    text = text.replace("request_user_input", "AskUserQuestion")
    # Installed protocol/reference location (handles the deeper path too).
    text = text.replace("~/.codex/", "~/.claude/")
    # Repo-relative reviewer-agent directory -> installed agent directory.
    text = text.replace(".codex/agents/", "~/.claude/agents/")
    # Runtime name in prose (whole word only; leaves ".codex" paths untouched
    # because those are lowercase and already rewritten above).
    text = re.sub(r"\bCodex\b", "Claude Code", text)
    return text


def with_banner(text: str) -> str:
    """Insert the banner after YAML frontmatter, or at the top otherwise."""
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                lines.insert(i + 1, "")
                lines.insert(i + 2, BANNER)
                return "\n".join(lines) + "\n"
    return BANNER + "\n\n" + text


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def copy_skill(source: Path, dest: Path) -> None:
    """Copy a skill tree, substituting Markdown and dropping agents/openai.yaml."""
    for item in sorted(source.rglob("*")):
        if item.is_dir():
            continue
        rel = item.relative_to(source)
        # The Codex-only interface file becomes a slash command instead.
        if rel.parts and rel.parts[0] == "agents":
            continue
        target = dest / rel
        if item.suffix == ".md":
            write(target, with_banner(substitute(item.read_text(encoding="utf-8"))))
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)


def parse_interface(yaml_path: Path) -> dict[str, str]:
    """Extract interface fields from a simple single-line-quoted openai.yaml."""
    text = yaml_path.read_text(encoding="utf-8")
    fields: dict[str, str] = {}
    for key in ("display_name", "short_description", "default_prompt"):
        match = re.search(rf'{key}:\s*"(.+)"\s*$', text, flags=re.MULTILINE)
        if match:
            fields[key] = match.group(1)
    return fields


def build_command(name: str, yaml_path: Path, commands_dir: Path) -> str:
    fields = parse_interface(yaml_path)
    description = fields.get("short_description", f"Run the {name} skill")
    prompt = substitute(fields.get("default_prompt", f"Use /{name}."))
    body = (
        "---\n"
        f'description: "{description}"\n'
        "---\n\n"
        f"{BANNER}\n\n"
        f"{prompt}\n\n"
        "$ARGUMENTS\n"
    )
    write(commands_dir / f"{name}.md", body)
    return name


def build_agent(toml_path: Path, agents_dir: Path) -> str:
    data = tomllib.loads(toml_path.read_text(encoding="utf-8"))
    name = data["name"]
    description = data["description"].replace('"', "'")
    instructions = substitute(data["developer_instructions"].strip())
    lines = ["---", f"name: {name}", f'description: "{description}"', f"model: {REVIEWER_MODEL}"]
    if data.get("sandbox_mode") == "read-only":
        lines.append(f"tools: {READ_ONLY_TOOLS}")
    lines += ["---", "", BANNER, "", instructions, ""]
    write(agents_dir / f"{name}.md", "\n".join(lines))
    return name


def main() -> int:
    repo = Path(__file__).resolve().parent
    out = repo / "claude"
    if out.exists():
        shutil.rmtree(out)

    skills_out = out / "skills"
    commands_out = out / "commands"
    agents_out = out / "agents"

    skill_msgs, command_msgs, agent_msgs = [], [], []

    for source_name, installed_name in SKILLS:
        copy_skill(repo / "skills" / source_name, skills_out / installed_name)
        skill_msgs.append(installed_name)
        yaml_path = repo / "skills" / source_name / "agents" / "openai.yaml"
        if yaml_path.exists():
            command_msgs.append(build_command(installed_name, yaml_path, commands_out))
        else:
            command_msgs.append(f"{installed_name} (skipped: no openai.yaml)")

    for toml_path in sorted((repo / ".codex" / "agents").glob("*.toml")):
        agent_msgs.append(build_agent(toml_path, agents_out))

    reference_msgs = []
    for reference in sorted((repo / "references").glob("*.md")):
        write(
            out / "references" / "econ-agent-workflows" / reference.name,
            with_banner(substitute(reference.read_text(encoding="utf-8"))),
        )
        reference_msgs.append(reference.name)

    print("build_claude: generated claude/")
    print(f"- skills:   {', '.join(skill_msgs)}")
    print(f"- commands: {', '.join(command_msgs)}")
    print(f"- agents:   {len(agent_msgs)} reviewer subagents")
    print(f"- references: {', '.join(reference_msgs)}")
    print("\nReview the generated tree, then run install_claude.py to install it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
