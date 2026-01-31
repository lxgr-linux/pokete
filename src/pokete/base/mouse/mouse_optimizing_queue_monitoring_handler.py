from pokete import bs_rpc
from pokete.base.input.mouse import MouseEventType
from pokete.base.single_event import QueueMonitoringHandler, SingleEvent

from .interaction_single_event import InteractionSingleEvent


class MouseOptimizingQueueMonitoringHandler(QueueMonitoringHandler):
    THRESHHOLD = 0.2

    def optimize(self, chan: bs_rpc.Channel[SingleEvent]):
        elements = [
            i
            for i in chan.state
            if isinstance(i, InteractionSingleEvent)
            and i.enabled
            and i.event.type == MouseEventType.MOVE
        ]
        for idx, element in enumerate(elements):
            if idx != 0 and idx + 1 != len(elements):
                prior = elements[idx - 1]
                next = elements[idx + 1]
                if (
                    (element.timestamp - prior.timestamp < self.THRESHHOLD)
                    and (next.timestamp - element.timestamp < self.THRESHHOLD)
                    and prior.enabled
                    and next.enabled
                ):
                    element.disable()
