# Architecture & Design Principles

This document outlines the core architectural decisions for the Flow system. It serves as a blueprint for development, ensuring we build a cohesive and understandable full-stack ecosystem.

## 1. Core Philosophy: Server-Side First

Our approach is heavily inspired by the simplicity and power of server-centric frameworks like Ruby on Rails and Laravel, combined with the modern, reactive user experience of tools like HTMX and Phoenix LiveView.

- **The Server is the Source of Truth:** All application state and rendering logic resides on the server.
- **The Frontend is a Thin Client:** The browser's role is to render HTML and send user events to the server. We will avoid complex client-side state management.
- **The TUI is the IDE:** The `FlowTUI` is not the application itself, but a powerful visual editor for building and understanding applications based on this architecture.

## 2. The Tech Stack

- **Backend:** Python with **FastAPI**. This keeps us in a single language and provides a simple, high-performance foundation.
- **State Management:** Standard server-side practices. State will be managed via sessions, secure cookies, or JWTs.
- **Frontend:** A minimal, custom JavaScript library (`flow.js`) designed specifically for this architecture.

## 3. The "Flow-as-a-Resource" Model

This is the central concept of the backend. It adapts standard RESTful/resource-oriented design for our interactive goals.

- **Flows are Python Classes:** Each "Flow" is a Python class that inherits from a common `BaseFlow`. This makes them discoverable, testable, and easy to reason about.
- **Methods are HTTP Verbs:** The `BaseFlow` class will define methods corresponding to HTTP verbs (`get`, `post`, `put`, `delete`). This aligns our system with web standards and provides a clear structure for handling user actions.
- **No Magic Decorators:** We will favor clean, explicit class-based structures over decorators to keep the code beautiful and easy to understand.

**Example Flow:**
```python
# flows/auth.py

from flow_system import BaseFlow

class login(BaseFlow):
    def get(self, params: dict) -> dict:
        """Renders the initial view state."""
        return {"error_message": ""}

    def post(self, payload: dict) -> dict:
        """Handles the form submission."""
        if authenticate(payload):
            return {"redirect_to": "/dashboard"}
        else:
            return {"error_message": "Invalid credentials."}
```

## 4. The View Layer

- **Templates are HTML:** Views are standard HTML files.
- **Declarative Attributes for Wiring:** We use a special `flow:` attribute namespace to create a declarative, co-located link between the view, the server, and client-side behaviors.
  - `flow:click`, `flow:submit`, `flow:change`: Specifies which Flow to trigger on a user interaction.
  - `flow:trigger`: Triggers a flow on other events (e.g., `every 5s`, `keyup changed delay:500ms`).
  - `flow:poll`: A shorthand to periodically trigger a flow (e.g., `flow:poll="15s"`).
  - `flow:target`: A CSS selector defining which part of the page should be updated by the Flow's response.
  - `flow:loading-class`: A CSS class to apply to an element during the request.
  - `flow:transition`: A CSS class to manage smooth transitions on new content.
  - `flow:push-url`: Updates the browser's URL after a successful request.
  - `flow:on-success`: Triggers a secondary flow after the primary one completes.
  - `flow:before-send="..."`: Executes a block of client-side JavaScript *before* the request is sent.
  - `flow:after-swap="..."`: Executes JavaScript *after* a successful server response has been swapped into the DOM.

## 5. The Frontend (`flow.js`) & The Core Reactive Loop

The "magic" that creates a seamless user experience is handled by a small, efficient JavaScript library.

- **Lightweight & Non-Intrusive:** `flow.js` is not a framework. It attaches event listeners once on page load and then goes dormant. It does **not** run a constant diffing process like React's Virtual DOM.
- **The Loop:**
  1. A user interacts with an element (e.g., `<form flow:submit="auth.login" ...>`).
  2. `flow.js` executes any `flow:before-send` code.
  3. It then intercepts the event and sends a simple JSON payload to a universal FastAPI endpoint (e.g., `/___flow___`). The payload contains the flow name and form data.
  4. The FastAPI server executes the corresponding Flow class method (e.g., `login().post(...)`).
  5. The Flow method returns a new state dictionary. The server uses this to render an updated **HTML fragment** from the view template.
  6. The server responds with the raw HTML fragment.
  7. `flow.js` receives the HTML and performs a **targeted DOM swap**. It replaces the inner HTML of the element specified in the `flow:target` attribute.
  8. Finally, `flow.js` executes any `flow:after-swap` code.

This approach, inspired by HTMX, gives us the responsive feel of a Single-Page Application with the simplicity and robustness of a server-rendered architecture.

## 6. Client-Side Freedom & Interactivity

To provide creative freedom and handle immediate UI feedback (like spinners or disabling buttons), `flow.js` provides a powerful, yet constrained, set of client-side tools.

### A. The Two States
We make a clear distinction between two types of state:
- **Application State:** The source of truth. Lives on the server (e.g., user data, shopping cart contents).
- **Transient UI State:** Temporary, visual-only state. Lives on the client (e.g., is a button currently disabled? is a spinner visible?). `flow.js` is designed to manage this second category elegantly.

### B. Inline Hooks & DOM Convenience
This is the "C++ Builder" model: behavior is attached directly to the visual element.

- **Contextual Keywords:** Inside `flow:*` attributes, these keywords are available:
  - `this`: The element the attribute is on.
  - `$target`: A direct reference to the element in the `flow:target` attribute.
  - `$event`: The original browser event that triggered the flow.
- **DOM Utility:** We provide a simple `$flow()` helper to avoid verbose code like `document.getElementById`. It returns a collection of elements with chainable helper methods (`.show()`, `.hide()`, `.disable()`, `.addClass()`, etc.).

**Example:** Disabling a form and showing a spinner during a request.
```html
<form
    flow:submit="profile.update"
    flow:target="#profile-view"
    flow:before-send="
        const form = $flow.closest('form', this);
        $flow('.spinner', form).show();
        $flow('input, button', form).disable();
    "
    flow:after-swap="
        const form = $flow.closest('form', this);
        $flow('.spinner', form).hide();
        $flow('input, button', form).enable();
    "
>
    <div class="spinner" style="display: none;">Saving...</div>
    <!-- Form fields and submit button -->
</form>
```

### C. The Signal System (Advanced Escape Hatch)
Inspired by Godot's signals, this is for more complex scenarios where inline code isn't enough. `flow.js` dispatches custom events on the elements involved in the reactive loop.

- **Emitted on the Trigger Element:** `flow:beforeSend`, `flow:response`, `flow:error`.
- **Emitted on the Target Element:** `flow:afterSwap`.

This allows external JavaScript files to "connect" to these signals for complex integrations (like re-initializing a third-party library) without sacrificing the tight, opinionated coupling of the core system.
```javascript
// in a separate app.js
document.getElementById('profile-view').addEventListener('flow:afterSwap', (event) => {
  // Re-initialize a rich text editor inside the newly loaded content.
});
```
