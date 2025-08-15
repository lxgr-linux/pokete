from abc import ABC, abstractmethod
from typing import Optional

from pokete import bs_rpc
from pokete.base.context import Context
from pokete.base.exception_propagation.propagating_thread import (
    PropagatingThread,
)
from pokete.base.input.mouse import MouseEvent, MouseEventType, mouse_manager
from pokete.base.single_event import single_event_periodic_event
from pokete.base.single_event.single_event import SingleEvent

type Area = tuple[tuple[int, int], tuple[int, int]]


class MouseInteractor(ABC):
    @abstractmethod
    def get_interaction_areas(
        self,
    ) -> list[Area]: ...

    @abstractmethod
    def interact(self, ctx: Context, area_idx: int, event: MouseEvent): ...


class InteractionSingleEvent(SingleEvent):
    def __init__(
        self, interactor: MouseInteractor, idx: int, event: MouseEvent
    ) -> None:
        super().__init__()
        self.interactor = interactor
        self.event = event
        self.idx = idx

    def run(self, ctx: Context):
        self.interactor.interact(ctx, self.idx, self.event)


class MouseInteractionManager:
    def __init__(self) -> None:
        self.__interactors: list[MouseInteractor] = []
        self.__last: Optional[tuple[MouseInteractor, int, MouseEventType]] = (
            None
        )
        PropagatingThread(target=self.run, daemon=True).start()

    def attach(self, interactors: list[MouseInteractor]):
        self.__interactors = interactors

    def run(self):
        for event in bs_rpc.ChannelGenerator(mouse_manager.events)():
            for interactor in self.__interactors:
                for idx, area in enumerate(interactor.get_interaction_areas()):
                    if (
                        area[0][0] <= event.x <= area[1][0]
                        and area[0][1] <= event.y <= area[1][1]
                    ):
                        self.cast_event(interactor, idx, event)
                        break
                else:
                    self.cast_event(interactor, -1, event)

    def cast_event(
        self, interactor: MouseInteractor, idx: int, event: MouseEvent
    ):
        curr = (interactor, idx, event.type)

        if curr != self.__last:
            single_event_periodic_event.add(
                InteractionSingleEvent(interactor, idx, event)
            )
            # logging.info("Casting %s", curr)
            self.__last = curr


mouse_interaction_manager = MouseInteractionManager()
