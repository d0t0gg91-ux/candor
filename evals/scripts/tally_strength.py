#!/usr/bin/env python3
"""Per-model stats + variance + leak scan for the strengthened benchmark."""
import json
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path

data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
res = data.get("results") or data.get("result", {}).get("results")

bym = defaultdict(lambda: {"wq": [], "bq": [], "wp": [], "wt": [], "bp": [], "bt": []})
for r in res:
    m = r["model"]
    for g in r["withG"]:
        bym[m]["wq"].append(g["quality_0_100"]); bym[m]["wp"].append(g["assertions_passed"]); bym[m]["wt"].append(g["assertions_total"])
    for g in r["baseG"]:
        bym[m]["bq"].append(g["quality_0_100"]); bym[m]["bp"].append(g["assertions_passed"]); bym[m]["bt"].append(g["assertions_total"])

for m, d in bym.items():
    wq, bq = d["wq"], d["bq"]
    print(f"{m}: graded with={len(wq)} base={len(bq)}")
    print(f"  quality  with = {statistics.mean(wq):.1f} +/- {statistics.pstdev(wq):.1f}   base = {statistics.mean(bq):.1f} +/- {statistics.pstdev(bq):.1f}   delta = +{statistics.mean(wq) - statistics.mean(bq):.1f}")
    print(f"  passrate with = {sum(d['wp']) / sum(d['wt']):.3f}              base = {sum(d['bp']) / sum(d['bt']):.3f}")
    lows = sorted(q for q in bq if q < 50)
    print(f"  baseline quality<50 (possible wrong-answer/leak): {len(lows)} {lows[:10]}")

notes = " ".join(g.get("note", "") for r in res for g in (r["withG"] + r["baseG"]))
hits = re.findall(r"Persage|Popup|build-release|tech-stack|CLAUDE\.md|§6|section 6|operating protocol", notes, re.I)
print(f"\nleak-indicator hits in grader notes: {len(hits)} {sorted(set(hits))}")
