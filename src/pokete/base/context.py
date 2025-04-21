from copy import copy
from typing import TypeVar

from .game_map import CompatMap
from .periodic_event_manager import PeriodicEventManager
from .ui.overview import Overview

T = TypeVar('T')

class Context[T]:
    def __init__(
        self, pevm: PeriodicEventManager, _map: CompatMap,
        overview: Overview, figure: T
    ):
        self.pevm = pevm
        self.map = _map
        self.overview = overview
        self.figure: T = figure

    def with_pevm(self, pevm: PeriodicEventManager) -> "Context":
        ctx = copy(self)
        ctx.pevm = pevm
        return ctx

    def with_overview(self, overview: Overview) -> "Context":
        ctx = copy(self)
        ctx.overview = overview
        return ctx
