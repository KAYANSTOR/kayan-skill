#!/usr/bin/env python3
"""Validate the catalog without executing any skill code."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CATEGORY_RE = re.compile(r"^\d{2}-")
LINK_RE = re.compile(r"\[[^]]*\]\(([^)]+)\)")


def parse_frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    errors: list[str] = []
    if not lines or lines[0].strip() != "---":
        return {}, [f"{path}: missing YAML frontmatter"]
    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        return {}, [f"{path}: unterminated YAML frontmatter"]
    data: dict[str, str] = {}
    index = 1
    while index < end:
        line = lines[index]
        if not line.strip() or line.lstrip().startswith("#"):
            index += 1
            continue
        if ":" not in line:
            errors.append(f"{path}: invalid frontmatter line: {line}")
            index += 1
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if key in data:
            errors.append(f"{path}: duplicate frontmatter key: {key}")
        if value in ("", ">", ">-", "|", "|-") and index + 1 < end and (not lines[index + 1].strip() or lines[index + 1].startswith((" ", "\t"))):
            block: list[str] = []
            index += 1
            while index < end and (not lines[index].strip() or lines[index].startswith((" ", "\t"))):
                block.append(lines[index].strip())
                index += 1
            if key == "description":
                data[key] = " ".join(block).strip()
            continue
        if value.startswith(("\"", "'")) and value.endswith(value[0]):
            value = value[1:-1]
        data[key] = value
        index += 1
    for key in ("name", "description"):
        if not data.get(key):
            errors.append(f"{path}: missing frontmatter field: {key}")
    if "TODO" in data.get("description", ""):
        errors.append(f"{path}: placeholder description is not allowed")
    return data, errors


def skill_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for category in sorted(root.iterdir()):
        if category.is_dir() and CATEGORY_RE.match(category.name):
            files.extend(sorted(category.rglob("SKILL.md")))
    return files


def validate(root: Path) -> tuple[list[str], list[str], list[dict[str, object]]]:
    errors: list[str] = []
    warnings: list[str] = []
    records: list[dict[str, object]] = []
    categories = [p for p in root.iterdir() if p.is_dir() and CATEGORY_RE.match(p.name)]
    if not categories:
        errors.append("no numbered skill categories found")
    seen_names: dict[str, Path] = {}
    for path in skill_files(root):
        rel = path.relative_to(root)
        data, parse_errors = parse_frontmatter(path)
        errors.extend(parse_errors)
        name = data.get("name", "")
        if name:
            if name in seen_names:
                warnings.append(f"duplicate skill name {name!r}: {seen_names[name]} and {path}; registry uses paths as stable IDs")
            seen_names[name] = path
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        if line_count > 500:
            warnings.append(f"{rel}: {line_count} lines; consider moving detail to references/")
        for target in LINK_RE.findall(path.read_text(encoding="utf-8")):
            target = target.split("#", 1)[0].strip().strip("<>")
            if not target or target.startswith(("http://", "https://", "mailto:", "#")) or "{" in target or target in {"url"}:
                continue
            candidate = (path.parent / target).resolve()
            if not candidate.exists():
                errors.append(f"{rel}: broken local link: {target}")
        records.append({
            "name": name,
            "path": rel.as_posix(),
            "category": rel.parts[0] if rel.parts else "",
            "description": data.get("description", ""),
        })
    for path in root.rglob("*"):
        if path.is_symlink():
            errors.append(f"symlink is not allowed in catalog: {path.relative_to(root)}")
    registry = root / "registry" / "SKILLS_REGISTRY.json"
    if registry.exists():
        try:
            payload = json.loads(registry.read_text(encoding="utf-8"))
            for item in payload.get("skills", []):
                item_path = item.get("path")
                if item_path and not (root / item_path).exists():
                    errors.append(f"registry points to missing path: {item_path}")
        except json.JSONDecodeError as exc:
            errors.append(f"invalid registry JSON: {exc}")
    return errors, warnings, records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    root = args.root.resolve()
    errors, warnings, records = validate(root)
    result = {"root": str(root), "skills": len(records), "errors": errors, "warnings": warnings}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Validated {len(records)} SKILL.md files")
        for warning in warnings:
            print(f"WARNING: {warning}")
        for error in errors:
            print(f"ERROR: {error}")
        print("Validation passed" if not errors else f"Validation failed with {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
