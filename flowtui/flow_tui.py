from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Button, Tree
import random

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

# -------------------------------------------------
# Deploy Info Widget
# -------------------------------------------------

class DeployInfo(Static):
    """A static widget to display deployment info with a retro-tech aesthetic."""

    def _get_status_color(self, val: int) -> str:
        if val > 80: return "red"
        if val > 50: return "yellow"
        return "green"

    def compose(self) -> ComposeResult:
        yield Static("🚀 [bold cyan]INFRASTRUCTURE STATUS[/]")
        server_tree = Tree("")
        server_tree.show_root = False
        servers = {
            "Hetzner-1": (random.randint(75, 95), random.randint(40, 60)),
            "DO-Try-12": (random.randint(10, 30), random.randint(20, 40)),
        }
        for name, (cpu, mem) in servers.items():
            cpu_color = self._get_status_color(cpu)
            mem_color = self._get_status_color(mem)
            server_node = server_tree.root.add(f"🛰️ [white]{name}[/]")
            server_node.add(f"└─ CPU:[{cpu_color}] {cpu:>3}% [/] MEM:[{mem_color}] {mem:>3}% [/]")
        server_tree.root.expand_all()
        yield server_tree

        yield Static("\n🕹️ [bold cyan]DEPLOYMENT CONTROL[/]")
        yield Button("🚀 DEPLOY TO PRODUCTION", variant="primary", id="deploy-button")
        
        history_tree = Tree("📜 Recent Deployments")
        history_tree.root.expand()
        history_tree.root.add("✅ [green]#a1b2c3d - 5 mins ago[/]")
        history_tree.root.add("❌ [red]#e4f5g6h - 1 hr ago[/]")
        yield history_tree

        yield Static("\n📡 [bold cyan]LIVE PIPELINE[/]")
        pipeline_tree = Tree("⚡ Deploying #a1b2c3d...")
        pipeline_tree.root.expand()
        pipeline_tree.root.add("✅ [green]Linting[/]")
        pipeline_tree.root.add("⏳ [yellow]Testing (58%)[/]")
        pipeline_tree.root.add("... [gray]Pushing[/]")
        yield pipeline_tree

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
                views = impl_tree.root.add("🖼️ Views")
                index_html = views.add("📄 index.html")
                page = index_html.add("<html>")
                main = page.add("<main>")
                loop = main.add("🔄 Loop: [i]for product in products[/]")
                loop.add("↪️ Subview: [b]show.html[/]")
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
                    yield utilities_tree
                    
                with Panel("Deploy", "🚀") as p:
                    yield DeployInfo(classes="panel-body")
        yield Footer()

if __name__ == "__main__":
    FlowTUI().run()
