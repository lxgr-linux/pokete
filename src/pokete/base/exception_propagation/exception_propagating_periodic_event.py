from pokete import bs_rpc
from pokete.base.context import Context
from pokete.base.periodic_event_manager import PeriodicEvent


class ExceptionPropagatingPeriodicEvent(PeriodicEvent[Context]):
    def __init__(self):
        self.__channel = bs_rpc.Channel[Exception]()

    def enq(self, e: Exception):
        self.__channel.push(e)

    def tick(self, ctx: Context, tick: int):
        if not self.__channel.is_empty():
            for e in bs_rpc.ChannelGenerator(self.__channel)():
                raise e


exception_propagating_periodic_event = ExceptionPropagatingPeriodicEvent()
