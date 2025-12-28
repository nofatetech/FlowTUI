import os
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Tree
from textual.widgets.tree import TreeNode

class FlowImplementationContent(Vertical):
    """
    Displays the implementation details of a selected Flow, including its views and contracts.
    Dynamically scans HTML views and renders them as a proper tree.
    """

    def _parse_html_view(self, file_path: str) -> list[tuple[int, str]]:
        """
        Reads an HTML file and returns a list of (indent, text) tuples.
        """
        structure = []
        emojis = {
            "header": "🔝", "main": "📰", "section": "📑", "footer": "🔚",
            "h1": "-", "h2": "–", "p": " ", "button": "🔘", "nav": "🧭", "ul": "…",
            "a": "🔗"
        }
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    stripped_line = line.strip()
                    if not stripped_line:
                        continue
                    
                    indent = len(line) - len(line.lstrip(' '))
                    
                    if stripped_line.lower().startswith("<!-- 🔄 loop:"):
                        loop_desc = stripped_line.split(":", 1)[1].split("-->")[0].strip()
                        structure.append((indent, f"🔄 [b]Loop[/]: [i]{loop_desc}[/]"))
                        continue

                    if stripped_line.startswith('<'):
                        tag = stripped_line.split('>')[0].split(' ')[0][1:].lower()
                        emoji = emojis.get(tag, "📄")
                        structure.append((indent, f"{emoji} {stripped_line}"))

        except Exception:
            return [(0, "⚠️ [red]Read Error[/]")]
        return structure

    def _populate_html_tree(self, parent_node: TreeNode, parsed_data: list[tuple[int, str]]):
        """Recursively populates a Tree node from a list of (indent, text) tuples."""
        node_stack = [(parent_node, -1)] # (node, indent_level)

        for indent, text in parsed_data:
            last_node, last_indent = node_stack[-1]
            
            # If current indent is greater, it's a child of the last node
            if indent > last_indent:
                new_node = last_node.add(text)
                node_stack.append((new_node, indent))
            else:
                # Pop until we find a parent with a smaller indent
                while indent <= last_indent:
                    node_stack.pop()
                    last_node, last_indent = node_stack[-1]
                
                new_node = last_node.add(text)
                node_stack.append((new_node, indent))

    def compose(self) -> ComposeResult:
        impl_tree = Tree("📁 catalog.products")
        
        # --- Layouts & Controllers (Static) ---
        impl_tree.root.add("🎨 Layouts").add("📄 layout.html ([i]Pico.css[/])")
        impl_tree.root.add("▶️ Controllers").add("📄 index")

        # --- Views (Dynamically Scanned) ---
        views_root = impl_tree.root.add("🖼️ Views")
        PROJECT_PATH = "app_templates/web_app_template"
        views_dir = os.path.join(PROJECT_PATH, "views")

        if os.path.isdir(views_dir):
            for file in sorted(os.listdir(views_dir)):
                if file.endswith(".html") and not file.startswith("_"):
                    view_node = views_root.add(f"📄 [b blue]{file}[/]")
                    parsed_data = self._parse_html_view(os.path.join(views_dir, file))
                    self._populate_html_tree(view_node, parsed_data)

        # --- Blender Scene (Static Concept) ---
        blender_scene = views_root.add("🧊 [b]Blender Scene[/] (main.py)")
        blender_scene.add("📂 Collections").add("🖼️ UI Elements")

        # --- Contracts (Static) ---
        impl_tree.root.add("📜 Contracts").add("📄 ProductSchema")
        
        impl_tree.root.expand_all()
        yield impl_tree
