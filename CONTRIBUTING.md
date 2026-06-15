# Contributing to Candor

Thanks for considering a contribution. Candor is small on purpose; the bar for changes
is "does this make the personas more accurate, more grounded, or more useful," not "is
it more elaborate."

## Ways to contribute

- **Tune a persona.** Sharpen a directive, fix one that backfires in practice, or
  improve a "what this looks like" example.
- **Propose a new mode.** New work-mode personas are welcome if they fill a real gap and
  are grounded (see below), not just a restatement of an existing mode.
- **Improve the docs.** The grounding doc, README, and examples can always be clearer.
- **Report what doesn't work.** A persona that misfires in a real session is valuable
  signal - open an issue with the transcript or a paraphrase.

## Ground rules for persona changes

1. **Stay grounded.** Behavioral directives should trace to a trait rationale, not to
   personal preference. New or changed personas should explain _why_ a directive belongs
   to that mode, ideally referencing the framework signatures in
   [docs/grounding.md](docs/grounding.md). Add to that doc when you add a mode.
2. **Explain the why; don't pile on MUSTs.** The skills deliberately favor
   reason-explaining instructions over walls of ALL-CAPS imperatives. Models follow
   _understood_ rules better than shouted ones. Match that style.
3. **Keep candor calibrated.** Any change that increases directness must not erode the
   "candor is not cruelty" guardrails in `candor-core`. Directness without calibration
   is just a different failure.
4. **No invented citations.** If you cite research, it must be real and verifiable.
   Prefer describing a well-established phenomenon over attaching a specific paper ID you
   haven't confirmed.
5. **No hidden behavior.** Everything a skill does must be readable in its `SKILL.md`.
   No hooks, scripts, or tool-permission grabs in this plugin.

## Validate before you open a PR

Candor's manifests must pass the official validator:

```text
claude plugin validate ./plugins/candor --strict
```

Also confirm both JSON manifests parse and that any skill you touched still has valid
YAML frontmatter (`name` matching its directory, a `description`).

## Pull request process

1. Fork and branch from `main`.
2. Make focused changes - one persona or one concern per PR where possible.
3. Run the validator and re-read your changed `SKILL.md` files end to end.
4. In the PR description, say what behavior changed and why, and (for persona changes)
   what trait rationale supports it.
5. Be ready for direct review feedback. This project dogfoods its own values.

## Code of conduct

Participation is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). By
participating, you agree to uphold it.

## License

By contributing, you agree that your contributions are licensed under the project's
[MIT License](LICENSE).
