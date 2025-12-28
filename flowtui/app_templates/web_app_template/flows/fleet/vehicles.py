from models.fleet.vehicle import Vehicle

class Vehicles:
    """
    Manages the fleet of RC vehicles.
    Routes: LIST, GET, COMMAND, STATUS
    """

    def list(self):
        """Returns a list of all vehicles."""
        pass

    def get(self, vehicle_id: str):
        """Returns the state of a single vehicle."""
        pass

    def command(self, vehicle_id: str, command: dict):
        """Sends a command to a vehicle (e.g., move, start_mission)."""
        pass

    def status(self, vehicle_id: str, status: dict):
        """Sends status."""
        pass
