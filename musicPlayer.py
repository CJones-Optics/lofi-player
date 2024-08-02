
import pygame

class MP3Player:
    def __init__(self):
        pygame.mixer.init()
        self.is_playing = False

    def play(self, file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        self.is_playing = True

        try:
            while self.is_playing and pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except KeyboardInterrupt:
            self.stop()
        finally:
            self.stop()

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False

    def resume(self):
        if not self.is_playing:
            pygame.mixer.music.unpause()
            self.is_playing = True

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
