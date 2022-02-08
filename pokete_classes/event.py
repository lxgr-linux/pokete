"""Contains event var"""


class Event:
    """Event class to enable dependency injection
    ARGS:
        _ev: Initial char"""

    def __init__(self, event=""):
        self._ev = event

    def get(self):
        """Getter
        RETURNS:
            Current char"""
        return self._ev

    def set(self, event):
        """Setter
        ARGS:
            _ev: New char"""
        self._ev = event

    def clear(self):
        """Clears the event"""
        self._ev = ""


_ev = Event()
