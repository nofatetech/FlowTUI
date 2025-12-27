import random
from textual.app import ComposeResult
from textual.widgets import Static, Button, Tree

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
