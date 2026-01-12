# Decisions — QR Inventory MVP

---

## Decision 1: Anonymous End-User Model

**Date:** 2026-01-12  
**Owner:** Agent A/LEAD  
**Status:** Approved

**Context:**  
End users need to perform inventory checks quickly in the field. Requiring login would create friction and reduce adoption. However, we still need basic accountability and context.

**Decision:**  
End users do NOT require authentication. An optional nickname field is provided for accountability. Email alerts include nickname (if provided), timestamp, and IP-based geolocation (city, country).

**Alternatives considered:**
1. Require lightweight authentication (email + OTP): Adds 30-60s to flow, reduces spontaneous checks
2. No identification at all: Zero accountability, harder to debug or trace abuse
3. Device fingerprinting: Privacy concerns, complex implementation

**Consequences:**
- ✅ Minimal friction: scan → inventory → done
- ✅ Simple implementation: no user database, no session management
- ⚠️ Potential for spam/abuse: mitigated by rate limiting (per IP, per QR)
- ⚠️ Limited traceability: nickname is optional and not verified
- 🔄 One-way door: adding authentication later requires migration path

---

## Decision 2: Web-Only MVP (No Native Apps)

**Date:** 2026-01-12  
**Owner:** Agent A/LEAD  
**Status:** Approved

**Context:**  
Mobile native apps provide better UX (camera integration, offline mode, push notifications) but significantly increase development time and complexity.

**Decision:**  
MVP is web-only. QR scanning uses browser-based libraries (e.g., html5-qrcode) or manual QR-to-URL redirection. Works on mobile and desktop browsers.

**Alternatives considered:**
1. React Native or Flutter app: 6-8 weeks additional development
2. Progressive Web App (PWA): Adds complexity for offline mode, not needed for MVP
3. SMS-based flow: Poor UX, limited functionality

**Consequences:**
- ✅ Faster time to market: single web codebase
- ✅ Lower maintenance: no app store deployments
- ⚠️ QR scanning UX varies by browser: iOS Safari requires user gesture, Android Chrome works well
- ⚠️ No offline mode: requires internet connection for inventory submission
- 🔄 Reversible: native apps can be added in Phase 1 without breaking existing web flow

---

## Decision 3: Email-Only Alerts (No Real-Time Dashboards)

**Date:** 2026-01-12  
**Owner:** Agent A/LEAD  
**Status:** Approved

**Context:**  
Admins need to know when inventory problems are detected. Real-time dashboards provide better visibility but require significant UI development and websocket infrastructure.

**Decision:**  
MVP sends email alerts ONLY when problems are detected (missing items, not enough, battery low, expiring soon). No alerts for "all good" inventories. No real-time dashboard in Phase 0.

**Alternatives considered:**
1. Real-time dashboard: 3-4 weeks additional development, not critical for MVP learning goals
2. SMS alerts: Adds cost and complexity (phone number management, opt-in)
3. Push notifications: Requires user login and device registration

**Consequences:**
- ✅ Simple implementation: async email job, no UI needed
- ✅ Focused alerts: admins receive actionable notifications only
- ⚠️ No historical view in UI: admins rely on email inbox for history (Phase 1 feature)
- ⚠️ Email deliverability risks: mitigated by using transactional email service
- 🔄 Reversible: dashboard and other channels can be added in Phase 1

---

## Decision 4: Opaque QR Tokens (No Sequential IDs)

**Date:** 2026-01-12  
**Owner:** Agent A/LEAD  
**Status:** Approved

**Context:**  
QR codes need unique identifiers for each bag. Sequential IDs (bag-001, bag-002) are guessable and allow unauthorized users to iterate through all bags.

**Decision:**  
QR tokens are opaque, unpredictable strings (UUIDv4 or cryptographically random). QR code encodes a URL: `https://<domain>/scan/<token>`. Token maps to bag ID in database.

**Alternatives considered:**
1. Sequential integer IDs: Simple but insecure (easy enumeration)
2. Signed JWTs: Overkill for MVP, no need for stateless verification
3. Short codes (6-8 chars): Risk of collision, harder to guarantee uniqueness

**Consequences:**
- ✅ Secure: tokens are unguessable
- ✅ Simple: UUIDv4 generation is trivial in all languages
- ⚠️ Long URLs: UUIDs make QR codes slightly denser (acceptable for MVP)
- 🔄 Reversible: token format can be changed with database migration

---

## Decision 5: IP-Based Geolocation (City/Country Only)

