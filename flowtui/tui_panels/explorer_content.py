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

    def refresh_tree(self, app_graph: dict) -> None:
        """Receives a new app graph and rebuilds the tree."""
        self.app_graph = app_graph
        tree = self.query_one(Tree)
        tree.clear()
        self._populate_unified_tree(tree.root)

    def _populate_unified_tree(self, root: TreeNode) -> None:
        """Populates the entire tree with a unified project structure."""
        if not self.app_graph:
            root.add("⚠️ [red]app_graph.json not found or invalid.[/]")
            return

        # --- Backend Node ---
        backend_node = root.add("📦 [b]Backend[/b]")
        self._populate_for_backend(backend_node)

        # --- Frontends Node ---
        frontends_node = root.add("🖥️ [b]Frontends[/b]")
        frontend_targets = self.app_graph.get("frontend_targets", [])
        for target in frontend_targets:
            target_node = frontends_node.add(f"🚀 [{self._get_color_for_type(target['type'])}]{target['id']}[/]")
            self._populate_for_frontend(target_node, target)

        root.expand_all()

    def _get_color_for_type(self, target_type: str) -> str:
        """Returns a color based on the frontend target type for visual distinction."""
        return "cyan" if target_type == "web" else "magenta"

    def _populate_for_backend(self, backend_root: TreeNode) -> None:
        """Populates the tree with backend domains (flows) and shared models, with namespacing."""

        # --- Domains (Flows) ---
        domains_root = backend_root.add("▶️ [b]Domains[/b]")
        domain_groups = {}
        for flow in self.app_graph.get("backend", {}).get("flows", []):
            domain_name = flow['domain'].split('.')[0]
            domain_groups.setdefault(domain_name, []).append(flow)

        for domain_name, flows in sorted(domain_groups.items()):
            current_domain_node = domains_root.add(f"📦 [green][b]{domain_name}[/b][/green]")
            for flow in sorted(flows, key=lambda f: f['domain']):
                domain_parts = flow['domain'].split('.')
                flow_name = ".".join(domain_parts[1:]) if len(domain_parts) > 1 else flow['file'].split('/')[-1].replace(".py", "")
                
                flow_node = current_domain_node.add(f"▶️ [cyan]{flow_name}[/cyan]")
                flow_node.data = {"file_path": flow['file'], "name": flow['domain'], "type": "flow"}

        # --- Shared Models ---
        models_root = backend_root.add("📄 [b]Models[/b]")
        shared_models = self.app_graph.get("shared_models", {}).get("models", [])
        
        namespaced_models = {}
        for model in shared_models:
            relative_path = os.path.relpath(model['file'], self.app_graph['shared_models']['path'])
            parts = relative_path.replace(".py", "").split(os.sep)
            
            current_level = namespaced_models
            for part in parts[:-1]:
                current_level = current_level.setdefault(part, {})
            current_level[parts[-1]] = model

        def add_namespaced_nodes(parent_node: TreeNode, data: dict):
            for name, content in sorted(data.items()):
                if "file" in content: # It's a model
                    model_node = parent_node.add(f"🔹 [yellow]{content['name']}[/yellow]")
                    model_node.data = {"file_path": content['file'], "name": content['name'], "type": "model"}
                else: # It's a directory/namespace
                    dir_node = parent_node.add(f"📁 [blue]{name}[/blue]")
                    add_namespaced_nodes(dir_node, content)
        
        add_namespaced_nodes(models_root, namespaced_models)

    def _populate_for_frontend(self, target_root: TreeNode, target_data: dict) -> None:
        """Populates a node with a specific frontend target's views and assets."""
        # Add Views
        views_node = target_root.add("📄 [b]Views[/b]")
        for view in target_data.get("views", []):
            view_node = views_node.add(f"[yellow]{view['file'].split('/')[-1]}[/yellow]")
            view_node.data = {"file_path": view['file'], "name": view['file'], "type": "view"}
            for wiring in view.get("flow_wirings", []):
                wiring_node = view_node.add(f"⚡️ [dim]on[/dim] [cyan]{wiring['element']}[/cyan]")
                wiring_node.add(f"  [dim]↳ triggers[/dim] [green]{wiring['action']}[/green]")

        # Add Renderers (if any)
        if target_data.get("renderers"):
            renderers_node = target_root.add("🎨 [b]Renderers[/b]")
            for renderer in target_data.get("renderers", []):
                renderers_node.add(f"🖌️ [yellow]{renderer['file'].split('/')[-1]}[/yellow]")

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """When a selectable node is clicked, post a message."""
        if event.node.data and "file_path" in event.node.data:
            node_data = event.node.data
            self.post_message(self.FlowSelected(
                name=node_data["name"],
                file_path=node_data["file_path"],
                target_type=node_data["type"]
            ))

    def compose(self) -> ComposeResult:
        """Render the explorer with a single, unified tree."""
        yield Tree("🌐 [b]Project[/b]")

    def on_mount(self) -> None:
        """Populate the unified tree once the DOM is ready."""
        self._populate_unified_tree(self.query_one(Tree).root)
