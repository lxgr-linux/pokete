import logging
from pokete import bs_rpc
from ..context import Context
from ..periodic_event_manager import PeriodicEvent
from .single_event import SingleEvent


class SingleEventPeriodicEvent(PeriodicEvent):
    def __init__(self):
        self.__event_channel: bs_rpc.Channel[SingleEvent] = bs_rpc.Channel()
        self.__root_context:Context

    def set_root_context(self, ctx: Context):
        self.__root_context = ctx

    def add(self, event: SingleEvent):
        self.__event_channel.push(event)
        logging.info("yes")

    def tick(self, tick: int):
        if not self.__event_channel.is_empty():
            event = self.__event_channel.listen()
            if event != None:
                event.run(self.__root_context)

single_event_periodic_event: SingleEventPeriodicEvent = SingleEventPeriodicEvent()
