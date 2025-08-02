from abc import ABC, abstractmethod

from pokete import bs_rpc
from pokete.base.exception_propagation.propagating_thread import (
    PropagatingThread,
)
from pokete.base.input.mouse import MouseEvent, mouse_manager

type Area = tuple[tuple[int, int], tuple[int, int]]


class MouseInteractor(ABC):
    @abstractmethod
    def get_interaction_areas(
        self,
    ) -> list[Area]: ...

    @abstractmethod
    def interact(self, area_idx: int, event: MouseEvent): ...


class MouseInteractionManager:
    def __init__(self) -> None:
        self.__interactors: list[MouseInteractor] = []
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
                        interactor.interact(idx, event)


mouse_interaction_manager = MouseInteractionManager()
