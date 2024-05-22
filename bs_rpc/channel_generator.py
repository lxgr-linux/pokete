from .channel import Channel


class ChannelGenerator:
    def __init__(self, ch: Channel, close_fn):
        self.__ch: Channel = ch
        self.__close_fn = close_fn

    def __call__(self):
        while True:
            ret = self.__ch.listen()
            if ret is None:
                self.__close_fn()
                return
            yield ret
