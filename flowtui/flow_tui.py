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
# Deploy Panel Widget
# -------------------------------------------------

class DeployPanel(Vertical):
    def compose(self) -> ComposeResult:
        # This panel's content is managed via on_mount and on_button_pressed
        yield Vertical(id="deploy-initial-view")
        yield Vertical(id="deploy-progress-view", classes="hidden")

    def on_mount(self) -> None:
        self.initial_view = self.query_one("#deploy-initial-view")
        self.progress_view = self.query_one("#deploy-progress-view")
        self.populate_initial_view()
        self.populate_progress_view()

    def populate_initial_view(self) -> None:
        history_tree = Tree("📜 Recent Deployments")
        history_tree.root.expand()
        history_tree.root.add("✅ [green]#a1b2c3d - 5 mins ago[/]")
        history_tree.root.add("❌ [red]#e4f5g6h - 1 hr ago[/]")
        
        self.initial_view.mount(Button("🚀 Deploy to Production", variant="primary", id="deploy-button"))
        self.initial_view.mount(history_tree)

    def populate_progress_view(self) -> None:
        self.progress_view.mount(Static("⏳ [yellow]Deployment in Progress...[/]"))
        
        pipeline_tree = Tree("🚀 Deploying commit #a1b2c3d...")
        pipeline_tree.root.expand()
        pipeline_tree.root.add("✅ [green]Linting[/]")
        pipeline_tree.root.add("✅ [green]Building[/]")
        pipeline_tree.root.add("⏳ [yellow]Testing (58%)[/]")
        pipeline_tree.root.add("... [gray]Pushing to registry[/]")
        self.progress_view.mount(pipeline_tree)
        
        self.progress_view.mount(Static("🪵 [bold]Logs:[/]\n> Running 128 tests..."))
        self.progress_view.mount(Button("Abort", variant="error"))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "deploy-button":
            self.initial_view.add_class("hidden")
            self.progress_view.remove_class("hidden")
            event.stop()

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
    .hidden { display: none; }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal():
            # --- COLUMN 1: EXPLORER ---
            with Panel("Explorer", "🌐", id="col-1"):
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
            with Panel("Flow Implementation", "📁", id="col-2"):
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
            with Panel("Inspector", "🔍", id="col-3"):
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
                    yield DeployPanel(classes="panel-body")
        yield Footer()

if __name__ == "__main__":
    FlowTUI().run()
