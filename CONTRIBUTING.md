# Contributing Guide

Thank you for contributing to this project.

This repository follows a **doc-first, multi-agent, GitHub-first workflow**.
Please read this document carefully before making changes.

---

## Golden Rules

1. **One task = one branch = one Pull Request**
2. **Never commit directly to `main`**
3. **A task is done only after the PR is merged into `main`**
4. **Always start new work from an up-to-date `main`**
5. **Write docs before writing code**

---

## Branching Strategy

- Branch naming:
    pr/<task-id>-<short-slug>

Examples:
- `pr/infra-1-setup`
- `pr/db-1-core-schema`
- `pr/be-2-sites-crud`

---

## Development Workflow

1. Start with documentation (PRFAQ / feature / decisions / tasks)
2. Create a branch **before coding**
3. Implement **one task only**
4. Push branch to GitHub
5. Open a Pull Request to `main`
6. Request C/REVIEW approval
7. Merge PR into `main`
8. Sync local `main`
9. Start next task

---

## Pull Request Requirements

Each PR must include:
- Task ID in the title (e.g. `BE-2: Site CRUD endpoints`)
- Clear scope description
- How to run tests
- Migration upgrade/downgrade confirmation (if applicable)
- Risk and rollback notes

---

## Testing

Before requesting review:
```bash
python -m pytest -q

For database changes:
 alembic upgrade head
 alembic downgrade -1