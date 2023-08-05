import pygame

# If you want to influence pygame.init() make sure
# to initialize before gdlib is imported.
pygame.init()

import pygame.event

import gdlib.states
from gdlib.game_manager import GameManager
from gdlib.sound import SoundManger
from gdlib.states import StateMachine

# The empty global namespace, use is however you want

from gdlib.controlling import KeyboardAdapter

# Here are global instances that are always available.
game_manager = GameManager()
sound_manager = SoundManger()
scene_manager = StateMachine("SCENE")
clock = pygame.time.Clock()
control_adapter = KeyboardAdapter()


def process_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_manager.quit()
        # We make sure that only the active scene processes events.
        # See events.EventHandler for further information.
        scene_manager.current_state.event_handler.process_event(event)


def run(scene, screen):
    scene_manager.current_state = scene
    clock.tick(conf.FPS)
    dt = 0
    while game_manager.running:
        control_adapter.update()
        process_events()
        scene_manager.update(dt)
        scene_manager.draw(screen)
        scene_manager.check_next_state()
        pygame.display.flip()
        dt = clock.tick(conf.FPS) / 1000
    pygame.quit()
