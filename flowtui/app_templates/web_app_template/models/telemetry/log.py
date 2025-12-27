from pydantic import BaseModel
from datetime import datetime

class Log(BaseModel):
    """
    Represents a single telemetry log entry from a vehicle.
    """
    timestamp: datetime
    vehicle_id: str
    speed_kph: float
    position_x: float
    position_y: float
    event: str | None = None # Optional event, e.g., "obstacle_detected"
