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
    A dynamic property editor that receives element data via messages
    and can write changes back to the source file.
    """
    
    def __init__(self) -> None:
        super().__init__()
        # Add instance variables to store the context of the selected element
        self.element_data: dict = {}
        self.file_path: str = ""
        self.original_line: str = ""

    def on_mount(self) -> None:
        """Initially, the inspector is empty."""
        self.mount(Static("⬅️ [i]Select an HTML element to inspect.[/i]", classes="placeholder"))

    def update_inspector(self, data: dict) -> None:
        self.query("*").remove()
        self.mount(Static("🆔 [b]Identity[/b]"))
        self.mount(Horizontal(
            Static("Tag  :", classes="label"),
            Input(value=data.get("tag", ""), id="inp_tag", classes="prop-input"),
            classes="prop-row"
        ))
        if "id" in data:
            self.mount(Horizontal(
                Static("ID   :", classes="label"),
                Input(value=data.get("id", ""), id="inp_id", classes="prop-input"),
                classes="prop-row"
            ))
        if "class" in data:
            self.mount(Static("\n🎨 [b]Styling[/b]"))
            self.mount(Horizontal(
                Static("CSS  :", classes="label"),
                Input(value=data.get("class", ""), id="inp_class", classes="prop-input"),
                classes="prop-row"
            ))
        
        self.mount(Static("\n⚡️ [b]Bindings & Hooks[/b]"))
        flow_attrs = {k: v for k, v in data.items() if k.startswith("flow:")}
        if flow_attrs:
            for key, value in flow_attrs.items():
                self.mount(self.create_code_editor(f"[cyan]{key}[/]", value, key))
        else:
            self.mount(Static("  [gray]No flow bindings found.[/]"))

    def on_flow_implementation_content_element_selected(self, message: FlowImplementationContent.ElementSelected) -> None:
        """Receives the message and stores the context, then updates the UI."""
        self.element_data = message.element_data
        self.file_path = message.file_path
        self.original_line = message.original_line
        self.update_inspector(self.element_data)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handles the user pressing Enter in an input field to save changes."""
        if not self.file_path or not self.original_line:
            return

        # 1. Update our in-memory data with the new value from the input
        input_id = event.input.id
        attr_key = input_id.replace("inp_", "") # e.g., "inp_id" -> "id"
        self.element_data[attr_key] = event.value

        # 2. Reconstruct the new HTML line from the (potentially updated) data
        tag = self.element_data.get("tag", "div")
        attrs_parts = []
        for key, val in self.element_data.items():
            if key not in ["tag", "display", "original_line", "file_path"]:
                attrs_parts.append(f'{key}="{val}"')
        
        # Preserve original indentation
        indentation = " " * (len(self.original_line) - len(self.original_line.lstrip(' ')))
        new_line = f"{indentation}<{tag} {' '.join(attrs_parts)}>\n"

        # 3. Read, replace, and write the file
        try:
            with open(self.file_path, "r") as f:
                content = f.read()
            
            content = content.replace(self.original_line, new_line)

            with open(self.file_path, "w") as f:
                f.write(content)
            
            # 4. Update the original_line so we can make subsequent edits
            self.original_line = new_line
            self.app.log(f"✅ Saved changes to {os.path.basename(self.file_path)}")

        except Exception as e:
            self.app.log(f"❌ [bold red]Error saving file:[/] {e}")

    # (create_code_editor and on_button_pressed remain for future use)
    def create_code_editor(self, label: str, value: str, prop_id: str) -> Horizontal:
        display_value = value.replace('\n', ' ↵ ').strip()
        return Horizontal(
            Static(label, classes="label", shrink=True),
            Static(f"[i gray50]{display_value or '...'}[/]", classes="code-preview"),
            Button("Edit", id=f"edit_{prop_id}", classes="edit-btn"),
            classes="prop-row"
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.bell()
        self.app.log(f"Editing for code blocks is not yet implemented for saving.")
