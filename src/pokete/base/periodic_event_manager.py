"""Contains the pevm"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class PeriodicEvent(ABC, Generic[T]):
    @abstractmethod
    def tick(
        self,
        ctx: T,
        tick: int,
    ):
        pass


class PeriodicEventManager(Generic[T]):
    """As the name states: It manages periodic events in the game loop"""

    def __init__(self, events: list[PeriodicEvent[T]], tick=0):
        self.events: list[PeriodicEvent[T]] = events
        self.tick: int = tick

    def with_events(
        self, events: list[PeriodicEvent[T]]
    ) -> "PeriodicEventManager":
        return PeriodicEventManager(self.events + events, self.tick)

    def event(self, ctx: T):
        """Executes the events"""
        for event in self.events:
            event.tick(ctx, self.tick)
        self.tick += 1
