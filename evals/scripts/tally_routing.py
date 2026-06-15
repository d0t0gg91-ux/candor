#!/usr/bin/env python3
"""Tally the trigger-routing workflow output into accuracy + a confusion view.

Usage: py tally_routing.py <routing.output> <candor-evals-dir>
"""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

out = Path(sys.argv[1])
ce = Path(sys.argv[2])
data = json.loads(out.read_text(encoding="utf-8"))
preds = data.get("preds") or data.get("result", {}).get("preds")


def ok(p):
    if p["expected"] == "none":
        return p["predicted"] in ("none", "candor-core")
    return p["predicted"] == p["expected"]


correct = [p for p in preds if ok(p)]
wrong = [p for p in preds if not ok(p)]

print(f"routing accuracy: {len(correct)}/{len(preds)} = {len(correct) / len(preds):.0%}")
print("\n--- misroutes ---")
for p in wrong:
    print(f"  q{p['id']}: expected={p['expected']} -> predicted={p['predicted']} (conf {p.get('confidence')})  ::  {p['q'][:62]}")

print("\n--- predictions grouped by expected skill ---")
byexp = defaultdict(Counter)
for p in preds:
    byexp[p["expected"]][p["predicted"]] += 1
for exp in sorted(byexp):
    print(f"  {exp:18s} -> {dict(byexp[exp])}")

(ce / "routing-summary.json").write_text(
    json.dumps(
        {
            "accuracy": round(len(correct) / len(preds), 3),
            "correct": len(correct),
            "total": len(preds),
            "misroutes": wrong,
            "preds": preds,
        },
        indent=2,
    ),
    encoding="utf-8",
)
print(f"\nsaved: {ce / 'routing-summary.json'}")
