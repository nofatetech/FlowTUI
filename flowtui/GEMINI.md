# Gemini's Project Guide: FlowTUI

This document outlines my understanding of the FlowTUI project, its architecture, and goals. It will serve as my internal guide for assisting with development.

## 1. Core Project Understanding

- **What it is:** `FlowTUI` is not the end-user application. It is a powerful, terminal-based IDE designed for building and understanding web applications that follow a specific server-centric architectural pattern.
- **Core Philosophy:** The project is heavily inspired by server-rendered frameworks (like Rails, Laravel) but with a modern, reactive user experience powered by a minimal frontend library (like HTMX, Phoenix LiveView).
- **My Role:** My primary function is to help build and evolve the `FlowTUI` itself. I must understand that the TUI's features (Explorer, Inspector, etc.) are meant to visualize and manipulate the components of this server-centric architecture.

## 2. The "Flow" Architecture

This is the architecture that the TUI helps to build.

### A. The Big Picture
1.  **Server is King:** All application state and rendering logic resides on the server (Python/FastAPI).
2.  **Thin Client:** The frontend (`flow.js`) is minimal. Its only job is to render HTML from the server and send user events back up. There is no complex client-side state management.
3.  **The Reactive Loop:**
    - A user interacts with an element in the browser (e.g., clicks a button with a `flow:click` attribute).
    - `flow.js` intercepts this, sends a JSON payload to a universal `/___flow___` endpoint on the server.
    - The FastAPI backend finds the correct "Flow" (a Python class) and executes the right method (e.g., `post`).
    - The method returns new state, which the server uses to render a small, updated **HTML fragment**.
    - `flow.js` receives this HTML fragment and performs a targeted swap into the DOM, updating the page without a full reload.

### B. Backend: Flows-as-Resources
- **Flows are Python Classes:** Each backend workflow (e.g., `login`, `addItemToCart`) is an explicit Python class inheriting from `BaseFlow`. This makes them discoverable and testable.
- **Methods are Verbs:** Class methods map directly to HTTP verbs (`get`, `post`, `put`, `delete`), providing a clean, REST-like structure without magic decorators.

### C. Frontend: Declarative Wiring
- **HTML Templates:** Views are standard HTML.
- **`flow:` Attributes:** Special HTML attributes create a declarative link between the view and the backend Flows.
  - `flow:submit`, `flow:click`: Specifies which Flow and method to trigger.
  - `flow:target`: A CSS selector for where the returned HTML fragment should be placed.
  - `flow:before-send`, `flow:after-swap`: Hooks to run small pieces of client-side JavaScript for managing transient UI state (e.g., showing/hiding spinners, disabling buttons).

## 3. Project Goals & Tasks

This is the development roadmap for the TUI, based on `docs/tasks.md`.

### Immediate Priorities:
- Focus on simplicity, clarity, and making the tool fun and easy to explore.
- Avoid premature abstractions and enterprise-level complexity.
- Solidify the core mental model of how the TUI represents the "Flow" architecture.

### Near-Term Goals:
- Implement interactivity in the TUI (e.g., making Inspector fields editable).
- Enable click-to-select propagation across all panels.
- Refine the visual hierarchy and implement keyboard-first navigation.

### Future Vision:
- The TUI will eventually interact with real codebases:
  - Parsing HTML to build the view tree.
  - Executing Flows in a sandbox.
  - Visualizing logs and traces.
  - Deploying to various targets.
  - Exporting work to real, standalone projects.

## 4. Development Conventions

- **Package Installation:** Use `uv pip install` when adding dependencies.
