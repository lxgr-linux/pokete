from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar("T")


class PeriodicEvent[T](ABC):
    @abstractmethod
    def tick(
        self,
        ctx: T,
        tick: int,
    ) -> None:
        pass
