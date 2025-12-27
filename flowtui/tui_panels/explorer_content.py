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
        Parses a Python file's source code to find a class and its public methods.
        Convention: The file contains one class, and public methods don't start with '_'.
        """
        methods = []
        try:
            tree = ast.parse(source_code)
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    # Found the class, now find its methods
                    for method_node in node.body:
                        if isinstance(method_node, ast.FunctionDef) and not method_node.name.startswith('_'):
                            methods.append(f"⚡️ {method_node.name}")
        except Exception:
            return ["⚠️ [red]Parse Error[/]"]
        return methods

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
        Scans a directory for .py files and applies a parser function to each.
        Returns a dictionary mapping file names to the parsed data.
        """
        results = {}
        if not os.path.isdir(root_path):
            return {"error": [f"Directory not found: {root_path}"]}

        for filename in sorted(os.listdir(root_path)):
            if filename.endswith(".py") and not filename.startswith("__"):
                domain_name = filename.replace(".py", "")
                try:
                    with open(os.path.join(root_path, filename), "r") as f:
                        source = f.read()
                    results[domain_name] = parser_func(source)
                except Exception:
                    results[domain_name] = ["⚠️ [red]Read Error[/]"]
        return results

    # --- UI Composition ---

    def compose(self) -> ComposeResult:
        """Render the explorer by scanning the project directory."""
        
        # Convention: The TUI is opinionated and knows the project structure.
        PROJECT_PATH = "app_templates/web_app_template" # Hardcoded for now
        
        flows_path = os.path.join(PROJECT_PATH, "flows")
        models_path = os.path.join(PROJECT_PATH, "models")

        flow_data = self._scan_directory(flows_path, self._parse_flow_file)
        model_data = self._scan_directory(models_path, self._parse_model_file)

        # --- Build Flows (Domains) Tree ---
        flows_tree = Tree("📦 [b]Flows (Domains)[/]")
        flows_tree.root.expand()
        for name, methods in flow_data.items():
            node = flows_tree.root.add(f"▶️ [b cyan]{name}[/]")
            for method in methods:
                node.add(method)
        yield flows_tree
        
        # --- Build Models Tree ---
        models_tree = Tree("📄 [b]Models[/b]")
        models_tree.root.expand()
        for name, attributes in model_data.items():
            node = models_tree.root.add(f"🔹 [b yellow]{name.capitalize()}[/]")
            for attr in attributes:
                node.add(attr)
        yield models_tree
