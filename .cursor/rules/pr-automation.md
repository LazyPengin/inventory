# PR Automation (GitHub CLI) — Mandatory

## Requirement
All agents must create Pull Requests via GitHub CLI (`gh`) when completing a task.

This only works if:
- `gh` is installed
- `gh auth status` shows logged in
- the branch is pushed to origin

If `gh` is not available, the agent must STOP and ask the user to create the PR manually.

---

## Standard end-of-task procedure (for B/BUILD)

### 1) Ensure branch and clean working tree
- Must be on `pr/<task-id>-<slug>`
- `git status` must be clean

### 2) Run tests
- `python -m pytest -q` (or project equivalent)
- DB tasks: also run alembic upgrade/downgrade checks

### 3) Commit
Commit format:
`<TASK-ID>: <summary> (AgentID:<id>)`

### 4) Push branch
`git push -u origin <branch>`

### 5) Create PR automatically
Use:
`gh pr create --base main --head <branch> --title "<TASK-ID>: <title>" --body "<body>"`

### 6) Post PR link in handoff
Handoff MUST include:
- PR URL (must be /pull/<number>, not /pull/new/...)
- `git show --stat`
- test output

---

## PR body template (copy/paste)

### Scope
- What changed (1–5 bullets)

### Out of scope
- Explicitly excluded items

### How to test
- Commands to run tests locally

### Risks & rollback
- Risk level + how to rollback

---

## Failure mode
If PR creation fails:
- Print the exact error output
- Do NOT proceed to next task
- Ask the user to fix `gh` auth or permissions