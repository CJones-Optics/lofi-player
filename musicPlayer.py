import pygame
import time
import threading
from fileParser import *
import logging

# TO-DO: Standardise the messages

class MP3Player:
    def __init__(self):

        # Set up logging configuration to append to the existing log file
        logging.basicConfig(filename='lofiRadio.log',     # Log file name
                            level=logging.DEBUG,        # Log level
                            filemode='a',               # 'a' mode to append to the file if it exists
                            format='%(asctime)s - %(levelname)s - %(message)s')

        pygame.mixer.init()
        self.volume = 1.0
        self.is_playing = False
        self.play_event = threading.Event()
        self.stop_event = threading.Event()

    def play(self, appPlaylist):
        self.is_playing = True
        self.play_event.set()
        self.stop_event.clear()

        # While the play flag is still set, keep playing the next track
        while self.is_playing:
            file_path = appPlaylist.nextTrack()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                # Check every 0.1 seconds if we should stop
                if self.stop_event.wait(0.1):
                    break
        self.stop()

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.play_event.clear()
        self.stop_event.set()

    def pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.play_event.clear()

    def resume(self):
        if not self.is_playing and self.play_event.is_set():
            pygame.mixer.music.unpause()
            self.is_playing = True
            self.play_event.set()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)
        self.volume = volume

    def __del__(self):
        pygame.mixer.quit()

def player_process(command_queue,messages_queue):

    logging.basicConfig(filename='lofiRadio.log',     # Log file name
                        level=logging.DEBUG,        # Log level
                        filemode='a',               # 'a' mode to append to the file if it exists
                        format='%(asctime)s - %(levelname)s - %(message)s')

    sourceDir = "tracks"
    files = fileHandler(sourceDir)
    tracks = files.getTracks()
    logging.info("Tracks have been loaded.")

    appPlaylist = playlist(tracks,shuffle=True,messages_queue=messages_queue)
    logging.info("Playlist has been created.")
    player = MP3Player()
    logging.info("Player has been created.")

    def play_worker(appPlaylist):
        player.play(appPlaylist)

    play_thread = None
    mute = False
    oldVolume = 1

    logging.info("Entering player process loop.")
    while True:
        cmd, *args = command_queue.get()
        if cmd == 'play':
            logging.info("cmd: play")
            if play_thread and play_thread.is_alive():
                player.stop()
                play_thread.join()
            play_thread = threading.Thread(target=play_worker, args=(appPlaylist,))
            play_thread.start()
            messages_queue.put(f"Play>True")

        elif cmd == 'chanel_list':
            logging.info("cmd: chanel_list")
            # print(appPlaylist.chanelList)
            chanels = files.chanelList
            str = "ChanelList>"
            for i in range(len(chanels)):
                str+=(f"{i+1}. {chanels[i]},")
            # Remove the last comma
            str = str[:-1]
            messages_queue.put(str)

        elif cmd == 'chanel':
            logging.info("cmd: chanel")
            chanels = files.chanelList
            newChanel = chanels[int(args[0])-1]
            files.changeChannel(newChanel)
            shuffleState = appPlaylist.shuffle
            appPlaylist = playlist(files.getTracks(),shuffle=shuffleState,messages_queue=messages_queue)
            messages_queue.put(f"Chanel>{newChanel}")
            logging.info(f"msg: Chanel>{newChanel}")

        elif cmd == 'stop':
            logging.info("cmd: stop")
            player.stop()
            if play_thread:
                play_thread.join()
            messages_queue.put("Play>False")
        elif cmd == 'pause':
            logging.info("cmd: pause")
            player.pause()
            messages_queue.put("Play>False")
        elif cmd == 'resume':
            logging.info("cmd: resume")
            player.resume()
            messages_queue.put("Play>True")
        elif cmd == 'shuffle':
            logging.info("cmd: shuffle")
            appPlaylist.shuffle = not appPlaylist.shuffle
            messages_queue.put(f"Shuffle>{'True' if appPlaylist.shuffle else 'False'}")

        elif cmd == 'volume':
            logging.info(f"cmd: volume, args: {args}")
            player.set_volume(float(args[0])**3)
            messages_queue.put(f"Volume>{args[0]}")

        elif cmd == 'mute':
            logging.info("cmd: mute")
            mute = not mute
            if mute:
                oldVolume = player.volume
                player.set_volume(0)
                messages_queue.put("Mute>True")
            else:
                # if it is already muted, unmute it
                player.set_volume(oldVolume)
                messages_queue.put("Mute>False")

        elif cmd == 'exit':
            logging.info("cmd: exit")
            player.stop()
            if play_thread:
                play_thread.join()
            break

# Example usage
# player = MP3Player()
# player.play("path/to/your/mp3file.mp3")
# player.pause()
# player.resume()
# player.set_volume(0.5)
# player.stop()
