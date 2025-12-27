from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Button

# -------------------------------------------------
# Generic Panel Widget
# -------------------------------------------------

class Panel(Vertical):
    def __init__(self, title: str, icon: str = "", **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.icon = icon

    def compose(self) -> ComposeResult:
        yield Static(f"{self.icon} {self.title}", classes="panel-title")
        yield Vertical(classes="panel-body")

# -------------------------------------------------
# Main App
# -------------------------------------------------

class FlowTUI(App):
    TITLE = "Flow TUI - Stable Foundation"
    CSS = """
    Screen { layout: vertical; }
    Horizontal { height: 1fr; }

    /* Assign widths to columns */
    #col-1 { width: 1.5fr; }
    #col-2 { width: 1.5fr; }
    #col-3 { width: 2fr; }
    #col-4 { width: 1fr; }

    .panel-title { 
        background: #1e1e1e; 
        color: #ffffff; 
        padding: 0 1; 
        text-style: bold; 
    }
    .panel-body { 
        height: 1fr; 
        padding: 1; 
        border: round #333333; 
    }
    
    /* Ensure child widgets in the body fill the space */
    .panel-body > Static {
        height: 100%;
    }
    
    /* Specific styling for the last column's sub-panels */
    #col-4 > Panel {
        height: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal():
            with Panel("Explorer", "🌐", id="col-1") as p:
                p.border_title = "COLUMN 1"
                yield Static("Domain Explorer & Models Go Here")

            with Panel("Flow Implementation", "📁", id="col-2") as p:
                p.border_title = "COLUMN 2"
                yield Static("Flow Details Go Here")

            with Panel("Inspector", "🔍", id="col-3") as p:
                p.border_title = "COLUMN 3"
                yield Static("Inspector Goes Here")

            with Vertical(id="col-4"):
                with Panel("Services", "🔌") as p:
                    p.border_title = "COLUMN 4a"
                    yield Static("Services Go Here")
                with Panel("Deploy", "🚀") as p:
                    p.border_title = "COLUMN 4b"
                    yield Static("Deploy Controls Go Here")
        yield Footer()

if __name__ == "__main__":
    FlowTUI().run()
