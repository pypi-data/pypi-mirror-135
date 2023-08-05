import json
import os

import pygame


class Tileset():
    '''Wrapper for Tiled Tilesets.
    '''

    def __init__(self, file_path, crop=False):
        with open(file_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)
            self.name = self.data["name"]
            self.tileheight = self.data["tileheight"]
            self.tilewidth = self.data["tilewidth"]
            self.tilecount = self.data["tilecount"]
            self.imagewidth = self.data["imagewidth"]
            self.imageheight = self.data["imageheight"]
            self.spacing = self.data["spacing"]
            self.margin = self.data["margin"]
            directory = os.path.dirname(file_path)
            image_path = os.path.join(directory, self.data["image"])
            print(f"Loading tileset from {image_path}")
            self.image = pygame.image.load(image_path).convert_alpha()

            self.tiles = []
            left_top = [self.margin, self.margin]
            width_height = (self.tilewidth, self.tileheight)

            self.rows = 0

            for tile in range(self.tilecount):
                surface = self.image.subsurface(left_top, width_height)
                if crop:
                    surface = surface.subsurface(surface.get_bounding_rect())
                self.tiles.append(surface)
                left_top[0] += self.tilewidth + self.spacing
                if left_top[0] > self.imagewidth - self.margin - self.tilewidth:
                    self.rows += 1
                    left_top[0] = self.margin
                    left_top[1] += self.tileheight + self.spacing

            self.columns = int(self.tilecount / self.rows)
            print(f"Got {self.tilecount} tiles ({self.rows}/{self.columns}).")

            # If the tileset is used in a tilemap,
            # firstgid contains the offset for global identifiers
            self.firstgid = 0

    def get(self, row, column=-1):
        if column == -1:
            # We simply use the index, i.e. the tile ID in Tiled
            return self.tiles[row - self.firstgid]
        else:
            # For convenience, you can also access via row and column
            return self.tiles[row * self.columns + column]


class Layer():

    def __init__(self, name, data, x, y, width, height):
        self.name = name.lower()
        self.data = data
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Tilemap():

    def __init__(self, file_path):
        with open(file_path, "r", encoding="UTF-8") as f:
            self.data = json.load(f)
            self.width = self.data["width"]
            self.height = self.data["height"]
            self.tilewidth = self.data["tilewidth"]
            self.tileheight = self.data["tileheight"]
            self.tilesets = []
            for ts in self.data["tilesets"]:
                directory = os.path.dirname(file_path)
                ts_path = os.path.join(directory, ts["source"])
                tileset = Tileset(ts_path)
                tileset.firstgid = ts["firstgid"]
                self.tilesets.append(tileset)

            self.layers = []
            for l in self.data["layers"]:
                if l["type"] != "tilelayer":
                    continue
                layer = Layer(l["name"], l["data"], l["x"], l["y"], l["width"], l["height"])
                self.layers.append(layer)

    def get_dimensions(self):
        return self.width * self.tilewidth, self.height * self.tileheight

    def get_tile(self, gid) -> pygame.surface.Surface:
        for tileset in self.tilesets[::-1]:
            if gid >= tileset.firstgid:
                return tileset.get(gid)

    def get_layer(self, name):
        for l in self.layers:
            if name.lower() == l.name:
                return l
        return None

    def get_image(self, name):
        layer = self.get_layer(name)
        if not layer:
            return None
        surface = pygame.surface.Surface((layer.width * self.tilewidth, layer.height * self.tileheight),
                                         flags=pygame.SRCALPHA)
        for row in range(self.height):
            for col in range(self.width):
                index = row * self.width + col
                if layer.data[index] > 0:
                    tile = self.get_tile(layer.data[index])
                    rect = tile.get_rect()
                    rect.x = col * self.tilewidth
                    rect.bottom = row * self.tileheight + self.tileheight
                    surface.blit(tile, rect)
        return surface

    def get_sprites(self, name, sprite_class=pygame.sprite.Sprite, group=None):
        '''Return all tiles in a layer as sprite group.

        The sprite_class can be changed to support custom classes.
        '''
        layer = self.get_layer(name)
        if not layer:
            return None
        if not group:
            group = pygame.sprite.Group()
        for row in range(self.height):
            for col in range(self.width):
                index = row * self.width + col
                if layer.data[index] > 0:
                    tile = self.get_tile(layer.data[index])
                    rect = tile.get_rect()
                    rect.x = col * self.tilewidth
                    rect.bottom = row * self.tileheight + self.tileheight
                    sprite = sprite_class(group)
                    sprite.image = tile
                    sprite.rect = rect
        return group

    def get_rects(self, name):
        '''Returns only rects for positioning custom objects.
        '''
        layer = self.get_layer(name)
        if not layer:
            return None
        rects = []
        for row in range(self.height):
            for col in range(self.width):
                index = row * self.width + col
                if layer.data[index] > 0:
                    tile = self.get_tile(layer.data[index])
                    rect = tile.get_rect()
                    rect.x = col * self.tilewidth
                    rect.bottom = row * self.tileheight + self.tileheight
                    rects.append(rect)
        return rects

    def get_position(self, name):
        '''Returns a single position in a layer, assuming, there is only one.
        '''
        layer = self.get_layer(name)
        if not layer:
            return None
        for row in range(self.height):
            for col in range(self.width):
                index = row * self.width + col
                if layer.data[index] > 0:
                    tile = self.get_tile(layer.data[index])
                    rect = tile.get_rect()
                    rect.x = col * self.tilewidth
                    rect.bottom = row * self.tileheight + self.tileheight
                    return rect
        return None
