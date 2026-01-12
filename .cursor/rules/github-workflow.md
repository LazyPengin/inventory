# GitHub Workflow (Mandatory)

This document defines how GitHub is used in this project.
All contributors and agents MUST follow these rules.

This workflow is designed for:
- GitHub-first development
- Small, incremental Pull Requests
- Automation via GitHub CLI (gh)
- Multi-agent collaboration (Lead / Build / Review)

---

## 1. Branching Strategy

- Never commit directly to main
- Every task must be implemented in its own branch

Branch naming convention:
pr/<task-id>-<short-slug>

Examples:
- pr/infra-1-project-setup
- pr/be-3-bags-crud
- pr/db-1-core-schema

---

## 2. One Task = One Pull Request

- Each task from tasks.md maps to exactly one Pull Request
- Do not bundle multiple tasks in the same PR
- A task is considered complete only after its PR is merged into main

---

## 3. Local Development Rules

Before pushing code:
- Working tree must be clean
- Only files related to the task may be committed
- All required tests must pass

Project defaults:
- Backend: python -m pytest -q
- Database changes: alembic upgrade and downgrade must succeed

---

## 4. Commit Rules

Commit message format (mandatory):

<TASK-ID>: <short description> (AgentID:<id>)

Example:
BE-3: bags CRUD + qr_token (AgentID:B01)

---

## 5. Push Rules

- Push the branch to origin before requesting review
- Use:
git push -u origin <branch-name>

---

## 6. Pull Request Creation (Mandatory)

Preferred method: GitHub CLI (gh)

If gh is available, PRs must be created using:

gh pr create --base main --head <branch-name> --title "<TASK-ID>: <title>" --body "<PR body>"

PR validity rule:
- A valid PR URL must be in the form /pull/<number>
- Links like /pull/new/... are NOT valid PRs
- If a handoff does not include a real PR URL, review must be refused

---

## 7. Pull Request Content Requirements

Each Pull Request must include:
- Clear description of what changed
- Explicit out-of-scope items
- How to test the change locally
- Risks and rollback plan

PRs should remain small and easy to review.

---

## 8. Review and Merge Rules

- All PRs target main
- Merge only after:
  - Tests pass
  - C/REVIEW approval
- After merge:
  - Sync local main
  - Delete the branch (local and remote)

---

## 9. Handoff Contract

A handoff to C/REVIEW is valid only if it includes:
- A real PR URL (/pull/<number>)
- git show --stat output
- Test output
- Short summary of changes and risks

If any element is missing, the handoff is invalid.

---

## 10. Automation Expectation

Builders are expected to:
- Use GitHub CLI when available
- Follow the End-of-Task checklist
- Stop and report errors instead of bypassing the workflow

Related documents:
- workflow.md
- end-of-task.md
