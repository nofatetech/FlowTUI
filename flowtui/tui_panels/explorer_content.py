import json
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Tree, RadioSet, RadioButton
from textual.message import Message
from textual.widgets.tree import TreeNode


class ExplorerContent(Vertical):
    """
    A file explorer that visualizes the application graph from app_graph.json,
    allows selecting different frontend/backend targets, and emits a message
    when a relevant node is selected.
    """

    class FlowSelected(Message):
        """Posted when a flow or view file/node is selected in the explorer."""

        def __init__(self, name: str, file_path: str, target_type: str) -> None:
            super().__init__()
            self.name = name
            self.file_path = file_path
            self.target_type = target_type

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_graph = self._load_app_graph()

    def _load_app_graph(self) -> dict:
        """Loads and parses the app_graph.json file."""
        try:
            with open("app_graph.json", "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}  # Return an empty graph on error

    def _clear_and_populate_tree(self) -> None:
        """Clears the tree and repopulates it based on the selected target."""
        tree = self.query_one(Tree)
        selected_button = self.query_one(RadioSet).pressed_button
        if not selected_button:
            return

        tree.clear()
        tree.root.label = str(selected_button.label)
        target_id = selected_button.id

        if target_id == "backend":
            self._populate_for_backend(tree.root)
        else:
            self._populate_for_frontend(tree.root, target_id)
        tree.root.expand_all()

    def _populate_for_backend(self, root: TreeNode) -> None:
        """Populates the Tree with backend flows and shared models."""
        if not self.app_graph:
            root.add("⚠️ [red]app_graph.json not found or invalid.[/]")
            return

        # --- Add Flows ---
        flows_node = root.add("📦 [b]Domains > Flows[/b]")
        backend_flows = self.app_graph.get("backend", {}).get("flows", [])
        for flow in backend_flows:
            domain_node = flows_node.add(f"▶️ [cyan][b]{flow['domain']}[/b][/cyan]")
            domain_node.data = {"file_path": flow['file'], "name": flow['domain'], "type": "flow"}
            for verb in flow.get("verbs", []):
                domain_node.add(f"↳ [green]{verb.upper()}[/]")

        # --- Add Shared Models ---
        models_node = root.add("📄 [b]Shared Models[/b]")
        shared_models = self.app_graph.get("shared_models", {}).get("models", [])
        for model in shared_models:
            model_node = models_node.add(f"🔹 [yellow]{model['name']}[/yellow]")
            model_node.data = {"file_path": model['file'], "name": model['name'], "type": "model"}


    def _populate_for_frontend(self, root: TreeNode, target_id: str) -> None:
        """Populates the Tree with a specific frontend target's views and assets."""
        target_data = next((t for t in self.app_graph.get("frontend_targets", []) if t["id"] == target_id), None)
        if not target_data:
            return

        root.add(f"EntryPoint: [dim]{target_data.get('entrypoint')}[/dim]")

        # --- Add Views ---
        views_node = root.add("🖥️ [b]Views[/b]")
        for view in target_data.get("views", []):
            view_node = views_node.add(f"📄 [yellow]{view['file'].split('/')[-1]}[/yellow]")
            view_node.data = {"file_path": view['file'], "name": view['file'], "type": "view"}
            for wiring in view.get("flow_wirings", []):
                wiring_node = view_node.add(f"⚡️ [dim]on[/dim] [cyan]{wiring['element']}[/cyan]")
                wiring_node.add(f"  [dim]triggers[/dim] [green]{wiring['action']}[/green]")
                wiring_node.add(f"  [dim]targets[/dim] [magenta]{wiring['target_element']}[/magenta]")

        # --- Add other target-specific info ---
        if target_data.get("renderers"):
            renderers_node = root.add("🎨 [b]Renderers[/b]")
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

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        """When the target is changed, re-populate the tree."""
        self._clear_and_populate_tree()

    def compose(self) -> ComposeResult:
        """Render the explorer with a target selector and a dynamic tree."""
        buttons = [RadioButton("Backend", id="backend")]
        if self.app_graph:
            for target in self.app_graph.get("frontend_targets", []):
                buttons.append(RadioButton(f"{target['type'].title()} App", id=target['id']))
        
        yield RadioSet(*buttons, id="target_selector")
        yield Tree("Explorer")

    def on_mount(self) -> None:
        """Set the initial state of the explorer after the DOM is ready."""
        try:
            radio_set = self.query_one(RadioSet)
            self.app.log(f"[DEBUG] ExplorerContent on_mount: RadioSet found: {radio_set}")
            self.app.log(f"[DEBUG] RadioSet children: {radio_set.children}")

            # Setting the value to True will trigger the `on_radio_set_changed`
            # event, which will then call `_clear_and_populate_tree`.
            # We do not need to call it directly from here.
            first_radio_button = next((child for child in radio_set.children if isinstance(child, RadioButton)), None)
            if first_radio_button:
                first_radio_button.value = True

        except Exception as e:
            self.app.log(f"[ERROR] Error in ExplorerContent on_mount: {e}")
            # Optionally, display an error message in the TUI itself
            self.query_one(Tree).root.add(f"⚠️ [red]Initialization Error: {e}[/]")
            self.query_one(Tree).root.expand()
