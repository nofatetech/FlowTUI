# This is the "View" in MVC.
# Its only job is to take data models and render them into a visible form.
# This is the ONLY file in the architecture that should import `bpy`.
# This separation ensures that if Blender's API changes, or we want to
# render to a different engine (e.g., Godot, Unreal), we only need to
# change this file.

import bpy
from models.ui_element import UIElement

class ObjectFactory:
    """
    Takes data models and turns them into visible 3D objects in the scene.
    """
    def render_layout(self, elements: list[UIElement]):
        """
        Renders a list of UIElement models into the Blender scene.
        This is the equivalent of rendering a Jinja2 template.
        """
        print(f"View: Rendering {len(elements)} elements into the scene.")
        for model in elements:
            # Decide what kind of primitive to create based on the model's type
            if model.element_type in ["panel", "button"]:
                bpy.ops.mesh.primitive_cube_add(
                    location=model.location,
                    scale=model.scale
                )
            
            # The newly created object is automatically the active one
            blender_obj = bpy.context.object
            blender_obj.name = model.id_name # Set the object name to our ID

            # --- Declarative Data-Binding ---
            # Here, we attach the abstract data from the model to the concrete
            # Blender object using Custom Properties.
            blender_obj["element_type"] = model.element_type
            blender_obj["label"] = model.label
            
            # This is the crucial step that wires the object for interactivity.
            # We are "binding" the flow action to the object itself.
            if model.flow_action:
                blender_obj["flow_action"] = model.flow_action
                print(f"  - Bound '{model.flow_action}' to object '{model.id_name}'")
