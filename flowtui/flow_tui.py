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
    TITLE = "Flow TUI - Architectural Blueprint"
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
    #col-1 > Vertical {
        height: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal():
            with Vertical(id="col-1"):
                with Panel("Flows", "➡️") as p:
                    p.border_title = "Flow List"
                    yield Static(
                        "- Billing.Invoices /invoices\n"
                        "- Catalog.Products /products\n"
                        "- Catalog.Categories /categories\n"
                        "- And More...",
                        classes="panel-body"
                    )
                with Panel("Models", "📦") as p:
                    p.border_title = "Model List"
                    yield Static(
                        "- User (id, name, email)\n"
                        "- Product (id, name, price)\n"
                        "- Invoice (id, user_id, amount)\n"
                        "- And More...",
                        classes="panel-body"
                    )

            with Panel("Flow Implementation", "📁", id="col-2") as p:
                p.border_title = "Flow Details"
                yield Static(
                    "- Controllers (index, show, create...)\n"
                    "- Views (HTML structure)\n"
                    "- Contracts (Input/Output schemas)\n"
                    "- And More...",
                    classes="panel-body"
                )

            with Panel("Inspector", "🔍", id="col-3") as p:
                p.border_title = "Inspector"
                yield Static(
                    "- Selected Element Properties\n"
                    "- Bindings (flow:click, state:model)\n"
                    "- Inline JavaScript Hooks (before-send, after-swap)\n"
                    "- Model Schema/Definition\n"
                    "- Code Snippets",
                    classes="panel-body"
                )

            with Vertical(id="col-4"):
                with Panel("Services", "🔌") as p:
                    p.border_title = "Services"
                    yield Static(
                        "- Database (PostgreSQL)\n"
                        "- Email Provider (SendGrid)\n"
                        "- Payment Gateway (Stripe)\n"
                        "- Logging Service",
                        classes="panel-body"
                    )
                with Panel("Deploy", "🚀") as p:
                    p.border_title = "Deploy"
                    yield Static(
                        "- Environment: local\n"
                        "- Status: 🟢 Running\n"
                        "- Version: v0.1.3\n"
                        "- Last Deploy: 2 min ago",
                        classes="panel-body"
                    )
        yield Footer()

if __name__ == "__main__":
    FlowTUI().run()
