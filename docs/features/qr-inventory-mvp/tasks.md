# Tasks — QR Inventory MVP

**Feature:** QR Inventory MVP  
**Owner (STO):** Agent A/LEAD (definition) → Agent B/BUILD (execution)  
**Status:** Planning  
**Last Updated:** 2026-01-12

---

## Overview

**Total tasks:** 20  
**Completed:** 0  
**In progress:** 0  
**Blocked:** 0  

**Timeline:** 4-5 weeks  
**Target completion:** 2026-02-15

---

## Phase 0: MVP Slice (Weeks 1-4)

### Foundation (Week 1)

- [ ] **INFRA-1:** Set up project structure and dependencies — B/BUILD (1 day)
  - Initialize web framework (e.g., Flask/Express/Django)
  - Configure database (SQLite for dev, PostgreSQL for prod)
  - Set up environment variables (.env)
  - Success: Server runs locally, database connects

- [ ] **INFRA-2:** Configure email service integration — B/BUILD (1 day)
  - Integrate SMTP or transactional email API (e.g., SendGrid)
  - Test email sending with template
  - Add email sending to logs
  - Success: Test email received

- [ ] **INFRA-3:** Integrate IP geolocation service — B/BUILD (0.5 day)
  - Add geolocation API client (e.g., ipapi.co)
  - Fallback to "unknown" if API fails
  - Success: IP → city/country lookup works

### Database Schema (Week 1)

- [ ] **DB-1:** Create core schema (sites, bags, items) — B/BUILD (1 day)
  - Table: `sites` (id, name, created_at)
  - Table: `bags` (id, site_id, qr_token, name, created_at)
  - Table: `items` (id, bag_id, name, requires_battery_test, tracks_expiry, created_at)
  - Success: Tables created, constraints validated

- [ ] **DB-2:** Create inventory and alert schemas — B/BUILD (1 day)
  - Table: `inventory_sessions` (id, bag_id, nickname, ip_address, city, country, created_at)
  - Table: `inventory_results` (id, session_id, item_id, status, notes, created_at)
  - Table: `alert_log` (id, session_id, alert_type, email_sent_at, created_at)
  - Success: Schema supports full MVP flow

- [ ] **DB-3:** Add basic indexes and constraints — B/BUILD (0.5 day)
  - Index: `bags.qr_token` (unique, indexed for lookups)
  - Index: `inventory_sessions.created_at` (for metrics queries)
  - Constraints: foreign keys, NOT NULL where applicable
  - Success: Query performance acceptable (<100ms for QR lookup)

### Admin Backend (Week 2)

- [ ] **BE-1:** Implement admin authentication — B/BUILD (1 day)
  - Simple login endpoint (username/password)
  - Session management (JWT or server-side session)
  - Password hashing (bcrypt)
  - Success: Admin can log in and access protected endpoints

- [ ] **BE-2:** Implement site CRUD endpoints — B/BUILD (1 day)
  - POST /api/sites (create)
  - GET /api/sites (list)
  - PUT /api/sites/:id (update)
  - DELETE /api/sites/:id (soft delete or restrict if bags exist)
  - Success: CRUD operations work via API tests

- [ ] **BE-3:** Implement bag CRUD endpoints — B/BUILD (1.5 days)
  - POST /api/bags (create, auto-generate qr_token)
  - GET /api/bags (list with site filter)
  - PUT /api/bags/:id (update)
  - DELETE /api/bags/:id (soft delete or restrict if inventory exists)
  - Success: Bag created with unique QR token

- [ ] **BE-4:** Implement item configuration endpoints — B/BUILD (1 day)
  - POST /api/bags/:id/items (add expected item)
  - GET /api/bags/:id/items (list items for bag)
  - PUT /api/items/:id (update item config)
  - DELETE /api/items/:id (remove expected item)
  - Success: Admin can configure items with battery/expiry flags

### End-User Flow (Week 2-3)

- [ ] **BE-5:** Implement QR lookup endpoint — B/BUILD (0.5 day)
  - GET /scan/:token → returns bag details and expected items
  - Return 404 if token invalid
  - Log lookup event (for metrics)
  - Success: Valid QR token returns bag + items JSON

- [ ] **BE-6:** Implement inventory submission endpoint — B/BUILD (1.5 days)
  - POST /api/inventory/:token (submit inventory results)
  - Validate status values (present, missing, not_enough, battery_low)
  - Store in inventory_sessions and inventory_results tables
  - Extract IP and perform geolocation lookup
  - Return success response immediately (async analysis)
  - Success: Inventory stored, response <500ms

- [ ] **BE-7:** Implement async analysis and alert logic — B/BUILD (2 days)
  - Background job: check for problems (missing, not_enough, battery_low, expiring soon)
  - If problems found: generate alert email
  - Send email via configured service
  - Log alert to alert_log table
  - Success: Email received within 5 minutes with correct details

