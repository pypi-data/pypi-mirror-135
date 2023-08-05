import pygame


class Sheet:
    """
    The sheet class is used to extract single images from a
    sprite sheet, also called sprite atlas or texture atlas.
    """

    def __init__(self, file_path, tile_width, tile_height, rows, cols, border=0, spacing=0, x_offset=0, y_offset=0,
                 color_key=None):
        print(f"Loading sheet from {file_path}")
        self.image = pygame.image.load(file_path).convert_alpha()
        if color_key:
            self.image.set_colorkey(color_key)
        self.tile_height = tile_height
        self.tile_width = tile_width
        self.rows = rows
        self.cols = cols
        self.spacing = spacing
        self.border = border
        self.x_offset = x_offset
        self.y_offset = y_offset

        self.tiles = []
        width_height = (self.tile_width, self.tile_height)
        for row in range(self.rows):
            for col in range(self.cols):
                x = self.x_offset + self.border + (col * (self.tile_width + 2 * self.border + self.spacing))
                y = self.y_offset + self.border + (row * (self.tile_height + 2 * self.border + self.spacing))
                self.tiles.append(self.image.subsurface((x, y), width_height))

        print(f"Got {len(self.tiles)} tiles ({self.rows}/{self.cols}).")

    def __getitem__(self, key):
        # We support both continuous index and
        # access via row and column.
        # Therefore we have to find out if we 
        # have something like a tuple or not.
        try:
            iterator = iter(key)
            row, column = iterator
        except TypeError:
            row = key
            column = -1
        if column == -1:
            # Simple index access
            return self.tiles[row]
        else:
            # For convenience, you can also access via row and column
            return self.tiles[row * self.cols + column]

    def get_frames(self, keys):
        """
        Returns the selected images to be used for an animation.
        keys is a list of indices or (row,col) tuples.
        """
        frames = []
        for key in keys:
            frames.append(self[key])
        return frames


class Animation(pygame.sprite.Sprite):
    """
    An animation is a sprite playing the given frames at a given rate.
    """

    def __init__(self, frames, rate=12, play_once=False, callback=None):
        """
        __init__.

        Parameters
        ----------
        frames :
            A list of frames to be played.
        rate :
            The rate (frames per second) at which the animation is played.
        play_once :
            If true, the animation kills itself after one round.
        callback :
            If a callback is set, it is called, after the animation ends.
        """

        super().__init__()
        self.frames = frames
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect()
        self.last_switch = pygame.time.get_ticks()
        self.delay = 1000 / rate  # ms
        self.play_once = play_once
        self.finished = False
        self.callback = callback

    def update(self, *args, **kwargs):
        """
        Updates the animation. Parameters are ignored.

        Parameters
        ----------
        args :
            args
        kwargs :
            kwargs
        """
        if self.finished:
            return
        now = pygame.time.get_ticks()
        if self.last_switch + self.delay > now:
            return
        self.index += 1
        if self.index >= len(self.frames):
            if self.play_once:
                self.finished = True
                self.kill()
                if self.callback:
                    self.callback(self)
                return
            else:
                self.index = 0
        center = self.rect.center
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_switch = now
