# Security Policy

## Threat model for this project

Candor is a **prompt-level** Claude Code plugin. It ships only Markdown (`SKILL.md`
files) and two JSON manifests. It contains:

- **No executable code** - no scripts, binaries, or build steps.
- **No hooks, MCP servers, LSP servers, or monitors** - nothing that runs commands or
  starts processes.
- **No `allowed-tools` declarations** - installing candor grants Claude no tool
  permissions it did not already have. Your existing
  [permission settings](https://code.claude.com/docs/en/permissions) remain fully in
  control.

Because of this, the realistic security surface is limited to the **content of the
instructions themselves**: whether any directive could induce unsafe behavior, leak
data, or smuggle in a prompt injection. The skills are written to avoid this, and every
rule is in plain language for you to audit.

## Before you trust it

Treat candor the way you should treat any third-party skill: **read the `SKILL.md`
files before installing.** Skills become part of the model's instructions, so a
malicious skill is a real (if low-tech) risk in the ecosystem generally. All of
candor's behavior is in:

```
plugins/candor/skills/*/SKILL.md
```

There is nothing hidden elsewhere.

## Supported versions

| Version | Supported |
| ------- | --------- |
| 0.1.x   | Yes       |

This is a pre-1.0 project; only the latest released version receives fixes.

## Reporting a vulnerability

Please report suspected security issues **privately**, not in a public issue:

1. Open a private vulnerability report via this repository's
   **Security → Report a vulnerability** tab (GitHub private vulnerability reporting), or
2. Open a regular issue **only** if the problem is not sensitive (for example, a broken
   link or a typo in a directive).

Examples of things worth reporting here: a directive that could be read as instructing
data exfiltration, a prompt-injection vector hidden in skill text, or a manifest field
that could escalate permissions unexpectedly.

When you report, please include the affected file and line, what behavior you observed
or expect, and the Claude Code version you tested on. You can expect an initial response
within a reasonable window for a hobby-scale open-source project; there is no paid bug
bounty.
