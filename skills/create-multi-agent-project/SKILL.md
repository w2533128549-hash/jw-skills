---
name: create-multi-agent-project
description: Create a project-local Codex-style multi-agent team scaffold. Use when the user asks Codex to create, initialize, generate, or standardize a multi-agent project setup with a project manager agent, specialist agents, an agents/ directory, config.toml, AGENTS.md, high-risk handoff rules, and workspace-only write constraints.
---

# Create Multi-Agent Project

Use this skill to create a local multi-agent project scaffold for Codex.

## Required output shape

Create or update exactly these project-level artifacts unless the user explicitly asks for a different shape:

```text
<project-root>/
  agents/
    project-manager.toml
    system-deployment.toml
    development.toml
    debug-testing.toml
    design-docs.toml
    security-audit.toml
  config.toml
  AGENTS.md
```

`AGENTS.md` must list every child agent and must explicitly include a project manager agent. The project manager is the user-facing coordinator: it listens to the user's request, creates the plan and workflow, assigns work to specialist agents, tracks progress, handles high-risk handoffs, and produces the final report.

## Workflow

1. Confirm the target project root. If unspecified, use the current working directory.
2. Treat writes outside the target project root as high risk. Do not do them unless the user explicitly asks and approves.
3. Use `scripts/scaffold_multi_agent_project.py` to create the scaffold whenever possible.
4. If existing files would be overwritten, use the script without `--force` first so it reports conflicts. Ask the project manager logic to decide whether overwriting is appropriate.
5. Do not automatically delete unrelated project files. If the user asks for a directory containing only `agents/`, `config.toml`, and `AGENTS.md`, treat deletion of extras as high risk and require explicit user confirmation.
6. Validate generated TOML files with Python `tomllib` when available.

## Safety rules

- Keep all generated project configuration local to the project directory.
- Do not modify global Codex config unless the user explicitly asks for global installation or global configuration.
- Do not place secrets, tokens, cookies, credentials, or private paths in generated agent files.
- Route destructive, irreversible, production, credential, cost-incurring, and outside-workspace operations to the project manager first.
- The project manager decides whether to request a security audit or user confirmation.

## Reference

Read `references/project-structure.md` when the user asks for schema details, wants to customize agent names/responsibilities, or wants to understand the expected project files.