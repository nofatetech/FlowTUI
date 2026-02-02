# Application Architecture Reference

## Purpose

This document describes the **opinionated architecture** used in the codebase of the apps managed by FlowTUI.

Goals:
- Single deployable **monolith** + optional external Frontend Apps.
- Supports **MPA (server-rendered pages)** and **JSON APIs**
- Clear internal boundaries (DDD-inspired, not dogmatic)
- Shared core logic across internal and external frontends
- Predictable structure for humans and AI agents

This is a **modular monolith with escape hatches**, not microservices.

---

## High-Level Structure

backend/
contracts/
modules/
main/
api/
frontend/
views/
services/
repositories/
providers/
infra/

ext_frontend_1_landing_page/
ext_frontend_2_admin_dashboard/


---

## Core Principles

### 1. One Backend, Many Delivery Mechanisms
- One backend application
- Multiple ways to consume it:
  - Server-rendered pages (MPA)
  - JSON APIs
  - External frontends (SPA, mobile, etc.)

All delivery mechanisms share the same **business logic**.

---

### 2. Services Are the Center of Gravity
All meaningful application logic lives in `services`.

views → services
api → services


Never:
views → api → services


---

### 3. Contracts Define Boundaries
`contracts/` contains **schemas and DTOs** used across boundaries:
- API input/output
- Frontend ↔ backend communication
- External consumer integration

Contracts:
- Have no business logic
- Have no infrastructure dependencies
- Are safe to share across apps

---

## Directory Responsibilities

### `backend/contracts/`
**What the outside world sees**

Contains:
- Request / response schemas
- Public data shapes
- Validation models

Rules:
- No database access
- No service logic
- No framework-specific behavior

May be imported by:
- `api`
- `frontend`
- External frontends

---

### `modules/`
Contains application modules.

Each module is a **vertical slice** of the system.

---

### `modules/main/`
The primary application module.

Responsibilities:
- App composition
- Routing
- Wiring dependencies
- Hosting MPA + API entry points

`main` must remain **thin**.
Business logic does not live here.

---

### `api/`
JSON API endpoints.

Responsibilities:
- HTTP handling
- Authentication / authorization
- Mapping HTTP ↔ contracts
- Calling services

Rules:
- No database access
- No business rules
- No cross-service orchestration

---

### `frontend/views/`
Server-rendered pages (MPA).

Responsibilities:
- HTML rendering
- User interaction handling
- Calling services
- Formatting view models

Rules:
- No API-to-API calls
- No business rules
- No persistence logic

---

### `services/`
**Application use cases**

Responsibilities:
- Business rules
- Application workflows
- Permission checks
- Orchestration of repositories

Rules:
- Framework-agnostic where possible
- No HTTP concerns
- No rendering logic

Services are organized by **use case**, not entity.

---

### `repositories/`
Persistence abstraction layer.

Responsibilities:
- Database queries
- Data mapping
- Storage concerns

Rules:
- No business rules
- No HTTP or frontend logic

---

### `providers/`
Dependency wiring and adapters.

Responsibilities:
- External services
- Third-party APIs
- Email, cache, message brokers

---

### `infra/`
Infrastructure-specific implementations.

Responsibilities:
- ORM models
- Database engines
- Framework integrations
- Low-level technical details

---

## External Frontends

ext_frontend_*/

yaml
Copy code

External applications:
- Use `contracts/` as their source of truth
- Communicate via API only
- Contain no backend business logic

Backend does **not** depend on external frontends.

---

## Dependency Rules (Non-Negotiable)

Allowed:
api → services
frontend → services
services → repositories
services → contracts
api → contracts
frontend → contracts

makefile
Copy code

Forbidden:
services → api
services → frontend
repositories → services
contracts → anything


---

## Request Flow Examples

### Server-Rendered Page (MPA)

HTTP Request
→ frontend/views
→ services
→ repositories


---

### API Request

HTTP Request
→ api
→ services
→ repositories


---

## Why This Architecture

- Avoids premature microservices
- Scales with team size and time
- Keeps logic centralized
- Enables frontend flexibility
- Easy to reason about and refactor

This structure optimizes for:
**clarity > cleverness**  
**boundaries > abstractions**  
**long-term velocity > short-term hacks**

---

## Final Rule

If you don’t know where code belongs:
- If it decides → `services`
- If it stores → `repositories`
- If it formats → `frontend`
- If it communicates → `api`
- If it crosses boundaries → `contracts`