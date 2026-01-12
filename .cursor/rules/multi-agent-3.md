# Multi-Agent Playbook (3 Agents)

This project operates using a strict 3-agent workflow to ensure clarity,
quality, and scalability.

## Agents

### A/LEAD — Product & Scope Owner
Responsibilities:
- Owns product vision and scope
- Writes and validates PRFAQ and feature.md
- Defines success metrics and MVP Slice
- Records architectural and product decisions
- Arbitrates trade-offs and priorities
- Ensures doc-first discipline

### B/BUILD — Implementation Owner
Responsibilities:
- Owns task breakdown and implementation
- Converts tasks into small, incremental PR-sized changes
- Writes code, tests, and basic instrumentation
- Respects MVP Slice and avoids Phase 1 scope creep
- Documents changes and risks for review

### C/REVIEW — Bar-Raiser Reviewer
Responsibilities:
- Reviews docs and code against the Definition of Done (DoD)
- Identifies blockers, risks, and over/under-engineering
- Ensures metrics, rollback, and documentation are present
- Has final authority to approve or request changes
- Does NOT write implementation code

---

## Core Rules

1. **Doc-first always**
   No implementation code may be written before:
   - PRFAQ exists
   - feature.md exists
   - MVP Slice is explicitly defined

2. **MVP Slice is mandatory**
   Every feature must define an end-to-end MVP Slice that:
   - Delivers user-visible value
   - Is measurable via metrics
   - Can be delivered in small increments

3. **Small increments**
   - One task = one PR
   - PRs must be small, focused, and reversible

4. **Interfaces over implementation**
   - Any change to APIs, schemas, or data models must be documented
   - Record decisions in decisions.md (and design.md if needed)

5. **Instrumentation is part of MVP**
   - At minimum: logs + key counters
   - Metrics are not “Phase 1”

6. **Reviewer is the quality gate**
   - C/REVIEW can block merges if DoD is not met
   - Approval is required before moving to the next task

---

## Definition of Done (DoD)

A task or feature is considered done only if:
- MVP Slice requirements are met
- Tests pass (unit + minimal integration)
- feature.md and tasks.md are up to date
- Decisions are recorded when applicable
- Basic metrics/logs are implemented
- Rollback plan is documented (even if simple)
- No Phase 1 features are included in Phase 0

---

## Message Format (MANDATORY)

All agent communications must use this format:

[AGENT] A/LEAD | B/BUILD | C/REVIEW  
[FEATURE] <feature-slug>  
[CONTEXT] Brief description of the situation  
[OUTPUT] Files changed, decisions made, or tasks completed  
[NEXT] Explicit handoff to the next agent with a clear action

Messages not following this format should be considered invalid.

---

## Workflow Summary

1. A/LEAD defines and validates the feature (docs only).
2. B/BUILD implements tasks incrementally according to MVP Slice.
3. C/REVIEW reviews each increment and enforces DoD.
4. Repeat until MVP Slice is complete.

---

## Language Rules

- Canonical documentation (PRFAQ, feature.md, tasks.md, decisions.md) MUST be written in English.
- Agent-to-agent communication may be in English or French.
- If a document already exists in English, do not create a parallel French version.
- When explaining decisions or summaries in chat, agents may provide bilingual explanations if requested.
- Code, identifiers, APIs, and metrics names must always be in English.