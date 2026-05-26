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
