import os
import subprocess
import tempfile
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal, VerticalScroll
from textual.widgets import Static, Input, Button
from textual.binding import Binding

# Import the message classes from the other panels
from tui_panels.flow_implementation_content import FlowImplementationContent
from tui_panels.explorer_content import ExplorerContent

class InspectorContent(VerticalScroll):
    """
    A dynamic property editor that receives element data via messages
    and can write changes back to the source file.
    """
    
    def __init__(self) -> None:
        super().__init__()
        # --- HTML Element Context ---
        self.element_data: dict = {}
        self.original_line: str = ""
        # --- Controller Method Context ---
        self.method_data: dict = {}
        # --- Common Context ---
        self.file_path: str = ""
        self.current_context = None # "html" or "method"

    def on_mount(self) -> None:
        """Initially, the inspector is empty."""
        self.mount(Static("⬅️ [i]Select an element to inspect.[/i]", classes="placeholder"))

    # --- Method Inspector ---

    def update_method_inspector(self, data: dict) -> None:
        """Renders the inspector for a controller method."""
        self.query("*").remove()
        
        status, color = ("Implemented", "green") if data['is_implemented'] else ("Not Implemented", "gray")

        self.mount(Static("▶️ [b]Controller Method[/b]"))
        self.mount(Horizontal(Static("Flow :", classes="label"), Static(f"[cyan]{data['flow_name']}[/]"), classes="prop-row"))
        self.mount(Horizontal(Static("Route:", classes="label"), Static(f"[cyan]{data['route_name']}[/]"), classes="prop-row"))
        self.mount(Horizontal(Static("Verb :", classes="label"), Static(f"[cyan]{data['verb'].upper()}[/]"), classes="prop-row"))
        self.mount(Horizontal(Static("Status:", classes="label"), Static(f"[{color}]{status}[/{color}]"), classes="prop-row"))
        
        self.mount(Static("\n[b]Actions[/b]"))
        self.mount(Button("Edit in Neovim", id="edit_method", variant="primary", classes="edit-btn"))

    # --- HTML Inspector ---
    
    OPINIONATED_FLOW_ATTRS = [
        # Core Triggers
        "flow:click", "flow:submit", "flow:change",
        # Real-time & Polling
        "flow:trigger", "flow:poll",
        # UX & Polish
        "flow:loading-class", "flow:transition", "flow:push-url",
        # Advanced Control Flow
        "flow:on-success",
        # Core Logic
        "flow:target",
        # JS Hooks
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
        
        for attr in self.OPINIONATED_FLOW_ATTRS:
            current_value = data.get(attr, "")
            self.mount(self.create_code_editor(f"[cyan]{attr}[/]", current_value, attr))

    # --- Message Handlers & Event Logic ---

    def on_flow_implementation_content_element_selected(self, message: FlowImplementationContent.ElementSelected) -> None:
        """Receives the message and stores the context, then updates the UI."""
        self.current_context = "html"
        self.element_data = message.element_data
        self.file_path = message.file_path
        self.original_line = message.original_line
        self.update_inspector(self.element_data)
        
    def on_flow_implementation_content_method_selected(self, message: FlowImplementationContent.MethodSelected) -> None:
        """Receives message from implementation panel and updates inspector for a method."""
        self.current_context = "method"
        self.method_data = message.__dict__
        self.file_path = message.file_path
        self.update_method_inspector(self.method_data)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if self.current_context != "html" or not self.file_path or not self.original_line:
            return

        input_id = event.input.id
        if not input_id: return
        
        attr_key = input_id.replace("inp_", "").replace("_", ":")

        if event.value:
            self.element_data[attr_key] = event.value
        elif attr_key in self.element_data:
            del self.element_data[attr_key]

        tag = self.element_data.get("tag", "div")
        attrs_parts = []
        for key, val in self.element_data.items():
            if key not in ["tag", "display", "original_line", "file_path"]:
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

        except Exception as e:
            self.app.log(f"❌ [bold red]Error saving file:[/] {e}")

    def create_code_editor(self, label: str, value: str, prop_id: str) -> Horizontal:
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

    def _find_method_line_number(self, content: str, route_name: str, verb: str) -> int:
        """Finds the line number for a method using our naming convention."""
        # First, try the full routeName_verb convention
        method_name = f"{route_name.lower()}_{verb.lower()}"
        match = re.search(fr"^\s*def\s+{method_name}\s*\(", content, re.MULTILINE)
        if match:
            return content.count('\n', 0, match.start()) + 1

        # Second, try the special case where GET is just the route name
        if verb.lower() == 'get':
            method_name = route_name.lower()
            match = re.search(fr"^\s*def\s+{method_name}\s*\(", content, re.MULTILINE)
            if match:
                return content.count('\n', 0, match.start()) + 1
        
        return -1 # Not found

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if not self.file_path:
            self.app.bell()
            return

        line_number = -1
        try:
            with open(self.file_path, "r") as f:
                content = f.read()
                lines = content.splitlines()

            if self.current_context == "html":
                for i, line in enumerate(lines):
                    if line.strip() == self.original_line.strip():
                        line_number = i + 1
                        break
            
            elif self.current_context == "method":
                if self.method_data.get('is_implemented'):
                    line_number = self._find_method_line_number(content, self.method_data['route_name'], self.method_data['verb'])
                else:
                    # If not implemented, find the line of the class definition and go there
                    match = re.search(r"^\s*class \w+:", content, re.MULTILINE)
                    if match:
                        line_number = content.count('\n', 0, match.end()) + 1
                    else: # Fallback to end of file
                        line_number = len(lines)
            
            if line_number == -1:
                self.app.log("Could not find target line in file.")
                return

            self.app.action_suspend_process()
            subprocess.run(["nvim", f"+{line_number}", self.file_path])
            self.app.log("Resumed TUI. Note: Manual refresh may be needed to see changes.")

        except Exception as e:
            self.app.log(f"Error opening editor: {e}")

