import pygame


class CollisionManager:
    COLLISION_EVENT = pygame.event.custom_type()

    def __init__(self):
        # A layer contains a list of sprite groups as values
        self.layers = {}

    def add_group(self, group, layer):
        if layer not in self.layers:
            self.layers[layer] = []
        self.layers[layer].append(group)

    def update(self, _):
        for layer in self.layers:
            sprite_groups = self.layers[layer]
            for index, group in enumerate(sprite_groups[:-1]):
                for group2 in sprite_groups[index + 1:]:
                    collisions_dict = pygame.sprite.groupcollide(group, group2, False, False,
                                                                 pygame.sprite.collide_circle)
                    for sprite in collisions_dict:
                        event = pygame.event.Event(CollisionManager.COLLISION_EVENT, layer=layer, sprite=sprite,
                                                   collisions=collisions_dict[sprite])
                        pygame.event.post(event)
