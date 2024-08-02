from fileParser import *
from musicPlayer import *
import multiprocessing as mp
import cmd
import time

def player_process(command_queue):
    sourceDir = "tracks"
    files = fileHandler(sourceDir)
    tracks = files.getTracks()

    appPlaylist = playlist(tracks,shuffle=False)
    player = MP3Player()
    def play_worker(appPlaylist):
        player.play(appPlaylist)

    play_thread = None

    # TO_DO: Pass the playlist into the player object. Then inside the play loop,
    # call appPlaylist.nextTrack() to get the next track to play.
    while True:
        cmd, *args = command_queue.get()
        if cmd == 'play':
            if play_thread and play_thread.is_alive():
                player.stop()
                play_thread.join()
            play_thread = threading.Thread(target=play_worker, args=(appPlaylist,))
            play_thread.start()

        elif cmd == 'chanel_list':
            # print(appPlaylist.chanelList)
            print(f"Placeholders for chanel list")
            chanels = files.chanelList
            for i in range(len(chanels)):
                print(f"{i+1}. {chanels[i]}")

        elif cmd == 'chanel':
            chanels = files.chanelList
            newChanel = chanels[int(args[0])-1]
            files.changeChannel(newChanel)
            appPlaylist = playlist(files.getTracks())


        elif cmd == 'stop':
            player.stop()
            if play_thread:
                play_thread.join()

        elif cmd == 'pause':
            player.pause()

        elif cmd == 'resume':
            player.resume()

        elif cmd == 'shuffle':
            appPlaylist.shuffle = not appPlaylist.shuffle


        elif cmd == 'volume':
            player.set_volume(float(args[0]))

        elif cmd == 'exit':
            player.stop()
            if play_thread:
                play_thread.join()
            break

class PlayerShell(cmd.Cmd):
    intro = 'Welcome to the MP3 player shell. Type help or ? to list commands.\n'
    prompt = '(player) '

    def __init__(self, command_queue):
        super().__init__()
        self.command_queue = command_queue

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

    def do_exit(self, arg):
        'Exit the program'
        self.command_queue.put(('exit',))
        return True


def main():
    command_queue = mp.Queue()
    player_proc = mp.Process(target=player_process, args=(command_queue,))
    player_proc.start()

    PlayerShell(command_queue).cmdloop()

    player_proc.join()
    print("MP3 Player has been shut down.")

if __name__ == '__main__':
    main()
