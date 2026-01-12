# Standard Workflow

This file defines the global working rules for this project.
It applies to all agents (human or AI).

## Core Principles

1. Documentation before implementation
2. Small, incremental tasks (one task = one PR)
3. Explicit handoffs between agents
4. Single source of truth: tasks.md
5. Prefer reversible decisions
6. Clarity before optimization

## Task Lifecycle (Mandatory)

Every task follows this lifecycle:

1. Start New Task
2. Implementation
3. Pull Request
4. Merge to main
5. End Of Task
6. Start next task

Skipping any step invalidates the task.

## Cursor Prompts (Mandatory)

The following Cursor prompts MUST be used:

- Start New Task  
  See: .cursor/rules/start-new-task.md  
  Prompt: .cursor/rules/prompts/start-task.md

- Close Task  
  See: .cursor/rules/end-of-task.md  
  Prompt: .cursor/rules/prompts/close-task.md

Cursor is expected to refuse implementation if these prompts are skipped.

## Mandatory Task Initialization

Before starting ANY task:

- The "Start New Task" checklist MUST be completed
- No code may be written before this step
- Any work started without this step is invalid

Reference:
- .cursor/rules/start-new-task.md

## Mandatory Task Closure

Before considering ANY task complete:

- The **End Of Task** checklist MUST be completed
- Tests MUST pass
- The task MUST be merged to main
- A handoff MUST be written

Reference:
- .cursor/rules/end-of-task.md

A task is NOT complete until this step is done.

## GitHub First

All work MUST follow:
- .cursor/rules/github-workflow.md

No direct commits to main.
No branch without a task.

## Enforcement

Rule priority:
1. workflow.md
2. github-workflow.md
3. CONTRIBUTING.md
