import threading


class Channel:
    def __init__(self):
        self.__state: list = []
        self.__event: threading.Event = threading.Event()
        self.__closed = False

    def close(self):
        self.__closed = True

    def push(self, item):
        self.__state.append(item)
        self.__event.set()
        self.__event.clear()

    def is_closed(self) -> bool:
        return self.__closed

    def listen(self):
        if len(self.__state) == 0:
            if self.__closed:
                return None
            self.__event.wait()
        return self.__state.pop(0)
