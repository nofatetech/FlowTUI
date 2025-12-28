import os
import ast
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Tree, Static

class ExplorerContent(Vertical):
    """
    A file explorer that scans a target directory and displays a structured
    view of its Flows and Models based on opinionated conventions.
    """

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
            # Return a structure that the tree builder can understand as an error.
            results["⚠️ [red]Directory Not Found[/]"] = {}
            return results

        for dirpath, _, filenames in os.walk(root_path):
            # Find the current position in the results dict
            current_level = results
            # Create a relative path to build the nested dict keys
            rel_path = os.path.relpath(dirpath, root_path)
            if rel_path != ".":
                for part in rel_path.split(os.sep):
                    current_level = current_level.setdefault(part, {})

            for filename in sorted(filenames):
                if filename.endswith(".py") and not filename.startswith("__"):
                    module_name = filename.replace(".py", "")
                    try:
                        with open(os.path.join(dirpath, filename), "r") as f:
                            source = f.read()
                        # Parsed methods/attributes are stored under a special key
                        current_level.setdefault(module_name, {})["_items"] = parser_func(source)
                    except Exception:
                        current_level.setdefault(module_name, {})["_items"] = ["⚠️ [red]Read Error[/]"]
        return results

    def _populate_tree(self, tree_node, data: dict, icon: str, name_style: str):
        """Helper function to recursively populate a Tree widget from nested data."""
        for name, content in data.items():
            # Add a node for the directory/file
            sub_node = tree_node.add(f"{icon} [b {name_style}]{name}[/]")
            
            # If there are items (methods/attributes), add them
            if "_items" in content:
                for item in content["_items"]:
                    sub_node.add(item)
            
            # Recurse for any sub-directories
            # We filter out the special '_items' key before recursing
            sub_dirs = {k: v for k, v in content.items() if k != "_items"}
            if sub_dirs:
                self._populate_tree(sub_node, sub_dirs, icon, name_style)

    # --- UI Composition ---

    def compose(self) -> ComposeResult:
        """Render the explorer by scanning the project directory."""
        
        PROJECT_PATH = "app_templates/web_app_template"
        
        flows_path = os.path.join(PROJECT_PATH, "flows")
        models_path = os.path.join(PROJECT_PATH, "models")

        flow_data = self._scan_directory(flows_path, self._parse_flow_file)
        model_data = self._scan_directory(models_path, self._parse_model_file)

        # --- Build Flows (Domains) Tree ---
        flows_tree = Tree("📦 [b]Flows (Domains)[/]")
        flows_tree.root.expand()
        self._populate_tree(flows_tree.root, flow_data, "▶️", "cyan")
        yield flows_tree
        
        # --- Build Models Tree ---
        models_tree = Tree("📄 [b]Models[/b]")
        models_tree.root.expand()
        self._populate_tree(models_tree.root, model_data, "🔹", "yellow")
        yield models_tree
