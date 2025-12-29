from pydantic import BaseModel
from typing import List, Optional

from backend.models.fleet.vehicle import Vehicle

class VehicleSearchInput(BaseModel):
    """
    Input schema for searching vehicles.
    """
    query: Optional[str] = None
    limit: int = 10
    offset: int = 0

class VehicleListResult(BaseModel):
    """
    Output schema for a list of vehicles.
    """
    vehicles: List[Vehicle]
