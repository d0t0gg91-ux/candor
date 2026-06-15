#!/usr/bin/env python3
"""Tally blind A/B comparison verdicts back to with-skill vs baseline.

Usage:
    py tally_comparison.py <compare.output> <candor-evals-dir>

Reads the comparator workflow output (result.verdicts: [{key,winner,reason,confidence}])
and compare/mapping.json (key -> which of A/B was the with-skill response), maps each
winner to with/base/tie, and writes compare/comparison-summary.json + prints the tally.
"""
import json
import sys
from pathlib import Path

out_path = Path(sys.argv[1])
ce = Path(sys.argv[2])

data = json.loads(out_path.read_text(encoding="utf-8"))
verdicts = data.get("verdicts") or data.get("result", {}).get("verdicts")
mapping = json.loads((ce / "compare" / "mapping.json").read_text(encoding="utf-8"))

rows = []
counts = {"with": 0, "base": 0, "tie": 0, "null": 0}
conf_sum = 0
conf_n = 0
for v in verdicts:
    key = v["key"]
    a_is = mapping.get(key)  # "with" or "base" => what Response A was
    winner = v.get("winner")
    if winner == "TIE":
        outcome = "tie"
    elif winner == "A":
        outcome = a_is
    elif winner == "B":
        outcome = "base" if a_is == "with" else "with"
    else:
        outcome = "null"
    counts[outcome] = counts.get(outcome, 0) + 1
    c = v.get("confidence", 0) or 0
    if winner in ("A", "B"):
        conf_sum += c
        conf_n += 1
    rows.append({
        "key": key,
        "A_was": a_is,
        "winner_label": winner,
        "outcome": outcome,
        "confidence": c,
        "reason": v.get("reason", ""),
    })

decisive = counts["with"] + counts["base"]
summary = {
    "n": len(verdicts),
    "with_skill_wins": counts["with"],
    "baseline_wins": counts["base"],
    "ties": counts["tie"],
    "errors": counts["null"],
    "win_rate_among_decided": round(counts["with"] / decisive, 3) if decisive else None,
    "mean_confidence_when_decided": round(conf_sum / conf_n, 2) if conf_n else None,
    "rows": rows,
}
(ce / "compare" / "comparison-summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print(f"n={summary['n']}  with-skill={counts['with']}  baseline={counts['base']}  tie={counts['tie']}  err={counts['null']}")
print(f"win-rate among decided = {summary['win_rate_among_decided']}  mean confidence(decided) = {summary['mean_confidence_when_decided']}")
print("--- baseline wins (where the skill response lost) ---")
for r in rows:
    if r["outcome"] == "base":
        print(f"  {r['key']} (conf {r['confidence']}): {r['reason']}")
print("--- ties ---")
for r in rows:
    if r["outcome"] == "tie":
        print(f"  {r['key']}: {r['reason']}")
