# Gemini's Guide: Blender Application Template

This document outlines my understanding of the "Blender App" template. It's a proof-of-concept demonstrating how the core "Flow" architectural pattern (Model-View-Controller) can be applied to a non-web, 3D environment.

## 1. Core Architectural Pattern

The goal is to maintain a strict separation of concerns, just like in the web app template.

*   **Model (`models/`):** Defines the raw, application-agnostic data. These are simple Python data structures (like `dataclasses`) that hold information but contain **no Blender-specific code**. For example, a `Shape` model would store `name`, `location`, and `scale`, but would not know what a `bpy.ops.mesh` is. This makes the data portable and the logic pure.

*   **Flow/Controller (`flows/`):** Contains the "business logic." Its responsibility is to decide **WHAT** should exist in the scene. It creates and manages lists of the data models. For example, `SceneManager().get_initial_scene()` would return a `list[Shape]` models, but it does not know how to draw them.

*   **View (`views/`):** This is the "renderer." Its sole purpose is to take the data models provided by a Flow and translate them into actual objects within the Blender environment. It contains all the `bpy` specific code. The `ObjectFactory().render(shapes)` method iterates through the models and calls `bpy.ops.mesh.primitive_cube_add` etc., to create a visible representation of the data.

## 2. The Execution Loop

The application is bootstrapped by a main script (`main.py`) which executes the MVC flow in a clear sequence:

1.  **Setup:** The `main.py` script first prepares the environment (e.g., clearing the default Blender scene).
2.  **Call Flow:** It instantiates a Flow class (e.g., `SceneManager`) and calls a method to get the desired state of the world as a list of data models.
3.  **Call View:** It then passes this list of models to the View layer (e.g., `ObjectFactory`), which is responsible for rendering the final output in the Blender scene.

This opinionated structure makes the "application" easy to reason about, test, and expand, even in a creative environment like Blender.
