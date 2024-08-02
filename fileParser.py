
import os
import numpy as np
import multiprocessing as mp

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
        self.tracklist = tracklist
        self.currentTrack = 0
        self.trackCount = len(tracklist)
        self.shuffle = shuffle
        self.playing = False
        self.paused = False
        self.messages_queue = messages_queue

    def getTrackName(self):
        self.trackName = self.tracklist[self.currentTrack]
        # strip the path
        self.trackName = self.trackName.split("/")[-1]
        # strip the file extension
        self.trackName = self.trackName.split(".")[0]
        return self.trackName

    def nextTrack(self):
        if self.shuffle:
            old_track = self.currentTrack
            while self.currentTrack == old_track:
                self.currentTrack = np.random.randint(0,self.trackCount)
        else:
            self.currentTrack += 1
            if self.currentTrack >= self.trackCount:
                self.currentTrack = 0

        if self.messages_queue:
            self.getTrackName()
            self.messages_queue.put(f"Playing: {self.trackName}")
        return self.tracklist[self.currentTrack]




if __name__ == "__main__":
    sourceDir = "tracks"
    files = fileHandler(sourceDir)
    tracks = files.getTracks()

    player = playlist(tracks)
    for i in range(5):
        print(player.nextTrack())
