from pydantic import BaseModel
from typing import Literal

class Vehicle(BaseModel):
    """
    Represents a single remote-controlled vehicle in the fleet.
    """
    id: str  # e.g., "rover-01"
    status: Literal["idle", "running_mission", "maintenance", "offline"]
    battery_percent: float
    location: tuple[float, float] # Simple X, Y coordinates
