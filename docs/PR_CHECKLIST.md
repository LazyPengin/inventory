# PR Checklist (One Task)

- [ ] Branch name is pr/<task-id>-<slug>
- [ ] Changes match one task only
- [ ] `python -m pytest -q` passes
- [ ] (DB) `alembic upgrade head` and `alembic downgrade -1` verified
- [ ] No secrets committed (.env not tracked)
- [ ] PR description includes scope, test commands, rollback