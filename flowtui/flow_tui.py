from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import (
    Header,
    Footer,
    Static,
    ListView,
    ListItem,
    Label,
    Button,
    Tree,
    Input,
)
from textual.events import Click

# -------------------------------------------------
# Mock Data
# -------------------------------------------------

MOCK_FLOWS = [
    "core.auth.login",
    "core.auth.logout",
    "core.incident.create",
]

# -------------------------------------------------
# Flow View Tree (contracts + views)
# -------------------------------------------------

def build_flow_tree():
    tree = Tree("🌊 flow.core.auth.login")

    # Contracts
    contracts = tree.root.add("📜 contracts")
    contracts.add("📥 input.credentials")
    contracts.add("📤 output.session")

    # Main View
    view = tree.root.add("🧩 view.auth.login")
    layout = view.add("📐 layout.base")
    slot = layout.add("🔳 slot.content")

    form = slot.add("📝 component.form.login")
    form.add("🔤 input.email")
    form.add("🔒 input.password")
    form.add("➡️ button.submit")

    # Subview
    tree.root.add("🧩 subview.auth.footer")

    return tree


# -------------------------------------------------
# Inspector Data (mocked by node label)
# -------------------------------------------------

def inspect_node(label: str) -> dict:
    return {
        "Info": {
            "Node": label,
            "Type": "UI Element",
        },
        "Properties": {
            "id": "auto",
            "visible": "true",
            "class": "default",
        },
        "Behaviours": {
            "bound_flow": "core.auth.login",
            "model": "User",
        },
    }


# -------------------------------------------------
# Generic Panel
# -------------------------------------------------

class Panel(Vertical):
    def __init__(self, title: str, icon: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        self.icon = icon

    def compose(self) -> ComposeResult:
        yield Static(f"{self.icon} {self.title}", classes="panel-title")


# -------------------------------------------------
# Left Panel: Flows
# -------------------------------------------------

class FlowList(Vertical):
    def compose(self) -> ComposeResult:
        yield ListView(
            *[ListItem(Label(flow)) for flow in MOCK_FLOWS],
        )
        yield Button("➕ Create Flow", variant="primary")


# -------------------------------------------------
# App
# -------------------------------------------------

class FlowTUI(App):
    TITLE = "Flow TUI"
    SUB_TITLE = "Flows • Contracts • Views • Inspector"

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
    }

    ListView {
        height: 1fr;
        border: round #333333;
    }

    Tree {
        height: 1fr;
        border: round #333333;
    }

    .inspector {
        border: round #333333;
        padding: 1;
    }

    .inspector-category {
        margin-top: 1;
        text-style: bold;
    }

    .inspector-item {
        margin: 1 0 0 2;
    }

    Input {
        margin: 0 0 0 2;
    }

    Button {
        margin-top: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Horizontal():
            with Panel("Flows", "📦"):
                yield FlowList(classes="panel-body")

            with Panel("Flow View", "🌳"):
                self.flow_tree = build_flow_tree()
                self.flow_tree.add_class("panel-body")
                yield self.flow_tree

            with Panel("Inspector", "🔍"):
                self.inspector = VerticalScroll(
                    Static("Select an element\nfrom the Flow View"),
                    classes="inspector panel-body",
                )
                yield self.inspector

            with Panel("Deploy", "🚀"):
                with Vertical(classes="panel-body"):
                    yield Static(
                        "Environment: local\n"
                        "Status: 🟢 Running\n"
                        "Version: v0.1.3\n"
                        "Last Deploy: 2 min ago",
                        classes="inspector",
                    )
                    yield Button("🚀 Deploy")
                    yield Button("🔄 Restart", variant="warning")

        yield Footer()

    # -------------------------------------------------
    # Interaction: click tree node → inspector
    # -------------------------------------------------

    async def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        label = event.node.label
        data = inspect_node(str(label))

        await self.inspector.remove_children()

        for category, items in data.items():
            await self.inspector.mount(
                Static(category, classes="inspector-category")
            )
            for key, value in items.items():
                await self.inspector.mount(Label(f"{key}:", classes="inspector-item"))
                await self.inspector.mount(Input(value=str(value)))


# -------------------------------------------------
# Entry Point
# -------------------------------------------------

if __name__ == "__main__":
    FlowTUI().run()
