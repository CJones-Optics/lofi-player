
import pygame
import time
import threading


class MP3Player:
    def __init__(self):
        pygame.mixer.init()
        self.is_playing = False
        self.play_event = threading.Event()
        self.stop_event = threading.Event()

    def play(self, file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        self.is_playing = True
        self.play_event.set()
        self.stop_event.clear()

        while self.is_playing and pygame.mixer.music.get_busy():
            if self.stop_event.wait(0.1):  # Check every 0.1 seconds if we should stop
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

    def __del__(self):
        pygame.mixer.quit()
# Example usage
# player = MP3Player()
# player.play("path/to/your/mp3file.mp3")
# player.pause()
# player.resume()
# player.set_volume(0.5)
# player.stop()
