import os
import re
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Tree
from textual.widgets.tree import TreeNode
from textual.message import Message

class FlowImplementationContent(Vertical):
    """
    Displays the implementation details of a selected Flow.
    Dynamically scans HTML views and publishes selection events.
    """

    # 1. Define a custom message for inter-panel communication
    class ElementSelected(Message):
        """Posted when an HTML element is selected in the tree."""
        def __init__(self, element_data: dict) -> None:
            super().__init__()
            self.element_data = element_data

    def _parse_html_line(self, line: str) -> tuple[int, dict]:
        """
        Parses a single line of HTML, extracting indent, tag, and attributes.
        Returns a tuple of (indent, data_dictionary).
        """
        indent = len(line) - len(line.lstrip(' '))
        content = line.strip()
        
        # Regex to capture the tag and all attributes
        match = re.match(r"<([a-zA-Z0-9]+)\s*([^>]*)>", content)
        if not match:
            return indent, {"display": content}

        tag, attrs_str = match.groups()
        
        data = {"tag": tag}
        # Regex to find key="value" pairs
        for attr_match in re.finditer(r'([a-zA-Z0-9:-]+)="([^"]*)"', attrs_str):
            key, value = attr_match.groups()
            data[key] = value

        # Create a display string for the tree
        cls = data.get('class', '')
        id = data.get('id', '')
        data["display"] = f"<{tag}{'#' + id if id else ''}{'.' + cls if cls else ''}>"
        return indent, data

    def _populate_html_tree(self, parent_node: TreeNode, file_path: str):
        """Builds a tree from a file, attaching parsed data to each node."""
        node_stack = [(parent_node, -1)]
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    if not line.strip().startswith("<"): continue
                    
                    indent, data = self._parse_html_line(line)
                    
                    last_node, last_indent = node_stack[-1]
                    if indent > last_indent:
                        # Child of the previous node
                        new_node = last_node.add(data["display"])
                        new_node.data = data # Attach the parsed data to the node
                        node_stack.append((new_node, indent))
                    else:
                        # Pop until we find a suitable parent
                        while indent <= last_indent:
                            node_stack.pop()
                            _, last_indent = node_stack[-1]
                        parent = node_stack[-1][0]
                        new_node = parent.add(data["display"])
                        new_node.data = data # Attach data here too
                        node_stack.append((new_node, indent))
        except Exception:
            parent_node.add("⚠️ [red]Parse Error[/]")

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """
        2. When a node is clicked, publish the ElementSelected message.
        """
        # We post the message with the data we attached earlier.
        if event.node.data:
            self.post_message(self.ElementSelected(event.node.data))

    def compose(self) -> ComposeResult:
        impl_tree = Tree("📁 catalog.products")
        
        impl_tree.root.add("▶️ Controllers").add("📄 index")

        views_root = impl_tree.root.add("🖼️ Views")
        PROJECT_PATH = "app_templates/web_app_template"
        views_dir = os.path.join(PROJECT_PATH, "views")

        if os.path.isdir(views_dir):
            for file in sorted(os.listdir(views_dir)):
                if file.endswith(".html") and not file.startswith("_"):
                    view_node = views_root.add(f"📄 [b blue]{file}[/]")
                    self._populate_html_tree(view_node, os.path.join(views_dir, file))
        
        impl_tree.root.expand_all()
        yield impl_tree
