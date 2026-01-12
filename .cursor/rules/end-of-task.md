# End-of-Task Checklist (Mandatory)

This checklist MUST be executed at the end of every task.
A task is NOT considered complete until all steps below are done.

If any step fails, STOP and report the full error output.

---

## 1. Verify branch and working state

- You must NOT be on main
- Working tree must be clean (or changes must belong only to this task)

Commands:
git status
git branch

---

## 2. Run tests (required)

Run the full test suite before any commit.

Backend projects:
python -m pytest -q

Database changes:
- alembic upgrade head
- alembic downgrade -1
- alembic upgrade head

Test output MUST be included in the handoff.

---

## 3. Commit changes

Stage only files related to the task.

Commit message format (mandatory):
<TASK-ID>: <short description> (AgentID:<id>)

Example:
BE-4: bag item configuration endpoints (AgentID:B01)

Commands:
git add <files>
git commit -m "<TASK-ID>: <description> (AgentID:<id>)"

---

## 4. Push branch

Push the branch to origin and set upstream.

Command:
git push -u origin <branch-name>

---

## 5. Create Pull Request (mandatory)

Preferred method: GitHub CLI (gh)

Prerequisites:
- gh installed
- gh auth status shows authenticated

Command:
gh pr create --base main --head <branch-name> --title "<TASK-ID>: <title>" --body "
Scope:
- Describe what changed

Out of scope:
- Explicitly list what is NOT included

How to test:
- cd backend
- python -m pytest -q

Risks & rollback:
- Risk level (Low/Medium/High)
- Rollback: revert merge commit
"

IMPORTANT:
- The returned PR URL MUST be a real PR: /pull/<number>
- Links like /pull/new/... are NOT valid

If PR creation fails:
- STOP
- Paste the exact error output
- Ask for guidance

---

## 6. Final handoff (required)

The handoff message to C/REVIEW MUST include:
- Real PR URL (/pull/<number>)
- git show --stat output
- Test output
- Short summary of changes
- Explicit out-of-scope confirmation

Handoffs missing any of these elements are INVALID.
