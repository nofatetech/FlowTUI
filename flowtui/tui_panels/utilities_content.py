import os
import ast
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Tree

class UtilitiesContent(Vertical):
    """
    A panel that discovers and displays the status of core services and external providers.
    """

    def _parse_service_file(self, source_code: str) -> tuple[str, list[str]]:
        """
        Parses a service/provider file to find its STATUS and public methods.
        """
        status = "[gray]Unknown[/]"
        methods = []
        try:
            tree = ast.parse(source_code)
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    # Find the STATUS attribute
                    for item in node.body:
                        if isinstance(item, ast.Assign) and item.targets[0].id == "STATUS":
                            status_value = item.value
                            # A simple attempt to read the status string value
                            if isinstance(status_value, ast.Constant):
                                status = status_value.value
                            else: # Handle conditional status like in spotify_api
                                status = "[yellow]Dynamic[/]"
                    
                    # Find public methods
                    for method_node in node.body:
                        if isinstance(method_node, ast.FunctionDef) and not method_node.name.startswith('_'):
                            methods.append(f"- {method_node.name}")
        except Exception:
            return "⚠️ [red]Parse Error[/]", []
        return status, methods

    def _build_tree(self, tree: Tree, root_path: str):
        """Helper to scan a directory and populate a tree with service info."""
        if not os.path.isdir(root_path):
            tree.root.add(f"⚠️ [red]Directory not found[/]")
            return

        for filename in sorted(os.listdir(root_path)):
            if filename.endswith(".py") and not filename.startswith("__"):
                service_name = filename.replace(".py", "")
                try:
                    with open(os.path.join(root_path, filename), "r") as f:
                        source = f.read()
                    status, methods = self._parse_service_file(source)
                    node = tree.root.add(f"🔌 [b white]{service_name.capitalize()}[/]: [green]{status}[/]")
                    for method in methods:
                        node.add(f"  [cyan]{method}[/]")
                except Exception:
                    tree.root.add(f"⚠️ [red]Error reading {filename}[/]")


    def compose(self) -> ComposeResult:
        PROJECT_PATH = "app_templates/web_app_template"
        services_path = os.path.join(PROJECT_PATH, "services")
        providers_path = os.path.join(PROJECT_PATH, "providers")

        # --- Core Services ---
        services_tree = Tree("🚀 Core Services")
        services_tree.root.expand()
        self._build_tree(services_tree, services_path)
        yield services_tree

        # --- External Providers ---
        providers_tree = Tree("🛰️ External Providers")
        providers_tree.root.expand()
        self._build_tree(providers_tree, providers_path)
        yield providers_tree