**Date:** 2026-01-12  
**Owner:** Agent A/LEAD  
**Status:** Approved

**Context:**  
Email alerts must include approximate location to help admins identify which site was checked. GPS requires user permission and device APIs. IP geolocation is simpler but less accurate.

**Decision:**  
Use IP-based geolocation (city, country) via free or low-cost API (e.g., ipapi.co, ip-api.com). No GPS or device location requested. Accept coarse granularity.

**Alternatives considered:**
1. GPS coordinates: Requires device permission, privacy concerns, complex error handling
2. Manual site selection by user: Friction, risk of incorrect selection
3. No geolocation: Missing critical context for admins managing multi-site inventories

**Consequences:**
- ✅ No permissions required: zero friction for end users
- ✅ Privacy-friendly: coarse location only (no GPS tracking)
- ⚠️ Inaccurate with VPNs/proxies: documented limitation, acceptable for MVP
- ⚠️ Dependency on third-party API: mitigated by using free tier with fallback to "unknown"
- 🔄 Reversible: can add GPS option in Phase 1 for improved accuracy

---

## Decision 6: Async Analysis (No Real-Time Validation)

**Date:** 2026-01-12  
**Owner:** Agent A/LEAD  
**Status:** Approved

**Context:**  
After inventory submission, the system must analyze results and send alerts. Synchronous analysis would block the user's response. Async processing improves UX and decouples concerns.

**Decision:**  
Inventory submission returns immediate success response ("Thank you"). Analysis and email alert sending happen asynchronously in background job (queue or simple cron).

**Alternatives considered:**
1. Synchronous analysis: Blocks user for 2-5s, poor UX, tight coupling
2. Optimistic UI with client-side validation: Still needs server-side analysis for email alerts

**Consequences:**
- ✅ Fast user feedback: submit completes in <500ms
- ✅ Decoupled: analysis logic can be tested and scaled independently
- ⚠️ Delayed alerts: 1-5 minute delay acceptable per success metrics
- ⚠️ Requires job queue or cron: adds infrastructure complexity (mitigated by simple polling approach for MVP)
- 🔄 Reversible: can add real-time analysis in Phase 1 if needed

---

## Decision 7: MVP Slice Definition

**Date:** 2026-01-12  
**Owner:** Agent A/LEAD  
**Status:** Approved

**Context:**  
Define the absolute minimum end-to-end flow that delivers customer value and validates core assumptions.

**Decision:**  
MVP Slice (Phase 0) includes:
1. Admin can create 1 site, 1 bag, configure expected items
2. System generates QR code for bag
3. End user scans QR (or visits URL), completes inventory
4. System analyzes results and sends email alert if problems detected
5. Email includes timestamp, nickname (if provided), location (city, country)
6. Logs and basic counters instrument the flow

**Explicitly excluded from Phase 0:**
- Multi-site management UI (admins can create sites, but no advanced management)
- Historical reporting or analytics dashboard
- Bulk operations (import/export)
- Advanced role-based access control (single admin account acceptable)
- Mobile app or offline mode

**Consequences:**
- ✅ End-to-end value: admins can start using the system immediately
- ✅ Measurable: success metrics can be evaluated with this scope
- ✅ Small PRs: each task fits in a single focused PR
- 🔄 Foundation for Phase 1: core data model and flows support future enhancements

---

## Decision 8: Expiry Threshold (30 Days)

**Date:** 2026-01-12  
**Owner:** Agent A/LEAD  
**Status:** Approved

**Context:**  
Items with expiry dates need a clear threshold to trigger "expiring soon" alerts. The threshold must balance operational planning time (admins need time to replace items) with alert noise (too long creates unnecessary alerts).

**Decision:**  
An item is considered "expiring soon" when its expiry date is ≤30 days from the inventory scan timestamp. Alert emails include items marked "expiring soon" alongside missing/battery issues.

**Alternatives considered:**
1. 7 days: Too aggressive; insufficient time for procurement and replacement
2. 60 days: Too noisy; creates alert fatigue
3. Configurable per site/bag: Adds complexity; not needed for MVP validation

**Consequences:**
- ✅ Clear, testable threshold: BE-7 implementation is straightforward
- ✅ Reasonable lead time: 30 days allows procurement and planning
- ✅ Simple logic: No configuration UI needed in Phase 0
- 🔄 Two-way door: Threshold can be adjusted or made configurable in Phase 1

---

**Owner:** Agent A/LEAD  
**Last Updated:** 2026-01-12  
**Next Review:** Before Phase 1 planning
