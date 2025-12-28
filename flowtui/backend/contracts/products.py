from pydantic import BaseModel, Field

class ProductInput(BaseModel):
    """
    Contract for creating or updating a product.
    """
    name: str = Field(..., min_length=2, description="The name of the product.")
    price: float = Field(..., gt=0, description="The price of the product.")

class ProductOutput(BaseModel):
    """
    Contract for displaying a product.
    """
    id: int
    name: str
