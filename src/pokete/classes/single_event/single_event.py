from abc import ABC, abstractmethod

from pokete.classes.context import Context


class SingleEvent(ABC):
    @abstractmethod
    def run(self, ctx:Context):
        pass
