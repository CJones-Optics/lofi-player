from fileParser import *
from musicPlayer import MP3Player, player_process
from shell import PlayerShell
import multiprocessing as mp
import cmd
import time
import threading

from TUI import MP3PlayerApp


tui = True

def main():
    command_queue = mp.Queue()
    message_queue = mp.Queue()
    player_proc = mp.Process(target=player_process, args=(command_queue,message_queue))
    player_proc.start()

    if tui:
        app = MP3PlayerApp(command_queue, message_queue)
        app.run()

    else:
        PlayerShell(command_queue,message_queue).cmdloop()

    player_proc.join()
    print("MP3 Player has been shut down.")

if __name__ == '__main__':
    main()
