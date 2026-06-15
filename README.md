# Candor

**Anti-sycophancy behavioral modes for Claude Code.** A small plugin that swaps
flattery, hedging, and "this should work" for directness, verification, and per-task
efficiency - and switches its style to fit the kind of work you're doing.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Status: experimental](<https://img.shields.io/badge/status-experimental%20(v0.1.0)-orange.svg>)

---

## What it is

Candor is a Claude Code [plugin](https://code.claude.com/docs/en/plugins) containing
five [skills](https://code.claude.com/docs/en/skills): one shared anti-sycophancy
**core**, and four **work-mode personas** that tune Claude's behavior for the task in
front of it. The skills load automatically when they're relevant, and you can also
invoke any of them by name.

The goal is narrow and practical: reduce the specific, measurable ways an
RLHF-trained assistant becomes _less useful_ - reflexive agreement, hollow praise,
caving under pushback without new evidence, padding, false balance, and claiming
success without checking - while keeping it genuinely helpful. Candor is **not** an
instruction to be harsh; a whole section of the core skill exists to keep directness
from tipping into manufactured contrarianism.

## The five skills

| Skill                 | When it engages                                                         | Persona it adopts                                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **candor-core**       | Always-relevant baseline; honest-feedback requests                      | The shared rules: lead with the disagreement and the reason; don't fold without new evidence; verify before claiming; cut hollow affirmation; stay calibrated |
| **candor-coding**     | Implementation, code review, debugging, refactors, failing builds/tests | Systematic and closure-seeking; blunt, specific code review; evidence-ordered failure reports; verify before "done"                                           |
| **candor-logic**      | Analysis, argument evaluation, root-cause work                          | Premise-testing and evidence-first; separates inference from fact; names the weak link; resists premature closure                                             |
| **candor-creative**   | Writing, design, narrative, editing, art direction                      | Maximum imaginative reach with honest, values-grounded critique instead of encouragement                                                                      |
| **candor-brainstorm** | Generating options, exploring a problem space, stress-testing a plan    | High-volume divergent ideas; challenges the framing; holds divergence until you're ready to converge                                                          |

Each persona is grounded in established personality-science frameworks rather than
invented from scratch - see [docs/grounding.md](docs/grounding.md) for the full
rationale and the trait signatures behind each mode.

## Install

Candor is distributed as a plugin marketplace hosted in this repository.

```text
/plugin marketplace add d0t0gg91-ux/candor
/plugin install candor@candor
```

The second argument is `plugin@marketplace` - here both happen to be named `candor`.

**Trying it before it's public, or from a local clone:**

```text
git clone https://github.com/d0t0gg91-ux/candor.git
/plugin marketplace add ./candor
/plugin install candor@candor
```

After installing, restart or reload so the skills register.

## Using it

Once installed, the skills are **auto-invocable**: Claude loads the relevant mode based
on what you're doing (reviewing code pulls in `candor-coding`, "let's brainstorm" pulls
in `candor-brainstorm`, and so on). The core baseline applies whenever directness is
warranted.

You can also invoke any mode explicitly - plugin skills are namespaced by the plugin
name:

```text
/candor:candor-core
/candor:candor-coding
/candor:candor-logic
/candor:candor-creative
/candor:candor-brainstorm
```

**Turning it on or off:** manage the whole plugin from the `/plugin` menu (enable,
disable, or uninstall). To stop a specific mode from auto-loading, disable the plugin or
remove that skill's directory in a fork.

## How it works

These are **prompt-level behavioral skills** - plain Markdown instructions, no code.
When a skill is active, its directives become part of Claude's working context and shape
how it responds. There is no model fine-tuning, no background process, and no change to
your settings. Remove the plugin and the behavior reverts immediately.

Because the effect is instructional, results vary with the model and the situation -
treat candor as a strong, consistent nudge, not a guarantee.

## Safety and transparency

- **No code execution.** The plugin ships only Markdown and JSON. It contains no hooks,
  MCP servers, scripts, or executables.
- **No permissions granted.** None of the skills declare `allowed-tools`, so installing
  candor does not give Claude any tool access it didn't already have.
- **Auditable.** Every behavioral rule is in the `SKILL.md` files in plain language.
  Read them before you trust them - that advice applies to any skill from anyone.

See [SECURITY.md](SECURITY.md) for the full posture and how to report an issue.

## Status

**v0.1.0 - experimental.** This is an initial public release of a prompt-level
behavioral design. It has not been through large-scale evaluation; expect to tune the
personas to your own taste. Feedback and pull requests are welcome - see
[CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE).

## Acknowledgements

The work-mode personas were derived from analysis across four established
personality-science frameworks (the Five-Factor Model, the 16-type model, the twelve
Jungian/brand archetypes, and the Predictive Index four-drive model). See
[docs/grounding.md](docs/grounding.md) for sources and methodology.
