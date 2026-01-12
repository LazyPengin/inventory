# End Of Task Checklist

This checklist defines the mandatory steps to officially complete a task.

A task is NOT considered complete until all steps below are satisfied.
This applies to all agents (human or AI).

## Preconditions

Before running this checklist, ALL of the following must be true:

- Task scope was defined via Start New Task
- Work was done on a dedicated branch
- A Pull Request exists for the task

## Code & Tests

Confirm that:

- All changes are committed
- Branch is up to date with main
- All tests pass locally

Required command:
python -m pytest -q

## GitHub / Merge

Confirm that:

- Pull Request has been approved
- Pull Request is merged into main
- No additional commits are pending on the task branch

## Documentation & Scope Check

Confirm that:

- Implementation matches the approved scope
- No out-of-scope features were added
- Relevant documentation has been updated if needed
- Decisions are recorded if new trade-offs were introduced

## Handoff

Write a clear handoff including:

- Task ID
- Summary of what was implemented
- Test results
- Known limitations or follow-ups
- Confirmation that the task is complete

The handoff must be explicit.

END OF TASK CONFIRMATION

Task ID: <TASK-ID>
Branch: pr/<task-id>-<slug>
PR: <PR URL>
Tests: PASS
Scope respected: YES
Out-of-scope changes: NO

Task is complete and merged to main.

## Final Rule

If any step above is incomplete:
- The task is NOT done
- Do NOT start a new task
- Resolve issues first

This checklist is mandatory and non-negotiable.
