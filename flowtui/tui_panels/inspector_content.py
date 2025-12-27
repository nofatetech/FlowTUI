import os
import subprocess
import tempfile
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal, VerticalScroll
from textual.widgets import Static, Input, Button
from textual.binding import Binding


class InspectorContent(VerticalScroll):
    """
    A dynamic and interactive property editor for the selected element.
    """
    
    # This is our mock data model representing the "selected" element.
    # In a real app, this would be passed in or updated via a message.
    MOCK_DATA = {
        "id": "add_item_button",
        "tag": "button",
        "css_classes": "btn primary",
        "binding": "flow:click='products.add_item'",
        "hook_before_send": "this.disabled = true;\n$flow('.spinner').show();",
        "hook_after_swap": "this.disabled = false;\n$flow('.spinner').hide();",
    }

    def compose(self) -> ComposeResult:
        """Create the child widgets for the inspector."""
        
        # --- 1. Identity Section ---
        yield Static("🆔 [b]Identity[/b]")
        yield Horizontal(
            Static("Tag  :", classes="label"),
            Input(value=self.MOCK_DATA["tag"], id="inp_tag", classes="prop-input"),
            classes="prop-row"
        )
        yield Horizontal(
            Static("ID   :", classes="label"),
            Input(value=self.MOCK_DATA["id"], id="inp_id", classes="prop-input"),
            classes="prop-row"
        )

        # --- 2. Styling Section ---
        yield Static("\n🎨 [b]Styling[/b]")
        yield Horizontal(
            Static("CSS  :", classes="label"),
            Input(value=self.MOCK_DATA["css_classes"], id="inp_css", classes="prop-input"),
            classes="prop-row"
        )
        
        # --- 3. Bindings & Hooks (Code) Section ---
        yield Static("\n⚡️ [b]Bindings & Hooks[/b]")
        yield self.create_code_editor(
            label="Bind :",
            value=self.MOCK_DATA["binding"],
            prop_id="binding"
        )
        yield self.create_code_editor(
            label="Hook : [cyan]before-send[/]",
            value=self.MOCK_DATA["hook_before_send"],
            prop_id="hook_before_send"
        )
        yield self.create_code_editor(
            label="Hook : [cyan]after-swap[/]",
            value=self.MOCK_DATA["hook_after_swap"],
            prop_id="hook_after_swap"
        )

    def create_code_editor(self, label: str, value: str, prop_id: str) -> Horizontal:
        """Helper to create a row for a code property."""
        # Display a truncated, single-line version of the code.
        display_value = value.replace('\n', ' ↵ ').strip()
        
        return Horizontal(
            Static(label, classes="label"),
            Static(f"[i gray50]{display_value or '...'}[/]", classes="code-preview"),
            Button("Edit", id=f"edit_{prop_id}", classes="edit-btn"),
            classes="prop-row"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle clicks on our 'Edit' buttons."""
        prop_id = event.button.id.replace("edit_", "")
        
        # 1. Get the current code from our data model
        current_code = self.MOCK_DATA.get(prop_id, "")
        
        # 2. Use a temporary file to pass the code to the editor
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode='w+') as tf:
            tf.write(current_code)
            temp_filename = tf.name

        # 3. Open the file in a terminal editor (e.g., nvim, nano, vim)
        # We suspend the Textual UI to give control to the editor.
        editor = os.environ.get("EDITOR", "nvim") # Default to nvim
        with self.app.suspend():
            subprocess.run([editor, temp_filename])

        # 4. After the editor is closed, read the new content
        with open(temp_filename, "r") as tf:
            new_code = tf.read()
        os.remove(temp_filename) # Clean up the temp file

        # 5. Update our data model and the UI
        self.MOCK_DATA[prop_id] = new_code
        
        # In a real app, you'd send a message to refresh this component.
        # For this mock, we'll just find the preview and update it directly.
        preview = self.query_one(f"#{event.button.id}").parent.query_one(".code-preview")
        display_value = new_code.replace('\n', ' ↵ ').strip()
        preview.update(f"[i gray50]{display_value or '...'}[/]")
