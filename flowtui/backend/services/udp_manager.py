class UdpManager:
    """
    Manages UDP communication for real-time messages, like with RC cars.
    """
    # Convention: The STATUS attribute provides a human-readable state for the TUI.
    STATUS = "Listening on Port 9000"

    def __init__(self, host="127.0.0.1", port=9000):
        self.host = host
        self.port = port
        # Real implementation would bind a socket here.

    def send_command(self, vehicle_id: str, command: str):
        """Sends a command string to a specific vehicle."""
        print(f"UDP: Sending '{command}' to {vehicle_id}...")
        pass

    def receive_telemetry(self):
        """Listens for incoming telemetry data."""
        pass
