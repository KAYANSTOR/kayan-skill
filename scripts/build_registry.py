#!/usr/bin/env python3
"""Build registry/SKILLS_REGISTRY.json from the catalog's SKILL.md files."""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_catalog import parse_frontmatter, skill_files  # noqa: E402

SOURCE_HINTS = {
    "01-Core-Workflows": "Multiple upstream workflow repositories; see registry/SOURCES_MANIFEST.json",
    "02-Architecture-Quality": "Multiple upstream architecture and quality repositories; see registry/SOURCES_MANIFEST.json",
    "03-UI-UX-Design": "Multiple upstream UI/UX repositories and documented libraries; see registry/SOURCES_MANIFEST.json",
    "04-Web-Frameworks": "vercel-labs/agent-skills",
    "05-AI-Infrastructure": "Multiple upstream AI infrastructure repositories; see registry/SOURCES_MANIFEST.json",
    "06-Code-Analysis": "Graphify-Labs/graphify",
    "07-SEO-Marketing": "AgriciDaniel/claude-seo",
    "08-Security-Auditing": "Multiple upstream security repositories; see registry/SOURCES_MANIFEST.json",
}


def main() -> int:
    records = []
    generated = date.today().isoformat()
    for path in skill_files(ROOT):
        metadata, errors = parse_frontmatter(path)
        if errors:
            print("Skipping invalid skill:", path, file=sys.stderr)
            for error in errors:
                print(" ", error, file=sys.stderr)
            return 1
        rel = path.relative_to(ROOT)
        category = rel.parts[0]
        records.append({
            "id": rel.as_posix().removesuffix("/SKILL.md"),
            "name": metadata["name"],
            "description": metadata["description"],
            "path": rel.as_posix(),
            "category": category,
            "when_to_use": None,
            "required_tools": [],
            "supported_platforms": ["generic-agent"],
            "dependencies": [],
            "source": {
                "repository": SOURCE_HINTS.get(category),
                "upstream_path": None,
                "commit_or_tag": None,
                "license": None,
                "copied_verbatim": True,
                "last_reviewed": None,
            },
            "verification": {
                "status": "catalog-validated",
                "checked_at": generated,
                "notes": "Metadata, path, and local Markdown links are checked by scripts/validate_catalog.py; upstream provenance requires source-level review.",
            },
        })
    records.sort(key=lambda item: item["path"])
    payload = {
        "schema_version": "1.0",
        "generated_at": generated,
        "catalog": "KAYANSTOR/kayan-skill",
        "skill_count": len(records),
        "skills": records,
    }
    output = ROOT / "registry" / "SKILLS_REGISTRY.json"
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(records)} skills to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
