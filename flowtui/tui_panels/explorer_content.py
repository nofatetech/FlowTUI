import os
import json
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Tree
from textual.message import Message
from textual.widgets.tree import TreeNode


class ExplorerContent(Vertical):
    """
    A file explorer that visualizes the entire application graph from app_graph.json
    in a single, unified tree structure.
    """

    class FlowSelected(Message):
        """Posted when a selectable file/node is chosen in the explorer."""
        def __init__(self, name: str, file_path: str, target_type: str) -> None:
            super().__init__()
            self.name = name
            self.file_path = file_path
            self.target_type = target_type

    class ScanProjectRequested(Message):
        """Posted when the user clicks the rescan button."""
        pass

    def refresh_tree(self, app_graph: dict) -> None:
        """Receives a new app graph and rebuilds the tree."""
        self.app_graph = app_graph
        tree = self.query_one(Tree)
        tree.clear()
        self._populate_unified_tree(tree.root)

    def _populate_unified_tree(self, root: TreeNode) -> None:
        """Populates the tree based on the new, deep 'apps' structure."""
        scan_node = root.add("🔄 [bold cyan]Rescan Project[/]")
        scan_node.data = {"action": "scan"}

        if not self.app_graph:
            root.add("⚠️ [red]No apps found or scan failed.[/]")
            return

        def _add_nodes_recursively(parent_node: TreeNode, node_data: dict):
            """Helper function to recursively add nodes to the tree."""
            for name, content in sorted(node_data.items()):
                if content is None:  # It's a file
                    parent_node.add(f"📄 {name}")
                else:  # It's a directory
                    dir_node = parent_node.add(f"📁 {name}")
                    _add_nodes_recursively(dir_node, content)

        for app_name, app_data in self.app_graph.items():
            app_node = root.add(f"🚀 [b]{app_name}[/b]")
            
            if app_data.get("backend_tree"):
                backend_node = app_node.add("📦 Backend")
                _add_nodes_recursively(backend_node, app_data["backend_tree"])

            if app_data.get("frontends"):
                frontends_node = app_node.add("🖥️ Frontends")
                for frontend in app_data["frontends"]:
                    fe_node = frontends_node.add(f"🌐 {frontend['name']}")
                    if frontend.get("tree"):
                        _add_nodes_recursively(fe_node, frontend["tree"])
        
        root.expand_all()

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """Post a message when a node is selected."""
        if not event.node.data:
            return

        # Check if the rescan button was clicked
        if event.node.data.get("action") == "scan":
            self.post_message(self.ScanProjectRequested())
            return

        # Otherwise, handle as a file selection
        if "file_path" in event.node.data:
            node_data = event.node.data
            self.post_message(self.FlowSelected(
                name=node_data["name"],
                file_path=node_data["file_path"],
                target_type=node_data["type"]
            ))

    def compose(self) -> ComposeResult:
        """Render the explorer with a single, unified tree."""
        yield Tree("🌐 [b]Project[/b]")
