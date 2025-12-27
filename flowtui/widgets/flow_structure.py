from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Tree
from .data import MOCK_RESOURCES

class FlowStructure(Vertical):
    def compose(self) -> ComposeResult:
        yield Tree("Select a Flow", classes="panel-body")

    def on_mount(self) -> None:
        self.structure_tree = self.query_one(Tree)

    def show_flow(self, flow_id: str):
        self.structure_tree.clear()
        self.structure_tree.root.label = f"📁 {flow_id}"
        
        resource = MOCK_RESOURCES[flow_id]
        
        # Add nodes for controller, model, etc.
        c_node = self.structure_tree.root.add("▶️ Controller")
        c_node.data = {"type": "code", "content": resource["controller"]}
        
        m_node = self.structure_tree.root.add("📦 Model")
        m_node.data = {"type": "code", "content": resource["model"]}
        
        # Add views with nested HTML tree
        views_node = self.structure_tree.root.add("🖼️ Views")
        for view_name, view_data in resource["views"].items():
            view_file_node = views_node.add(f"📄 {view_name}")
            
            # Recursively add the HTML tree from the view data
            def add_html_nodes(parent, data):
                root_label = data.get("root", "element")
                root_node = parent.add(root_label)
                root_node.data = {"type": "element", "content": data}
                if "children" in data:
                    for child_label, child_data in data["children"].items():
                        add_html_nodes(root_node, {"root": child_label, **child_data})

            add_html_nodes(view_file_node, view_data)
            
        self.structure_tree.root.expand_all()
