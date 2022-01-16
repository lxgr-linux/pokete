"""Contains event var"""

class Event:
    """Event class to enable dependency injection
    ARGS:
        _ev: Initial char"""

    def __init__(self, _ev=""):
        self._ev = _ev

    def get(self):
        """Getter
        RETURNS:
            Current char"""
        return self._ev

    def set(self, _ev):
        """Setter
        ARGS:
            _ev: New char"""
        self._ev = _ev

    def clear(self):
        """Clears the event"""
        self._ev = ""


_ev = Event()
