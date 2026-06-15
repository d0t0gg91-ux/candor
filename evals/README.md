# Candor evaluation harness

This directory holds the benchmark behind [../docs/evals/RESULTS.md](../docs/evals/RESULTS.md):
the prompt sets and the scoring scripts, so the claim "candor changes behavior, here's
where" is auditable rather than asserted.

## What's here

- **`prompts/iteration-1.json`**, **`prompts/iteration-2.json`** - the 20 evaluation
  prompts. Each entry has an `id`, a `name`, the `skills` (relative `SKILL.md` paths) the
  with-skill arm should load, the `prompt`, and the `assertions` it is graded against.
  Iteration 1 uses blatant sycophancy/efficiency traps; iteration 2 uses harder ones.
- **`scripts/`** - dependency-free Python (stdlib only) that turns run outputs into the
  viewer layout, a `benchmark.json`, and the blind-preference tally.

## Method (and how to reproduce)

The benchmark compares two conditions per prompt and grades them blind:

1. **Generate two responses per prompt.**
   - _with-skill_: an assistant that has read `candor-core` plus the prompt's listed mode
     skill(s) and applies them, then answers.
   - _baseline_: the same model answering the same prompt with no skill.

   Use any capable model; the published run drove this with Claude Code workflow
   subagents (Sonnet-class) on both arms, so the only difference is the skill. The
   generation harness is intentionally not vendored here - it's a thin loop over the
   prompt files - but the prompts and scoring are fully specified.

2. **Grade each response blind** against its `assertions` with a grader that does not know
   which arm produced it, emitting `{text, passed, evidence}` per assertion plus a
   summary. `scripts/assemble.py` then builds the per-eval workspace and a `benchmark.json`
   in the [skill-creator](https://github.com/anthropics/skills) viewer schema.

3. **Blind A/B preference (optional, stronger signal).** `scripts/build_comparison.py`
   pairs each prompt's two responses as "Response A" / "Response B" with the assignment
   alternated to balance position bias and the mapping stored separately; a blind judge
   picks the better one; `scripts/tally_comparison.py` de-randomizes and tallies
   with-skill vs baseline wins.

## Results summary

See [../docs/evals/RESULTS.md](../docs/evals/RESULTS.md). Headline: binary pass-rate
80/80 (with-skill) vs 78/80 (baseline) - near ceiling, because the modern base model is
already candid - and 14-4 (2 ties) in blind head-to-head preference, with honest caveats
(the judge isn't fully independent; N is small; candor occasionally over-explains).

Contributions that turn the generation step into a committed, model-agnostic runner are
welcome - see [../CONTRIBUTING.md](../CONTRIBUTING.md).
