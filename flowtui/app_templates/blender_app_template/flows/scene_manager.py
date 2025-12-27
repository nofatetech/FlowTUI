# This is the "Controller" in MVC or an "Application Service" in DDD.
# Its job is to orchestrate the business logic. It fetches and prepares
# data models, but does NOT know how to render them.

from models.ui_element import UIElement

class SceneManager:
    """
    Defines WHAT should be in the scene by creating and managing lists of data models.
    This mimics the backend logic in the FastAPI template.
    """

    def get_homepage_layout(self) -> list[UIElement]:
        """
        This is analogous to a `get` request in the web app.
        It returns the list of UIElement data models that constitute our static "homepage".
        """
        print("Flow: Defining the initial state of the 'homepage'.")

        # Define a main panel
        main_panel = UIElement(
            id_name="main_panel",
            element_type="panel",
            location=(0, 0, 0),
            scale=(3, 2, 0.1),
            label="Product Display"
        )

        # Define a button that will sit on the panel
        add_button = UIElement(
            id_name="add_item_button",
            element_type="button",
            location=(0, -1.5, 0.2), # Position relative to the panel
            scale=(0.8, 0.4, 0.2),
            label="Add Item",
            # This declaratively wires up the button for future interactivity.
            # An event handler would look for this property to trigger the correct logic.
            flow_action="products.add_item"
        )
        
        return [main_panel, add_button]

    def add_item(self, params: dict) -> UIElement:
        """
        This is analogous to a `post` request. In a real interactive app,
        an event handler would call this method. It returns a NEW data model.
        The view would then take this model and render just the new object,
        mimicking an HTMX DOM swap.
        """
        print(f"Flow: 'add_item' would be called with params: {params}")
        new_item = UIElement(
            id_name="new_item_1",
            element_type="item",
            location=(0, 0, 0.2), # Position for a new item
            scale=(0.5, 0.5, 0.5),
            label="New Item"
        )
        return new_item

