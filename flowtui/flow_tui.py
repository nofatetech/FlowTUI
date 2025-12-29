from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer

from tui_panels.panel import Panel
from tui_panels.deploy_info import DeployInfo
from tui_panels.explorer_content import ExplorerContent
from tui_panels.flow_implementation_content import FlowImplementationContent
from tui_panels.inspector_content import InspectorContent
from tui_panels.utilities_content import UtilitiesContent
from tui_panels.oracle_content import OracleContent

# -------------------------------------------------
# Main App
# -------------------------------------------------

class FlowTUI(App):
    TITLE = "Flow TUI - The Oracle"
    CSS = """
    Screen { layout: vertical; }
    Horizontal { height: 1fr; }
    #col-1, #col-2, #col-3, #col-4, #col-5 { height: 100%; }
    #col-1 { width: 1fr; }
    #col-2 { width: 1.5fr; }
    #col-3 { width: 1.5fr; }
    #col-4 { width: 1fr; }
    #col-5 { width: 2.5fr; border-left: thick #4A0404; } /* Oracle column is wider and has a red border */
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

    /* --- Oracle Panel Styling --- */
    #oracle-container {
        padding: 0;
        layout: vertical;
    }
    #oracle-log {
        height: 3fr; /* Takes up most of the space */
        padding: 0 1;
    }
    .user-prompt {
        text-align: right;
        color: #cccccc;
        margin: 1 0 0 4;
        background: #2a2a2a;
        padding: 0 1;
        border: round #444444;
    }
    .user-prompt-action {
        text-align: right;
        color: #F5A623; /* Action color */
        margin: 1 0 0 4;
        background: #2a2a2a;
        padding: 0 1;
        border: round #F5A623;
        width: auto;
    }
    .oracle-response {
        color: #E0E0E0;
        margin: 1 4 0 0;
        background: #1e1e1e;
        padding: 1;
        border: round #FF0000;
        width: 100%;
        overflow: auto;
    }
    #oracle-chat-list-container {
        height: 1fr; /* Takes up less space */
        border-top: wide #4A0404;
        padding: 1;
    }
    #oracle-chat-list-container ListView {
        background: #1e1e1e;
    }
    #oracle-chat-list-container #active-chat {
        background: #4A0404;
    }
    #new-chat-btn {
        width: 100%;
        margin-top: 1;
    }
    #oracle-input-bar {
        height: auto;
        padding: 1;
        align: right middle;
        border-top: wide #4A0404;
    }
    #oracle-input {
        width: 1fr;
        border: none;
        background: #2a2a2a;
    }
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
                yield InspectorContent()

            # --- COLUMN 4: UTILITIES & DEPLOY ---
            with Vertical(id="col-4"):
                with Panel("Utilities", "🛠️") as p:
                    yield UtilitiesContent(classes="panel-body")

                with Panel("Deploy", "🚀") as p:
                    yield DeployInfo(classes="panel-body")

            # --- COLUMN 5: THE ORACLE ---
            with Panel("The Oracle (●)", "🤖", id="col-5"):
                yield OracleContent()
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
