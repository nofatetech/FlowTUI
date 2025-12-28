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

    
    OPINIONATED_FLOW_ATTRS = [
        "flow:click", "flow:submit", "flow:change",
        "flow:target",
        "flow:before-send", "flow:after-swap",
    ]

    def update_inspector(self, data: dict) -> None:
        self.query("*").remove()
        self.mount(Static("🆔 [b]Identity[/b]"))
        self.mount(Horizontal(
            Static("Tag  :", classes="label"),
            Input(value=data.get("tag", ""), id="inp_tag", classes="prop-input"),
            Button("Edit", id="edit_tag", classes="edit-btn"),
            classes="prop-row"
        ))
        if "id" in data:
            self.mount(Horizontal(
                Static("ID   :", classes="label"),
                Input(value=data.get("id", ""), id="inp_id", classes="prop-input"),
                Button("Edit", id="edit_id", classes="edit-btn"),
                classes="prop-row"
            ))
        if "class" in data:
            self.mount(Static("\n🎨 [b]Styling[/b]"))
            self.mount(Horizontal(
                Static("CSS  :", classes="label"),
                Input(value=data.get("class", ""), id="inp_class", classes="prop-input"),
                Button("Edit", id="edit_class", classes="edit-btn"),
                classes="prop-row"
            ))
        
        self.mount(Static("\n⚡️ [b]Bindings & Hooks[/b]"))
        
        # Display our opinionated list of flow attributes
        for attr in self.OPINIONATED_FLOW_ATTRS:
            current_value = data.get(attr, "")
            self.mount(self.create_code_editor(f"[cyan]{attr}[/]", current_value, attr))

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

        input_id = event.input.id
        if not input_id: return
        
        attr_key = input_id.replace("inp_", "")

        # Update data, removing the attribute if the new value is empty
        if event.value:
            self.element_data[attr_key] = event.value
        elif attr_key in self.element_data:
            del self.element_data[attr_key]

        tag = self.element_data.get("tag", "div")
        attrs_parts = []
        for key, val in self.element_data.items():
            if key not in ["tag", "display", "original_line", "file_path"]:
                # Ensure we only add attributes with non-empty values
                if val:
                    attrs_parts.append(f'{key}="{val}"')
        
        attrs_str = " " + " ".join(sorted(attrs_parts)) if attrs_parts else ""
        
        indentation = " " * (len(self.original_line) - len(self.original_line.lstrip(' ')))
        new_line = f"{indentation}<{tag}{attrs_str}>\n"

        try:
            with open(self.file_path, "r") as f: content = f.read()
            content = content.replace(self.original_line, new_line, 1)
            with open(self.file_path, "w") as f: f.write(content)
            
            self.original_line = new_line
            self.app.log(f"✅ Saved changes to {os.path.basename(self.file_path)}")
            # No need to manually refresh the inspector, it's already showing the new value

        except Exception as e:
            self.app.log(f"❌ [bold red]Error saving file:[/] {e}")

    def create_code_editor(self, label: str, value: str, prop_id: str) -> Horizontal:
        """Creates a row with a label, input, and edit button."""
        safe_id = prop_id.replace(":", "_")
        return Horizontal(
            Static(label, classes="label", shrink=True),
            Input(value=value, id=f"inp_{safe_id}", classes="prop-input"),
            Button("Edit", id=f"edit_{safe_id}", classes="edit-btn"),
            classes="prop-row"
        )
    
    BINDINGS = [
        Binding("ctrl+s", "suspend_process", "Suspend/Resume", show=False),
    ]
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if not self.file_path or not self.original_line:
            self.app.bell()
            return

        try:
            with open(self.file_path, "r") as f:
                lines = f.readlines()
            
            line_number = -1
            for i, line in enumerate(lines):
                # Use strip() for a more robust comparison
                if line.strip() == self.original_line.strip():
                    line_number = i + 1
                    break
            
            if line_number == -1:
                self.app.log(f"Could not find line in file: {self.original_line.strip()}")
                return

            self.app.action_suspend_process()
            subprocess.run(["nvim", f"+{line_number}", self.file_path])
            
            self.app.log("Resumed TUI. Note: Manual refresh may be needed to see changes.")

        except Exception as e:
            self.app.log(f"Error opening editor: {e}")
