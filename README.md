# QR Inventory MVP

A web-based system for performing visual inventory checks on physical bags/kits using QR codes, with automatic email alerts for administrators.

## Overview

**Status:** In Development (Phase 0 - MVP Slice)

QR Inventory allows anyone to scan a QR code on a bag or kit and quickly perform an inventory check. No login required for end users. Administrators receive email alerts only when problems are detected (missing items, low batteries, expiring items).

## Features (MVP Slice)

- ✅ Admin authentication and site/bag/item management
- ✅ QR code generation for bags
- ✅ Anonymous inventory check flow (scan → checklist → submit)
- ✅ Automatic email alerts for detected problems
- ✅ IP-based geolocation (city, country)
- ✅ Structured logging and basic metrics

## Documentation

- **PRFAQ**: `docs/features/qr-inventory-mvp/prfaq.md`
- **Feature Spec**: `docs/features/qr-inventory-mvp/feature.md`
- **Tasks**: `docs/features/qr-inventory-mvp/tasks.md`
- **Decisions**: `docs/features/qr-inventory-mvp/decisions.md`

## Project Structure

```
inventory/
├── backend/              # Flask REST API
│   ├── app.py           # Main application
│   ├── database.py      # Database configuration
│   ├── requirements.txt # Python dependencies
│   └── README.md        # Backend setup instructions
├── frontend/            # React web application (coming in FE-1)
├── docs/                # Documentation
│   └── features/
│       └── qr-inventory-mvp/
└── README.md           # This file
```

## Quick Start

### Backend Setup

See `backend/README.md` for detailed instructions.

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Server runs at: http://localhost:5000

### Frontend Setup

Coming in task FE-1 (Week 3)

## Development Workflow

This project follows a strict multi-agent workflow:

- **A/LEAD**: Product and scope owner
- **B/BUILD**: Implementation owner (one task = one PR)
- **C/REVIEW**: Quality gate reviewer

See `.cursor/rules/multi-agent-3.md` for complete playbook.

## Success Metrics

| Metric | Target |
|--------|--------|
| Email alert latency | <5 minutes from submission |
| Inventory completion rate | >90% |
| Check duration | <2 minutes (median) |
| Bag coverage | 75% checked ≥1x per 30 days |
| System uptime | 99.5% |

## Tech Stack

- **Backend**: Flask (Python 3.11+)
- **Frontend**: React (coming in FE-1)
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Email**: SendGrid / SMTP (configured in INFRA-2)
- **Geolocation**: ipapi.co (configured in INFRA-3)

## Current Status

**Phase 0 - Foundation (Week 1)**

- [x] **INFRA-1**: Project structure and dependencies ✅
- [ ] **INFRA-2**: Email service integration
- [ ] **INFRA-3**: IP geolocation service
- [ ] **DB-1**: Core database schema
- [ ] **DB-2**: Inventory and alert schemas
- [ ] **DB-3**: Indexes and constraints

See `docs/features/qr-inventory-mvp/tasks.md` for complete task list.

## Contributing

All contributions must follow:
1. Doc-first approach (PRFAQ → feature.md → tasks.md)
2. One task = one PR
3. Definition of Done enforced by C/REVIEW
4. No Phase 1 features in Phase 0

## License

Internal project - not for public distribution.

---

**Last Updated**: 2026-01-12  
**Owner**: Agent B/BUILD (implementation)  
**Version**: 0.1.0
