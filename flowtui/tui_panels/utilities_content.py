from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Tree

class UtilitiesContent(Vertical):
    def compose(self) -> ComposeResult:
        utilities_tree = Tree("🔧 Utilities")
        utilities_tree.root.expand()
        services = utilities_tree.root.add("🚀 Core Services")
        services.add("🐘 Database: [green]Connected[/]")
        providers = utilities_tree.root.add("🔌 External Providers")
        providers.add("✉️ Email: [green]API Key Loaded[/]")
        yield utilities_tree
