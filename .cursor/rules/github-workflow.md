# GitHub Workflow Rules (Mandatory)

## Golden rule
One task = one branch = one PR = merge to main before starting next task.

## Branch naming
- pr/<task-id>-<short-slug>
Examples:
- pr/db-1-core-schema
- pr/be-2-sites-crud
- pr/infra-2-email

## Before coding (required)
Builder must output:
- Task ID
- Branch name
- Files expected to change
- Out of scope list
Then wait for C/REVIEW approval.

## Work must NOT happen on main
- No direct commits on main.
- If work accidentally lands on main:
  - immediately create a branch from that state
  - reset main back to origin/main
  - open PR from the branch

## Commit rules
- Small commits allowed, but PR must contain only one task.
- Commit message:
  - <task-id>: <summary> (AgentID:<id>)
Examples:
- DB-1: core schema + migration (AgentID:B01)
- BE-2: sites CRUD endpoints (AgentID:B01)

## PR rules (required)
PR description must include:
- Task ID + scope
- How to run tests
- Migration up/down confirmation (if DB change)
- Risk + rollback

## Merge rules
- Merge only after:
  - tests pass locally
  - C/REVIEW approves
- After merge:
  - delete the PR branch (remote and local)
  - sync local main: git checkout main && git pull

## Mandatory end-of-task checklist (Builder)
- git status clean
- tests passing
- push branch
- PR opened
- handoff posted to C/REVIEW with:
  - git show --stat
  - pytest output
  - alembic upgrade/downgrade output (if relevant)