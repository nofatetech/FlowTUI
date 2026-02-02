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
        """Populates the tree based on the simple file tree from the CodeScannerService."""
        scan_node = root.add("🔄 [bold cyan]Rescan Project[/]")
        scan_node.data = {"action": "scan"}

        if not self.app_graph:
            root.add("⚠️ [red]No apps found or scan failed.[/]")
            return

        def _get_node_meta(path: str, is_dir: bool) -> dict:
            """Infers the node type and icon from its path."""
            if is_dir:
                return {"type": "directory", "icon": "📁"}
            
            if "backend/flows" in path:
                return {"type": "flow", "icon": "▶️"}
            if "backend/models" in path:
                return {"type": "model", "icon": "🔹"}
            if "backend/contracts" in path:
                return {"type": "contract", "icon": "📜"}
            if "backend/services" in path:
                return {"type": "service", "icon": "🛠️"}
            if "backend/providers" in path:
                return {"type": "provider", "icon": "🔌"}
            if ".html" in path:
                return {"type": "view", "icon": "🖼️"}
            
            return {"type": "file", "icon": "📄"}

        def _add_nodes_recursively(parent_node: TreeNode, node_data: dict, current_path: str):
            """Helper function to recursively add nodes from a simple file tree."""
            for name, content in sorted(node_data.items()):
                new_path = os.path.join(current_path, name)
                is_dir = isinstance(content, dict)
                
                meta = _get_node_meta(new_path, is_dir)
                node_type = meta["type"]
                icon = meta["icon"]

                node = parent_node.add(f"{icon} {name}")
                node.data = {"type": node_type, "file_path": new_path, "name": name}

                if is_dir:
                    _add_nodes_recursively(node, content, new_path)

        # Add the core backend at the root level
        if self.app_graph.get("backend_tree"):
            backend_node = root.add("📦 [b]Backend[/b]")
            backend_base_path = "backend"
            backend_node.data = {"type": "directory", "file_path": backend_base_path}
            _add_nodes_recursively(backend_node, self.app_graph["backend_tree"], backend_base_path)

        # Add the apps
        apps_data = self.app_graph.get("apps", {})
        if not apps_data:
            return # No apps to show

        apps_root_node = root.add("🚀 [b]Apps[/b]")
        for app_name, app_data in apps_data.items():
            app_node = apps_root_node.add(f"📱 {app_name}")
            app_path = os.path.join("apps", app_name) # Base path for the app

            if app_data.get("backend_tree"):
                backend_base_path = os.path.join(app_path, "backend")
                backend_node = app_node.add("📦 Backend")
                backend_node.data = {"type": "directory", "file_path": backend_base_path}
                _add_nodes_recursively(backend_node, app_data["backend_tree"], backend_base_path)

            if app_data.get("frontends"):
                frontends_node = app_node.add("🖥️ Frontends")
                for frontend in app_data["frontends"]:
                    fe_node = frontends_node.add(f"🌐 {frontend['name']}")
                    frontend_path = os.path.join(app_path, frontend['name'])
                    fe_node.data = {"type": "directory", "file_path": frontend_path}
                    if frontend.get("tree"):
                        _add_nodes_recursively(fe_node, frontend["tree"], frontend_path)
        
        root.expand_all()

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """Post a message when any node (file or directory) is selected."""
        if not event.node.data:
            return

        action = event.node.data.get("action")
        if action == "scan":
            self.post_message(self.ScanProjectRequested())
            return

        # Handle both file and directory selections
        node_type = event.node.data.get("type")
        file_path = event.node.data.get("file_path")
        name = event.node.data.get("name", os.path.basename(file_path or ""))

        if node_type and file_path:
            self.post_message(self.FlowSelected(
                name=name,
                file_path=file_path,
                target_type=node_type
            ))

    def compose(self) -> ComposeResult:
        """Render the explorer with a single, unified tree."""
        yield Tree("🌐 [b]Project[/b]")
