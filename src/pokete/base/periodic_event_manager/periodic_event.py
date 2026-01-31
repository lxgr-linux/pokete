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
