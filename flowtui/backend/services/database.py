class Database:
    """
    Defines the contract for database operations.
    The actual connection is managed by the main application runtime.
    """
    # This static status is a fallback in case the manifest isn't found.
    STATUS = "Not Connected"

    def query(self, sql: str):
        """Executes a raw SQL query."""
        pass

    def find_user(self, user_id: int):
        """Fetches a user by their ID."""
        pass
