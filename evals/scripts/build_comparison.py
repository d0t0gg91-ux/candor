#!/usr/bin/env python3
"""Build blind A/B comparison items from the two eval workflow outputs.

Usage:
    py build_comparison.py <candor-evals-dir> <iter1.output> <iter2.output>

For each of the 20 (prompt) pairs it writes a neutral item file containing the user
message and the two responses as "Response A" / "Response B", with the with-skill vs
baseline assignment alternated by index (parity) to balance position bias. The judge
never sees which is which; the mapping is stored separately for de-randomization.
"""
import json
import sys
from pathlib import Path

ce = Path(sys.argv[1])
out_paths = sys.argv[2:]
iters = ["iteration-1", "iteration-2"]

items_dir = ce / "compare" / "items"
items_dir.mkdir(parents=True, exist_ok=True)

mapping = {}
manifest = []
idx = 0
for it, op in zip(iters, out_paths):
    data = json.loads(Path(op).read_text(encoding="utf-8"))
    results = data.get("results") or data.get("result", {}).get("results")
    for r in results:
        key = f"{it}-e{r['id']}-{r['name']}"
        w = r.get("withResp") or "(no response)"
        b = r.get("baseResp") or "(no response)"
        a_is = "with" if idx % 2 == 0 else "base"
        A, B = (w, b) if a_is == "with" else (b, w)
        md = (
            f"## User message\n\n{r['prompt']}\n\n"
            f"## Response A\n\n{A}\n\n"
            f"## Response B\n\n{B}\n"
        )
        p = items_dir / f"{key}.md"
        p.write_text(md, encoding="utf-8")
        mapping[key] = a_is
        manifest.append({"key": key, "path": str(p)})
        idx += 1

(ce / "compare" / "mapping.json").write_text(json.dumps(mapping, indent=2), encoding="utf-8")
(ce / "compare" / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(f"built {len(manifest)} comparison items")
print("MANIFEST_JSON=" + json.dumps({"manifest": manifest}))
