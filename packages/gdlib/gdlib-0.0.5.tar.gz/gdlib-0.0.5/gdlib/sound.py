import pygame


class SoundManger:

    def __init__(self, initial_volume=0.5):
        self._sfx_list = {}
        self._muted = False
        self._volume = initial_volume
        pygame.mixer.set_num_channels(16)

    def preload_sfx(self, filename):
        if filename not in self._sfx_list:
            self._sfx_list[filename] = pygame.mixer.Sound(filename)

    def play_sfx(self, filename):
        if self._muted:
            return
        if filename not in self._sfx_list:
            self._sfx_list[filename] = pygame.mixer.Sound(filename)
        # We set the volume each time when we play.
        # Does this add lag? If so, we could set the volume
        # only if we add a new sound and if we change the volume.
        self._sfx_list[filename].set_volume(self.volume)
        if self._sfx_list[filename].get_num_channels() < pygame.mixer.get_num_channels() / 2:
            self._sfx_list[filename].play()

    def stop_sfx(self, filename):
        if filename not in self._sfx_list:
            self._sfx_list[filename] = pygame.mixer.Sound(filename)
        self._sfx_list[filename].stop()

    def fadeout_sfx(self, filename, time=2000):
        if filename not in self._sfx_list:
            self._sfx_list[filename] = pygame.mixer.Sound(filename)
        self._sfx_list[filename].fadeout(time)

    def set_music(self, filename):
        pygame.mixer.music.load(filename)
        if not self._muted:
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play()

    def toggle_mute(self):
        self._muted = not self._muted
        if not self._muted:
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.stop()

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = value
        if self._volume > 1:
            self._volume = 1
        if self._volume < 0:
            self._volume = 0
        pygame.mixer.music.set_volume(self._volume)

    def raise_volume(self):
        self.volume += .01

    def lower_volume(self):
        self.volume -= .01
