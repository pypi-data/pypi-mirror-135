class EventHandler:
    '''
    This event handle uses the observer pattern to get events and post
    it to registered handlers. This way a hierarchy can be built where events
    are processed globally, then handed to the current scene (i.e. state) and
    potentially further down to more specific subsystems.

    It is important that event handler are not called if they are not active
    in the game (to prevent code executions in inactive parts) and that sprites
    and other objects kill their event handler during clean up or it will keep
    references to the instances and prevent garbage collection, which will result
    in a memory leak.

    You can deliberately break the dependency chain by not using the registration
    at certain places, and instead only call process_event from a top-level event
    handler. This is for example done with the scene event handler to prevent events
    propagating to inactive scenes.
    '''

    def __init__(self, instance):
        '''The event handler is always bound to an instance of some object.

        It keeps track of handlers it observes (registered_at) and of
        its own observers (registered_by). Upon registration and unregistration,
        the registered handler gets notified to ensure that the sets remain consistent.

        Events are submitted via process_event(event). The handler distributes the event
        to its registered handlers. If the instance has a process_event(event) method,
        it is called so that events can be processed.

        Parameters
        ----------
        instance
            The instance this handler belongs to.
        '''
        self._instance = instance
        self._registered_at: set = set()
        self._registered_by: set = set()

    def register(self, handler):
        self._registered_by.add(handler)
        handler.notify_registered(self)

    def unregister(self, handler):
        self._registered_by.remove(handler)
        handler.notify_unregistered(self)

    def notify_registered(self, handler):
        self._registered_at.add(handler)

    def notify_unregistered(self, handler):
        self._registered_at.remove(handler)

    def process_event(self, event):
        if hasattr(self._instance, "process_event"):
            self._instance.process_event(event)
        for handler in self._registered_by:
            handler.process_event(event)

    def kill(self):
        '''Removes all references to other objects.

        Must be called when the instance is killed or removed.
        '''
        self._instance = None
        for handler in self._registered_at:
            handler.unregister(self)
        for handler in self._registered_by:
            handler.notify_unregistered(self)
        self._registered_at.clear()
        self._registered_by.clear()
