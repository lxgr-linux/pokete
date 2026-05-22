from abc import abstractmethod
from typing import Protocol


class Overview(Protocol):
    @abstractmethod
    def resize_view(self):
        pass
