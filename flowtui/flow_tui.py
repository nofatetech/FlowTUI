from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import (
    Header,
    Footer,
    Static,
    Label,
    Button,
    Tree,
    Input,
    ListView,
    ListItem
)

from widgets.panel import Panel
from widgets.flow_list import FlowList
from widgets.flow_structure import FlowStructure

class FlowTUI(App):
    TITLE = "Flow TUI"
    SUB_TITLE = "Resource-Centric View"

    CSS = """
    Screen {
        layout: vertical;
    }
    Horizontal {
        height: 1fr;
    }
    .panel-title {
        background: #1e1e1e;
        color: #ffffff;
        padding: 1;
        text-style: bold;
    }
    .panel-body {
        height: 1fr;
        padding: 1;
        border: round #333333;
    }
    #utilities_panel > Vertical {
        height: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal():
            with Panel("Flow API", "➡️"):
                self.flow_list = FlowList()
                yield self.flow_list

            with Panel("Flow Structure", "📁"):
                self.flow_structure = FlowStructure()
                yield self.flow_structure

            with Panel("Inspector", "🔍"):
                self.inspector = VerticalScroll(
                    Static("Select an element"), classes="panel-body"
                )
                yield self.inspector

            with Vertical(id="utilities_panel"):
                with Panel("Services", "🔌"):
                    yield Static("Database (PostgreSQL)\nEmail (SendGrid)\nPayments (Stripe)", classes="panel-body")
                with Panel("Deploy", "🚀"):
                    yield Static("Env: local\nStatus: 🟢 Running", classes="panel-body")
                    yield Button("🚀 Deploy")

        yield Footer()

    async def on_list_view_selected(self, event: ListView.Selected):
        self.flow_structure.show_flow(event.item.id)
        await self.inspector.remove_children()
        await self.inspector.mount(Static("Select a structural element"))


    async def on_tree_node_selected(self, event: Tree.NodeSelected):
        await self.inspector.remove_children()
        node_data = event.node.data
        if not node_data:
            return

        node_type = node_data.get("type")
        content = node_data.get("content")

        if node_type == "code":
            await self.inspector.mount(Static(f"📄 Source for {event.node.label}"))
            await self.inspector.mount(Static(str(content), classes="inspector-item"))
            await self.inspector.mount(Button("✏️ Edit in Neovim"))
        
        elif node_type == "element":
            await self.inspector.mount(Static(f"DOM Element: <{event.node.label}>"))
            for key, value in content.items():
                if key not in ["root", "children"]:
                    await self.inspector.mount(Label(f"{key}:", classes="inspector-item"))
                    await self.inspector.mount(Input(value=str(value)))


# -------------------------------------------------
# Entry Point
# -------------------------------------------------

if __name__ == "__main__":
    FlowTUI().run()

# -------------------------------------------------
# Generic Panel
# -------------------------------------------------
