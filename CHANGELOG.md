# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2026-06-15

### Added

- **Twelve plugin subagents** (`plugins/candor/agents/candor-*.md`). Installing candor now
  also provides twelve named agents - `candor:candor-coding`, `candor:candor-debug`, and so
  on - available in the `/agents` picker and for auto-delegation. Each ships the persona
  from `AGENTS.md` as a real subagent (the agents auto-discover from `agents/`; no manifest
  change needed).

## [0.4.2] - 2026-06-15

### Added

- **`AGENTS.md`** - each of the twelve skills distilled into a ready-to-run agent prompt:
  a self-contained system prompt you can drop into a Claude Code subagent
  (`.claude/agents/`), the `/agents` picker, another agent framework, or the top of a
  chat, to spin up an agent that prefers that mode. Docs only; no skill behavior changed.

## [0.4.1] - 2026-06-15

### Added

- **Strengthened benchmark** in `docs/evals/RESULTS.md`: 32 prompts x 2 models (Sonnet,
  Haiku) x 2 runs = 256 graded responses, scored on a continuous 0-100 quality rubric
  alongside the binary assertions. Candor lifts quality on both models (+6.5 to +7.4) and
  narrows response variance; the hardened clean-baseline removed the prior repo-context
  artifact (0 of 64 baseline responses leaked).
- `evals/scripts/tally_strength.py`.

### Changed

- Rewrote the RESULTS caveats to reflect the strengthened run - small-N / one-model /
  ceiling / artifact are now weakened or resolved. No skill behavior changed.

## [0.4.0] - 2026-06-15

### Added

- **`candor-curator`** - the knowledge-base curation persona (ISTJ-A / Archivist / PI
  Controller): audits docs and wikis for staleness, reconciles contradictions, prunes
  superseded content, preserves the audit trail rather than rewriting history, and keeps a
  single source of truth in sync with reality. The third ISTJ-rooted "guardian" - alongside
  security (systems) and data (evidence), it guards the knowledge itself. Brings the set to
  twelve skills.

## [0.3.1] - 2026-06-15

### Added

- **Benchmark coverage for the v0.3.0 modes** (`evals/prompts/iteration-3.json`):
  security, debug, architect, decide, and data, with results folded into
  `docs/evals/RESULTS.md` (binary 10/10 vs 10/10; blind preference 8-2 for candor).
- **Trigger-routing accuracy test** (`evals/prompts/routing.json`,
  `evals/scripts/tally_routing.py`): 33 labeled queries routed against the eleven real
  descriptions - **33/33 correct**, confirming the v0.3.0 trigger disambiguation holds.

### Notes

- Documented that the skill-creator's `run_loop.py` trigger optimizer does not run on
  Windows (POSIX `select` on a pipe; non-spawnable `claude` shim); the routing test is
  the cross-platform substitute. No skill behavior changed in this release.

## [0.3.0] - 2026-06-15

### Added

- **Two more work-mode personas**, bringing the set to eleven skills:
  - `candor-decide` - ruthless prioritization, scoping, and saying no (ESTJ-A / Executive).
  - `candor-data` - skeptical reading of numbers, stats, and experiments (ISTJ-A / Analyzer).
- **Eval harness** committed under `evals/` - the prompt sets and dependency-free scoring
  scripts behind `docs/evals/RESULTS.md`, so the benchmark is reproducible.
- **Repo automation**: `scripts/validate_repo.py` (stdlib-only structure/manifest check)
  and a GitHub Actions workflow that runs it on push and pull requests.
- **Contributor scaffolding**: issue templates (bug, persona proposal) and a PR template.
- A **trademark / non-affiliation note** in `docs/grounding.md`.

### Changed

- **Disambiguated skill triggers** so the right persona loads: `candor-coding` no longer
  claims debugging/failing-tests (now routed to `candor-debug`), `candor-creative` no
  longer claims technical writing (now `candor-writing`), and `candor-logic` routes actual
  code bugs to `candor-debug`.

## [0.2.0] - 2026-06-15

### Added

- **Four new work-mode personas**, bringing the set to nine skills:
  - `candor-security` - adversarial, low-trust threat-modeling and defensive review
    (ISTJ-T / Sentinel / PI Guardian). Defensive scope only.
  - `candor-debug` - repro-first, hypothesis-driven bug hunting (ISTP-A troubleshooter).
  - `candor-architect` - system design at altitude: explicit trade-offs and failure
    modes, one committed recommendation (INTJ-A / Magician).
  - `candor-writing` - clear technical communication that refuses to fake-affirm
    understanding (ENFJ-A / Mentor).
- **`docs/evals/RESULTS.md`** - results of a 20-prompt blind A/B benchmark (with-skill vs
  baseline) measuring directness, candor, and efficiency.

### Changed

- **`candor-core`**: added a "length should match the question" directive, after the
  benchmark showed the personas occasionally padding a correct answer with unrequested
  detail.

## [0.1.0] - 2026-06-15

Initial release.

### Added

- **`candor` plugin** with five skills:
  - `candor-core` - the shared anti-sycophancy baseline (position integrity, response
    form, verification, and "candor is not cruelty" calibration guardrails).
  - `candor-coding` - systematic, closure-seeking coding/review persona.
  - `candor-logic` - evidence-first, premise-testing analytical persona.
  - `candor-creative` - high-imagination persona with values-grounded critique.
  - `candor-brainstorm` - divergent, framing-challenging brainstorming persona.
- **Marketplace manifest** (`.claude-plugin/marketplace.json`) so the repository can be
  added directly with `/plugin marketplace add`.
- **Grounding documentation** (`docs/grounding.md`) explaining the framework basis for
  each persona.
- Project docs: README, SECURITY, CONTRIBUTING, CODE_OF_CONDUCT, MIT LICENSE.

[0.5.0]: https://github.com/d0t0gg91-ux/candor/releases/tag/v0.5.0
[0.4.2]: https://github.com/d0t0gg91-ux/candor/releases/tag/v0.4.2
[0.4.1]: https://github.com/d0t0gg91-ux/candor/releases/tag/v0.4.1
[0.4.0]: https://github.com/d0t0gg91-ux/candor/releases/tag/v0.4.0
[0.3.1]: https://github.com/d0t0gg91-ux/candor/releases/tag/v0.3.1
[0.3.0]: https://github.com/d0t0gg91-ux/candor/releases/tag/v0.3.0
[0.2.0]: https://github.com/d0t0gg91-ux/candor/releases/tag/v0.2.0
[0.1.0]: https://github.com/d0t0gg91-ux/candor/releases/tag/v0.1.0
