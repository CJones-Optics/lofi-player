from numpy.random.mtrand import shuffle
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.containers import ScrollableContainer
from textual.widgets import Button, Input, Static
from textual.widgets import Label, ListItem, ListView
from textual.widgets import  Footer, Header
from textual.widgets import Log
from textual.reactive import reactive
from queue import Queue
import threading
import time
import logging

DEBUG = False
LOG = False


logging.basicConfig(filename='lofiRadio.log',     # Log file name
                    level=logging.DEBUG,        # Log level
                    filemode='a',               # 'a' mode to append to the file if it exists
                    format='%(asctime)s - %(levelname)s - %(message)s')



def render_bool(label: str, value: bool) -> str:
    true_icon = "■"
    false_icon = "□"
    return f"{true_icon if value else false_icon} - {label}"

class VolumeBar(Static):
    """A widget to represent a volume bar."""
    value = reactive(1)
    def compose(self) -> ComposeResult:
        yield Static(self.render_Vbar(self.value), id="VbarInner")
    def on_mount(self):
        self.update_Vbar()
    def render_Vbar(self,V) -> str:
        filled = int(V*10)
        empty = 10 - filled
        return f"Volume: [ {filled * '■'}{empty * '□'} ] {round(self.value*100)}%"
    def update_Vbar(self):
        self.query_one("#VbarInner").update(self.render_Vbar(self.value))

