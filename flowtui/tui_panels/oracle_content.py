from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll, Horizontal
from textual.widgets import Static, Button, Input, Label

class OracleContent(Static):
    """
    A mock UI for The Oracle panel.
    This demonstrates the chat view with sample conversation and action buttons.
    """

    def compose(self) -> ComposeResult:
        """Create the Oracle's UI."""
        with Vertical(id="oracle-container"):
            # The main chat log area
            with VerticalScroll(id="oracle-log"):
                yield Static(
                    "[b i]Context: products.list.get[/b i]", classes="oracle-context-log"
                )
                yield Static(
                    "Create a new flow to handle product reviews.", classes="user-prompt"
                )
                yield Static(
                    """
[b]ORACLE:[/]
Certainly. I will scaffold a new domain file, `reviews.py`.

It will contain a default `Index` flow with `get` and `post` verbs. The `post` verb will be configured to accept `product_id` and `review_text` from the client.

The corresponding view template will be created at `views/reviews/index.html`.
""",
                    classes="oracle-response",
                )
                yield Horizontal(
                    Button("[Create Domain & Flow]", variant="success"),
                    Button("[Show me the code]", variant="default"),
                    classes="action-buttons",
                )
                yield Static("Now generate the HTML form for this.", classes="user-prompt")
                yield Static(
                    """
[b]ORACLE:[/]
Here is the standard HTML form. It will be wired to the `reviews.index.post` verb and will target the `#review-list` element for updates.
                    """,
                    classes="oracle-response",
                )

            # The input area at the bottom
            with Horizontal(id="oracle-input-bar"):
                yield Label("Context: [b]products.list[/b]", id="oracle-context-label")
                yield Input(placeholder="Ask The Oracle...", id="oracle-input")
