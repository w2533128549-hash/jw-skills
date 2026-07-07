# Multi-Agent Project Structure

This skill creates a project-local multi-agent setup. It intentionally uses project-local files so different projects can have different agent teams without changing global Codex behavior.

## Root files

- `config.toml`: Project-local coordination, workspace, workflow, and risk policy configuration.
- `AGENTS.md`: Human-readable Codex guidance. It must list all child agents and must state that the project manager creates the plan and workflow from the user's request.
- `agents/`: One TOML file per child agent.

## Required agents

- `project_manager`: User-facing coordinator. Creates the plan and workflow, assigns work, tracks progress, handles high-risk handoffs, and reports results.
- `system_deployment`: Manages local environment, dependencies, services, and deployment preparation.
- `development`: Implements code, integrations, bug fixes, and scoped refactors.
- `debug_testing`: Runs programs, reads logs, reproduces issues, writes tests, and verifies fixes.
- `design_docs`: Designs flows, interactions, documentation, and acceptance criteria.
- `security_audit`: Reviews high-risk operations, deletion risk, script safety, and secret/privacy exposure.

## Required workflow loop

Planning -> parallel development -> cross review -> repair -> verification -> delivery.

The project manager owns planning and final delivery. Specialist agents own only assigned work. High-risk work is handed to the project manager, which decides whether security audit or user confirmation is required.

## Minimum agent TOML fields

Each `agents/*.toml` file should contain:

- `id`
- `name`
- `description`
- `[codex]`
- `[permissions]`
- `[handoff]`
- `developer_instructions`

Use `developer_instructions` for the agent's operational prompt.