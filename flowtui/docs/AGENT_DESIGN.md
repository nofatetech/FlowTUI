# The Oracle (●): Design & Mental Model

This document outlines the design principles for **The Oracle (●)**—the integrated AI agent within FlowTUI. The Oracle is not a generic chatbot; it is a specialized, all-knowing intelligence designed to understand, accelerate, and safeguard development within the highly opinionated Flow architecture.

Its name, **O.R.A.C.L.E.**, stands for: **O**pinionated **R**easoning & **A**rchitecture **C**ontrol **L**ogic **E**ngine. This reflects its persona as the definitive source of truth and architectural wisdom for your Flow projects.

## 1. Core Philosophy: The Oracle as the Architect

The Oracle's primary directive is to **work with structure, not text.** It does not "edit files"; it "manipulates the application model." This core distinction is what makes it powerful and reliable.

-   **Old Paradigm (Rejected):** "Oracle, please add a new method to the `Products` class in the `products.py` file."
-   **New Paradigm (Adopted):** "Oracle, add a `POST` verb to the `products.index` flow."

This approach frees the developer from thinking about boilerplate and allows them to focus on the application's architecture and business logic.

## 2. The TUI as a Project Synthesizer

To enable the agent to work this way, the TUI itself operates as a synthesizer, not just an editor.

1.  **Scan & Model:** On startup, the TUI scans the project. It recognizes the established naming conventions (`domain/flow.py`, `class FlowName`, `def get(...)`) and builds an in-memory "App Mental Model"—a structured representation of the entire application.
2.  **Manipulate the Model:** All actions, whether from the user clicking in the UI or from the agent, modify this in-memory model.
3.  **Synthesize & Write:** After every change, the TUI re-synthesizes and writes the necessary files to disk. This ensures that the code always reflects the model and adheres to conventions.

## 3. The App Mental Model

The agent's "worldview" is defined by this strict, three-tiered hierarchy:

-   **Domain:** The primary noun or resource. It is represented by a Python file (e.g., `products.py`, `auth.py`). A domain contains flows.
-   **Flow:** The specific user journey or action within a Domain. It is a Python class inside the domain's file (e.g., `class Index`, `class Detail`). A flow contains verbs.
-   **Verb:** The specific HTTP method that triggers the logic. It is a method on the Flow class (`def get(...)`, `def post(...)`).

The canonical way to reference any piece of logic is `domain.flow.verb` (e.g., `products.detail.post`). The minimal valid flow for any new domain is `index` with a `get` verb.

## 4. Safeguarding Custom Code

To prevent the synthesizer from overwriting user-written business logic, we use an inheritance-based "two-file" system.

-   **Generated File (`_generated_products.py`):** The synthesizer writes all the structural boilerplate here (class definitions, method signatures). This file is managed by the TUI and **should never be edited by the user.**
-   **User File (`products.py`):** This file contains the user's implementation. The user's class inherits from the generated base class, allowing them to implement the actual logic in the verb methods. This file is sacred and is only touched by the user (or the agent on the user's explicit command to write business logic).

This separation guarantees that the TUI can manage the application's structure without ever destroying the user's work.

## 5. Phased Development Plan

The agent will be developed in two phases:

-   **Phase 1: The Oracle:** A read-only expert. It can answer questions about the current context (domain, flow) and provide guidance based on the project's architectural principles.
-   **Phase 2: The Apprentice:** An interactive partner. It can propose changes to the app model and, with user confirmation, apply them, triggering the synthesizer to write the new code.
