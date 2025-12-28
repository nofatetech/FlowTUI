import os
import ast
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Tree, Static
from textual.message import Message


class ExplorerContent(Vertical):
    """
    A file explorer that scans a target directory, displays a structured
    view, and emits a message when a Flow is selected.
    """

    class FlowSelected(Message):
        """Posted when a flow file/node is selected in the explorer."""
        def __init__(self, flow_name: str, file_path: str) -> None:
            super().__init__()
            self.flow_name = flow_name
            self.file_path = file_path

    # --- Scanner & Parser Logic ---

    def _parse_flow_file(self, source_code: str) -> list[str]:
        """
        Parses a Flow file's source to find the class docstring and extract "Routes:".
        Convention: The file contains one class, with a docstring line like:
        "Routes: GET, POST, DELETE"
        """
        try:
            tree = ast.parse(source_code)
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    docstring = ast.get_docstring(node)
                    if docstring:
                        for line in docstring.split('\n'):
                            if line.strip().lower().startswith("routes:"):
                                routes = line.split(":", 1)[1].strip()
                                return [f"↳ [green]{r.strip()}[/]" for r in routes.split(",")]
            return ["- [gray]No routes defined[/]"]
        except Exception:
            return ["⚠️ [red]Parse Error[/]"]

    def _parse_model_file(self, source_code: str) -> list[str]:
        """
        Parses a Python file's source code to find a class and its attributes.
        Convention: The file contains one Pydantic-style model with typed attributes.
        """
        attributes = []
        try:
            tree = ast.parse(source_code)
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    # Found the class, now find its annotated attributes
                    for attr_node in node.body:
                        if isinstance(attr_node, ast.AnnAssign):
                            attr_name = attr_node.target.id
                            attr_type = attr_node.annotation.id
                            attributes.append(f"🔹 {attr_name}: [cyan]{attr_type}[/]")
        except Exception:
            return ["⚠️ [red]Parse Error[/]"]
        return attributes

    def _scan_directory(self, root_path: str, parser_func) -> dict:
        """
        Recursively scans a directory for .py files and applies a parser function.
        Returns a nested dictionary representing the folder structure.
        """
        results = {}
        if not os.path.isdir(root_path):
            results["⚠️ [red]Directory Not Found[/]"] = {}
            return results

        for dirpath, _, filenames in os.walk(root_path):
            current_level = results
            rel_path = os.path.relpath(dirpath, root_path)
            if rel_path != ".":
                for part in rel_path.split(os.sep):
                    current_level = current_level.setdefault(part, {})

            for filename in sorted(filenames):
                if filename.endswith(".py") and not filename.startswith("__"):
                    module_name = filename.replace(".py", "")
                    file_path = os.path.join(dirpath, filename)
                    try:
                        with open(file_path, "r") as f:
                            source = f.read()
                        
                        # Store items and the file path
                        items = parser_func(source)
                        current_level.setdefault(module_name, {})["_items"] = items
                        current_level[module_name]["_file_path"] = file_path
                    except Exception:
                        current_level.setdefault(module_name, {})["_items"] = ["⚠️ [red]Read Error[/]"]
        return results

    def _populate_tree(self, tree_node, data: dict, icon: str, name_style: str):
        """Helper function to recursively populate a Tree widget from nested data."""
        for name, content in data.items():
            sub_node = tree_node.add(f"{icon} [{name_style}][b]{name}[/b][/{name_style}]")
            
            # Attach the file path to the node's data if it exists
            if "_file_path" in content:
                sub_node.data = {"file_path": content["_file_path"], "flow_name": name}

            if "_items" in content:
                for item in content["_items"]:
                    sub_node.add(item)
            
            sub_dirs = {k: v for k, v in content.items() if k not in ["_items", "_file_path"]}
            if sub_dirs:
                self._populate_tree(sub_node, sub_dirs, icon, name_style)

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """When a flow node is selected, post a message."""
        if event.node.data and "file_path" in event.node.data:
            self.post_message(self.FlowSelected(
                flow_name=event.node.data["flow_name"],
                file_path=event.node.data["file_path"]
            ))

    # --- UI Composition ---

    def compose(self) -> ComposeResult:
        """Render the explorer by scanning the project directory."""
        
        BACKEND_PATH = "backend"
        
        flows_path = os.path.join(BACKEND_PATH, "flows")
        models_path = os.path.join(BACKEND_PATH, "models")

        flow_data = self._scan_directory(flows_path, self._parse_flow_file)
        model_data = self._scan_directory(models_path, self._parse_model_file)

        # --- Build Flows (Domains) Tree ---
        flows_tree = Tree("📦 [b]Domains > Flows[/]")
        flows_tree.root.expand()
        self._populate_tree(flows_tree.root, flow_data, "▶️", "cyan")
        yield flows_tree
        
        # --- Build Models Tree ---
        models_tree = Tree("📄 [b]Models[/b]")
        models_tree.root.expand()
        self._populate_tree(models_tree.root, model_data, "🔹", "yellow")
        yield models_tree
