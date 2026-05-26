"""Validate skill frontmatter stays machine-readable."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOTS = [
    ROOT / ".claude" / "skills",
    ROOT / ".agents" / "skills",
    ROOT / "python-factory-plugin" / "skills",
]


def parse_simple_yaml(frontmatter: str) -> dict[str, object]:
    """Parse the small YAML subset used by SKILL.md frontmatter."""
    parsed: dict[str, object] = {}
    current_mapping: dict[str, str] | None = None

    for line in frontmatter.splitlines():
        if not line.strip():
            continue

        if line.startswith("  "):
            assert current_mapping is not None, f"Unexpected nested line: {line}"
            key, separator, value = line.strip().partition(":")
            assert separator, f"Invalid nested frontmatter line: {line}"
            current_mapping[key] = value.strip().strip('"')
            continue

        key, separator, value = line.partition(":")
        assert separator, f"Invalid frontmatter line: {line}"
        key = key.strip()
        value = value.strip()

        if value:
            parsed[key] = value.strip('"')
            current_mapping = None
        else:
            current_mapping = {}
            parsed[key] = current_mapping

    return parsed


def skill_files() -> list[Path]:
    files: list[Path] = []
    for root in SKILL_ROOTS:
        files.extend(root.glob("*/SKILL.md"))
    return sorted(files)


def codex_expected_content(claude_content: str) -> str:
    """Convert Claude-only frontmatter to the Codex-compatible equivalent."""
    if not claude_content.startswith("---\n"):
        return claude_content

    _, frontmatter, body = claude_content.split("---", 2)
    lines = frontmatter.strip("\n").splitlines()
    expected_lines: list[str] = []
    argument_hint: str | None = None

    for line in lines:
        if line == "disable-model-invocation: true":
            continue
        if line.startswith("argument-hint: "):
            argument_hint = line.partition(":")[2].strip()
            continue
        expected_lines.append(line)

    if argument_hint is not None:
        expected_lines.extend(["metadata:", f"  argument-hint: {argument_hint}"])

    return "---\n" + "\n".join(expected_lines) + "\n---" + body


def test_skill_frontmatter_parses():
    skills = skill_files()
    assert skills, "No SKILL.md files found"

    for path in skills:
        content = path.read_text(encoding="utf-8")
        assert content.startswith("---\n"), f"{path} is missing opening frontmatter"

        _, frontmatter, _ = content.split("---", 2)
        parsed = parse_simple_yaml(frontmatter)

        assert parsed.get("name"), f"{path} is missing name"
        assert parsed.get("description"), f"{path} is missing description"

        metadata = parsed.get("metadata")
        assert metadata is None or isinstance(metadata, dict), (
            f"{path} metadata must be a mapping"
        )


def test_agents_skills_mirror_claude_skills():
    """Codex skill copies stay synchronized with Claude skill bodies."""
    claude_skills = {
        path.name for path in (ROOT / ".claude" / "skills").iterdir() if path.is_dir()
    }
    agent_skills = {
        path.name for path in (ROOT / ".agents" / "skills").iterdir() if path.is_dir()
    }

    assert agent_skills == claude_skills

    for skill_name in claude_skills:
        claude_dir = ROOT / ".claude" / "skills" / skill_name
        agent_dir = ROOT / ".agents" / "skills" / skill_name

        claude_files = {
            path.relative_to(claude_dir)
            for path in claude_dir.rglob("*")
            if path.is_file()
        }
        agent_files = {
            path.relative_to(agent_dir)
            for path in agent_dir.rglob("*")
            if path.is_file()
        }
        assert agent_files == claude_files, f"{skill_name} file set differs"

        for relative_path in claude_files:
            claude_content = (claude_dir / relative_path).read_text(encoding="utf-8")
            agent_content = (agent_dir / relative_path).read_text(encoding="utf-8")

            if relative_path.as_posix() == "SKILL.md":
                claude_content = codex_expected_content(claude_content)

            assert agent_content == claude_content, (
                f".agents/skills/{skill_name}/{relative_path} differs from "
                f".claude/skills/{skill_name}/{relative_path}"
            )
