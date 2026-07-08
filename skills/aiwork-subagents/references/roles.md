# AIWork Role Templates

Source directory: `D:\AIWork\agents`

| Template | Role | Best use |
| --- | --- | --- |
| `project-manager.toml` | Project manager | User-facing coordination, task split, high-risk routing, final delivery. |
| `development.toml` | Development | Implement features, fix bugs, refactor within a bounded file/module scope. |
| `debug-testing.toml` | Debug/testing | Reproduce problems, run tests, inspect logs, verify fixes. |
| `design-docs.toml` | Design/docs | PRD, tech spec, workflow design, UI/interaction notes, delivery docs. |
| `security-audit.toml` | Security audit | Read-only review of destructive, credential, deployment, production, or outside-workspace risks. |
| `system-deployment.toml` | System/deployment | Local runtime, dependency, service startup, environment checks, deployment preparation. |

## Output Expectations

Ask each subagent to use the output format defined in its TOML. If the task is only a quick probe, a one-sentence result is enough.

## Safety Defaults

- Keep write work inside `D:\AIWork`.
- Do not expose secrets, tokens, cookies, certificates, or private data.
- Do not run destructive commands, production deploys, remote scripts, global installs, or paid-resource actions without explicit user confirmation.
- Use `security-audit.toml` for high-risk review before execution.
