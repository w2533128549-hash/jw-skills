---
name: aiwork-subagents
description: Spawn and coordinate AIWork role-based Codex subagents from the TOML templates in D:\AIWork\agents. Use when the user asks to create subagents, delegate work to the AIWork multi-agent team, test whether subagents can be created, or run project-manager/development/debug-testing/design-docs/security-audit/system-deployment style agents.
---

# AIWork Subagents

Use the existing AIWork role templates instead of inventing new agent roles.

## Quick Start

1. Inspect `D:\AIWork\agents` and read the TOML file for each requested role.
2. Choose the smallest useful delegation:
   - `project-manager.toml`: planning, routing, final integration.
   - `development.toml`: bounded code changes.
   - `debug-testing.toml`: reproduce bugs, run checks, validate fixes.
   - `design-docs.toml`: PRD, tech spec, workflows, handoff docs.
   - `security-audit.toml`: read-only risk review.
   - `system-deployment.toml`: local environment, dependency, startup, deployment prep.
3. Spawn with `multi_agent_v1.spawn_agent`.
4. If using `fork_context=true`, omit `agent_type`, `model`, and `reasoning_effort`; the tool rejects full-history forks with explicit overrides.
5. Tell the subagent it is not alone in the codebase and must not revert edits made by others.
6. Wait only when the result blocks the next step. Close completed agents when no longer needed.

## Prompt Shape

Use this structure and fill it from the selected TOML template:

```text
You are the AIWork <role name> agent.

Role source:
<absolute path to TOML template>

You are not alone in the codebase. Do not revert edits made by others. Work within D:\AIWork unless the user explicitly confirms a broader scope.

Task goal:
<specific delegated task>

Background:
<minimal context needed>

Expected output:
<concise deliverable>

Risk rule:
High-risk work must stop and be handed back to the project manager/user before execution.
```

## Spawn Rules

For a quick context-aware subagent:

```json
{
  "fork_context": true,
  "message": "<filled prompt>"
}
```

For a fresh worker without full context, use `agent_type` only when it helps:

```json
{
  "agent_type": "worker",
  "message": "<filled prompt>"
}
```

Never set a model override unless the user explicitly asks for a different model.

## Role Reference

Read `references/roles.md` when you need the role map or output formats without opening every TOML file.
