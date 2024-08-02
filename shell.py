from fileParser import *
from musicPlayer import MP3Player, player_process
import multiprocessing as mp
import cmd
import time
import threading

class PlayerShell(cmd.Cmd):
    intro = 'Welcome to the MP3 player shell. Type help or ? to list commands.\n'
    prompt = '(player) '

    def __init__(self, command_queue,messages_queue):
        super().__init__()
        self.command_queue = command_queue
        self.messages_queue = messages_queue
        self.should_exit = False
        threading.Thread(target=self.check_messages, daemon=True).start()

    def check_messages(self):
        while not self.should_exit:
            if not self.messages_queue.empty():
                message = self.messages_queue.get()
                print(f"\n{message}")
                print(self.prompt, end='', flush=True)
            time.sleep(0.1)

    def do_play(self, arg):
        'Play an MP3 file: play <filepath>'
        self.command_queue.put(('play', arg))

    def do_stop(self, arg):
        'Stop playing'
        self.command_queue.put(('stop',))

    def do_pause(self, arg):
        'Pause playback'
        self.command_queue.put(('pause',))

    def do_resume(self, arg):
        'Resume playback'
        self.command_queue.put(('resume',))

    def do_chanel_list(self, arg):
        'List all the available chanel'
        self.command_queue.put(('chanel_list',))

    def do_shuffle(self,arg):
        'Toggle shuffle mode'
        self.command_queue.put(('shuffle',))
        # print(f"Shuffle mode: {"On" if appPlaylist.shuffle else "Off"}")

    def do_chanel(self, arg):
        'Change the chanel: chanel <chanel_number>'
        # Check if the chanel number is valid
        try:
            chanel = int(arg)
            if 0 <= chanel <= 2:
                self.do_stop('')
                self.command_queue.put(('chanel', arg))
                self.do_play('')
            else:
                print("Please provide a valid chanel number")
        except ValueError:
            print("Please provide a valid number")

    def do_volume(self, arg):
        'Set volume (0.0 to 1.0): volume <level>'
        try:
            vol = float(arg)
            if 0 <= vol <= 1:
                self.command_queue.put(('volume', arg))
            else:
                print("Volume must be between 0.0 and 1.0")
        except ValueError:
            print("Please provide a valid number")

    def do_mute(self, arg):
        'Mute the volume'
        self.command_queue.put(('mute',))

    def do_exit(self, arg):
        'Exit the program'
        self.command_queue.put(('exit',))
        return True
