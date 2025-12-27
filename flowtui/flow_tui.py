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

from textual.widgets import Header, Footer, Static, Button, Tree

from tui_panels import (
    inspector_content,
    services_content,
    deploy_content,
)

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
    
    .panel-body > Tree {
        border: none;
        padding: 0;
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
                    flows_tree = Tree("📦 Domains", classes="panel-body")
                    flows_tree.root.expand()
                    billing = flows_tree.root.add("💳 Billing")
                    billing.add("🧾 Invoices (/invoices)")
                    catalog = flows_tree.root.add("📚 Catalog")
                    catalog.add("👕 Products (/products)")
                    catalog.add("📂 Categories (/categories)")
                    yield flows_tree

                with Panel("Models", "📦") as p:
                    p.border_title = "Model List"
                    models_tree = Tree("📦 Domains", classes="panel-body")
                    models_tree.root.expand()
                    billing = models_tree.root.add("💳 Billing")
                    billing.add("📄 Invoice")
                    catalog = models_tree.root.add("📚 Catalog")
                    catalog.add("📄 Product")
                    catalog.add("📄 Category")
                    shared = models_tree.root.add("👤 Shared")
                    shared.add("📄 User")
                    yield models_tree

            with Panel("Flow Implementation", "📁", id="col-2") as p:
                p.border_title = "Flow Details"
                impl_tree = Tree("📁 catalog.products", classes="panel-body")
                impl_tree.root.expand()
                
                controllers = impl_tree.root.add("▶️ Controllers")
                controllers.add("📄 index")
                controllers.add("📄 show")

                views = impl_tree.root.add("🖼️ Views")
                
                # --- Detailed index.html ---
                index_html = views.add("📄 index.html")
                page = index_html.add("<html>")
                header = page.add("<header>")
                header.add("<h1>Welcome to our Store!</h1>")
                nav = header.add("<nav>")
                nav.add("<a>Home</a>")
                nav.add("<a>Products</a>")
                
                main = page.add("<main>")
                sidebar = main.add("<div.sidebar>")
                sidebar.add("<h2>Filters</h2>")
                
                content = main.add("<div.content>")
                loop = content.add("🔄 Loop: for product in products")
                
                # --- Reusable show.html subview ---
                subview = loop.add("↪️ Subview: show.html")
                card = subview.add("<div.product-card>")
                card.add("<img> {{ product.image_url }}")
                card.add("<h3> {{ product.name }} </h3>")
                card.add("<p> {{ product.description }} </p>")
                price = card.add("<p.price> {{ product.price }} </p>")
                price.data = {"binding": "product.price"}
                
                button = card.add("<button> Add to Cart </button>")
                button.data = {"flow:click": "cart.add_item(product.id)"}

                admin_link = card.add("<a> Edit (Admin Only) </a>")
                admin_link.data = {"state:show": "user.is_admin"}

                footer = page.add("<footer>")
                footer.add("<p>© 2025 Flow Inc.</p>")
                
                impl_tree.root.expand_all()
                yield impl_tree

            with Panel("Inspector", "🔍", id="col-3") as p:
                p.border_title = "Inspector"
                yield Static(inspector_content.CONTENT, classes="panel-body")

            with Vertical(id="col-4"):
                with Panel("Utilities", "🛠️") as p:
                    p.border_title = "Utilities"
                    utilities_tree = Tree("🔧 Utilities", classes="panel-body")
                    utilities_tree.root.expand()

                    # --- Core Services ---
                    services = utilities_tree.root.add("🚀 Core Services")
                    db = services.add("🐘 Database")
                    db.add("Status: [green]Connected[/]")
                    db.add("Models: [cyan]User, Product, Invoice[/]")
                    db.add("[bold blue]migrate()[/]")
                    cache = services.add("⚡ Cache")
                    cache.add("Status: [green]Connected[/]")
                    cache.add("[bold blue]clear_all()[/]")

                    # --- External Providers ---
                    providers = utilities_tree.root.add("🔌 External Providers")
                    email = providers.add("✉️ Email (SendGrid)")
                    email.add("API Key: [green]Loaded[/]")
                    email.add("📜 Contract: SendEmailSchema")
                    email.add("[bold blue]send()[/]")
                    payments = providers.add("💳 Payments (Stripe)")
                    payments.add("API Key: [yellow]Test Mode[/]")
                    payments.add("📜 Contract: ChargeSchema")
                    payments.add("[bold blue]charge()[/]")
                    payments.add("[bold blue]refund()[/]")

                    # --- Tooling & CI/CD ---
                    tooling = utilities_tree.root.add("⚙️ Tooling & CI/CD")
                    tooling.add("✅ Linter: [green]Passing[/]")
                    tooling.add("🧪 Tests: [green]128 Passing[/]")
                    deploy = tooling.add("🚢 Deployment")
                    deploy.add("Pipeline: [cyan]main.yml[/]")
                    deploy.add("Last Run: [green]Success[/]")
                    
                    yield utilities_tree
                    
                with Panel("Deploy", "🚀") as p:
                    p.border_title = "Deploy"
                    yield Static(deploy_content.CONTENT, classes="panel-body")
        yield Footer()

if __name__ == "__main__":
    FlowTUI().run()
