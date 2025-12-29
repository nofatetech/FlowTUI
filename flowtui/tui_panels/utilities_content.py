import os
import ast
import json
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Tree

class UtilitiesContent(Vertical):
    """
    A panel that discovers and displays the status of core services and external providers.
    It combines static analysis (.py files) with runtime analysis (manifest.json).
    """

    def _parse_service_file(self, source_code: str) -> tuple[str, list[str]]:
        """
        Parses a service/provider file to find its fallback STATUS and public methods.
        """
        status = "[gray]Unknown[/]"
        methods = []
        try:
            tree = ast.parse(source_code)
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    # Find the STATUS attribute (used as a fallback)
                    for item in node.body:
                        if isinstance(item, ast.Assign) and hasattr(item.targets[0], 'id') and item.targets[0].id == "STATUS":
                            status_value = item.value
                            if isinstance(status_value, ast.Constant):
                                status = status_value.value
                            else:
                                status = "[yellow]Dynamic[/]"
                    
                    # Find public methods
                    for method_node in node.body:
                        if isinstance(method_node, ast.FunctionDef) and not method_node.name.startswith('_'):
                            methods.append(f"- {method_node.name}")
        except Exception:
            return "⚠️ [red]Parse Error[/]", []
        return status, methods

    def _build_tree(self, tree: Tree, root_path: str, manifest: dict, manifest_key: str):
        """
        Helper to scan a directory and populate a tree, using the manifest for status.
        """
        if not os.path.isdir(root_path):
            tree.root.add(f"⚠️ [red]Directory not found[/]")
            return

        for filename in sorted(os.listdir(root_path)):
            if filename.endswith(".py") and not filename.startswith("__"):
                service_name = filename.replace(".py", "")
                try:
                    with open(os.path.join(root_path, filename), "r") as f:
                        source = f.read()
                    
                    static_status, methods = self._parse_service_file(source)
                    
                    runtime_status = manifest.get(manifest_key, {}).get(service_name, {}).get("status")
                    display_status = runtime_status or static_status
                    
                    color = "green" if display_status == "Connected" else "yellow"
                    
                    node = tree.root.add(f"🔌 [b white]{service_name.capitalize()}[/]: [{color}]{display_status}[/]")
                    for method in methods:
                        node.add(f"  [cyan]{method}[/]")
                except Exception:
                    tree.root.add(f"⚠️ [red]Error reading {filename}[/]")


    def compose(self) -> ComposeResult:
        BACKEND_PATH = "backend"
        services_path = os.path.join(BACKEND_PATH, "services")
        providers_path = os.path.join(BACKEND_PATH, "providers")
        
        # Manifest data is not available in this simplified version, so we pass empty dicts
        manifest_data = {}

        # Core Services
        services_tree = Tree("🚀 Core Services")
        services_tree.root.expand()
        self._build_tree(services_tree, services_path, manifest_data, "services")
        yield services_tree

        # External Providers
        providers_tree = Tree("🛰️ External Providers")
        providers_tree.root.expand()
        self._build_tree(providers_tree, providers_path, manifest_data, "providers")
        yield providers_tree