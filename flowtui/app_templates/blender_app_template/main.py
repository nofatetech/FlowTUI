# This is the main entry point for the Blender application.
# It acts as the application's bootstrap, orchestrating the
# Model-View-Controller (MVC) components.

import bpy

# To make this script runnable within Blender's text editor, we need to handle
# Python's module caching if we re-run the script.
if "bpy" in locals():
    import importlib
    from . import flows, views, models
    importlib.reload(models.ui_element)
    importlib.reload(flows.scene_manager)
    importlib.reload(views.object_factory)
else:
    from . import flows, views, models

from flows.scene_manager import SceneManager
from views.object_factory import ObjectFactory

def run_app():
    """
    Executes the application logic. This is the equivalent of a user
    visiting the homepage in the web application.
    """
    print("-" * 30)
    print("Executing Blender App Template...")

    # --- Setup ---
    # A clean slate ensures the operation is idempotent.
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # --- Step 1: Call the Controller (Flow) ---
    # Get the "business logic" - a list of data models defining the desired scene state.
    # The main script doesn't know *how* this list is created, only that the Flow provides it.
    scene_flow = SceneManager()
    ui_models = scene_flow.get_homepage_layout()

    # --- Step 2: Pass data to the View (Renderer) ---
    # The View takes the pure data models and translates them into actual 3D objects.
    # The main script doesn't know *how* they are rendered, only that the View handles it.
    object_renderer = ObjectFactory()
    object_renderer.render_layout(ui_models)

    print("Blender app initial layout executed successfully.")
    print("-" * 30)

# --- How to Run ---
# 1. Open Blender.
# 2. Go to the "Scripting" workspace.
# 3. Open this `main.py` file in the Text Editor.
# 4. Ensure the `blender_app_template` directory is in Blender's script path,
#    or run Blender from the directory containing the template.
# 5. Click the "Run Script" button (the play icon).

# This will execute the script in Blender's context.
if __name__ == "__main__":
    run_app()
