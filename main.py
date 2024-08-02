from fileParser import *
from musicPlayer import *


def main():
    sourceDir = "tracks"
    files = fileHandler(sourceDir)
    tracks = files.getTracks()

    player = playlist(tracks)
    track = player.nextTrack()

    # play_mp3(track)
    player = MP3Player()
    player.play(track)

if __name__ == "__main__":
    main()
