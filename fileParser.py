
import os
import numpy as np

class fileHandler(object):
    def __init__(self, sourceDir,chanelDir=None):
        self.sourceDir = sourceDir
        self.chanelDir = chanelDir

        self.getChanel()
        self.path = sourceDir + "/" + self.chanelDir
        self.fileList = []
        self.chanelList = []
        self.fileList = self.getTracks()

    def getTracks(self):
        files = os.listdir(self.path)
        self.tracklist = self.path + "/" + np.array(files)
        return self.tracklist

    def getChanel(self):
        if self.chanelDir != None:
            return self.chanelDir
        else:
            chanel = os.listdir(self.sourceDir)
            self.chanelDir =  chanel[0]
            return self.chanelDir

class playlist(object):
    def __init__(self, tracklist,shuffle=False):
        self.tracklist = tracklist
        self.currentTrack = 0
        self.trackCount = len(tracklist)
        self.shuffle = shuffle
        self.playing = False
        self.paused = False

    def nextTrack(self):
        if self.shuffle:
            self.currentTrack = np.random.randint(0,self.trackCount)
        else:
            self.currentTrack += 1
            if self.currentTrack >= self.trackCount:
                self.currentTrack = 0
        return self.tracklist[self.currentTrack]




if __name__ == "__main__":
    sourceDir = "tracks"
    files = fileHandler(sourceDir)
    tracks = files.getTracks()

    player = playlist(tracks)
    for i in range(5):
        print(player.nextTrack())
