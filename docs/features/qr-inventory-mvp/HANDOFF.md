# Handoff: QR Inventory MVP — Agent A/LEAD → Agent B/BUILD

**Date:** 2026-01-12  
**From:** Agent A/LEAD  
**To:** Agent B/BUILD  
**Feature:** qr-inventory-mvp

---

## Summary

The QR Inventory MVP feature package is complete and ready for implementation. All documentation follows the doc-first approach required by our multi-agent playbook.

---

## What's Ready

✅ **PRFAQ** (`prfaq.md`)  
- Customer problem, solution, and wow moment defined
- Success metrics and MVP scope documented
- FAQ addresses customer and internal questions

✅ **Feature Definition** (`feature.md`)  
- Clear customer impact and success metrics
- Non-goals explicitly listed (no scope creep)
- Risks and rollback plan documented

✅ **Decisions** (`decisions.md`)  
- 7 key architectural and product decisions recorded
- Alternatives and consequences documented
- Reversibility assessed (two-way vs one-way doors)

✅ **Tasks Breakdown** (`tasks.md`)  
- 20 tasks organized into logical phases
- Each task sized for a single PR
- Definition of Done provided

---

## MVP Slice (Phase 0)

**End-to-end flow:**
1. Admin logs in and configures: site → bag → expected items
2. System generates unique QR code for bag
3. End user scans QR (or visits URL manually)
4. End user completes visual inventory checklist (no login)
5. System analyzes results asynchronously
6. If problems detected: email alert sent to admin (with timestamp, location, nickname)

**What's included:**
- Admin authentication and CRUD (sites, bags, items)
- QR code generation (opaque tokens)
- Anonymous inventory flow (optional nickname)
- Status capture: present, missing, not enough, battery low
- Expiry date tracking (optional per item)
- Battery testing flag (optional per item)
- Async analysis and email alerts (problems only)
- IP-based geolocation (city, country)
- Structured logs and basic metrics

**What's explicitly excluded (Phase 1+):**
- Native mobile apps (web-only MVP)
- User authentication for end users
- Real-time dashboards
- Multi-language support
- Photo uploads
- Offline mode
- Bulk import/export

---

## Execution Order

**Priority: Complete each task before moving to the next. Each task = 1 PR.**

### Week 1: Foundation + Database
1. **INFRA-1:** Project setup and dependencies
2. **INFRA-2:** Email service integration
3. **INFRA-3:** IP geolocation integration
4. **DB-1:** Core schema (sites, bags, items)
5. **DB-2:** Inventory and alert schemas
6. **DB-3:** Indexes and constraints

### Week 2: Backend Core
7. **BE-1:** Admin authentication (single admin account, no RBAC)
8. **BE-2:** Site CRUD endpoints
9. **BE-3:** Bag CRUD endpoints (with QR token generation)
10. **BE-4:** Item configuration endpoints
11. **BE-5:** QR lookup endpoint
12. **BE-6:** Inventory submission endpoint (with rate limiting per IP/QR)

### Week 3: Async Processing + Admin UI
13. **BE-7:** Async analysis and email alerts (expiring soon = ≤30 days)
14. **FE-1:** Admin login page
15. **FE-2:** Site management UI
16. **FE-3:** Bag management UI (with QR display)
17. **FE-4:** Item configuration UI

### Week 4: End-User UI + Instrumentation
18. **FE-5:** Inventory checklist page
19. **FE-6:** Success confirmation page
20. **OPS-1:** Structured logging
21. **OPS-2:** Basic metrics/counters

---

## Critical Success Factors

**1. Small, incremental PRs**
- Each task = one focused PR
- No bundling multiple tasks together
- Easier for C/REVIEW to approve

**2. Instrumentation is part of MVP**
- Logs must include: qr_token, session_id, timestamp, response_time
- Metrics required: counters (lookups, submissions, alerts) + timer (submission duration)
- OPS-1 and OPS-2 are NOT optional

**3. Respect the MVP Slice**
- Do NOT implement Phase 1 features (dashboards, bulk ops, advanced auth)
- Simplicity over completeness
- Focus on learning and validation

**4. Email deliverability**
- Test with multiple email providers (Gmail, Outlook, etc.)
- Avoid spam folder (use reputable transactional email service)
- Provide admin test feature

**5. Security and abuse prevention**
- Admin passwords: bcrypt or similar
- QR tokens: UUIDv4 or cryptographically random
- HTTPS required for all endpoints
- Rate limiting on inventory submission (per IP address and per QR token)
  - Simple middleware or in-memory limits sufficient for MVP
  - Prevents spam/abuse of anonymous scanning

**6. Alert logic thresholds**
- "Expiring soon" = item expiry date ≤30 days from scan timestamp
- No configuration UI needed; hardcoded threshold for MVP
- See Decision 8 in decisions.md for rationale

---

## Key Decisions Summary

**Decision 8 (NEW):** Expiry threshold = 30 days
- Items are flagged "expiring soon" when expiry date ≤30 days from scan
- Provides reasonable lead time for procurement
- Hardcoded in BE-7; no admin configuration in Phase 0

**Admin authentication scope (clarified):**
- Single admin account for MVP
- No role-based access control (RBAC) in Phase 0
- Multi-admin and permissions are Phase 1 features

**Rate limiting (clarified):**
- Applied to BE-6 (inventory submission endpoint)
- Per IP address: prevent spam from single source
- Per QR token: prevent repeated abuse of specific bag
- Simple in-memory limits acceptable for MVP scale

---

## Key Metrics to Instrument

| Metric | Measurement | Target |
|--------|-------------|--------|
| Email alert latency | timestamp(submit) → timestamp(email_sent) | <5 minutes |
| Inventory completion rate | (completed / started) × 100 | >90% |
| Check duration | timestamp(submit) - timestamp(first_load) | <2 minutes (median) |
| Bag coverage | distinct bags checked per 30 days | 75% |
| System uptime | health check monitoring | 99.5% |

---

## Handoff to C/REVIEW

### GitHub-first (Mandatory)
For every task:
- Create a branch **before** coding: `pr/<task-id>-<slug>`
- Push the branch to GitHub
- Open a Pull Request (PR) to `main`
- Only then request C/REVIEW approval
- **Merge the PR before starting the next task**
- Delete the branch after merge (remote + local)

### PR Validity Rule (Mandatory)

- The handoff MUST include a real Pull Request URL in the form:
  `/pull/<number>`
- Links like `/pull/new/...` or "PR ready" without a number are NOT accepted
- If a valid PR URL is missing, C/REVIEW must refuse the handoff
- Builders should create PRs via GitHub UI or GitHub CLI (`gh pr create`)

### Review loop (per task)
After each task is implemented:
1. B/BUILD submits a PR with task ID in title (e.g., "INFRA-1: Project setup")
2. B/BUILD posts handoff including:
   - `git show --stat`
   - test output (`python -m pytest -q`)
   - migration up/down output (if DB change)
3. C/REVIEW validates against DoD (Definition of Done)
4. C/REVIEW approves or requests changes
5. Once approved: merge PR → sync `main` → start next task

---

## Questions or Clarifications

If you encounter ambiguity:
1. Prefer simple, reversible solutions (two-way doors)
2. Consult `decisions.md` for architectural guidance
3. Escalate to Agent A/LEAD if decision impacts MVP Slice or metrics

---

**Ready to implement. Start with INFRA-1.**

---

**Prepared by:** Agent A/LEAD  
**Date:** 2026-01-12  
**Next Agent:** Agent B/BUILD
