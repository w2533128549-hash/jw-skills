#!/usr/bin/env python3
"""Create a project-local multi-agent scaffold for Codex-style work."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

AGENTS = [
    {
        "id": "project_manager",
        "file": "project-manager.toml",
        "name": "项目经理",
        "description": "Listen to the user, create the plan and workflow, assign tasks, track progress, handle high-risk handoffs, and report results.",
        "type": "coordinator",
        "instructions": """你是项目经理 Agent，也是唯一直接面向用户的协调者。根据用户需求制定 plan 和 workflow，拆解任务，分配给专业 Agent，跟进进度，检查结果，决定重试、修复或交付。任何高危任务必须先交给你判断；涉及删除、写入工作区外、系统修改、密钥、生产环境、费用或不可逆后果时，你必须决定是否交给用户最终确认。""",
    },
    {
        "id": "system_deployment",
        "file": "system-deployment.toml",
        "name": "系统管理与部署",
        "description": "Manage local environment, downloads, dependencies, services, deployment preparation, and dependency conflicts.",
        "type": "specialist",
        "instructions": """你是系统管理与部署 Agent。负责本地环境、依赖、工具链、服务启动和部署准备。只执行项目经理分配的任务。遇到安装软件、运行远程脚本、修改系统配置、写入工作区外或连接生产资源时，立即转交项目经理。""",
    },
    {
        "id": "development",
        "file": "development.toml",
        "name": "编程开发",
        "description": "Write code, modify code, implement features, integrate APIs, fix bugs, and perform scoped refactors.",
        "type": "specialist",
        "instructions": """你是编程开发 Agent。负责代码实现、修改、API 接入、bug 修复和必要的小范围重构。保持项目风格，不做无关重构，不硬编码密钥。遇到删除目录、批量覆盖、安全敏感逻辑、生产资源或工作区外写入时，立即转交项目经理。""",
    },
    {
        "id": "debug_testing",
        "file": "debug-testing.toml",
        "name": "调试测试",
        "description": "Run programs, inspect logs, locate issues, write tests, and verify fixes.",
        "type": "specialist",
        "instructions": """你是调试测试 Agent。负责运行程序、查看日志、复现问题、定位问题、编写测试和验证修复。遇到会删除数据、修改系统、使用真实密钥、连接生产服务或产生费用的测试操作时，立即转交项目经理。""",
    },
    {
        "id": "design_docs",
        "file": "design-docs.toml",
        "name": "设计与文档",
        "description": "Plan feature flows, design interactions, organize documentation, and record operating procedures.",
        "type": "specialist",
        "instructions": """你是设计与文档 Agent。负责功能流程、交互设计、接口说明、使用说明、操作记录和验收标准。文档必须和实际实现一致。遇到密钥、隐私、生产配置或不可公开信息时，立即转交项目经理。""",
    },
    {
        "id": "security_audit",
        "file": "security-audit.toml",
        "name": "安全审计",
        "description": "Review high-risk operations, script safety, deletion risk, and privacy or secret leakage risk.",
        "type": "reviewer",
        "instructions": """你是安全审计 Agent。负责审核高风险操作、脚本安全、删除风险、权限风险、密钥与隐私泄露风险。你只能提供风险建议，不能自行批准高危任务。最终由项目经理判断；必要时由用户确认。""",
    },
]

CONFIG = '''[workspace]
root = "{root}"
write_policy = "workspace_only"
allowed_write_roots = ["{root}"]
deny_write_outside_workspace = true
do_not_modify_global_config = true

[agents]
directory = "agents"
entry_agent = "project_manager"
single_user_facing_coordinator = true
handoff_high_risk_to = "project_manager"
security_review_agent = "security_audit"
project_manager_may_escalate_to_user = true
max_parallel_agents = 4
max_repair_rounds_before_user_update = 2

[workflow]
stages = ["planning", "parallel_development", "cross_review", "repair", "verification", "delivery"]

[risk_policy]
must_ask_user_when = [
  "write_outside_workspace",
  "delete_directory_or_bulk_files",
  "irreversible_operation",
  "modify_system_or_global_configuration",
  "install_unknown_software_or_run_remote_script",
  "use_real_credentials_or_secrets",
  "connect_to_production_resources",
  "deploy_or_publish_to_external_service",
  "incur_costs",
  "project_manager_uncertain_about_impact"
]
'''

AGENTS_MD = '''# Project Agent Rules

This project uses a local multi-agent setup. The project root should contain:

- `agents/`
- `config.toml`
- `AGENTS.md`

## Child Agents

| Agent | File | Responsibility |
| --- | --- | --- |
| 项目经理 | `agents/project-manager.toml` | User-facing coordinator. Listens to the user's request, creates the plan and workflow, assigns work, tracks progress, handles high-risk handoffs, and reports results. |
| 系统管理与部署 | `agents/system-deployment.toml` | Manages local environment, resources, dependencies, services, and deployment preparation. |
| 编程开发 | `agents/development.toml` | Implements code, modifies code, integrates APIs, fixes bugs, and performs scoped refactors. |
| 调试测试 | `agents/debug-testing.toml` | Runs programs, reads logs, locates issues, writes tests, and verifies fixes. |
| 设计与文档 | `agents/design-docs.toml` | Plans feature flows, designs interactions, organizes docs, and records operations. |
| 安全审计 | `agents/security-audit.toml` | Reviews high-risk operations, script safety, deletion risk, and secret/privacy exposure. |

## Coordination

- The project manager is the only user-facing coordinator.
- User goals enter through the project manager.
- The project manager must create the plan and workflow from the user's request.
- Specialist agents only act on tasks assigned by the project manager.
- High-risk work must be handed to the project manager first.
- The project manager decides whether security audit is enough or whether the user must make the final decision.

## Workflow

Use this loop:

1. Planning
2. Parallel development
3. Cross review
4. Repair
5. Verification
6. Delivery

## Safety

- Write access is limited to `{root}`.
- Do not write, delete, move, or overwrite files outside `{root}`.
- Do not expose secrets, tokens, cookies, credentials, certificates, or private user data.
- Do not install unknown software, run remote scripts, deploy, publish, or use production resources without project manager review and user confirmation when required.

## Delivery

Final reports must include:

- Whether the user goal was completed.
- What changed.
- Which files were created or modified.
- What was tested or verified.
- Whether high-risk work occurred.
- Whether any high-risk work was audited or confirmed by the user.
- Remaining risks or unresolved issues.
'''


def toml_string(value: str) -> str:
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'


def agent_toml(agent: dict[str, str], root: str) -> str:
    can_write = "false" if agent["id"] == "security_audit" else "true"
    write_scope = "read_only_review" if agent["id"] == "security_audit" else "workspace_only"
    is_project_manager = str(agent["id"] == "project_manager").lower()
    lines = [
        f"id = {toml_string(agent['id'])}",
        f"name = {toml_string(agent['name'])}",
        f"description = {toml_string(agent['description'])}",
        'version = "1.0"',
        '',
        '[codex]',
        f"agent_type = {toml_string(agent['type'])}",
        'callable = true',
        f"entry_agent = {is_project_manager}",
        f"user_facing = {is_project_manager}",
        '',
        '[permissions]',
        f"workspace_root = {toml_string(root)}",
        f"write_scope = {toml_string(write_scope)}",
        f"allowed_write_roots = [{toml_string(root)}]",
        f"can_write_workspace = {can_write}",
        'can_write_outside_workspace = false',
        'must_handoff_high_risk_tasks = true',
        '',
        '[handoff]',
        'reports_to = "project_manager"',
        'high_risk_handoff_target = "project_manager"',
        'security_review_agent = "security_audit"',
        '',
        "developer_instructions = '''" + agent["instructions"] + "'''",
        '',
    ]
    return "\n".join(lines)
def write_file(path: Path, content: str, force: bool) -> bool:
    if path.exists() and not force:
        return False
    path.write_text(content, encoding="utf-8", newline="\n")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a local multi-agent project scaffold.")
    parser.add_argument("target", nargs="?", default=".", help="Project root to scaffold. Defaults to current directory.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing scaffold files. Does not delete unrelated files.")
    args = parser.parse_args()

    root = Path(args.target).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    agents_dir = root / "agents"
    agents_dir.mkdir(exist_ok=True)

    root_text = str(root)
    operations = []
    conflicts = []

    files = {
        root / "config.toml": CONFIG.format(root=root_text.replace("\\", "\\\\")),
        root / "AGENTS.md": AGENTS_MD.format(root=root_text),
    }
    for agent in AGENTS:
        files[agents_dir / agent["file"]] = agent_toml(agent, root_text)

    for path, content in files.items():
        if write_file(path, content, args.force):
            operations.append(f"wrote {path}")
        else:
            conflicts.append(str(path))

    for item in operations:
        print(item)
    if conflicts:
        print("Conflicts: existing files were not overwritten. Re-run with --force only after project-manager approval:", file=sys.stderr)
        for path in conflicts:
            print(f"  {path}", file=sys.stderr)
        return 2

    print(f"Created multi-agent scaffold in {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())