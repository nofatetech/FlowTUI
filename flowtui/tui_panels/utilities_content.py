from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button

class UtilitiesContent(Vertical):
    """
    A panel containing utility buttons for the application.
    """
    def compose(self) -> ComposeResult:
        """Render the utilities panel."""
        yield Button("Scan Project", id="scan_project_button", variant="primary")
