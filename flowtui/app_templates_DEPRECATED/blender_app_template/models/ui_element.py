# In Domain-Driven Design (DDD), this is an "Entity" or "Value Object".
# It is a pure data container with no logic or framework-specific code.
# This is the "Model" in MVC.
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class UIElement:
    """
    Represents the abstract data for a UI element in our scene.
    It knows nothing about Blender, 3D geometry, or how to draw itself.
    """
    id_name: str  # The unique identifier, like an HTML 'id' attribute.
    element_type: str  # e.g., 'panel', 'button'. Used by the View to decide how to render.
    
    # --- Data specific to the element's state ---
    location: tuple[float, float, float]
    scale: tuple[float, float, float]
    label: str
    
    # --- This is the key to our "Flow" architecture in Blender ---
    # This string declaratively defines what action should be triggered on interaction.
    # It's the direct equivalent of `flow:click="products.add_item"` in the web template.
    flow_action: Optional[str] = None
