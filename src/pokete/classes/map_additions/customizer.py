from abc import ABC, abstractmethod

from pokete.classes.classes import PlayMap


class MapCustomizer(ABC):
    @abstractmethod
    def customize(self, _map: PlayMap):
        pass
