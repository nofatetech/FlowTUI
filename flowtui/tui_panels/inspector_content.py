from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Tree

class InspectorContent(Vertical):
    def compose(self) -> ComposeResult:
        inspector_tree = Tree("✨ Inspector")
        inspector_tree.root.expand()
        identity = inspector_tree.root.add("🆔 Identity")
        identity.add("Tag: [cyan]button[/]")
        styling = inspector_tree.root.add("🎨 Styling")
        styling.add("CSS Classes: [yellow]btn primary[/]")
        events = inspector_tree.root.add("⚡️ Events (Signals)")
        events.add("flow:click: [blue]cart.add_item[/]")
        yield inspector_tree
