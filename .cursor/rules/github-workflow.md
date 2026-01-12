# GitHub Workflow

This file defines how GitHub is used in this project.
It applies to all contributors and agents.

## Branching Rules

- Default branch: main
- All work happens on a branch

Branch naming:
pr/<task-id>-<short-slug>

Examples:
- pr/be-2-sites-crud
- pr/db-1-core-schema

## Pull Requests

Every task MUST result in a Pull Request.

PR requirements:
- Title includes task ID
- Clear summary
- Test output included
- Migration output included if applicable

## Merge Rules

- PR approval required
- All tests must pass
- No direct commits to main
- Merge before starting next task
- Delete branch after merge

## Task Completion

A task is only considered complete when:
- PR is merged into main
- Tests are green
- End-of-task checklist has been completed

## Order of Operations

1. Create branch
2. Implement task
3. Run tests
4. Push branch
5. Open PR
6. Review
7. Merge
8. Sync main
9. Start next task

## Tooling

Using GitHub CLI is encouraged.

Example:
gh pr create --base main --head <branch> --title "<TASK-ID>: <title>"

## Task Completion Contract

A task is only complete when ALL of the following are true:

- PR is merged into main
- Tests are green
- End Of Task checklist has been completed
- Main branch is synced locally

If not, no new task may start.
