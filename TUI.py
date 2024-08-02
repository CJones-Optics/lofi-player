from textual.app import App, ComposeResult
from textual.widgets import Button, Footer, Header
from textual.containers import Container
import subprocess

class AudioPlayerApp(App):
    CSS = """
    Button {
        width: 20;
    }

    #controls {
        layout: horizontal;
        content-align: center middle;
        height: 5;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Container(
            Button("Play", id="play"),
            Button("Pause", id="pause"),
            Button("Stop", id="stop"),
            id="controls"
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "play":
            subprocess.run(["shell_command", "play"])
        elif event.button.id == "pause":
            subprocess.run(["shell_command", "pause"])
        elif event.button.id == "stop":
            subprocess.run(["shell_command", "stop"])

    def on_key(self, event):
        if event.key == "q":
            self.exit()

if __name__ == "__main__":
    app = AudioPlayerApp()
    app.run()
