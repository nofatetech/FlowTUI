import os
import re
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Tree
from textual.widgets.tree import TreeNode
from textual.message import Message

class FlowImplementationContent(Vertical):
    """
    Scans HTML views and publishes detailed selection messages, including
    file path and line content, to enable external editing.
    """

    class ElementSelected(Message):
        """Posted when an HTML element is selected in the tree."""
        def __init__(self, element_data: dict, file_path: str, original_line: str) -> None:
            super().__init__()
            self.element_data = element_data
            self.file_path = file_path
            self.original_line = original_line

    def _parse_html_line(self, line: str) -> tuple[int, dict]:
        """Parses a single line of HTML, also storing the original line."""
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
        data["display"] = f"<{tag}{'#' + id if id else ''}{'.' + cls if cls else ''}>"
        return indent, data

    def _populate_html_tree(self, parent_node: TreeNode, file_path: str):
        """Builds a tree, attaching parsed data and file_path to each node."""
        node_stack = [(parent_node, -1)]
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    if not line.strip().startswith("<"): continue
                    
                    indent, data = self._parse_html_line(line)
                    data["file_path"] = file_path # Store the file path
                    
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

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """When a node is clicked, publish the ElementSelected message with full context."""
        if event.node.data:
            self.post_message(self.ElementSelected(
                element_data=event.node.data,
                file_path=event.node.data.get("file_path", ""),
                original_line=event.node.data.get("original_line", "")
            ))

    def compose(self) -> ComposeResult:
        # (compose method remains largely the same as the last correct version)
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
