
import os
import numpy as np
import multiprocessing as mp
import logging

class fileHandler(object):
    def __init__(self, sourceDir,chanelDir=None):
        self.sourceDir = sourceDir
        self.chanelDir = chanelDir

        self.getChanelList()
        self.getChanel()
        self.path = sourceDir + "/" + self.chanelDir
        self.fileList = self.getTracks()

    def changeChannel(self, chanel):
        self.chanelDir = chanel
        self.path = self.sourceDir + "/" + self.chanelDir
        self.fileList = self.getTracks()
        return self

    def getTracks(self):
        files = os.listdir(self.path)
        self.tracklist = self.path + "/" + np.array(files)
        return self.tracklist

    def getChanelList(self):
        self.chanelList = os.listdir(self.sourceDir)
        # If it is empty throw an error
        if len(self.chanelList) == 0:
            raise Exception("No chanels found")
        return self.chanelList

    def getChanel(self):
        if self.chanelDir != None:
            return self.chanelDir
        else:
            chanel = os.listdir(self.sourceDir)
            self.chanelDir =  chanel[0]
            return self.chanelDir

class playlist(object):
    def __init__(self, tracklist,shuffle=False,messages_queue=None):
        # Set up logging configuration to append to the existing log file
        logging.basicConfig(filename='lofiRadio.log',     # Log file name
                            level=logging.DEBUG,        # Log level
                            filemode='a',               # 'a' mode to append to the file if it exists
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.tracklist = tracklist
        self.currentTrack = 0
        self.trackCount = len(tracklist)
        self.shuffle = shuffle
        self.playing = False
        self.paused = False
        self.messages_queue = messages_queue
        logging.debug(f"playlist: {self.messages_queue}")
        logging.info("Playlist has been created.")

    def getTrackName(self):
        self.trackName = self.tracklist[self.currentTrack]
        # strip the path
        self.trackName = self.trackName.split("/")[-1]
        # strip the file extension
        self.trackName = self.trackName.split(".")[0]
        return self.trackName

    def nextTrack(self):
        logging.info("playlist: Next track")
        if self.shuffle:
            old_track = self.currentTrack
            while self.currentTrack == old_track:
                self.currentTrack = np.random.randint(0,self.trackCount)
        else:
            self.currentTrack += 1
            if self.currentTrack >= self.trackCount:
                self.currentTrack = 0

        logging.info(f"playlist: Current track: {self.currentTrack}")

        # if self.messages_queue != None:
        #     self.getTrackName()
        #     logging.info(f"message_queue: Playlist>{self.trackName}")
        #     self.messages_queue.put(f"Playlist>{self.trackName}")

        self.getTrackName()
        logging.info(f"message_queue: Playlist>{self.trackName}")
        # Chop of the end of the track name if larger than 20 characters
        if len(self.trackName) > 40:
            track_name = self.trackName[:40] + "..."
        else:
            track_name = self.trackName
        self.messages_queue.put(f"Playlist>{track_name}")

        return self.tracklist[self.currentTrack]




if __name__ == "__main__":
    sourceDir = "tracks"
    files = fileHandler(sourceDir)
    tracks = files.getTracks()

    player = playlist(tracks)
    for i in range(5):
        print(player.nextTrack())
