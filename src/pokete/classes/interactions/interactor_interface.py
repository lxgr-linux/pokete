from abc import ABC, abstractmethod


class InteractorInterface(ABC):
    @abstractmethod
    def text(self, text: list[str]) -> None:
        pass

    @abstractmethod
    def walk_point(self, _x: int, _y: int) -> bool:
        pass
