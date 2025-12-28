from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Tree

class UtilitiesContent(Vertical):
    def compose(self) -> ComposeResult:
        utilities_tree = Tree("🔧 Utilities")
        utilities_tree.root.expand()
        services = utilities_tree.root.add("🚀 Core Services")
        services.add("🐘 DB1 (postgres): [green]OK[/]")
        services.add("🐘 DB1 (chromadb): [green]OK[/]")
        services.add("🐘 DB3 (sqlite): [green]OK[/]")
        services = utilities_tree.root.add("🚀 Custom Services")
        services.add("🐘 SpotifyApiTest1: [yellow]Idle[/]")
        services.add("🐘 UDPManager: [yellow]Idle[/]")
        services.add("🐘 UDPManager > Contracts >> ")
        services.add("🐘 UDPManager > Methods >> ")
        providers = utilities_tree.root.add("🔌 External Providers")
        providers.add("✉️ Email: [green]API Key Loaded[/]")
        providers.add("✉️ Spotify SDK: [green]OK[/]")
        yield utilities_tree
