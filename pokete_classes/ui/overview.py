from abc import ABC


class Overview(ABC):
    def resize_view(self):
        raise NotImplemented()
