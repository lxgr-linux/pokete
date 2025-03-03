from abc import ABC, abstractmethod

from ..context import Context


class SingleEvent(ABC):
    @abstractmethod
    def run(self, ctx:Context):
        pass
