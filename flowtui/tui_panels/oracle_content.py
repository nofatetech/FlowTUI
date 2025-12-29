from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll, Horizontal
from textual.widgets import Static, Button, Input, Label, ListView, ListItem

class OracleContent(Static):
    """
    A mock UI for The Oracle panel, demonstrating a command-driven workflow.
    """

    def compose(self) -> ComposeResult:
        """Create the Oracle's UI."""
        with Vertical(id="oracle-container"):
            # The main chat log area
            with VerticalScroll(id="oracle-log"):
                yield Static(
                    "Create a new flow to handle product reviews.", classes="user-prompt"
                )
                yield Static(
                    """
[b]ORACLE:[/] I will execute the following command:
[b cyan]/create domain reviews flow:index verb:get verb:post[/b cyan]

This will create `reviews/index.py` with an `IndexFlow` class.
Do you want to proceed?

  1. [Execute]
  2. [Cancel]
""",
                    classes="oracle-response",
                )
                yield Static("1", classes="user-prompt-action")
                yield Static(
                    """
[b]ORACLE:[/] Command executed.
Now, what is the next command?
""",
                    classes="oracle-response",
                )

            # The list of chats
            with Vertical(id="oracle-chat-list-container"):
                yield Label("[b]Chat History[/b]")
                with VerticalScroll():
                    yield ListView(
                        ListItem(Label("Chat 1: Product Reviews"), id="active-chat"),
                        ListItem(Label("Chat 2: User Auth")),
                        ListItem(Label("Chat 3: Refactoring DB")),
                    )
                yield Button("[+] New Chat", variant="default", id="new-chat-btn")

            # The input area at the bottom
            with Horizontal(id="oracle-input-bar"):
                yield Input(
                    placeholder="Ask a question or type a /command...", id="oracle-input"
                )