# Contributing Guide

Thank you for contributing to this project.

This repository follows a GitHub-first, doc-first, multi-agent workflow
designed for clarity, safety, and incremental delivery.

By contributing, you agree to follow the rules below.


## Core Principles

- Doc-first: write before you build
- One task = one branch = one PR
- No direct commits to main
- Small, reviewable changes
- Explicit handoffs between roles
- Automation over manual steps

## Roles

A / LEAD
- Owns scope, priorities, and product decisions
- Validates PRFAQ, feature definitions, and decisions

B / BUILD
- Implements tasks exactly as defined in tasks.md
- Writes production-quality code and tests
- Never expands scope without approval

C / REVIEW
- Reviews work against Definition of Done
- Approves or requests changes

## Source of Truth

- tasks.md is the single source of truth for execution
- Code must follow tasks, not the other way around
- If code and tasks diverge, update tasks first

## Branching Rules

- Never commit directly to main
- Every task must use its own branch

Branch naming:
pr/<task-id>-<short-slug>

Examples:
pr/be-2-sites-crud
pr/db-1-core-schema

## Commit Rules

Commit message format:
<TASK-ID>: <short description> (AgentID:<id>)

Example:
BE-4: bag item configuration endpoints (AgentID:B01)

Only commit files related to the current task.

## Testing Requirements

Before opening a Pull Request:
- All relevant tests must pass

Default command:
cd backend
python -m pytest -q

## Pull Request Rules

- One task = one Pull Request
- Do not bundle multiple tasks

PR validity rule:
- A real PR URL must be /pull/<number>
- /pull/new/... links are not valid

Preferred PR creation method:
GitHub CLI (gh)

## Review and Merge

- All PRs target main
- Merge only after review approval
- After merge:
  - Sync local main
  - Delete the feature branch

## End-of-Task Checklist

A task is complete only after:
- Tests pass
- Code is committed
- Branch is pushed
- Pull Request is created
- Handoff includes PR link, git show --stat, and test output

See .cursor/rules/end-of-task.md for details.

## Stop Conditions

Stop and ask for guidance if:
- Scope is unclear
- A change impacts MVP goals
- A task modifies another task's interface
- Tests fail

## Related Documents

- .cursor/rules/workflow.md
- .cursor/rules/github-workflow.md
- .cursor/rules/end-of-task.md
