import pygame


class BackgroundGroup(pygame.sprite.Group):
    def __init__(self, image_file=None, size=(0, 0)):
        super().__init__()
        self.image = None
        self.rect = None
        if image_file:
            image = pygame.image.load(image_file)
            self.image = pygame.transform.scale(image, size)
            self.rect = self.image.get_rect()

    def draw(self, surface):
        """
        We overwrite the draw method of pygame.sprite.Group

        :param surface:
        :type surface:
        :return:
        :rtype:
        """

        # Draw background image, if it exists
        if self.image:
            surface.blit(self.image, self.rect)

        # Draw all background sprites
        super().draw(surface)
