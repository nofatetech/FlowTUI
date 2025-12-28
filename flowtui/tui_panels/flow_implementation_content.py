import os
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Tree

class FlowImplementationContent(Vertical):
    """
    Displays the implementation details of a selected Flow, including its views and contracts.
    Now dynamically scans HTML views.
    """

    def _parse_html_view(self, file_path: str) -> list[str]:
        """
        Reads an HTML file and extracts a simplified, indented tree structure.
        """
        structure = []
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    stripped_line = line.strip()
                    indent = "  " * (len(line) - len(line.lstrip(' ')))
                    
                    if stripped_line.lower().startswith(('<header', '<main', '<footer', '<section', '<nav')):
                        tag = stripped_line.split('>')[0] + '>'
                        structure.append(f"{indent}{tag}")
                    elif stripped_line.lower().startswith(('<h1>', '<h2>', '<p', '<li>', '<button')):
                        tag = stripped_line.split('>')[0].split(' ')[0] + '>'
                        # Basic content extraction
                        content = stripped_line.replace(f'<{tag[1:]}', '').rsplit('<', 1)[0]
                        if len(content) > 30:
                            content = content[:27] + '...'
                        if content:
                            structure.append(f"{indent}{tag} [i]'{content}'[/i]")
                        else:
                            structure.append(f"{indent}{tag}")
                    elif "<!-- 🔄 Loop:" in stripped_line:
                        loop_desc = stripped_line.split("<!-- 🔄 Loop:", 1)[1].split("-->", 1)[0].strip()
                        structure.append(f"{indent}🔄 [b]Loop[/]: [i]{loop_desc}[/]")

        except Exception:
            return ["⚠️ [red]Read Error[/]"]
        return structure

    def compose(self) -> ComposeResult:
        impl_tree = Tree("📁 catalog.products")
        impl_tree.root.expand()
        
        # --- Layouts ---
        layouts = impl_tree.root.add("🎨 Layouts")
        layouts.add("📄 layout.html ([i]Pico.css[/])")
        
        # --- Controllers ---
        controllers = impl_tree.root.add("▶️ Controllers")
        controllers.add("📄 index")

        # --- Views (Dynamically Scanned) ---
        views_root = impl_tree.root.add("🖼️ Views")
        
        PROJECT_PATH = "app_templates/web_app_template"
        views_dir = os.path.join(PROJECT_PATH, "views")

        if os.path.isdir(views_dir):
            for root, _, files in os.walk(views_dir):
                for file in sorted(files):
                    if file.endswith(".html") and not file.startswith("_") and "layouts" not in root:
                        file_path = os.path.join(root, file)
                        view_node = views_root.add(f"📄 [b blue]{file}[/]")
                        for line_content in self._parse_html_view(file_path):
                            view_node.add(line_content)
        else:
            views_root.add("⚠️ [red]Views directory not found[/]")

        # --- BLENDER SCENE VIEW (Concept) ---
        blender_scene = views_root.add("🧊 [b]Blender Scene[/] (main.py)")
        scene_root = blender_scene.add("📂 Collections")
        scene_root.add("🖼️ UI Elements (Objects)")
        scene_root.add("💡 Lights & 🎥 Cameras")
        scene_root.add("⚡️ Bindings (scene.add_item)")

        # --- Contracts ---
        contracts = impl_tree.root.add("📜 Contracts")
        contracts.add("📄 ProductSchema")
        
        impl_tree.root.expand_all()
        yield impl_tree
