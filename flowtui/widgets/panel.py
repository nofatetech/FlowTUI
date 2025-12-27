from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

class Panel(Vertical):
    def __init__(self, title: str, icon: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        self.icon = icon

    def compose(self) -> ComposeResult:
        yield Static(f"{self.icon} {self.title}", classes="panel-title")
