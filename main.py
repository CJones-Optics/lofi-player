from fileParser import *
from musicPlayer import MP3Player, player_process
from shell import PlayerShell
import multiprocessing as mp
import cmd
import time
import threading





def main():
    command_queue = mp.Queue()
    message_queue = mp.Queue()
    player_proc = mp.Process(target=player_process, args=(command_queue,message_queue))
    player_proc.start()

    PlayerShell(command_queue,message_queue).cmdloop()

    player_proc.join()
    print("MP3 Player has been shut down.")

if __name__ == '__main__':
    main()
