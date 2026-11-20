import time

from pokete import bs_rpc
from pokete.base.exception_propagation.propagating_thread import (
    PropagatingThread,
)

from ..context import Context
from ..periodic_event_manager import PeriodicEvent
from .queue_monitor import queue_monitor
from .single_event import SingleEvent


class SingleEventPeriodicEvent(PeriodicEvent[Context]):
    def __init__(self) -> None:
        self.__event_channel: bs_rpc.Channel[SingleEvent] = bs_rpc.Channel()

    def __monitor(self) -> None:
        while True:
            time.sleep(0.01)
            queue_monitor.optimize(self.__event_channel)

    def monitor(self) -> None:
        PropagatingThread(target=self.__monitor, daemon=True).start()

    def add(self, event: SingleEvent) -> None:
        self.__event_channel.push(event)

    def tick(self, ctx: Context, tick: int) -> None:
        while True:
            if not self.__event_channel.is_empty():
                event = self.__event_channel.listen()
                if event is not None and event.enabled:
                    event.run(ctx)
                    break
                else:
                    continue
            else:
                break


single_event_periodic_event: SingleEventPeriodicEvent = SingleEventPeriodicEvent()
