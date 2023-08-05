from abc import ABC, abstractmethod

import pygame
import warnings

try:
    from pyjoycon import ButtonEventJoyCon, get_R_id
except ImportError:
    ButtonEventJoyCon, get_R_id = None, None


class KeyState:
    def __init__(self, key_joycon, key_output):
        self.key_joycon = key_joycon
        self.key_output = key_output


class Unpressed(KeyState):
    def __init__(self, key_joycon, key_output):
        super().__init__(key_joycon, key_output)

    def handle(self, event):
        if event[self.key_joycon] == 1:
            JoyConAdapter.post_event(pygame.KEYDOWN, self.key_output)
            return Pressed(self.key_joycon, self.key_output)
        return self


class Pressed(KeyState):
    def __init__(self, key_joycon, key_output):
        super().__init__(key_joycon, key_output)

    def handle(self, event):
        if event[self.key_joycon] == 0:
            JoyConAdapter.post_event(pygame.KEYUP, self.key_output)
            return Unpressed(self.key_joycon, self.key_output)
        return self


class ControllingAdapter(ABC):
    # architecture not done yet
    # pygame.Keys are utf8 encoded, we need to list pressed keys to be able to modify it
    keys_pressed = pygame.key.get_pressed()

    @abstractmethod
    def update(self):
        pass


class KeyboardAdapter(ControllingAdapter):
    def update(self):
        ControllingAdapter.keys_pressed = pygame.key.get_pressed()


class JoyConAdapter(ControllingAdapter):
    def __init__(self):
        # if modules not installed
        if JoyConAdapter is None or get_R_id is None:
            warnings.warn("If you want to use your Joycons please install:"
                                      " pip install joycon-python hidapi pyglm. Setting back to keybaord for now.")
            self.update = KeyboardAdapter().update
        else:

            self.joycon_id_right = get_R_id()
            # self.joycon_id_left = get_L_id()

            # if joycon not connected
            if self.joycon_id_right[0] is None:
                warnings.warn("Switch Joycon controller is enabled but was not found. Setting back to keyboard only.")
                self.update = KeyboardAdapter().update
            else:
                self.joycon_right = ButtonEventJoyCon(*self.joycon_id_right)
                # self.joycon_left = ButtonEventJoyCon(*self.joycon_id_left)

                self.key_mappings = [Unpressed("x", pygame.K_SPACE)]

    @staticmethod
    def post_event(event_type, key):
        event = pygame.event.Event(event_type, key=key)
        pygame.event.post(event)

    def update(self):

        # for status_left, status_right in zip(self.joycon_left.get_status(), self.joycon_left.get_status()):
        status_right = self.joycon_right.get_status()

        status_btn_r = status_right["buttons"]["right"]
        for idx, key in enumerate(self.key_mappings):
            self.key_mappings[idx] = key.handle(status_btn_r)

        ControllingAdapter.keys_pressed = list(pygame.key.get_pressed())

        # TODO use also state machine
        # handle move left
        if status_right["analog-sticks"]["right"]["vertical"] < 1600:
            value = status_right["analog-sticks"]["right"]["vertical"]
            ControllingAdapter.keys_pressed[pygame.K_a] = 1 - (value - 850) / 750
        else:
            ControllingAdapter.keys_pressed[pygame.K_a] = pygame.key.get_pressed()[pygame.K_a]

        # handle move right
        if status_right["analog-sticks"]["right"]["vertical"] > 2000:
            value = status_right["analog-sticks"]["right"]["vertical"]
            ControllingAdapter.keys_pressed[pygame.K_d] = (value - 2000) / 1000
        else:
            ControllingAdapter.keys_pressed[pygame.K_d] = pygame.key.get_pressed()[pygame.K_d]
