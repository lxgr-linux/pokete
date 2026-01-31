from abc import ABC, abstractmethod

import scrap_engine as se

from pokete.base.context import Context
from pokete.base.input.mouse import MouseEvent


class MouseInteractor(ABC):
    def get_all_interaction_areas(
        self,
    ) -> list[se.Area]:
        return [
            j
            for i in self.get_all_interactors()
            for j in i.get_interaction_areas()
        ]

    @abstractmethod
    def get_interaction_areas(
        self,
    ) -> list[se.Area]: ...

    @abstractmethod
    def interact(self, ctx: Context, area_idx: int, event: MouseEvent): ...

    def get_all_interactors(self) -> list["MouseInteractor"]:
        interactors: list[MouseInteractor] = [self]
        for interactor in self.get_partial_interactors():
            interactors += interactor.get_all_interactors()
        return interactors

    def get_partial_interactors(self) -> list["MouseInteractor"]:
        return []
