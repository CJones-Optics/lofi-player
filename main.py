from fileParser import *
from musicPlayer import *
import multiprocessing as mp
import cmd
import time



def player_process(command_queue):
    player = MP3Player()
    play_thread = None

    def play_worker(file_path):
        player.play(file_path)

    while True:
        cmd, *args = command_queue.get()
        if cmd == 'play':
            if play_thread and play_thread.is_alive():
                player.stop()
                play_thread.join()
            play_thread = threading.Thread(target=play_worker, args=(args[0],))
            play_thread.start()
        elif cmd == 'stop':
            player.stop()
            if play_thread:
                play_thread.join()
        elif cmd == 'pause':
            player.pause()
        elif cmd == 'resume':
            player.resume()
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
        if arg:
            self.command_queue.put(('play', arg))
        else:
            print("Please provide a file path")

    def do_stop(self, arg):
        'Stop playing'
        self.command_queue.put(('stop',))

    def do_pause(self, arg):
        'Pause playback'
        self.command_queue.put(('pause',))

    def do_resume(self, arg):
        'Resume playback'
        self.command_queue.put(('resume',))

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



if __name__ == '__main__':
    command_queue = mp.Queue()
    player_proc = mp.Process(target=player_process, args=(command_queue,))
    player_proc.start()

    PlayerShell(command_queue).cmdloop()

    player_proc.join()
    print("MP3 Player has been shut down.")

# def main():
#     sourceDir = "tracks"
#     files = fileHandler(sourceDir)
#     tracks = files.getTracks()

#     player = playlist(tracks)
#     track = player.nextTrack()

#     # play_mp3(track)
#     player = MP3Player()
#     player.play(track)

# if __name__ == "__main__":
#     main()