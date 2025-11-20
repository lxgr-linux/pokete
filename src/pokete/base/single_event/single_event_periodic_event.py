from pokete import bs_rpc

from ..context import Context
from ..periodic_event_manager import PeriodicEvent
from .single_event import SingleEvent


class SingleEventPeriodicEvent(PeriodicEvent[Context]):
    def __init__(self):
        self.__event_channel: bs_rpc.Channel[SingleEvent] = bs_rpc.Channel()

    def add(self, event: SingleEvent):
        self.__event_channel.push(event)

    def tick(self, ctx: Context, tick: int):
        if not self.__event_channel.is_empty():
            event = self.__event_channel.listen()
            if event is not None:
                event.run(ctx)


single_event_periodic_event: SingleEventPeriodicEvent = (
    SingleEventPeriodicEvent()
)
