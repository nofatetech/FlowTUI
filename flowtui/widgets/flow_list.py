from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import ListView, ListItem, Label
from .data import MOCK_RESOURCES

class FlowList(Vertical):
    def compose(self) -> ComposeResult:
        yield ListView(*[
            ListItem(
                Label(f"➡️ {data['id']} [{', '.join(data['methods'])}] {data['route']}"),
                id=res_id
            )
            for res_id, data in MOCK_RESOURCES.items()
        ], classes="panel-body")
