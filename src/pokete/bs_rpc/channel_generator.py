from typing import Callable, Generator, Generic, TypeVar

from .channel import Channel

CloseFn = Callable[[], None]
T = TypeVar("T")


class ChannelGenerator(Generic[T]):
    def __init__(self, ch: Channel[T], close_fn: CloseFn | None = None):
        self.__ch: Channel[T] = ch
        self.__close_fn = close_fn

    def __call__(self) -> Generator[T, None, None]:
        while True:
            ret = self.__ch.listen()
            if ret is None:
                if self.__close_fn is not None:
                    self.__close_fn()
                return
            yield ret
