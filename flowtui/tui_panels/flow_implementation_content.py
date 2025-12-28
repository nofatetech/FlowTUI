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
        Reads an HTML file and extracts simple structural markers.
        Very basic parsing, looks for keywords.
        """
        content_lines = []
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                if "<html>" in content: content_lines.append("<html>")
                if "<main>" in content: content_lines.append("  <main>")
                # Look for mock loops
                if "<!-- 🔄 Loop:" in content:
                    for line in content.splitlines():
                        if "<!-- 🔄 Loop:" in line:
                            loop_desc = line.split("<!-- 🔄 Loop:", 1)[1].split("-->", 1)[0].strip()
                            content_lines.append(f"    🔄 Loop: [i]{loop_desc}[/]")
                if "{% block content %}" in content: content_lines.append("  {% block content %}")

        except Exception:
            return ["⚠️ [red]Read Error[/]"]
        return content_lines

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
