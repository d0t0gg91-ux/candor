#!/usr/bin/env python3
"""Structure + manifest validator for the candor plugin marketplace.

Dependency-free (stdlib only) so it runs anywhere, including CI without the Claude
Code CLI. Checks:

  - .claude-plugin/marketplace.json parses and has name, owner.name, plugins[] with
    each entry carrying name + source.
  - plugins/candor/.claude-plugin/plugin.json parses and has a name.
  - every plugins/candor/skills/<dir>/SKILL.md has YAML frontmatter whose `name`
    matches <dir> and which declares a `description`.

Exit code 0 on success, 1 on any problem (problems are printed). Run from anywhere:

    python scripts/validate_repo.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []


def err(msg):
    errors.append(msg)


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        err(f"missing file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as e:
        err(f"invalid JSON in {path.relative_to(ROOT)}: {e}")
    return None


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None
    fields = {}
    for line in m.group(1).splitlines():
        fm = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if fm:
            fields[fm.group(1)] = fm.group(2).strip()
    return fields


# 1. marketplace.json
mkt = load_json(ROOT / ".claude-plugin" / "marketplace.json")
if mkt is not None:
    if not mkt.get("name"):
        err("marketplace.json: missing 'name'")
    if not (isinstance(mkt.get("owner"), dict) and mkt["owner"].get("name")):
        err("marketplace.json: missing 'owner.name'")
    plugins = mkt.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        err("marketplace.json: 'plugins' must be a non-empty array")
    else:
        for i, p in enumerate(plugins):
            if not p.get("name"):
                err(f"marketplace.json: plugins[{i}] missing 'name'")
            if not p.get("source"):
                err(f"marketplace.json: plugins[{i}] missing 'source'")

# 2. plugin.json
plugin_root = ROOT / "plugins" / "candor"
pj = load_json(plugin_root / ".claude-plugin" / "plugin.json")
if pj is not None and not pj.get("name"):
    err("plugin.json: missing 'name'")

# 3. skills
skills_dir = plugin_root / "skills"
if not skills_dir.is_dir():
    err("missing plugins/candor/skills/ directory")
else:
    skill_dirs = sorted(d for d in skills_dir.iterdir() if d.is_dir())
    if not skill_dirs:
        err("no skills found under plugins/candor/skills/")
    for d in skill_dirs:
        sk = d / "SKILL.md"
        if not sk.exists():
            err(f"skills/{d.name}/: missing SKILL.md")
            continue
        fm = frontmatter(sk)
        if fm is None:
            err(f"skills/{d.name}/SKILL.md: missing YAML frontmatter")
            continue
        if fm.get("name") != d.name:
            err(f"skills/{d.name}/SKILL.md: frontmatter name '{fm.get('name')}' != directory '{d.name}'")
        if not fm.get("description"):
            err(f"skills/{d.name}/SKILL.md: missing 'description'")
    print(f"checked {len(skill_dirs)} skills")

if errors:
    print(f"\nVALIDATION FAILED ({len(errors)} problem(s)):", file=sys.stderr)
    for e in errors:
        print(f"  - {e}", file=sys.stderr)
    sys.exit(1)

print("OK: structure and manifests valid")
