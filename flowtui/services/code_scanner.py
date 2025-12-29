import os
from tree_sitter import Language, Parser
from tree_sitter_languages import get_language, get_parser

class CodeScannerService:
    """
    A service that uses Tree-sitter to scan source code and build
    a structured representation of the application graph.
    """

    def __init__(self):
        self.parser_py = get_parser("python")
        self.parser_html = get_parser("html")
        self.lang_py = get_language("python")
        self.lang_html = get_language("html")

    def _execute_query(self, language, node, query_string):
        """Helper to run a Tree-sitter query and return captures."""
        query = language.query(query_string)
        return query.captures(node)

    def scan_python_for_flows(self, file_path: str, content: str) -> list[dict]:
        """Scans a Python file for Flow classes and their public methods (verbs)."""
        tree = self.parser_py.parse(bytes(content, "utf8"))
        root_node = tree.root_node
        
        # This query finds class definitions that inherit from something (e.g., BaseFlow)
        # and the names of all public methods within them.
        query = """
        (class_definition
          name: (identifier) @class.name
          superclasses: (argument_list . (identifier) @class.superclass)
          body: (block .
            (function_definition
              name: (identifier) @method.name
            )
          )
        )
        """
        captures = self._execute_query(self.lang_py, root_node, query)
        
        flows = {}
        for node, capture_name in captures:
            if capture_name == "class.name":
                class_name = node.text.decode('utf8')
                if class_name not in flows:
                    flows[class_name] = {"verbs": []}
            elif capture_name == "method.name":
                method_name = node.text.decode('utf8')
                if not method_name.startswith("_"): # Exclude private/magic methods
                    flows[class_name]["verbs"].append(method_name)
        
        # We're making an assumption here about domain naming convention
        # In a real system, this would be more robust.
        results = []
        for name, data in flows.items():
            domain_name_base = os.path.basename(file_path).replace(".py", "")
            results.append({
                "domain": f"{domain_name_base}.{name.lower()}",
                "file": file_path,
                "verbs": data["verbs"]
            })
        return results

    def scan_python_for_models(self, file_path: str, content: str) -> list[dict]:
        """Scans a Python file for Model classes (very basic)."""
        tree = self.parser_py.parse(bytes(content, "utf8"))
        root_node = tree.root_node
        query = "(class_definition name: (identifier) @class.name)"
        captures = self._execute_query(self.lang_py, root_node, query)
        
        models = []
        for node, _ in captures:
            models.append({
                "name": node.text.decode('utf8'),
                "file": file_path
            })
        return models

    def scan_html_for_wirings(self, file_path: str, content: str) -> list[dict]:
        """Scans an HTML file for `flow:*` attributes."""
        tree = self.parser_html.parse(bytes(content, "utf8"))
        root_node = tree.root_node
        query = """
        (start_tag
            (tag_name) @tag
            (attribute
                (attribute_name) @attr.name
                (quoted_attribute_value
                    (attribute_value) @attr.value
                )
            )
        )
        """
        captures = self._execute_query(self.lang_html, root_node, query)
        
        wirings = []
        # This is a bit complex to reconstruct which attribute belongs to which tag,
        # but for now we will assume any flow:* attr is a wiring.
        for node, capture_name in captures:
            if capture_name == "attr.name" and node.text.decode('utf8').startswith("flow:"):
                # A more robust parser would build a complete picture of the element,
                # but this is a good start.
                wirings.append({
                    "element": "unknown", # We need a more complex query to get this
                    "trigger": node.text.decode('utf8'),
                    "action": "unknown", # And this
                    "target_element": "unknown",
                    "description": "Scanned from HTML"
                })
        return wirings

    def build_app_graph(self, root_dir: str) -> dict:
        """Walks the project directory and builds the app graph from source."""
        graph = {
            "project_name": "Scanned Project",
            "backend": {"flows": []},
            "shared_models": {"path": os.path.join(root_dir, "backend", "models"), "models": []},
            "frontend_targets": []
        }
        
        backend_flows_path = os.path.join(root_dir, "backend", "flows")
        backend_models_path = os.path.join(root_dir, "backend", "models")
        frontends_path = os.path.join(root_dir, "frontends")

        # Scan backend flows
        for subdir, _, files in os.walk(backend_flows_path):
            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(subdir, file)
                    with open(path, "r") as f:
                        content = f.read()
                    graph["backend"]["flows"].extend(self.scan_python_for_flows(path, content))

        # Scan backend models
        for subdir, _, files in os.walk(backend_models_path):
            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(subdir, file)
                    with open(path, "r") as f:
                        content = f.read()
                    graph["shared_models"]["models"].extend(self.scan_python_for_models(path, content))

        # Scan frontend targets
        if os.path.exists(frontends_path):
            for target_dir in os.listdir(frontends_path):
                target_path = os.path.join(frontends_path, target_dir)
                if os.path.isdir(target_path):
                    target = {
                        "id": target_dir,
                        "type": "web" if "htmx" in target_dir else "blender", # Basic type inference
                        "path": target_path,
                        "views": []
                    }
                    for subdir, _, files in os.walk(target_path):
                        for file in files:
                            if file.endswith(".html"):
                                path = os.path.join(subdir, file)
                                with open(path, "r") as f:
                                    content = f.read()
                                # For now, we're not using the complex wiring scan
                                target["views"].append({"file": path, "flow_wirings": []})
                    graph["frontend_targets"].append(target)
                    
        return graph