### Admin Frontend (Week 3)

- [ ] **FE-1:** Create admin login page — B/BUILD (0.5 day)
  - Form: username, password
  - Success: Admin can log in and redirect to dashboard

- [ ] **FE-2:** Create site management UI — B/BUILD (1 day)
  - List sites
  - Add/edit/delete site
  - Success: CRUD operations work via UI

- [ ] **FE-3:** Create bag management UI — B/BUILD (1.5 days)
  - List bags (with site filter)
  - Add/edit/delete bag
  - Display QR code (generate via library, e.g., qrcode.js)
  - Provide printable QR page
  - Success: QR code displays and scans correctly

- [ ] **FE-4:** Create item configuration UI — B/BUILD (1 day)
  - List items for selected bag
  - Add/edit/delete item
  - Checkboxes: requires_battery_test, tracks_expiry
  - Success: Admin can configure items via UI

### End-User Frontend (Week 3-4)

- [ ] **FE-5:** Create inventory checklist page — B/BUILD (1.5 days)
  - Display bag name and expected items
  - For each item: radio buttons or dropdown (present, missing, not_enough, battery_low)
  - Optional nickname field
  - Optional notes field per item
  - Submit button
  - Success: Inventory submission works end-to-end

- [ ] **FE-6:** Create success confirmation page — B/BUILD (0.5 day)
  - Thank you message
  - Optional: link to scan another bag
  - Success: User sees confirmation after submission

### Instrumentation & Quality (Week 4)

- [ ] **OPS-1:** Add structured logging — B/BUILD (1 day)
  - Log key events: QR lookup, inventory submission, email sent, errors
  - Include context: qr_token, session_id, timestamp, response time
  - Success: Logs are searchable and actionable

- [ ] **OPS-2:** Add basic metrics/counters — B/BUILD (1 day)
  - Counter: qr_lookups_total
  - Counter: inventory_submissions_total
  - Counter: alerts_sent_total
  - Timer: inventory_submission_duration_ms
  - Success: Metrics exposed (e.g., /metrics endpoint or logs)

---

## Definition of Done (MVP Slice)

### Documentation
- [x] PRFAQ written
- [x] Feature.md completed
- [x] Decisions.md completed
- [x] Tasks.md completed
- [ ] API documentation (inline or README)
- [ ] Runbook (basic troubleshooting guide)

### Implementation
- [ ] All 20 tasks completed
- [ ] Code reviewed by C/REVIEW
- [ ] No linter warnings
- [ ] No security vulnerabilities (basic scan)

### Testing
- [ ] Manual end-to-end test: admin setup → QR scan → inventory → alert email
- [ ] Unit tests for core logic (analysis, email alert triggers)
- [ ] Edge cases tested: invalid QR, missing items, no nickname

### Observability
- [ ] Logs structured and include session_id
- [ ] Metrics instrumented (4 counters + 1 timer minimum)
- [ ] Email alert test feature available to admins

### Operational
- [ ] Deployed to staging environment
- [ ] Rollback plan tested (feature flag toggle)
- [ ] Email deliverability validated (no spam folder)

---

## Task Breakdown Summary

| Phase | Duration | Owner | Tasks |
|-------|----------|-------|-------|
| Foundation | Week 1 | B/BUILD | 3 tasks |
| Database | Week 1 | B/BUILD | 3 tasks |
| Admin Backend | Week 2 | B/BUILD | 4 tasks |
| End-User Flow | Week 2-3 | B/BUILD | 3 tasks |
| Admin Frontend | Week 3 | B/BUILD | 4 tasks |
| End-User Frontend | Week 3-4 | B/BUILD | 2 tasks |
| Instrumentation | Week 4 | B/BUILD | 2 tasks |
| **Total** | **4 weeks** | **B/BUILD** | **20 tasks** |

---

## Dependencies

**Blocking this feature:**
- [ ] Email service account (SendGrid/SMTP) — Status: Pending setup
- [ ] Web hosting environment with HTTPS — Status: Pending infrastructure

**Blocked by this feature:**
- None (MVP is foundational)

---

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Email deliverability issues (spam filters) | High | Medium | Use reputable transactional email service; test with multiple email providers; provide admin test feature |
| QR scanning UX varies by browser | Medium | High | Document supported browsers; provide manual entry fallback (short URL or token input field) |
| IP geolocation inaccurate (VPN/proxy) | Low | Medium | Document limitation; coarse granularity acceptable for MVP; log raw IP for debugging |
| Scale exceeds MVP assumptions | Medium | Low | Monitor metrics; Phase 1 includes capacity planning; current limits documented in PRFAQ |

---

**Owner:** Agent A/LEAD (planning) → Agent B/BUILD (execution)  
**Last Updated:** 2026-01-12  
**Next Review:** Weekly during implementation (B/BUILD → C/REVIEW)
