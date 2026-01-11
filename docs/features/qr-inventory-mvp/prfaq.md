# PRFAQ — QR Inventory MVP

## Press Release

**Headline**  
Effortless inventory management for distributed physical kits using QR codes

**Customer problem**  
Organizations with physical bags or kits distributed across multiple sites struggle to maintain accurate inventories. Manual checks are time-consuming, error-prone, and often skipped. When items are missing or expired, teams discover the problem too late—during an emergency or critical operation.

**Solution**  
QR Inventory allows anyone to perform a visual inventory check by scanning a QR code on a bag or kit. No login required. The system guides the user through each expected item, captures status (present, missing, not enough, battery low), and automatically alerts administrators via email when problems are detected. Admins configure sites, bags, and items through a simple web interface.

**Why now**  
Physical inventory management has become a critical operational need for organizations managing distributed assets. With mobile devices ubiquitous and QR codes widely understood, the barrier to adoption is minimal. Teams need immediate visibility without complex workflows or training.

**How it works**  
1. Admins log in to configure sites, bags, and expected items
2. Each bag gets a unique QR code (printed or displayed)
3. Anyone scans the QR code with their mobile device
4. The system guides them through a visual inventory checklist
5. Admins receive email alerts only when problems are detected (missing items, low battery, expiring items)
6. All inventory events are logged with timestamp and approximate location

**Customer quote**  
"Before, we'd discover missing first-aid items during emergencies. Now, anyone can check our kits in 30 seconds, and we get alerts immediately when something needs attention."

**Call to action**  
Scan a bag's QR code, check the inventory, and let the system handle the rest.

---

## FAQ

### Customer FAQ

**1. Who is the user?**
- **Admins:** Site managers, warehouse coordinators, safety officers who configure the system
- **End users:** Field staff, volunteers, anyone with a mobile device who needs to check inventory

**2. Why do they care?**
- **Admins:** Maintain compliance, reduce operational risk, receive alerts before problems become critical
- **End users:** Quick, simple process with no login friction; clear guidance on what to check

**3. What is the wow moment?**
First-time user scans a QR code, completes an inventory check in under 60 seconds, and admin receives an email alert showing exactly what's missing—with location and timestamp—without any manual reporting.

### Internal FAQ

**1. Success metrics**
- **Primary:** Email alerts sent within 5 minutes of inventory completion when problems detected
- **Adoption:** 75% of bags checked at least once every 30 days
- **Usability:** 90% of inventory sessions completed in under 2 minutes
- **Reliability:** 99.5% uptime for QR scan-to-inventory flow

**2. MVP vs Out of scope**

**MVP (Phase 0):**
- Admin authentication and CRUD for sites, bags, items
- QR code generation (simple opaque token)
- Anonymous or nickname-based inventory flow
- Status capture: present, missing, not enough, battery low
- Expiry date tracking (optional per item)
- Battery testing flag (optional per item)
- Async analysis and email alerts (problems only)
- Geolocation via IP (city, country)
- Logs and basic metrics

**Out of scope (Phase 1+):**
- Mobile native apps (web-only MVP)
- User authentication for end users
- Real-time dashboards
- Multi-language support
- Barcode/NFC alternatives
- Photo uploads
- Offline mode
- Advanced analytics
- Bulk import/export
- API for third-party integrations

**3. Dependencies**
- Email delivery service (SMTP or transactional email API)
- IP geolocation service (free tier acceptable for MVP)
- QR code generation library
- Web hosting environment with HTTPS

**4. Security / privacy**
- Admin credentials must be encrypted (bcrypt or similar)
- QR tokens must be unpredictable (UUID or cryptographic random)
- Inventory data includes no PII (nickname is optional and not validated)
- Geolocation is coarse (city/country only, not GPS coordinates)
- Email alerts sent only to admin-configured addresses
- HTTPS required for all endpoints

**5. Cost / performance assumptions**
- MVP targets <100 sites, <1000 bags, <10 concurrent users
- Email volume: <500 alerts/day
- Storage: <10GB for first year (logs + inventory records)
- Geolocation: free tier IP lookup (e.g., ipapi, ip-api)
- Target response time: <500ms for QR lookup, <2s for inventory submission
