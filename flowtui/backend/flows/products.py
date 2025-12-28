from backend.models.product import Product

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
    Routes: INDEX, HTMX_SNIPPET_PRODUCT_LIST
    """
    def index_get(self) -> dict:
        """index get."""
        print("index get")
        return {} # ??

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

