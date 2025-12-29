from flow_system import BaseFlow
from backend.models.product import Product
from contracts.products import (
    ProductSearchInput,
    ProductListResult
)
from services.product_service import ProductService


# This acts as our in-memory database for the example.
# In a real app, this would be a database connection.
db_products = {
    1: Product(id=1, name="Laptop"),
    2: Product(id=2, name="Keyboard"),
    3: Product(id=3, name="Mouse"),
}


# TODO: ROUTES
# implement optional routes that point to flows, so we dont have to use the whole flow name;
# are routes per flow, per domain? i think per domain


class Products:
    """
    Manages the products domain.
    """




    # FLOW: index
    class index(BaseFlow):
        consumes = ProductSearchInput
        produces = ProductListResult
        template = "fragments/product_list.html"

        # GET default verb controller 
        def get(self, input: ProductSearchInput) -> ProductListResult:
            products = ProductService.search(input.query)
            return ProductListResult(products=products)

    # FLOW: htmx_blocks
    class htmx_blocks(BaseFlow):
        """
        Returns html blocks depending on what the frontend needs. 
        """
        # TODO: fix
        consumes = ProductSearchInput
        produces = ProductListResult
        template = "fragments/product_list.html"

        # GET verb controller
        def get(self, input: ProductSearchInput) -> ProductListResult:
            # products = ProductService.search(input.query)
            # return ProductListResult(products=products)
            pass


