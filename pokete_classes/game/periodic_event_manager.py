"""Contains the pevm"""


class PeriodicEvent:
    def tick(self, tick: int):
        raise NotImplemented()


class PeriodicEventManager:
    """As the name states: It manages periodic events in the game loop"""

    def __init__(self, events: list[PeriodicEvent], tick=0):
        self.events = events
        self.tick = tick

    def with_events(
        self,
        events: list[PeriodicEvent]
    ) -> "PeriodicEventManager":
        return PeriodicEventManager(self.events + events, self.tick)

    def event(self):
        """Executes the events"""
        for event in self.events:
            event.tick(self.tick)
        self.tick += 1