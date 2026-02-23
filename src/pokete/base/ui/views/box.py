from abc import ABC
from typing import Optional, override

import scrap_engine as se

from pokete.base.context import Context
from pokete.base.input.mouse import MouseEvent
from pokete.base.mouse.interactor import MouseInteractor
from pokete.base.ui.elements.box import Box
from pokete.base.ui.overview import Overview


class BoxView(Box, MouseInteractor, ABC):
    def __init__(
        self,
        height,
        width,
        name="",
        info: Optional[list[se.Text]] = None,
        overview: Optional[Overview] = None,
        ctx: Optional[Context] = None,
    ):
        super().__init__(height, width, name, info, overview, ctx)

    @override
    def get_partial_interactors(self) -> list[MouseInteractor]:
        return [
            label
            for label in self.info_labels
            if isinstance(label, MouseInteractor)
        ]

    @override
    def get_interaction_areas(self) -> list[se.Area]:
        return []

    @override
    def interact(self, ctx: Context, area_idx: int, event: MouseEvent):
        pass
