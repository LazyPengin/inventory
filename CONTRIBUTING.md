# Contributing Guide

This project supports multiple agents (human and AI).
Consistency and discipline are required.

## Before You Start

You MUST:
- Read workflow.md
- Follow github-workflow.md
- Run start-new-task.md

Skipping these steps may invalidate your contribution.

## How to Contribute

1. Pick a task from tasks.md
2. Run Start New Task checklist
3. Create a branch
4. Implement only the scoped task
5. Write tests
6. Run tests
7. Open PR
8. Wait for approval

## Coding Standards

- Keep changes focused
- Avoid unrelated refactors
- Follow existing patterns
- Tests are mandatory

## Task Gates (Mandatory)

This project enforces two mandatory gates:

1. Start New Task  
   Required before ANY code is written.

2. End Of Task  
   Required before starting the next task.

These gates apply to all contributors (human and AI).

See:
- .cursor/rules/start-new-task.md
- .cursor/rules/end-of-task.md

## Commits

Commits should include task ID when possible.
Example:
BE-3: bag CRUD endpoints

## Reviews

Reviews check:
- Scope
- Clarity
- Tests
- Alignment with decisions

## Completing a Task

After implementation and merge:
- Run the End Of Task checklist
- Write a clear handoff
- Confirm main is synced

See:
- .cursor/rules/end-of-task.md

## Final Rule

If something is unclear:
- Do not guess
- Check decisions.md
- Ask before implementing
