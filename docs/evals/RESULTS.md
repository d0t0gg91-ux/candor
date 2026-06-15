# Candor benchmark results

A small, honest benchmark of whether the candor skills change behavior - and where they
don't. Run 2026-06-15 against the v0.1.0 skills.

## TL;DR

- On 20 deliberately adversarial sycophancy/efficiency prompts, answered **with the skill
  active** vs a **baseline** (same model, no skill), then graded blind:
  - **Binary pass-rate:** with-skill **80/80 (100%)**, baseline **78/80 (97.5%)**. The
    modern base model is _already_ very candid on clear-cut prompts, so this metric is
    near its ceiling. The skill never regressed and caught the two cases the baseline
    missed.
  - **Blind head-to-head preference:** an independent judge, not told which response came
    from which, preferred the **candor response in 14 of 20 pairs** (baseline 4, ties 2) -
    a **78% win-rate among decided pairs**, mean confidence 3.06/5.
- The honest part: candor's edge is in **form and framing** (leading with the point,
  refusing false balance, not caving to pushback), not in raw correctness, which the base
  model already gets right. In a few cases the candor response **over-explained** and lost
  on concision - which directly motivated the v0.2.0 "length should match the question"
  tune to `candor-core`.

## Method

- **20 prompts** in two batches of 10. Each prompt is designed to invite a specific
  failure - a false premise to confirm, unfounded pushback to cave to, a flawed plan to
  hype, a mediocre artifact to praise, a clear answer to hedge on, an authority asserting
  something subtly wrong, and so on. Iteration 1 used fairly blatant traps; iteration 2
  used harder ones (mediocre-but-working code, false-balance bait, verbosity traps, a
  decision the user is attached to) after iteration 1 showed a ceiling effect.
- **Two conditions per prompt:** _with-skill_ (a subagent reads the relevant `SKILL.md`
  files - always `candor-core` plus the matching mode - and applies them, then answers)
  and _baseline_ (the same subagent model answers with no skill). Same model on both
  sides, so the delta is the skill's contribution.
- **Blind grading:** a separate grader scored each response against 3-4 objective
  assertions, without being told which condition produced it.
- **Blind preference:** every prompt's two responses were shown to a fresh judge as
  "Response A" / "Response B" with the assignment alternated to balance position bias. The
  judge picked the better one on directness, candor, efficiency, and usefulness, with no
  knowledge of which was the skill.
- **Model:** all generation and judging used a Sonnet-class model via the workflow runner.

## Results

### Binary assertion pass-rate

| Batch                       | With-skill       | Baseline          | Baseline miss                                                           |
| --------------------------- | ---------------- | ----------------- | ----------------------------------------------------------------------- |
| Iteration 1 (blatant traps) | 40/40 (1.00)     | 39/40 (0.975)     | brainstorm: accepted a "bigger popup" framing instead of challenging it |
| Iteration 2 (harder traps)  | 40/40 (1.00)     | 39/40 (0.975)     | false balance: enumerated "pros" of storing plaintext passwords         |
| **Combined**                | **80/80 (1.00)** | **78/80 (0.975)** |                                                                         |

The gap is small because the base model is genuinely strong here - it refuses obvious
sycophancy, corrects false premises, and holds its ground on facts without help. The
skill's value on this metric is that it closed the two gaps the base model left, with zero
regressions.

### Blind head-to-head preference

| Outcome                    | Count    |
| -------------------------- | -------- |
| Candor response preferred  | **14**   |
| Baseline preferred         | 4        |
| Tie                        | 2        |
| **Win-rate among decided** | **0.78** |

This is where the difference shows up: even when both responses "pass," the candor one was
usually judged better - for leading with the disagreement or the answer, refusing false
balance, and not softening the key point.

### What the baseline wins teach us

The four baseline wins are the most useful data, because they show where candor _didn't_
help:

- **Two were candor over-explaining.** On a simple "REST or GraphQL?" the candor response
  gave the right answer (REST) but padded it; the baseline said the same thing in half the
  words and won on concision. This is a real failure mode, and it motivated the v0.2.0
  addition to `candor-core`: _length should match the question; padding a correct answer
  with unrequested detail is a quieter failure than flattery, but still a failure._
- **Two were the baseline adding genuinely useful completeness** (an exhaustive list of
  valid `typeof` returns; concrete next-steps on a scam-coin plan). Here "more" really was
  better, and candor's brevity slightly under-delivered.

The two ties were trivial prompts ("in one word, dynamically or statically typed?") where
both produced the identical minimal answer - exactly where the skill _should_ make no
difference.

## Strengthened benchmark (addresses the caveats)

To weaken the caveats below, a larger run: 32 prompts (all four iterations) x two models
(Sonnet and Haiku) x {with-skill, clean-baseline} x 2 runs = 256 graded responses, scored
on both the binary assertions and a continuous 0-100 candor-quality rubric (grader held
constant at Sonnet). The baseline prompt was hardened to explicitly ignore any
repository-specific operating protocol.

| Model  | Quality (with) | Quality (base) | Δ        | Pass-rate (with) | Pass-rate (base) |
| ------ | -------------- | -------------- | -------- | ---------------- | ---------------- |
| Sonnet | 94.0 ± 4.3     | 86.5 ± 12.6    | **+7.4** | 0.987            | 0.961            |
| Haiku  | 88.4 ± 12.7    | 81.9 ± 15.4    | **+6.5** | 0.965            | 0.957            |

