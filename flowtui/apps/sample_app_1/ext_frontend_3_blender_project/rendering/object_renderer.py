# This is the "View" layer for Blender.
# It contains the logic for taking data models (e.g., from a Flow)
# and converting them into actual Blender objects (meshes, lights, etc.).

# import bpy

class ObjectRenderer:
    """
    Takes data contracts and renders them into the Blender scene.
    This module is the only one that should perform `bpy` operations
    to manipulate scene objects.
    """
    def render_product(self, product_model):
        """
        Consumes a 'Product' data model and creates a corresponding
        3D representation.
        """
        print(f"Rendering product: {product_model['name']}")
        # bpy.ops.mesh.primitive_cube_add(...)
        pass
