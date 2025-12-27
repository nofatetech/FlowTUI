from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Tree

class ExplorerContent(Vertical):
    def compose(self) -> ComposeResult:
        flows_tree = Tree("📦 Domains")
        flows_tree.root.expand()
        billing = flows_tree.root.add("💳 Billing")
        billing.add("🧾 Invoices (/invoices)")
        catalog = flows_tree.root.add("📚 Catalog")
        catalog.add("👕 Products (/products)")
        yield flows_tree
        
        models_tree = Tree("📦 Models")
        models_tree.root.expand()
        billing_m = models_tree.root.add("💳 Billing")
        billing_m.add("📄 Invoice")
        shared = models_tree.root.add("👤 Shared")
        shared.add("📄 User")
        yield models_tree
