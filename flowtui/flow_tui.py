from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import (
    Header,
    Footer,
    Static,
    ListView,
    ListItem,
    Label,
    Button,
    Tree,
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

def inspect_node(label: str) -> str:
    return "\n".join(
        [
            f"🔍 Inspector",
            "",
            f"Node: {label}",
            "",
            "Type:",
            "  UI Element",
            "",
            "Properties:",
            "  id: auto",
            "  visible: true",
            "  class: default",
            "",
            "Behaviours:",
            "  • bound_flow: core.auth.login",
            "  • model: User",
            "",
            "🚧 (editing coming later)",
        ]
    )


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
        yield Vertical(classes="panel-body")


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

    Button {
        margin-top: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Horizontal():
            with Panel("Flows", "📦"):
                yield FlowList()

            with Panel("Flow View", "🌳"):
                self.flow_tree = build_flow_tree()
                yield self.flow_tree

            with Panel("Inspector", "🔍"):
                self.inspector = Static(
                    "Select an element\nfrom the Flow View",
                    classes="inspector",
                )
                yield self.inspector

            with Panel("Deploy", "🚀"):
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

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        label = event.node.label
        self.inspector.update(inspect_node(str(label)))


# -------------------------------------------------
# Entry Point
# -------------------------------------------------

if __name__ == "__main__":
    FlowTUI().run()
