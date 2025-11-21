import logging
from abc import ABC, abstractmethod
from typing import Optional

from scrap_engine.addable.area import Area

from pokete import bs_rpc
from pokete.base.context import Context
from pokete.base.exception_propagation.propagating_thread import (
    PropagatingThread,
)
from pokete.base.input.mouse import MouseEvent, MouseEventType, mouse_manager
from pokete.base.single_event import single_event_periodic_event
from pokete.base.single_event.single_event import SingleEvent


class MouseInteractor(ABC):
    def get_all_interaction_areas(
        self,
    ) -> list[Area]:
        return [
            j
            for i in self.get_all_interactors()
            for j in i.get_interaction_areas()
        ]

    @abstractmethod
    def get_interaction_areas(
        self,
    ) -> list[Area]: ...

    @abstractmethod
    def interact(self, ctx: Context, area_idx: int, event: MouseEvent): ...

    def get_all_interactors(self) -> list["MouseInteractor"]:
        interactors: list[MouseInteractor] = [self]
        for interactor in self.get_partial_interactors():
            interactors += interactor.get_all_interactors()
        return interactors

    def get_partial_interactors(self) -> list["MouseInteractor"]:
        return []


class InteractionSingleEvent(SingleEvent):
    def __init__(
        self, interactor: MouseInteractor, idx: int, event: MouseEvent
    ) -> None:
        super().__init__()
        self.interactor = interactor
        self.event = event
        self.idx = idx

    def run(self, ctx: Context):
        interactors = self.interactor.get_all_interactors()
        logging.info("%d", len(interactors))
        if self.idx < 0:
            for interactor in interactors:
                interactor.interact(ctx, self.idx, self.event)
        else:
            current_idx = 0
            set = False
            for interactor in interactors:
                new_idx = current_idx + len(interactor.get_interaction_areas())
                logging.info("%d - %d", self.idx, current_idx)
                if self.idx < new_idx and not set:
                    interactor.interact(ctx, self.idx - current_idx, self.event)
                    set = True
                else:
                    interactor.interact(ctx, -1, self.event)
                current_idx = new_idx


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
                for idx, area in enumerate(
                    interactor.get_all_interaction_areas()
                ):
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
            logging.info("Casting %s", curr[2])
            self.__last = curr


mouse_interaction_manager = MouseInteractionManager()
