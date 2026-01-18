from abc import ABC, abstractmethod

from pokete import bs_rpc
from pokete.base.single_event.single_event import SingleEvent


class QueueMonitoringHandler(ABC):
    @abstractmethod
    def optimize(self, chan: bs_rpc.Channel[SingleEvent]): ...