Three things stand out. (1) Candor lifts quality on **both** models (+6.5 to +7.4 on the
0-100 scale) - the effect generalizes beyond the single model of the original run. (2) The
continuous quality metric shows a clear gap exactly where the binary pass-rate ceilings
(both ~96-99%): magnitude is visible where pass/fail is not. (3) The with-skill arm is also
**more consistent** - on Sonnet its quality stddev is 4.3 vs the baseline's 12.6 - so candor
narrows the spread, not just raises the mean.

The hardened baseline worked: **0 of 64 baseline responses leaked repository context**, so
the original internal-reference artifact is gone from the comparison. One residual: a single
_with-skill_ Haiku response added a project-specific closing paragraph (mild padding; it
still scored 88 and passed all assertions). So the comparison is clean; one low-impact leak
remains on the weaker model.

## Honest caveats

- **The judge is not fully independent.** It scored responses on the same directness/
  candor/efficiency criteria the skill is explicitly designed to produce. So the preference
  result is strong evidence that candor _makes responses match those criteria_ - not a
  neutral proof that those criteria are universally "better." A human reviewer is the right
  next step.
- **Sample, models, runs - strengthened, not exhaustive.** The headline now rests on 32
  prompts x 2 models (Sonnet, Haiku) x 2 runs = 256 graded responses, and the effect holds
  on both models (see above). Remaining limits: a single grader family (Sonnet) and no
  human grading - multi-vendor judges and a human pass are the next step.
- **Ceiling on the binary metric - addressed by a continuous metric.** Pass-rate ceilings
  because the base model is already calibrated; that is a true fact about the base model,
  not a flaw the skill can fix. The fix is to measure magnitude, which the 0-100 quality
  rubric (and the blind preference) do - and they show a clear, consistent gap.
- **The repo-context artifact - resolved for the comparison.** A hardened baseline prompt
  (ignore any repository operating protocol) eliminated it: 0 of 64 baseline responses in
  the strengthened run referenced repo internals. One low-impact residual remains - a
  single with-skill Haiku response added a project-specific paragraph (mild padding, no
  effect on correctness) - so it is reduced, not zero.

## Coverage update: the v0.3.0 modes

A third batch (iteration-3) extends the benchmark to the five modes added after the
original run - `candor-security`, `candor-debug`, `candor-architect`, `candor-decide`,
`candor-data` - with two prompts each (10 total), same with-skill vs baseline method.

- **Binary pass-rate:** with-skill **10/10**, baseline **10/10** - a complete ceiling.
  The base model already handles these prompts (it spots the command injection, the
  sunk-cost fallacy, the base-rate trap) without help, so pass/fail shows no gap.
- **Blind preference:** candor preferred **8 of 10** (baseline 2, 0 ties), in line with
  the original ~78%. The two baseline wins were security prompts where the candor
  response buried the strongest recommendation ("just remove the endpoint") under code -
  a useful, honest miss.

So the v0.3.0 modes behave like the originals: no measurable gap on raw correctness
(the base model is strong), a consistent ~80% edge in head-to-head quality.

`candor-curator` (v0.4.0) was spot-checked the same way: with-skill **2/2** vs baseline
**0.625** - the largest binary gap in the suite, because the base model handles "does this
stale page still look good?" worst of all, either punting for the file or (with repo
access) confidently answering about the wrong thing.

## Trigger-routing accuracy

After adding `candor-debug` and `candor-writing`, the `candor-coding`, `candor-logic`,
and `candor-creative` descriptions were tightened so the right persona loads. To check
that empirically, 39 labeled queries (3 per mode plus cross-mode near-misses and a few
matching nothing specific) were each routed by a judge given the twelve real
descriptions: which single skill should auto-load?

**Result: 39/39 correct (100%)** (re-run after `candor-curator` brought the set to
twelve). The confusion matrix is perfectly diagonal - every
near-miss routed to the intended skill: "review this code" -> coding (not debug); a
failing CI test -> debug (not coding); novel feedback -> creative (not writing); API docs
-> writing (not creative); "conversions went up 5%, did it work?" -> data (not decide);
"is this endpoint safe?" -> security (not coding); "how should I structure the services?"
-> architect (not coding); "bring the stale doc in line with the current code" ->
curator (not writing); "write a brand-new guide" -> writing (not curator). The
disambiguation holds across all twelve skills.

This is a _routing_ measure - a judge predicting which description matches - a faithful
proxy for auto-triggering rather than the runtime mechanism itself. See the next note.

## On run_loop.py (the description-trigger optimizer)

The skill-creator ships `run_loop.py`, which measures real auto-triggering by spawning
`claude -p` per query and watching whether the skill loads. It does not run on Windows:
it uses `subprocess.Popen(["claude", ...])` (the `claude` entrypoint is a `.ps1`/`.cmd`
shim, not a directly-spawnable executable, so every call fails with `WinError 2`) plus
POSIX `select()` on a pipe (unsupported for pipes on Windows). Verified by running it -
all queries returned a spurious "not triggered". The routing measurement above is the
cross-platform substitute. To run the real optimizer, use a macOS/Linux (or WSL)
checkout: `python -m scripts.run_loop --eval-set <set> --skill-path
plugins/candor/skills/<skill> --model <id> --report none`.

## Reproducing

The harness (eval prompts, the with-skill/baseline runner, the blind grader, the
preference judge, and the assembly/scoring scripts) was run outside this repo to keep
generated transcripts out of version control. The design is described above in enough
detail to rebuild: pair each prompt's with-skill and baseline responses, grade blind
against fixed assertions, and run a blind A/B preference pass with position-balanced
ordering. Contributions that turn this into a committed, re-runnable suite are welcome.
