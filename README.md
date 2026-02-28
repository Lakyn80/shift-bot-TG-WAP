# Shift Bot TG / WAP

Telegram and WhatsApp–oriented shift scheduling backend designed for small teams and service businesses.

The project focuses on clean backend architecture, role-based access, and deterministic business rules for attendance and shift tracking. It is built as a production-ready API with full test coverage and CI integration.

---

## Overview

Shift Bot is a backend system for managing work shifts, attendance, and roles (admin / manager / user).  
It is designed to be consumed by messaging bots (Telegram, WhatsApp) or lightweight frontends.

Key goals:
- clear separation of business rules
- strict role-based access control
- environment-driven configuration
- high testability and CI reliability

---

## Architecture

Client (Telegram / WhatsApp Bot or Web UI)  
→ REST API  
→ Business Rules (attendance, shifts, roles)  
→ Database (SQLAlchemy + Alembic)  

All sensitive configuration and behavior toggles are controlled via environment variables.

---

## Backend

Tech stack:
- Python 3.11+
- FastAPI
- SQLAlchemy
- Alembic
- JWT authentication
- pytest
- Docker

Core features:
- User authentication via JWT
- Role-based access control (admin / manager / user)
- Shift and attendance management
- Modular attendance rules configurable via env flags
- Deterministic business logic (no hidden side effects)

---

## Security

- JWT secret loaded strictly from environment variables
- No secrets committed to version control
- Role guards enforced at API level
- Clear separation between auth, business logic, and persistence

---

## Database & Migrations

- SQLAlchemy ORM
- Alembic migrations
- Seed logic for initial admin and manager roles
- Database-agnostic design (SQLite for dev, easily replaceable with Postgres)

---

## Testing & CI

- Full unit and integration test coverage with pytest
- Attendance logic fully covered by tests
- GitHub Actions pipeline for automated test execution
- Explicit PYTHONPATH configuration for CI stability

---

## Repository Structure

backend/ – application logic, auth, attendance rules, API routes  
.github/workflows/ – CI pipelines  
alembic.ini / migrations – database migrations  
pytest.ini – test configuration  
requirements.txt – backend dependencies  
README.md

---

## Project Status

Active development.

Planned extensions:
- Telegram bot integration
- WhatsApp (WAP) integration
- Shift notifications and reminders
- Reporting and export endpoints

---

## License
MIT License © 2026 Lukiora

