"""Contains event var"""

from typing import Callable, Optional

from pokete.base.input.key import Key

EmitFn = Callable[[], None]


class Event:
    """Event class to enable dependency injection
    ARGS:
        event: Initial char"""

    def __init__(self, event=None):
        self._ev: Optional[Key] = event
        self.emit_fn: EmitFn

    def get(self) -> Optional[Key]:
        """Getter
        RETURNS:
            Current char"""
        return self._ev

    def set(self, event: Key):
        """Setter
        ARGS:
            event: New char"""
        self._ev = event
        self.emit_fn()

    def clear(self):
        """Clears the event"""
        self._ev = None

    def set_emit_fn(self, emit_fn: EmitFn):
        """Sets the method used to emit events to the timer"""
        self.emit_fn = emit_fn


_ev = Event()
