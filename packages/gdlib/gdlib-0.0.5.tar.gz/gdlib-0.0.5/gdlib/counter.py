import pygame


class Counter:

    def __init__(self, position, font, size, color):
        self.font = pygame.font.Font(font, size)
        self.position = position
        self.color = color
        self.digits = 3
        self.set_value(0)

    def set_value(self, value):
        self._value = value
        number_format = "{{:0{}d}}".format(self.digits)
        self.image = self.font.render(number_format.format(self._value), True, self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position

    def change_value(self, value):
        self.set_value(self._value + value)

    def get_value(self):
        return self._value

    def draw(self, surface):
        surface.blit(self.image, self.rect)
