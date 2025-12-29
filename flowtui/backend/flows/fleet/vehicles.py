from flow_system import BaseFlow
from backend.models.fleet.vehicle import Vehicle
from backend.contracts.fleet import (
    VehicleSearchInput,
    VehicleListResult
)

class Vehicles:
    """
    Manages the vehicles in the fleet.
    """

    # FLOW: index
    class index(BaseFlow):
        """
        Manages the list of vehicles.
        Routes: LIST_VEHICLES
        """
        consumes = VehicleSearchInput
        produces = VehicleListResult
        template = "fragments/vehicles/list.html"

        # GET default verb controller
        def get(self, input: VehicleSearchInput) -> VehicleListResult:
            # Placeholder logic: In a real app, this would query a database or service
            # For now, return a dummy list of vehicles.
            return VehicleListResult(vehicles=[
                Vehicle(id="rover-01", status="idle", battery_percent=85.5, location=(10.0, 20.0)),
                Vehicle(id="drone-05", status="running_mission", battery_percent=30.2, location=(30.5, 15.0)),
            ])

    # FLOW: status_synch
    class status_synch(BaseFlow):
        """
        Handles status synchronization for vehicles.
        Routes: SYNC_STATUS
        """
        consumes = VehicleSearchInput # Assuming input might be needed to select vehicles
        produces = VehicleListResult # Assuming it returns updated vehicle status
        template = "fragments/vehicles/status_update.html"

        # GET verb controller
        def get(self, input: VehicleSearchInput) -> VehicleListResult:
            # Placeholder logic for status synchronization.
            # In a real app, this would update vehicle statuses based on some criteria.
            # For now, just return an empty list.
            return VehicleListResult(vehicles=[])
