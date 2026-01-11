# Feature — QR Inventory MVP

## Description
A web-based system allowing anyone to perform visual inventory checks on physical bags/kits by scanning QR codes, with automatic email alerts sent to admins when problems are detected.

## Single-Threaded Owner (STO)
Agent A/LEAD

## Status
Proposed

## Customer impact
**Who benefits:**
- Site managers gain visibility into inventory status without manual reporting
- Field staff perform fast, guided inventory checks without login friction
- Safety officers receive timely alerts when items are missing or expired

**How:**
- Reduces inventory check time from 10+ minutes (manual paperwork) to <2 minutes
- Eliminates missed checks (no login barrier)
- Provides proactive alerts with location context

## Success metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Email alert latency | <5 minutes from inventory completion | Server-side timer (submission → email sent) |
| Inventory completion rate | >90% of started sessions complete successfully | Log: (completed / started) × 100 |
| Check duration | <2 minutes (median) | Log: timestamp(submit) - timestamp(first_load) |
| Bag coverage | 75% of bags checked ≥1x per 30 days | Aggregation: distinct bag checks per month |
| System uptime | 99.5% for QR-to-inventory flow | Health check monitoring |

## Non-goals

Explicitly **out of scope** for MVP:
- Native mobile apps (web-only)
- User authentication for end users
- Real-time dashboards or analytics UI
- Multi-language support
- Photo uploads or evidence capture
- Offline mode or progressive web app features
- Barcode, NFC, or alternative scan methods
- Bulk operations (import/export)
- Third-party API integrations
- Advanced reporting or historical trend analysis

## Dependencies

**External:**
- Email delivery service (e.g., SMTP relay, SendGrid, AWS SES)
- IP geolocation service (e.g., ipapi.co, ip-api.com)

**Internal:**
- Web server with HTTPS support
- Relational database (SQLite/PostgreSQL/MySQL)
- QR code generation library

## Two-way door / One-way door

**Two-way door (reversible):**
- QR token format: can migrate tokens if needed
- Email alert templates: easily updated
- Geolocation provider: swappable
- Database schema (within reason): migrations supported

**One-way door (hard to reverse):**
- Anonymous end-user model: adding authentication later requires migration path
- Web-only approach: native apps would require separate codebase
- Email-only notifications: adding SMS/push requires new infrastructure

**Decision:** Acceptable. MVP focuses on learning and validation. Core flows are reversible.

## Risks & mitigations

| Risk | Mitigation |
|------|------------|
| Email delivery failures (spam filters, rate limits) | Use reputable transactional email service; test deliverability; provide admin email test feature |
| QR codes damaged/unreadable in field | Provide printable backup: bag ID + short URL for manual entry |
| IP geolocation inaccurate (VPN, proxy) | Document limitation; log raw IP; coarse granularity acceptable for MVP |
| Anonymous model abused (spam inventories) | Rate limiting per IP and per QR token; simple CAPTCHA if needed |
| Scale beyond MVP assumptions | Phase 1 planning includes capacity review; current limits documented |

## Rollback plan

**How to revert safely:**
1. **Feature flag:** All email alerts controlled by env var `ALERTS_ENABLED=false`
2. **Database:** Inventory logs are append-only; no destructive operations
3. **Graceful degradation:** If email service fails, log alert to database for manual review
4. **Emergency disable:** Admin UI includes "pause alerts" toggle per site or globally

**Rollback time:** <5 minutes (toggle feature flag or env var, restart service)

## Notes

- MVP Slice is **end-to-end**: admin setup → QR scan → inventory → alert email
- All documentation, code, APIs, and metrics names in English
- Focus on simplicity: no premature optimization, no over-engineering
- Instrumentation is part of MVP: logs + counters required for every phase
