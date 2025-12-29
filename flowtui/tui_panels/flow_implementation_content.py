import os
import re
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Tree, Static
from textual.widgets.tree import TreeNode
from textual.message import Message

# Import the message from the explorer panel
from tui_panels.explorer_content import ExplorerContent

class FlowImplementationContent(Vertical):
    """
    Displays the implementation details (Controllers and Views) for a
    Flow that is selected in the Explorer panel.
    """

    # --- (ElementSelected and HTML parsing methods remain the same) ---
    class ElementSelected(Message):
        """Posted when an HTML element is selected in the tree."""
        def __init__(self, element_data: dict, file_path: str, original_line: str) -> None:
            super().__init__()
            self.element_data = element_data
            self.file_path = file_path
            self.original_line = original_line
            
    class MethodSelected(Message):
        """Posted when a controller method/verb is selected in the tree."""
        def __init__(self, flow_name: str, route_name: str, verb: str, is_implemented: bool, file_path: str) -> None:
            super().__init__()
            self.flow_name = flow_name
            self.route_name = route_name
            self.verb = verb
            self.is_implemented = is_implemented
            self.file_path = file_path
    
    HTML_TAG_EMOJIS = {
        "div": "📦", "p": "¶", "span": "📄", "a": "🔗", "img": "🖼️",
        "h1": "👑", "h2": "<h2>", "h3": "<h3>", "h4": "<h4>", "h5": "<h5>", "h6": "<h6>",
        "ul": "📜", "ol": "🔢", "li": "-",
        "table": "📅", "tr": "➡️", "td": "<td>", "th": "<th>",
        "form": "📝", "input": "💬", "button": "🔘", "textarea": "📋",
        "select": "🔽", "option": "🔹",
        "header": "🔼", "footer": "🔽", "nav": "🧭", "main": "📘", "section": "📐", "article": "📰",
        "aside": "📑", "figure": "🎨", "figcaption": "✏️",
        "video": "🎬", "audio": "🎵", "source": "📀",
        "canvas": "🖌️", "svg": "📈",
        "details": "🔍", "summary": "📝",
        "dialog": "💬", "menu": "📋",
        "script": "📜", "style": "🎨", "link": "🔗", "meta": "⚙️",
        "body": "🧍", "html": "🌐", "head": "🧠",
        "default": "📄"
    }
    
    def _parse_html_line(self, line: str) -> tuple[int, dict]:
        indent = len(line) - len(line.lstrip(' '))
        content = line.strip()
        match = re.match(r"<([a-zA-Z0-9]+)\s*([^>]*)>", content)
        if not match:
            return indent, {"display": content, "original_line": line}
        tag, attrs_str = match.groups()
        data = {"tag": tag, "original_line": line}
        for attr_match in re.finditer(r'([a-zA-Z0-9:-]+)="([^"]*)"', attrs_str):
            key, value = attr_match.groups()
            data[key] = value
        cls = data.get('class', '')
        id = data.get('id', '')
        emoji = self.HTML_TAG_EMOJIS.get(tag, self.HTML_TAG_EMOJIS["default"])
        data["display"] = f"{emoji} <{tag}{'#' + id if id else ''}{'.' + cls if cls else ''}>"
        return indent, data

    def _populate_html_tree(self, parent_node: TreeNode, file_path: str):
        node_stack = [(parent_node, -1)]
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    if not line.strip().startswith("<"): continue
                    indent, data = self._parse_html_line(line)
                    data["file_path"] = file_path
                    last_node, last_indent = node_stack[-1]
                    if indent > last_indent:
                        new_node = last_node.add(data["display"])
                        new_node.data = data
                        node_stack.append((new_node, indent))
                    else:
                        while indent <= last_indent:
                            node_stack.pop()
                            _, last_indent = node_stack[-1]
                        parent = node_stack[-1][0]
                        new_node = parent.add(data["display"])
                        new_node.data = data
                        node_stack.append((new_node, indent))
        except Exception:
            parent_node.add("⚠️ [red]Parse Error[/]")
    
    # --- New Dynamic Tree Logic ---

    def _get_flow_structure(self, file_path: str) -> dict[str, dict[str, list[str] | set[str]]]:
        """
        Parses a flow file to find BaseFlow subclasses (flows), their routes from
        docstrings, and their public methods.
        Returns a dict like:
        {
            "flow_name": {
                "routes": ["ROUTE1", "ROUTE2"],
                "methods": {"get", "post"}
            },
            ...
        }
        """
        flow_data = {}
        try:
            with open(file_path, 'r') as f:
                content = f.read()

            # Regex to find inner classes inheriting from BaseFlow.
            # It captures: 
            # Group 1: flow_name (the name of the inner class)
            # Group 3/4: docstring content (optional)
            # Group 5: class body
            # The lookahead `(?=\n\s*class\s+\w+|\Z)` ensures it stops before the next class definition or at the end of the file.
            flow_class_pattern = re.compile(
                r"class\s+(\w+)\s*\(\s*BaseFlow\s*\)\s*:\s*(?:(?:\"\"\"(.*?)\"\"\")|(?:\'\'\'(.*?)\'\'\'))?([\s\S]*?)(?=\n\s*class\s+\w+|\Z)",
                re.MULTILINE
            )
            
            for match in flow_class_pattern.finditer(content):
                flow_name = match.group(1)
                # Extract docstring content, handling both triple double-quotes and triple single-quotes
                docstring = match.group(2) or match.group(3) or "" 
                class_body = match.group(4)

                current_flow_routes = []
                if docstring:
                    # Search for 'Routes:' within the extracted docstring
                    routes_match = re.search(r'Routes:\s*([A-Z0-9_, ]+)', docstring, re.IGNORECASE)
                    if routes_match:
                        routes_str = routes_match.group(1)
                        current_flow_routes = [route.strip() for route in routes_str.split(',')]

                current_flow_methods = set()
                if class_body:
                    # Find all public methods defined directly within this flow class's body
                    # We look for 'def ' followed by a method name and an opening parenthesis.
                    found_methods = re.findall(r'^\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', class_body, re.MULTILINE)
                    # Convert method names to lowercase and exclude private methods (starting with '_')
                    current_flow_methods = {m.lower() for m in found_methods if not m.startswith('_')}
                
                # Only add to flow_data if routes or methods were found, indicating a valid flow definition
                if current_flow_routes or current_flow_methods:
                    flow_data[flow_name] = {
                        "routes": current_flow_routes,
                        "methods": current_flow_methods
                    }

        except Exception as e:
            # Log any parsing errors for debugging purposes.
            print(f"Error parsing flow file {file_path}: {e}")
            pass # Continue processing other files if an error occurs
        return flow_data

        def _update_tree_for_flow(self, selected_flow_full_path: str, flow_file_path: str) -> None:
            """Clear and rebuild the tree to show the implementation of backend Flows in a file."""
            tree = self.query_one(Tree)
            tree.clear()
            # Use the file path for the root label, as it contains multiple flows
            tree.root.label = f"📁 {flow_file_path}"
    
            flow_structures = self._get_flow_structure(flow_file_path)
            
            if not flow_structures:
                tree.root.add("⚠️ [gray]No flows found or parsed correctly in this file. Ensure flows inherit from BaseFlow and have a 'Routes:' entry in their docstring.[/]")
                return
    
            # --- Controllers ---
            controllers_root = tree.root.add("▶️ [b]Controllers[/b]")
    
            sorted_flow_names = sorted(flow_structures.keys())
    
            # Determine the module path prefix for the file.
            # E.g., if selected_flow_full_path is "fleet.vehicles.index", the prefix is "fleet.vehicles".
            # This prefix will be used to construct the full path for each flow found in the file.
            module_path_prefix = '.'.join(selected_flow_full_path.split('.')[:-1])
    
            for flow_name in sorted_flow_names: # flow_name is e.g. 'index' or 'status_synch'
                flow_data = flow_structures[flow_name]
                
                # Construct the full path for the current flow.
                # If module_path_prefix is empty (e.g., for flows in the root of 'backend'),
                # the full path is just the flow_name. Otherwise, it's prefix.flow_name.
                if module_path_prefix:
                    current_full_flow_path = f"{module_path_prefix}.{flow_name}"
                else:
                    current_full_flow_path = flow_name
    
                flow_node_label = f"▶️ [cyan]{flow_name}[/cyan]"
                flow_node = controllers_root.add(flow_node_label)
                flow_node.data = {"full_path": current_full_flow_path, "file_path": flow_file_path, "type": "flow"}
    
                routes = flow_data.get("routes", [])
                actual_methods = flow_data.get("methods", set())
                standard_verbs = ["get", "post", "put", "delete"]
    
                if not routes:
                    flow_node.add("⚠️ [gray]No routes defined in docstring for this flow.[/]")
                
                # Iterate through routes defined in the flow's docstring
                for route in routes:
                    route_node = flow_node.add(f"▶️ [green]{route}[/green]")
                    # For each route, list all standard verbs
                    for verb in standard_verbs:
                        # Check if the verb (lowercase) is defined as a method in the current flow class
                        is_implemented = verb.lower() in actual_methods
                        label = f"↳ [cyan]{verb.upper()}[/]" if is_implemented else f"↳ [gray]{verb.upper()}[/]"
                        verb_node = route_node.add(label)
                        verb_node.data = {
                            "flow_name": current_full_flow_path, # This is the full path to the flow
                            "route_name": route,
                            "verb": verb,
                            "is_implemented": is_implemented,
                            "file_path": flow_file_path
                        }
    
            # --- Views (Hardcoded for now) ---
            views_root = tree.root.add("🖼️ [b]Associated Views[/b]")
            self._find_and_populate_views(views_root)
            
            # --- Contracts (Hardcoded for now) ---
            contracts_root = tree.root.add("📜 [b]Associated Contracts[/b]")
            self._find_and_populate_contracts(contracts_root)
            
            tree.root.expand_all()
    
    def _update_tree_for_view(self, view_name: str, view_file_path: str) -> None:
        """Clear and rebuild the tree to show the content of a View file."""
        tree = self.query_one(Tree)
        tree.clear()
        tree.root.label = f"📄 {view_name.split('/')[-1]}"
        self._populate_html_tree(tree.root, view_file_path)
        tree.root.expand_all()

    def _update_tree_for_model(self, model_name: str, model_file_path: str) -> None:
        """Clear and rebuild the tree to show the content of a Model file."""
        tree = self.query_one(Tree)
        tree.clear()
        tree.root.label = f"🔹 {model_name}"
        try:
            with open(model_file_path, 'r') as f:
                content = f.read()
            # Simple display for now, could be enhanced with syntax highlighting
            tree.root.add(content)
        except Exception:
            tree.root.add("⚠️ [red]Could not read file.[/]")

    def _find_and_populate_views(self, parent_node: TreeNode):
        """Helper to find and populate associated views (currently hardcoded)."""
        WEB_APP_PATH = "app_templates/web_app_template" # This should come from app_graph
        views_dir = os.path.join(WEB_APP_PATH, "views")
        if os.path.isdir(views_dir):
            for file in sorted(os.listdir(views_dir)):
                if file.endswith(".html") and not file.startswith("_"):
                    view_node = parent_node.add(f"📄 [blue]{file}[/blue]")
                    self._populate_html_tree(view_node, os.path.join(views_dir, file))

    def _find_and_populate_contracts(self, parent_node: TreeNode):
        """Helper to find and populate associated contracts (currently hardcoded)."""
        BACKEND_PATH = "backend" # This should come from app_graph
        contracts_dir = os.path.join(BACKEND_PATH, "contracts")
        if os.path.isdir(contracts_dir):
            for file in sorted(os.listdir(contracts_dir)):
                if file.endswith(".py") and not file.startswith("__"):
                    parent_node.add(f"📄 [yellow]{file}[/yellow]")

    def on_explorer_content_flow_selected(self, message: ExplorerContent.FlowSelected) -> None:
        """Listen for messages from the explorer and update this panel based on target type."""
        target_type = message.target_type
        
        if target_type == "flow":
            self._update_tree_for_flow(message.name, message.file_path)
        elif target_type == "view":
            self._update_tree_for_view(message.name, message.file_path)
        elif target_type == "model":
            self._update_tree_for_model(message.name, message.file_path)
        else:
            # Default case: clear the tree if the type is unknown
            self.query_one(Tree).clear()
            self.query_one(Tree).root.label = "Unsupported selection"

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """Post a message when a verb or an HTML element is selected."""
        self._on_tree_node_selected(event)
    
    def _on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        if not event.node.data:
            return

        # Case 1: A controller method/verb was selected
        if "verb" in event.node.data:
            data = event.node.data
            self.post_message(self.MethodSelected(
                flow_name=data["flow_name"],
                route_name=data["route_name"],
                verb=data["verb"],
                is_implemented=data["is_implemented"],
                file_path=data["file_path"]
            ))
        
        # Case 2: An HTML element was selected
        elif "tag" in event.node.data:
            data = event.node.data
            self.post_message(self.ElementSelected(
                element_data=data,
                file_path=data.get("file_path", ""),
                original_line=data.get("original_line", "")
            ))

    def compose(self) -> ComposeResult:
        """Compose the initial empty tree."""
        yield Tree("⬅️ [i]Select a target from the Explorer[/i]")
