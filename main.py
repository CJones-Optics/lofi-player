from fileParser import *
from musicPlayer import MP3Player, player_process
from shell import PlayerShell
import multiprocessing as mp
import cmd
import time
import threading
from TUI import MP3PlayerApp

import logging

tui = True

def main():

    # Set up basic configuration for logging
    logging.basicConfig(filename='lofiRadio.log',  # Log file name
                        level=logging.DEBUG,     # Log level
                        filemode='w',# 'w' mode to overwrite the file if it exists
                        format='%(asctime)s - %(levelname)s - %(message)s')

    command_queue = mp.Queue()
    message_queue = mp.Queue()
    logging.info("Command and message queues have been created.")
    player_proc = mp.Process(target=player_process, args=(command_queue,message_queue))
    player_proc.start()
    logging.info("Player process has been created.")

    if tui:
        logging.info("Starting TUI.")
        app = MP3PlayerApp(command_queue, message_queue)
        app.run()
    else:
        logging.info("Starting shell.")
        PlayerShell(command_queue,message_queue).cmdloop()

    logging.info("Shutting down MP3 Player.")
    player_proc.join()
    logging.info("MP3 Player has been shut down.")

if __name__ == '__main__':
    main()
