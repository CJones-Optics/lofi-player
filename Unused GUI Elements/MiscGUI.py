from textual.app import App, ComposeResult
from textual.containers import Container
from textual.containers import ScrollableContainer
from textual.widgets import Button, Input, Static
from textual.widgets import Label, ListItem, ListView
from textual.widgets import  Footer, Header
from textual.widgets import Log
from textual.reactive import reactive



class ButtonDock(Container):
    # CSS_PATH = "buttonDock.tcss"
   CSS ="""

    Button {
        width: 5%;
    }
    ButtonDock {
        layout: horizontal;
        height: 5;
        margin: 1;
        min-width: 50;
        padding: 1;
    }
    """
    def compose(self) -> ComposeResult:
        yield Button("P", id="play")
        yield Button("S", id="toggle_shuffle")
        yield Button("M", id="mute")
        yield Button("X", id="exit")



class ChanelListView(ListView):
    BINDINGS = [("enter", "select_cursor", "Select"),
                ("up", "cursor_up", "Cursor Up"),
                ("down", "cursor_down", "Cursor Down"),
                ("j", "cursor_up", "Cursor Up"),
                ("k", "cursor_down", "Cursor Down"),
    ]
    def __init__(self, items: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = items
    def compose(self) -> ComposeResult:
        chanelNo = 1
        for item in self.items:
            chanel_id = f"ch{str(chanelNo)}"
            yield ListItem(Label(str(item)),id=chanel_id)
            chanelNo += 1
