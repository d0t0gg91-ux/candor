<!-- Candor dogfoods its own values: expect direct review. Lead with what changed and why. -->

## What this changes

<!-- One or two sentences. The behavior, not the diff. -->

## Why

<!-- For a persona change: what trait rationale supports it? Link to docs/grounding.md if relevant. -->

## Checklist

- [ ] Ran `python scripts/validate_repo.py` (and, if available, `claude plugin validate ./plugins/candor`)
- [ ] Re-read every changed `SKILL.md` end to end
- [ ] Persona changes stay grounded (a trait rationale, not personal taste) and don't erode the `candor-core` "candor is not cruelty" guardrails
- [ ] No invented citations; no hidden behavior (no hooks/scripts/tool-permission grabs)
- [ ] Updated README / grounding / CHANGELOG if the set of skills changed
