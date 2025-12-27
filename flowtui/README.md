# Flow System — Agent Onboarding & Vision

This project is an experiment-turned-platform: a **unified way to design, connect, inspect, and deploy systems** ranging from small toys to serious production apps.

---

## What This Is

A **flow-first system editor** where:

- **Flows** orchestrate behavior (not just “actions”)
- **Views** are trees (HTML as a connected structure)
- **Contracts** define guarantees between parts
- **Inspector** makes wiring explicit and editable
- **Deploy** is built-in, boring, and reliable

Everything is discoverable, inspectable, and connected.

---

## Core Mental Model

- **Flow**  
  A named, composable unit of behavior.  
  Example: `core.auth.login`

- **View**  
  A tree, not a file.  
  Views contain components, layouts, subviews.

- **Contract**  
  Inputs / outputs / expectations.  
  Contracts are first-class, not comments.

- **Inspector**  
  The truth panel.  
  Shows properties, bindings, behaviors, models.

- **Deploy**  
  Treated like Next.js / Vercel / Heroku:  
  simple, opinionated, low-friction.

---

## Why This Exists

Modern dev pain points:
- Hidden wiring
- Invisible coupling
- Too many files, not enough understanding
- “Where is this defined?” fatigue
- Deployment anxiety

This system makes **structure visible** and **change safe**.

Old ideas, modern execution:
- Geocities simplicity
- Component mindset
- Flow-based thinking
- Visual + textual hybrid

---

## Current State (v0.x)

- One-file prototype
- Textual-based TUI
- 3–4 column layout:
  - Flows
  - Flow View (tree)
  - Inspector
  - Deploy (mock)

No real functionality yet.  
Everything is **visual + conceptual** on purpose.

---

## Immediate Priorities

1. Nail the **mental model**
2. Keep everything **simple and inspectable**
3. Avoid premature abstractions
4. Make it fun, not enterprise-heavy
5. Optimize for learning and exploration

---

## Near-Term Tasks

- Inspector: editable fields (still mocked)
- Click → selection propagation everywhere
- View tree refinements (components, slots, bindings)
- Flow discovery rules (dot notation, folders)
- Better visual hierarchy & spacing
- Keyboard-first navigation

---

## Future Direction

- Real HTML parsing → tree, behaviours, frontend integration, full stack
- Real contracts (schemas)
- Flow execution sandbox
- Logs & trace visualization
- Local + cloud deploy targets
- Plugin system for languages/frameworks
- Export to real projects

---

## Non-Goals (For Now)

- Full IDE replacement
- Complex backend logic
- Heavy config files
- Premature scaling concerns

---

## How to Think as an Agent

- Prefer **clarity over power**
- Prefer **visible structure over magic**
- If something is confusing, it probably needs an Inspector
- If something is hidden, surface it
- If something feels boring, that’s good (deploy, infra)

---

## Final Note

This is not just a tool.  
It’s a **way of thinking about systems**.

Build things that explain themselves.

---

## Detailed Architecture

For a deep dive into the technical implementation, including backend framework choices, Flow definition, and frontend interactivity (`flow.js`), please refer to [`ARCHITECTURE.md`](./ARCHITECTURE.md).
