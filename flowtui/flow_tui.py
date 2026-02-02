from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Button

from services.code_scanner import CodeScannerService
from tui_panels.panel import Panel
from tui_panels.deploy_info import DeployInfo
from tui_panels.explorer_content import ExplorerContent
from tui_panels.flow_implementation_content import FlowImplementationContent
from tui_panels.inspector_content import InspectorContent
from tui_panels.utilities_content import UtilitiesContent
# from tui_panels.oracle_content import OracleContent

# -------------------------------------------------
# Main App
# -------------------------------------------------

class FlowTUI(App):
    TITLE = "Flow TUI"
    CSS = """
    Screen { layout: vertical; }
    Horizontal { height: 1fr; }
    #col-1, #col-2, #col-3, #col-4, #col-5 { height: 100%; }
    #col-1 { width: 1fr; }
    #col-2 { width: 1.5fr; }
    #col-3 { width: 1.5fr; }
    #col-4 { width: 1fr; }
    .panel-title { background: #1e1e1e; color: #ffffff; padding: 0 1; text-style: bold; }
    .panel-body { height: 1fr; padding: 1; border: round #333333; }
    .panel-body > Tree { border: none; padding: 0; }
    #col-1 > Panel > .panel-body { padding: 0; }

    /* --- Inspector Panel Styling --- */
    #col-3 .prop-row {
        height: auto;
        align: left middle;
        margin: 0 1;
    }
    #col-3 .label {
        width: 25%;
        color: gray;
        text-align: right;
        margin-right: 2;
    }
    #col-3 .prop-input {
        width: 75%;
        border: none;
        background: #2a2a2a;
    }
    #col-3 .code-preview {
        width: 60%;
        height: auto;
        max-height: 5;
        content-align: left middle;
        background: #2a2a2a;
        padding: 0 1;
        border: none;
    }
    #col-3 .edit-btn {
        width: auto;
        height: 1;
        min-width: 0;
        margin-left: 1;
        border: none;
        background: #3a3a3a;
    }

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code_scanner = CodeScannerService()

    def on_mount(self) -> None:
        """Perform initial project scan when the app starts."""
        self.scan_and_refresh_explorer()

    def scan_and_refresh_explorer(self) -> None:
        """Scans the project and tells the explorer to refresh."""
        app_graph = self.code_scanner.scan_apps() # Scan current directory
        explorer = self.query_one(ExplorerContent)
        explorer.refresh_tree(app_graph)

    def on_explorer_content_scan_project_requested(
        self, message: ExplorerContent.ScanProjectRequested
    ) -> None:
        """Handle the request to rescan the project."""
        self.scan_and_refresh_explorer()

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
                yield InspectorContent()

            # --- COLUMN 4: UTILITIES & DEPLOY ---
            with Vertical(id="col-4"):
                with Panel("Utilities", "🛠️") as p:
                    yield UtilitiesContent(classes="panel-body")

                with Panel("Deploy", "🚀") as p:
                    yield DeployInfo(classes="panel-body")


        yield Footer()

    def on_flow_implementation_content_element_selected(
        self, message: FlowImplementationContent.ElementSelected
    ) -> None:
        """When an element is selected in the view tree, update the inspector."""
        inspector = self.query_one(InspectorContent)
        inspector.on_flow_implementation_content_element_selected(message)

    def on_explorer_content_flow_selected(
        self, message: ExplorerContent.FlowSelected
    ) -> None:
        """When a flow is selected in the explorer, update the implementation panel."""
        flow_implementation = self.query_one(FlowImplementationContent)
        flow_implementation.on_explorer_content_flow_selected(message)

    def on_flow_implementation_content_method_selected(
        self, message: FlowImplementationContent.MethodSelected
    ) -> None:
        """When a method is selected in the implementation panel, update the inspector."""
        inspector = self.query_one(InspectorContent)
        inspector.on_flow_implementation_content_method_selected(message)



if __name__ == "__main__":
    FlowTUI().run()
