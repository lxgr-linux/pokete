from pokete import bs_rpc

from .queue_monitoring_handler import (
    QueueMonitoringHandler,
)
from .single_event import SingleEvent


class QueueMonitor:
    def __init__(self) -> None:
        self.__handlers: list[QueueMonitoringHandler] = []

    def attach(self, handler: QueueMonitoringHandler) -> None:
        self.__handlers.append(handler)

    def optimize(self, chan: bs_rpc.Channel[SingleEvent]) -> None:
        for handler in self.__handlers:
            handler.optimize(chan)


queue_monitor = QueueMonitor()
