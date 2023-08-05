from __future__ import annotations

from typing import Union

import pygame

from gdlib.events import EventHandler

STATE_CHANGED = pygame.event.custom_type()


class State():
    def __init__(self, instance=None):
        '''Creates a state, possibly associated with an instance.
        Parameters
        ----------
        instance
            An optional reference to an instance this state is associated with.
        '''
        self.instance = instance
        self._next_state: Union[None, str, State] = None
        # Every state has an own event handler.
        self.event_handler = EventHandler(self)
        # It is registered to the
        # event handler of the associated instance by default.
        if self.instance and hasattr(self.instance, "event_handler"):
            if self.instance.event_handler:
                self.instance.event_handler.register(self.event_handler)

    def next(self, next_state: Union[None, str, State]) -> None:
        '''Set the state to be activated next.

        The actual change of the state happens when

        Parameters
        ----------
        next_state
        '''
        self._next_state = next_state

    def update(self, *args, **kwargs) -> None:
        '''Implementation of the update logic.'''

    def draw(self, surface: pygame.Surface) -> None:
        '''Handles the drawing to the surface.

        Parameters
        ----------
        surface
            The surface to be used for drawing.
        '''

    def process_event(self, event: pygame.event.Event) -> None:
        '''Event handling for this state.

        Parameters
        ----------
        event
            The current event.
        '''

    def exit_state(self) -> None:
        '''Called before the state is left.'''

    def enter_state(self):
        '''Called when the state is entered.'''

    def check_next_state(self) -> Union[None, str, State]:
        '''Return the next state or None.

        If this method is called, it returns the next state if it is set.
        In this case, the next state is reset to None.

        Returns
        -------
        The next state instance or state name or None.
        '''
        if self._next_state is None:
            return None
        else:
            state = self._next_state
            self._next_state = None
            return state


class EmptyState(State):
    '''The empty state does nothing.'''


class StateMachine():
    '''State Machine Utility Class.

    This is a utility class to make changing states even easier.
    You do not have to use it if you want to implement the state
    changing yourself.
    '''

    def __init__(self, name=None):
        '''If you set a name, state changes are posted as events.

        State machines can post events when the state is changed.
        To help identify relevant events, you can set a name. Only if
        a name is set, the event is posted!

        Parameters
        ----------
        name
            If set, an event will be posted when the state changes.
        '''
        self._current_state: State = EmptyState()
        # We support registering states and activating them via their name.
        self._registered_states = {}
        self.name = name

    @property
    def current_state(self) -> State:
        return self._current_state

    @current_state.setter
    def current_state(self, new_state: Union[str, State]) -> None:
        '''Set the new state.
        
        Parameters
        ----------
        new_state : The instance or the name of the new state
        '''
        self._current_state.exit_state()
        old_state = self._current_state
        if type(new_state) == str:
            if new_state not in self._registered_states:
                raise ValueError(f"The name of the next state is not known: {new_state}")
            self._current_state = self._registered_states[new_state]
        elif isinstance(new_state, State):
            self._current_state = new_state
        else:
            raise ValueError(f"Not a valid state or state name: {new_state}")
        if callable(self._current_state):
            self._current_state = self.current_state()
        self._current_state.enter_state()
        if self.name:
            event = pygame.event.Event(STATE_CHANGED, name=self.name, old_state=old_state,
                                       new_state=self._current_state)
            pygame.event.post(event)

    def register(self, name, state_instance):
        self._registered_states[name] = state_instance

    def draw(self, surface: pygame.Surface):
        '''Convenience method to draw the current state.'''
        self.current_state.draw(surface)

    def update(self, *args, **kwargs):
        '''Convenience method to update the current state.'''
        self.current_state.update(*args, **kwargs)

    def process_event(self, event: pygame.event.Event):
        '''Convenience method to pass the event to the current state.'''
        self.current_state.process_event(event)

    def check_next_state(self) -> None:
        '''Run this method to check for and handle state changes.'''
        new_state = self._current_state.check_next_state()
        if new_state:
            self.current_state = new_state
