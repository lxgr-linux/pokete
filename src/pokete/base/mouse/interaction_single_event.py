import time

from pokete.base.context import Context
from pokete.base.input.mouse import MouseEvent
from pokete.base.mouse.interactor import MouseInteractor
from pokete.base.single_event.single_event import SingleEvent


class InteractionSingleEvent(SingleEvent):
    def __init__(
        self, interactor: MouseInteractor, idx: int, event: MouseEvent
    ) -> None:
        super().__init__()
        self.interactor = interactor
        self.event = event
        self.idx = idx
        self.__enabled = True
        self.timestamp: float = time.time()

    @property
    def enabled(self) -> bool:
        return self.__enabled

    def disable(self):
        self.__enabled = False

    def run(self, ctx: Context):
        interactors = self.interactor.get_all_interactors()
        if self.idx < 0:
            for interactor in interactors:
                interactor.interact(ctx, self.idx, self.event)
        else:
            current_idx = 0
            set = False
            for interactor in interactors:
                new_idx = current_idx + len(interactor.get_interaction_areas())
                if self.idx < new_idx and not set:
                    interactor.interact(ctx, self.idx - current_idx, self.event)
                    set = True
                else:
                    interactor.interact(ctx, -1, self.event)
                current_idx = new_idx
