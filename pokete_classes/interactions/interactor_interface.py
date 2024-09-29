from abc import abstractmethod, ABC


class InteractorInterface(ABC):
    @abstractmethod
    def text(self, text: list[str]) -> None:
        pass

    @abstractmethod
    def walk_point(self, _x: int, _y: int) -> bool:
        pass
