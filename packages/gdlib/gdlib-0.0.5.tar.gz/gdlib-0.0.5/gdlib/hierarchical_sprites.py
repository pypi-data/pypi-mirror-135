import pygame


class HierarchicalGroup(pygame.sprite.Group):
    """
    This sprite group cascades update- and draw-calls to
    sub sprites, if they are in a group under sprite.sprites.
    """

    def __init__(self):
        super().__init__()

    def update(self, *args, **kwargs):
        """
        Before the sprites get updates, it is checked if
        they have sub sprites. If so, these get updated first.

        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """

        for sprite in self.sprites():
            if hasattr(sprite, "sprites"):
                sprite.sprites.update(*args, **kwargs)
        super().update(*args, **kwargs)

    def draw(self, surface, offset=(0, 0)):
        """
        First the sprite is drawn, possibly with an offset, then
        the call is cascaded to subsprites with the offset of the current
        sprite's position.

        :param surface:
        :type surface:
        :param offset:
        :type offset:
        :return:
        :rtype:
        """
        for spr in self.sprites():
            rect = spr.rect.copy()
            rect.center = pygame.Vector2(rect.center) + pygame.Vector2(offset)
            if hasattr(spr, "blit_special_flags"):
                self.spritedict[spr] = surface.blit(spr.image, rect, special_flags=spr.blit_special_flags)
            else:
                self.spritedict[spr] = surface.blit(spr.image, rect)
            if hasattr(spr, "sprites"):
                subsurface = pygame.Surface((surface.get_width(), surface.get_height()), flags=pygame.SRCALPHA)
                spr.sprites.draw(subsurface, offset=subsurface.get_rect().center)
                if hasattr(spr, "rotation"):
                    subsurface = pygame.transform.rotate(subsurface, spr.rotation)
                sub_rect = subsurface.get_rect()
                sub_rect.center = rect.center
                surface.blit(subsurface, sub_rect)


class HierarchicalSprite(pygame.sprite.Sprite):
    """
    This is a convenience class for a sprite with a group for sub sprites.
    """

    def __init__(self):
        super().__init__()
        self.sprites = HierarchicalGroup()
