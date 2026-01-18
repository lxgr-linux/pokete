from abc import ABC, abstractmethod

from ..context import Context


class SingleEvent(ABC):
    @abstractmethod
    def run(self, ctx: Context):
        pass

    @property
    def enabled(self) -> bool:
        return True
