from abc import ABC, abstractmethod


class Overview(ABC):
    @abstractmethod
    def resize_view(self):
        pass
