"""Contains event var"""


from typing import Callable


EmitFn = Callable[[], None]

class Event:
    """Event class to enable dependency injection
    ARGS:
        event: Initial char"""

    def __init__(self, event=""):
        self._ev = event
        self.emit_fn: EmitFn

    def get(self):
        """Getter
        RETURNS:
            Current char"""
        return self._ev

    def set(self, event):
        """Setter
        ARGS:
            event: New char"""
        self._ev = event
        self.emit_fn()

    def clear(self):
        """Clears the event"""
        self._ev = ""

    def set_emit_fn(self, emit_fn:EmitFn):
        """Sets the method used to emit events to the timer"""
        self.emit_fn = emit_fn


_ev = Event()
