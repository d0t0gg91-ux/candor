# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[0.1.0]: https://github.com/d0t0gg91-ux/candor/releases/tag/v0.1.0
