from pydantic import BaseModel
from typing import Literal

class Mission(BaseModel):
    """
    Represents a task assigned to a vehicle.
    """
    mission_id: str
    vehicle_id: str # The vehicle this mission is assigned to
    task: Literal["patrol_area", "retrieve_target", "return_to_base"]
    waypoints: list[tuple[float, float]]
