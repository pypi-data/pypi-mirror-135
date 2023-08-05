import pygame


class LightingGroup(pygame.sprite.Group):

    def __init__(self, *args):
        super().__init__(*args)

    def draw(self, surface):
        for light in self.sprites():
            surface.blit(light.image, light.rect, special_flags=pygame.BLEND_RGBA_ADD)

    def update(self, dt):
        for light in self.sprites():
            light.update(dt)
