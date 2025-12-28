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

    def _get_flow_structure(self, file_path: str) -> tuple[list[str], set[str]]:
        """
        Parses a flow file to get a list of routes from the docstring and a
        set of all public method names.
        """
        routes: list[str] = []
        methods: set[str] = set()
        try:
            with open(file_path, 'r') as f:
                content = f.read()

            # 1. Get all public method names using regex
            found_methods = re.findall(r'^\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', content, re.MULTILINE)
            methods = {m.lower() for m in found_methods if not m.startswith('_')}

            # 2. Get routes from the class docstring
            class_match = re.search(r'class \w+:\s*"""(.*?)"""', content, re.DOTALL)
            if class_match:
                docstring = class_match.group(1)
                routes_match = re.search(r'Routes:\s*([A-Z0-9_, ]+)', docstring, re.IGNORECASE)
                if routes_match:
                    routes_str = routes_match.group(1)
                    routes = [route.strip() for route in routes_str.split(',')]
        
        except Exception:
            # Errors will be handled by the caller
            pass
        return routes, methods

    def update_tree(self, flow_name: str, flow_file_path: str) -> None:
        """Clear and rebuild the tree based on the selected flow."""
        self.query_one(Tree).clear()
        tree = self.query_one(Tree)
        tree.root.label = f"📁 {flow_name}"

        # --- Controllers ---
        controllers_root = tree.root.add("▶️ [b]Controllers[/b]")
        
        routes, actual_methods = self._get_flow_structure(flow_file_path)
        standard_verbs = ["get", "post", "put", "delete"]

        if not routes:
            controllers_root.add("⚠️ [gray]No routes defined in docstring.[/]")
        
        for route in routes:
            route_node = controllers_root.add(f"▶️ [green]{route}[/green]")
            for verb in standard_verbs:
                # Opinionated naming convention: routeName_httpVerb
                expected_method = f"{route.lower()}_{verb}"
                
                # Special case: a method name matching the route name is the GET
                is_implemented = expected_method in actual_methods
                if not is_implemented and verb == "get" and route.lower() in actual_methods:
                    is_implemented = True

                label = f"↳ [cyan]{verb.upper()}[/]" if is_implemented else f"↳ [gray]{verb.upper()}[/]"
                verb_node = route_node.add(label)
                verb_node.data = {
                    "flow_name": flow_name,
                    "route_name": route,
                    "verb": verb,
                    "is_implemented": is_implemented,
                    "file_path": flow_file_path
                }

        # --- Views ---
        views_root = tree.root.add("🖼️ [b]Views[/b]")
        PROJECT_PATH = "app_templates/web_app_template"
        views_dir = os.path.join(PROJECT_PATH, "views")
        
        if os.path.isdir(views_dir):
            for file in sorted(os.listdir(views_dir)):
                if file.endswith(".html") and not file.startswith("_"):
                    view_node = views_root.add(f"📄 [blue]{file}[/blue]")
                    self._populate_html_tree(view_node, os.path.join(views_dir, file))
        
        tree.root.expand_all()

        # --- Contracts ---
        contracts_root = tree.root.add("📜 [b]Contracts[/b]")
        contracts_dir = os.path.join(PROJECT_PATH, "contracts")
        if os.path.isdir(contracts_dir):
            for file in sorted(os.listdir(contracts_dir)):
                if file.endswith(".py") and not file.startswith("__"):
                    contracts_root.add(f"📄 [yellow]{file}[/yellow]")
        
        tree.root.expand()

    def on_explorer_content_flow_selected(self, message: ExplorerContent.FlowSelected) -> None:
        """Listen for messages from the explorer and update this panel."""
        self.update_tree(message.flow_name, message.file_path)

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        if event.node.data and "tag" in event.node.data:
            self.post_message(self.ElementSelected(
                element_data=event.node.data,
                file_path=event.node.data.get("file_path", ""),
                original_line=event.node.data.get("original_line", "")
            ))

    def compose(self) -> ComposeResult:
        """Compose the initial empty tree."""
        yield Tree("⬅️ [i]Select a Flow from the Explorer[/i]")
