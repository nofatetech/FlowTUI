# This file defines the custom UI panels that will be shown
# inside the Blender user interface.

# import bpy

class MainScenePanel(): # (bpy.types.Panel)
    """
    Creates a new panel in the 3D View's sidebar.
    This is the user-facing part of the frontend.
    """
    # --- MOCK ---
    # bl_label = "Flow Controls"
    # bl_idname = "SCENE_PT_layout"
    # ... etc ...

    def draw(self, context):
        """
        Defines the panel's layout. The buttons here are the equivalent
        of the HTMX `flow:click` attributes.
        """
        layout = self.layout
        # This button is declaratively wired to a backend flow.
        # An operator would read this `flow_action` property and
        # make an API call to the backend.
        op = layout.operator("wm.flow_trigger", text="Spawn Vehicle")
        op.flow_action = "fleet.vehicles.create"
