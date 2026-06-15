#!/usr/bin/env python3
"""Assemble candor eval workflow results into the skill-creator viewer layout.

Usage:
    py assemble.py <results.json> <workspace-dir>

<results.json> is the extracted workflow return: {"results": [ {id,name,category,
prompt,assertions,withResp,baseResp,withGrade,baseGrade}, ... ]}.

Produces:
    <workspace>/iteration-1/eval-<id>-<name>/eval_metadata.json
    <workspace>/iteration-1/eval-<id>-<name>/{with_skill,without_skill}/outputs/response.md
    <workspace>/iteration-1/eval-<id>-<name>/{with_skill,without_skill}/grading.json
    <workspace>/benchmark.json   (skill-creator benchmark schema)

Note on metrics: per-run wall-clock and true token counts are not exposed by the
workflow runtime, so `tokens` is approximated as len(response)//4 (clearly an
estimate) and `time_seconds` is 0. The headline metric, pass_rate, is exact.
"""
import json
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

results_path = Path(sys.argv[1])
ws = Path(sys.argv[2])
iterlabel = sys.argv[3] if len(sys.argv) > 3 else "iteration-1"
iter_dir = ws / iterlabel

data = json.loads(results_path.read_text(encoding="utf-8"))
results = data.get("results") or data.get("result", {}).get("results")
if not results:
    raise SystemExit("no results[] found in input JSON")

runs = []
agg = {"with_skill": {"rate": [], "chars": []}, "without_skill": {"rate": [], "chars": []}}

CFG = [("with_skill", "withResp", "withGrade"), ("without_skill", "baseResp", "baseGrade")]

for r in results:
    edir = iter_dir / f"eval-{r['id']}-{r['name']}"
    edir.mkdir(parents=True, exist_ok=True)
    (edir / "eval_metadata.json").write_text(
        json.dumps(
            {"eval_id": r["id"], "eval_name": r["name"], "prompt": r["prompt"], "assertions": r["assertions"]},
            indent=2,
        ),
        encoding="utf-8",
    )
    for cfg, rk, gk in CFG:
        cdir = edir / cfg
        odir = cdir / "outputs"
        odir.mkdir(parents=True, exist_ok=True)
        resp = r.get(rk) or "(no response - agent returned null)"
        (odir / "response.md").write_text(resp, encoding="utf-8")

        grade = r.get(gk)
        total = len(r["assertions"])
        passed = 0
        pass_rate = 0.0
        expectations = []
        if grade and isinstance(grade, dict) and grade.get("summary"):
            passed = grade["summary"].get("passed", 0)
            total = grade["summary"].get("total", total) or total
            pass_rate = grade["summary"].get("pass_rate", (passed / total if total else 0.0))
            expectations = grade.get("expectations", [])
            (cdir / "grading.json").write_text(json.dumps(grade, indent=2), encoding="utf-8")

        chars = len(resp)
        runs.append({
            "eval_id": r["id"],
            "eval_name": r["name"],
            "configuration": cfg,
            "run_number": 1,
            "result": {
                "pass_rate": round(pass_rate, 3),
                "passed": passed,
                "failed": total - passed,
                "total": total,
                "time_seconds": 0,
                "tokens": chars // 4,
                "tool_calls": 0,
                "errors": 0,
            },
            "expectations": expectations,
            "notes": [],
        })
        agg[cfg]["rate"].append(pass_rate)
        agg[cfg]["chars"].append(chars)


def stat(xs):
    if not xs:
        return {"mean": 0, "stddev": 0, "min": 0, "max": 0}
    return {
        "mean": round(statistics.mean(xs), 3),
        "stddev": round(statistics.pstdev(xs), 3),
        "min": round(min(xs), 3),
        "max": round(max(xs), 3),
    }


w_rate, b_rate = stat(agg["with_skill"]["rate"]), stat(agg["without_skill"]["rate"])
w_tok = stat([c // 4 for c in agg["with_skill"]["chars"]])
b_tok = stat([c // 4 for c in agg["without_skill"]["chars"]])

bench = {
    "metadata": {
        "skill_name": "candor",
        "executor_model": "claude-sonnet (workflow general-purpose)",
        "analyzer_model": "claude-opus (orchestrator)",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "evals_run": [r["id"] for r in results],
        "runs_per_configuration": 1,
    },
    "runs": runs,
    "run_summary": {
        "with_skill": {"pass_rate": w_rate, "time_seconds": stat([0]), "tokens": w_tok},
        "without_skill": {"pass_rate": b_rate, "time_seconds": stat([0]), "tokens": b_tok},
        "delta": {
            "pass_rate": f"{(w_rate['mean'] - b_rate['mean']):+.3f}",
            "time_seconds": "+0.0",
            "tokens": f"{(w_tok['mean'] - b_tok['mean']):+.0f}",
        },
    },
    "notes": [
        "stddev is the spread across the 10 different eval prompts (1 run each), not run-to-run noise.",
        "'tokens' is an estimate (response chars // 4); true token counts were not exposed by the runtime.",
        "Grading was blind: the grader was not told which response came from with-skill vs baseline.",
    ],
}
bench_path = ws / f"benchmark-{iterlabel}.json"
bench_path.write_text(json.dumps(bench, indent=2), encoding="utf-8")

print(f"[{iterlabel}]")
print(f"with_skill  mean pass_rate = {w_rate['mean']}  (per-eval: {[round(x,2) for x in agg['with_skill']['rate']]})")
print(f"without     mean pass_rate = {b_rate['mean']}  (per-eval: {[round(x,2) for x in agg['without_skill']['rate']]})")
print(f"delta pass_rate = {bench['run_summary']['delta']['pass_rate']}")
print(f"workspace iteration dir: {iter_dir}")
print(f"benchmark: {bench_path}")
