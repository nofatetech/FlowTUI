from pydantic import BaseModel, Field
from typing import List

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

class ProductItem(BaseModel):
    id: int
    name: str
    price: float

class ProductSearchInput(BaseModel):
    query: str = ""

class ProductListResult(BaseModel):
    products: List[ProductItem]

