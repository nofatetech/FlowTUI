from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Button, Tree

# -------------------------------------------------
# Generic Panel Widget (Corrected)
# -------------------------------------------------

class Panel(Vertical):
    def __init__(self, title: str, icon: str = "", **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.icon = icon

    def compose(self) -> ComposeResult:
        yield Static(f"{self.icon} {self.title}", classes="panel-title")
        # Children are now yielded directly into this panel's layout

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
    #col-4 > Panel > .panel-body { padding: 1; }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal():
            # --- COLUMN 1: EXPLORER ---
            with Panel("Explorer", "🌐", id="col-1") as p:
                with Vertical(classes="panel-body"):
                    flows_tree = Tree("📦 Domains")
                    flows_tree.root.expand()
                    billing = flows_tree.root.add("💳 Billing")
                    billing.add("🧾 Invoices (/invoices)")
                    catalog = flows_tree.root.add("📚 Catalog")
                    catalog.add("👕 Products (/products)")
                    yield flows_tree

                    models_tree = Tree("📦 Models")
                    models_tree.root.expand()
                    billing_m = models_tree.root.add("💳 Billing")
                    billing_m.add("📄 Invoice")
                    shared = models_tree.root.add("👤 Shared")
                    shared.add("📄 User")
                    yield models_tree

            # --- COLUMN 2: FLOW IMPLEMENTATION ---
            with Panel("Flow Implementation", "📁", id="col-2") as p:
                impl_tree = Tree("📁 catalog.products", classes="panel-body")
                impl_tree.root.expand()
                
                layouts = impl_tree.root.add("🎨 Layouts")
                layouts.add("📄 layout.html ([i]Pico.css[/])")
                
                controllers = impl_tree.root.add("▶️ Controllers")
                controllers.add("📄 index")
                controllers.add("📄 show")

                views = impl_tree.root.add("🖼️ Views")
                index_html = views.add("📄 index.html")
                page = index_html.add("<html>")
                main = page.add("<main>")
                loop = main.add("🔄 Loop: [i]for product in products[/]")
                subview = loop.add("↪️ Subview: [b]show.html[/]")
                card = subview.add("<div.product-card>")
                card.add("<h3> {{ product.name }} </h3>")
                card.add("<button> Add to Cart </button>")

                contracts = impl_tree.root.add("📜 Contracts")
                contracts.add("📄 ProductSchema")

                impl_tree.root.expand_all()
                yield impl_tree

            # --- COLUMN 3: INSPECTOR ---
            with Panel("Inspector", "🔍", id="col-3") as p:
                inspector_tree = Tree("✨ Inspector", classes="panel-body")
                inspector_tree.root.expand()
                identity = inspector_tree.root.add("🆔 Identity")
                identity.add("Tag: [cyan]button[/]")
                styling = inspector_tree.root.add("🎨 Styling")
                styling.add("CSS Classes: [yellow]btn primary[/]")
                events = inspector_tree.root.add("⚡️ Events (Signals)")
                events.add("flow:click: [blue]cart.add_item[/]")
                alpine = inspector_tree.root.add(" Alpine.js")
                alpine.add("x-data: [green]{ open: false }[/]")
                yield inspector_tree

            # --- COLUMN 4: UTILITIES & DEPLOY ---
            with Vertical(id="col-4"):
                with Panel("Utilities", "🛠️") as p:
                    utilities_tree = Tree("🔧 Utilities", classes="panel-body")
                    utilities_tree.root.expand()
                    services = utilities_tree.root.add("🚀 Core Services")
                    services.add("🐘 Database: [green]Connected[/]")
                    providers = utilities_tree.root.add("🔌 External Providers")
                    providers.add("✉️ Email: [green]API Key Loaded[/]")
                    tooling = utilities_tree.root.add("⚙️ Tooling")
                    tooling.add("🧪 Tests: [green]128 Passing[/]")
                    yield utilities_tree
                    
                with Panel("Deploy", "🚀") as p:
                    with Vertical(classes="panel-body"):
                        yield Static("- 🌍 Env: local\n- 🟢 Status: Running")
                        yield Button("🚀 Deploy", variant="primary")
        yield Footer()

if __name__ == "__main__":
    FlowTUI().run()
