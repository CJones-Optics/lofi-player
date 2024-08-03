from numpy.random.mtrand import shuffle
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.containers import ScrollableContainer
from textual.widgets import Button, Input, Static
from textual.widgets import Label, ListItem, ListView
from textual.widgets import  Footer, Header
from textual.reactive import reactive
from queue import Queue
import threading
import time




class ChanelListView(ListView):
    def __init__(self, items: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = items
    def compose(self) -> ComposeResult:
        for item in self.items:
            yield ListItem(str(item))


class MP3PlayerApp(App):

    # Keybindings
    BINDINGS = [("q", "do_exit", "quit"),
                ("p", "do_play", "play"),
                ("s", "do_shuffle", "shuffle"),
                ("m", "do_mute", "mute"),
                ("h", "do_volume_down", "volume down"),
                ("l", "do_volume_up", "volume up"),
    ]
    def action_do_exit(self) -> None:
        self.do_exit()
    def action_do_mute(self) -> None:
        self.do_mute()
    def action_do_play(self) -> None:
        self.do_play()
    def action_do_shuffle(self) -> None:
        self.do_toggle_shuffle()
    def action_do_volume_down(self) -> None:
        current_volume = self.current_volume
        current_volume -= 0.1
        if current_volume < 0:
            current_volume = 0
        self.current_volume = current_volume
        self.do_volume(self.current_volume)
    def action_do_volume_up(self) -> None:
        current_volume = self.current_volume
        current_volume += 0.1
        if current_volume > 1:
            current_volume = 1
        self.current_volume = current_volume
        self.do_volume(self.current_volume)

    catagory        = reactive("")
    value           = reactive("")
    track           = reactive("")
    mute            = reactive(False)
    muteStatus      = reactive(False)
    shuffleStatus   = reactive(False)
    shuffle_mode    = reactive(False)
    current_volume  = reactive(0.5)
    channel_list    = reactive([])
    current_channel = reactive(0)
    current_status  = reactive("Stopped")

    def do_chanel_list(self):
        self.command_queue.put(('chanel_list',))
        time.sleep(0.2)
        if not self.messages_queue.empty():
            message = self.messages_queue.get()
            category, value = message.split(">")
        if  category == "ChanelList":
            self.channel_list = value.split(",")
        else:
            self.channel_list = ["Error"]

    def __init__(self, command_queue: Queue, messages_queue: Queue):
        super().__init__()
        self.command_queue = command_queue
        self.messages_queue = messages_queue
        self.should_exit = False
        self.do_chanel_list()



    def on_mount(self) -> None:
        self.check_messages_thread = threading.Thread(target=self.check_messages, daemon=True)
        self.check_messages_thread.start()


    def check_messages(self):
        while not self.should_exit:
            if not self.messages_queue.empty():
                message = self.messages_queue.get()
                self.update_message(message)
            time.sleep(0.1)

    def update_message(self, message: str):
        # self.query_one("#messages").update(f"Messages: {message}")
        catagoryDict = {
            "Play":      "#status",
            "Volume":    "#volume",
            "Chanel":    "#channel",
            "Shuffle":   "#shuffleStatus",
            "Mute":      "#muteStatus",
            "Playlist":  "#track",
            "ChanelList":"#channel_list"
        }
        catagory, value = message.split(">")
        self.query_one("#catagory").update(f"Catagory: {catagory}")
        self.query_one("#value").update(f"Value: {value}")

        floatVars = ["Volume"]
        boolVars = ["Shuffle", "Mute","Play"]
        stringVars = ["Playlist","ChanelList","Chanel"]
        if catagory in boolVars:
            box = catagoryDict[catagory]
            status = 'On' if (str(True)==value) else 'Off'
            self.query_one(box).update(f"{catagory}: {status}")
        elif catagory in stringVars:
            box = catagoryDict[catagory]
            self.query_one(box).update(f"{catagory}: {value}")
        elif catagory in floatVars:
            box = catagoryDict[catagory]
            self.query_one(box).update(f"{catagory}: {float(value):.1f}")
        return

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with ScrollableContainer(id="player"):
            yield Static(f"Catagory: {self.catagory}", id="catagory")
            yield Static(f"Value: {self.value}", id="value")
            yield Static(f"Track: {self.track}", id="track")
            # yield ChanelListView(self.channel_list, id="channel_list")
            yield Static(f"Status: {self.current_status}", id="status")
            yield Static(f"Muted: {self.muteStatus}", id="muteStatus")
            yield Static(f"Volume: {self.current_volume:.1f}", id="volume")
            yield Static(f"Channel: {self.current_channel}", id="channel")
            yield Static(f"Shuffle: {'On' if self.shuffle_mode else 'Off'}", id="shuffleStatus")

            yield Button("Play", id="play")
            yield Button("Stop", id="stop")
            yield Button("Shuffle", id="toggle_shuffle")

            yield Input(placeholder="Enter channel number (0-2)", id="channel_input")
            yield Button("Change Channel", id="change_channel")

            yield Input(placeholder="Enter volume (0.0-1.0)", id="volume_input")
            yield Button("Set Volume", id="set_volume")

            yield Button("Mute", id="mute")
            yield Button("Exit", id="exit")

    def do_exit(self):
        self.command_queue.put(('exit',))
        self.should_exit = True
        self.exit()

    def do_mute(self):
        self.command_queue.put(('mute',))
    def do_toggle_shuffle(self):
        self.command_queue.put(('shuffle',))
    def do_play(self):
        self.command_queue.put(('play',))
    def do_stop(self):
        self.command_queue.put(('stop',))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "play":
           self.do_play()
        elif button_id == "stop":
            self.do_stop()
        elif button_id == "toggle_shuffle":
            self.do_toggle_shuffle()

        elif button_id == "change_channel":
            channel = self.query_one("#channel_input").value
            try:
                channel = int(channel)
                if 0 <= channel <= 2:
                    self.command_queue.put(('stop',))
                    self.command_queue.put(('chanel', str(channel)))
                    self.command_queue.put(('play',))
                    self.current_channel = channel
                else:
                    self.update_message("Please provide a valid channel number (0-2)")
            except ValueError:
                self.update_message("Please provide a valid number")

        elif button_id == "set_volume":
            volume = self.query_one("#volume_input").value
            self.do_volume(volume)

        elif button_id == "mute":
            self.do_mute()

        elif button_id == "exit":
            self.do_exit()

    def do_volume(self, volume: float):
        try:
            volume = float(volume)
            if 0 <= volume <= 1:
                self.command_queue.put(('volume', str(volume)))
                self.current_volume = volume
            else:
                self.update_message("Volume must be between 0.0 and 1.0")
        except ValueError:
            self.update_message("Please provide a valid number")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "channel_input":
            self.query_one("#change_channel").press()
        elif event.input.id == "volume_input":
            self.query_one("#set_volume").press()
