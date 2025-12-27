from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Tree

class FlowImplementationContent(Vertical):
    def compose(self) -> ComposeResult:
        impl_tree = Tree("📁 catalog.products")
        impl_tree.root.expand()
        layouts = impl_tree.root.add("🎨 Layouts")
        layouts.add("📄 layout.html ([i]Pico.css[/])")
        controllers = impl_tree.root.add("▶️ Controllers")
        controllers.add("📄 index")
        views = impl_tree.root.add("🖼️ Views")
        index_html = views.add("📄 index.html")
        page = index_html.add("<html>")
        main = page.add("<main>")
        loop = main.add("🔄 Loop: [i]for product in products[/]")
        loop.add("↪️ Subview: [b]show.html[/]")

        # --- BLENDER SCENE VIEW (Concept) ---
        blender_scene = views.add("🧊 [b]Blender Scene[/] (main.py)")
        scene_root = blender_scene.add("📂 Collections")
        scene_root.add("🖼️ UI Elements (Objects)")
        scene_root.add("💡 Lights & 🎥 Cameras")
        scene_root.add("⚡️ Bindings (scene.add_item)")

        contracts = impl_tree.root.add("📜 Contracts")
        contracts.add("📄 ProductSchema")
        impl_tree.root.expand_all()
        yield impl_tree