class MP3PlayerApp(App):
    CSS_PATH = "style.tcss"
    # Keybindings
    BINDINGS = [("q", "do_exit",        "quit"),
                ("p", "do_play",        "play"),
                ("s", "do_shuffle",     "shuffle"),
                ("m", "do_mute",        "mute"),
                ("h", "do_volume_down", "volume ↓"),
                ("j", "do_chanel_up",   "chanel ↑" ),
                ("k", "do_chanel_down", "chanel ↓"),
                ("l", "do_volume_up",   "volume ↑"),
    ]
    def action_do_exit(self) -> None:
        self.do_exit()
    def action_do_mute(self) -> None:
        self.do_mute()
    def action_do_play(self) -> None:
        self.do_toggle_play()
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
    def action_do_chanel_up(self) -> None:
        current_channel = self.current_channel
        current_channel += 1
        if current_channel > self.nChannels:
            current_channel = self.nChannels
        self.current_channel = current_channel
        self.do_chanel(str(self.current_channel))
    def action_do_chanel_down(self) -> None:
        current_channel = self.current_channel
        current_channel -= 1
        if current_channel < 1:
            current_channel = 1
        self.current_channel = current_channel
        self.do_chanel(str(self.current_channel))

    if DEBUG:
        catagory        = reactive("")
        value           = reactive("")
    track           = reactive("")
    mute            = reactive(False)
    muteStatus      = reactive(False)
    shuffleStatus   = reactive(True)
    shuffle_mode    = reactive(True)
    current_volume  = reactive(1.0)
    channel_list    = reactive([])
    current_channel = reactive(1)
    current_status  = reactive(False)
    status          = reactive(False)
    if LOG:
        logData = reactive("")

    def __init__(self, command_queue: Queue, messages_queue: Queue):
        super().__init__()
        self.command_queue = command_queue
        self.messages_queue = messages_queue
        self.should_exit = False
        # Saves the chanel list to the class
        self.do_chanel_list()
        self.nChannels = len(self.channel_list)
        # Set the chanel to Chanel 1.
        self.do_chanel(str(self.current_channel))
        # # toggle the shuffle twice to update the ui
        self.do_toggle_shuffle()
        self.do_toggle_shuffle()
        self.do_mute()
        self.do_mute()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with ScrollableContainer(id="player"):
            if DEBUG:
                yield Static(f"Catagory: {self.catagory}", id="catagory")
                yield Static(f"Value: {self.value}", id="value")
            # yield ChanelListView(self.channel_list)
            yield Static(f"Track: {self.track}", id="track")
            yield Static(f"Channel: {self.current_channel}", id="channel")
            yield Static(render_bool("Status",False), id="status")
            yield Static(render_bool("Mute",False), id="muteStatus")
            # yield TextCheckbox(id="Mute")
            # yield Static(f"Volume: {self.current_volume:.1f}", id="volume")
            yield Static(render_bool("Shuffle",True), id="shuffleStatus")
            # yield TextCheckbox(id="Shuffle")
            yield VolumeBar(id="VbarWidget")

            if LOG:
                yield Log()
            # yield ButtonDock()

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
        catagoryDict = {
            "Play":       "#status",
            "Volume":     "#volume",
            "Chanel":     "#channel",
            "Shuffle":    "#shuffleStatus",
            "Mute":       "#muteStatus",
            "Playlist":   "#track",
            "ChanelList": "#channel_list"
        }
        try:
            catagory, value = message.split(">")
        except:
            catagory = "err"
            value = "err"
        if DEBUG:
            self.query_one('#catagory').update(f"Category: {catagory}")
            self.query_one('#value').update(f"Value: {value}")
        if LOG:
            self.logData = f"{catagory}: {value}"
            log = self.query_one(Log)
            log.write_line(self.logData)

        floatVars = []
        boolVars = ["Shuffle", "Mute","Play"]
        # boolVars = ["Shuffle","Play"]
        stringVars = ["Playlist","ChanelList","Chanel"]

        if catagory in boolVars:
            box = catagoryDict[catagory]
            status = (str(True)==value)#'On' if (str(True)==value) else 'Off'
            self.query_one(box).update(render_bool(catagory,status))
        elif catagory in stringVars:
            box = catagoryDict[catagory]
            if catagory == "Playlist":
                catagory = "Track"
            self.query_one(box).update(f"{catagory}: {value}")
        elif catagory in floatVars:
            box = catagoryDict[catagory]
            self.query_one(box).update(f"{catagory}: {float(value):.1f}")
        return

    def do_exit(self):
        self.command_queue.put(('exit',))
        self.should_exit = True
        self.exit()
    def do_mute(self):
        self.command_queue.put(('mute',))
        # self.muteStatus = not self.muteStatus
        # muteBox = self.query_one('#Mute')
        # muteBox.value = self.muteStatus
        # muteBox.update_Cbox()

    def do_toggle_shuffle(self):
        self.command_queue.put(('shuffle',))
        # shuffleStatus = not self.shuffleStatus
        # shuffleBox = self.query_one('#Shuffle')
        # shuffleBox.value = self.shuffleStatus
        # shuffleBox.update_Cbox()
    def do_toggle_play(self):
        self.status = not self.status
        if self.status:
            self.do_play()
        else:
            self.do_stop()
    def do_play(self):
        self.command_queue.put(('play',))
    def do_stop(self):
        self.command_queue.put(('stop',))
    def do_chanel(self,chanel):
        try:
            chanel = int(chanel)
            if 1 <= chanel <= self.nChannels:
                self.command_queue.put(('stop',))
                self.command_queue.put(('chanel', str(chanel)))
                self.command_queue.put(('play',))
                self.current_channel = chanel
            else:
                self.update_message("Please provide a valid channel number (0-2)")
        except ValueError:
            self.update_message("Please provide a valid number")
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
    def do_volume(self, volume: float):
        try:
            volume = float(volume)
            if 0 <= volume <= 1:
                self.command_queue.put(('volume', str(volume)))
                self.current_volume = volume
                vbar = self.query_one("#VbarWidget")
                vbar.value = volume
                vbar.update_Vbar()
            else:
                self.update_message("Volume must be between 0.0 and 1.0")
        except ValueError:
            self.update_message("Please provide a valid number")

    # def on_button_pressed(self, event: Button.Pressed) -> None:
    #     button_id = event.button.id
    #     if button_id == "play":
    #         self.do_toggle_play()
    #     elif button_id == "toggle_shuffle":
    #         self.do_toggle_shuffle()
    #     elif button_id == "mute":
    #         self.do_mute()
    #     elif button_id == "exit":
    #         self.do_exit()

    # def on_list_view_selected(self,event:ChanelListView.Selected):
    #     self.current_channel = event.item.id
    #     # self.messages_queue.put(f"ChanelView>{self.current_channel}")
    #     chanel_index = int(self.current_channel[2:A])
    #     self.messages_queue.put(f"ChanelView>{chanel_index}")
    #     self.do_chanel(chanel_index)
