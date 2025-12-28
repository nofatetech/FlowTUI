import os
import subprocess
import tempfile
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal, VerticalScroll
from textual.widgets import Static, Input, Button
from textual.binding import Binding

# Import the message class from the other panel
from tui_panels.flow_implementation_content import FlowImplementationContent

class InspectorContent(VerticalScroll):
    """
    A dynamic and interactive property editor that updates based on
    'ElementSelected' messages.
    """
    
    def on_mount(self) -> None:
        """Initially, the inspector is empty."""
        self.mount(Static("⬅️ [i]Select an element to inspect its properties.[/i]", classes="placeholder"))

    def update_inspector(self, data: dict) -> None:
        """Clears and rebuilds the inspector UI with new data."""
        # Clear the placeholder/previous content
        self.query("*").remove()

        # --- 1. Identity Section ---
        self.mount(Static("🆔 [b]Identity[/b]"))
        self.mount(Horizontal(
            Static("Tag  :", classes="label"),
            Input(value=data.get("tag", ""), classes="prop-input"),
            classes="prop-row"
        ))
        # Only show ID if it exists
        if "id" in data:
            self.mount(Horizontal(
                Static("ID   :", classes="label"),
                Input(value=data.get("id", ""), classes="prop-input"),
                classes="prop-row"
            ))

        # --- 2. Styling Section ---
        if "class" in data:
            self.mount(Static("\n🎨 [b]Styling[/b]"))
            self.mount(Horizontal(
                Static("CSS  :", classes="label"),
                Input(value=data.get("class", ""), classes="prop-input"),
                classes="prop-row"
            ))
        
        # --- 3. Bindings & Hooks (Code) Section ---
        self.mount(Static("\n⚡️ [b]Bindings & Hooks[/b]"))
        
        # Find all flow:* attributes and create editors for them
        flow_attrs = {k: v for k, v in data.items() if k.startswith("flow:")}
        if flow_attrs:
            for key, value in flow_attrs.items():
                self.mount(self.create_code_editor(
                    label=f"[cyan]{key}[/]",
                    value=value,
                    prop_id=key
                ))
        else:
            self.mount(Static("  [gray]No flow bindings found.[/]"))

    def create_code_editor(self, label: str, value: str, prop_id: str) -> Horizontal:
        """Helper to create a row for a code property."""
        display_value = value.replace('\n', ' ↵ ').strip()
        return Horizontal(
            Static(label, classes="label", shrink=True),
            Static(f"[i gray50]{display_value or '...'}[/]", classes="code-preview"),
            Button("Edit", id=f"edit_{prop_id}", classes="edit-btn"),
            classes="prop-row"
        )
    
    def on_flow_implementation_content_element_selected(self, message: FlowImplementationContent.ElementSelected) -> None:
        """
        3. This handler receives the message and triggers the UI update.
        Textual automatically maps the message class name to this handler method name.
        """
        self.update_inspector(message.element_data)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle clicks on our 'Edit' buttons (remains the same)."""
        # This functionality can be expanded later to save back to the file.
        # For now, it just works in-memory.
        prop_id = event.button.id.replace("edit_", "")
        
        # For now, we don't have a central state to update, so we'll just log it.
        self.app.bell()
        self.app.log(f"Editing for '{prop_id}' would open here.")
