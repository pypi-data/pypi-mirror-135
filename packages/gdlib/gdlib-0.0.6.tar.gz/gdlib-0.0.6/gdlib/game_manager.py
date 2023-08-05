import pygame

class GameManager:
    SCORE_CHANGED = pygame.event.custom_type()

    """
    A global game state object to control
    for instance the running flag.
    """

    def __init__(self):
        self._running = True
        self._score = 0

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value
        event = pygame.event.Event(GameManager.SCORE_CHANGED, score=value)
        pygame.event.post(event)

    @property
    def running(self):
        return self._running

    def quit(self):
        self._running = False
