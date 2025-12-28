from models.product import Product

# This acts as our in-memory database for the example.
# In a real app, this would be a database connection.
db_products = {
    1: Product(id=1, name="Laptop"),
    2: Product(id=2, name="Keyboard"),
    3: Product(id=3, name="Mouse"),
}

class Products:
    """
    Manages the product catalog.
    Routes: LIST, CREATE, HTMX_SNIPPET_PRODUCT_LIST
    """
    def get_all(self) -> dict:
        """Returns the state for the initial page load."""
        print("Flow 'products.get_all' executed.")
        return {"products": list(db_products.values())}

    def add_item(self, params: dict) -> dict:
        """
        Handles adding a new item. 
        Returns ONLY the new item's data for partial rendering.
        """
        print(f"Flow 'products.add_item' executed with params: {params}")
        new_id = max(db_products.keys()) + 1 if db_products else 1
        
        # Basic validation
        item_name = params.get("name")
        if not item_name or len(item_name) < 2:
            # In a real app, you'd return a proper error response
            raise ValueError("Product name must be at least 2 characters.")

        new_product = Product(id=new_id, name=item_name)
        db_products[new_id] = new_product
        
        # Convention: The key in the returned dict ("product") should match
        # the variable name used in the partial template (_item.html).
        return {"product": new_product}

    def HTMX_SNIPPET_PRODUCT_LIST(self) -> dict:
        """
        Returns the full list of products for a complete re-render of the list.
        In a real app, you might add pagination or filtering here.
        """
        print("Flow 'products.HTMX_SNIPPET_PRODUCT_LIST' executed.")
        # Add a new mock product to demonstrate the reload is working
        if 4 not in db_products:
            db_products[4] = Product(id=4, name="Flow Mousepad")
        return {"products": list(db_products.values())}

