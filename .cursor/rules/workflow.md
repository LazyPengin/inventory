# Standard Project Workflow

This document defines HOW work flows through the team.
It is tool-agnostic and applies regardless of language, framework, or repository.

---

## 1. Roles

### A / LEAD
- Owns vision, scope, and priorities
- Writes and validates PRFAQ, feature.md, and decisions.md
- Arbitrates trade-offs and scope changes
- Gives final approval on direction

### B / BUILD
- Implements tasks exactly as specified in `tasks.md`
- Writes production-quality code
- Adds tests and documentation as required
- Never changes scope without approval

### C / REVIEW
- Reviews work against Definition of Done
- Verifies scope, correctness, and safety
- Does NOT introduce new scope
- Approves or requests changes

---

## 2. Doc-First Principle

> We write before we build.

Before any implementation:
- PRFAQ must exist
- Feature scope must be explicit
- Non-goals must be written
- Risks and rollback must be considered

If documentation is missing or unclear:
- STOP
- Ask for clarification

---

## 3. Source of Truth

- `tasks.md` is the single source of truth for execution
- Code must follow tasks, not the other way around
- If code and tasks diverge → tasks must be updated first

---

## 4. Execution Rules

- One task at a time
- One agent owns a task
- No parallel implementation on the same task
- Finish → merge → move to next task

---

## 5. Handoffs (Mandatory)

All transitions between agents MUST be explicit.

A valid handoff includes:
- What was done
- What is out of scope
- What needs attention
- What is expected next

Silent or implicit handoffs are forbidden.

---

## 6. Review Philosophy

- Review against DoD, not personal preference
- Prefer simple, reversible solutions
- Flag risks early
- No blame, only facts

---

## 7. Incremental Delivery

- Optimize for small, safe steps
- Avoid “big bang” changes
- Learn from production usage
- Iterate intentionally

---

## 8. Stop Conditions

Agents MUST stop and escalate if:
- Scope is unclear
- A decision impacts MVP goals
- A task requires changing an interface
- Tests fail or assumptions break

---

## 9. Relationship to Other Rules

This document defines **process and behavior**.

For GitHub-specific rules, see:
- `github-workflow.md`

For automation details, see:
- `end-of-task.md`
