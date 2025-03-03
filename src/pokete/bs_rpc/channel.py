import threading
from typing import Generic, TypeVar

T = TypeVar("T")


class Channel(Generic[T]):
    def __init__(self):
        self.__state: list[T] = []
        self.__event: threading.Event = threading.Event()
        self.__closed = False

    def close(self):
        self.__closed = True

    def push(self, item: T):
        self.__state.append(item)
        self.__event.set()
        self.__event.clear()

    def is_closed(self) -> bool:
        return self.__closed

    def is_empty(self) -> bool:
        return len(self.__state) == 0

    def listen(self) -> T | None:
        if self.is_empty():
            if self.__closed:
                return None
            self.__event.wait()
        return self.__state.pop(0)
