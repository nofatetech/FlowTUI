from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer

from tui_panels.panel import Panel
from tui_panels.deploy_info import DeployInfo
from tui_panels.explorer_content import ExplorerContent
from tui_panels.flow_implementation_content import FlowImplementationContent
from tui_panels.inspector_content import InspectorContent
from tui_panels.utilities_content import UtilitiesContent

# -------------------------------------------------
# Main App
# -------------------------------------------------

class FlowTUI(App):
    TITLE = "Flow TUI - Final Blueprint"
    CSS = """
    Screen { layout: vertical; }
    Horizontal { height: 1fr; }
    #col-1, #col-2, #col-3, #col-4 { height: 100%; }
    #col-1 { width: 1.5fr; }
    #col-2 { width: 1.5fr; }
    #col-3 { width: 2fr; }
    #col-4 { width: 1.2fr; }
    .panel-title { background: #1e1e1e; color: #ffffff; padding: 0 1; text-style: bold; }
    .panel-body { height: 1fr; padding: 1; border: round #333333; }
    .panel-body > Tree { border: none; padding: 0; }
    #col-1 > Panel > .panel-body { padding: 0; }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal():
            # --- COLUMN 1: EXPLORER ---
            with Panel("Explorer", "🌐", id="col-1"):
                yield ExplorerContent(classes="panel-body")

            # --- COLUMN 2: FLOW IMPLEMENTATION ---
            with Panel("Flow Implementation", "📁", id="col-2"):
                yield FlowImplementationContent(classes="panel-body")

            # --- COLUMN 3: INSPECTOR ---
            with Panel("Inspector", "🔍", id="col-3"):
                yield InspectorContent(classes="panel-body")

            # --- COLUMN 4: UTILITIES & DEPLOY ---
            with Vertical(id="col-4"):
                with Panel("Utilities", "🛠️") as p:
                    yield UtilitiesContent(classes="panel-body")

                with Panel("Deploy", "🚀") as p:
                    yield DeployInfo(classes="panel-body")
        yield Footer()

if __name__ == "__main__":
    FlowTUI().run()
