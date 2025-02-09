from copy import copy

from .game_map import CompatMap
from .game import PeriodicEventManager
from .ui.overview import Overview


class Context:
    def __init__(
        self, pevm: PeriodicEventManager, _map: CompatMap,
        overview: Overview, figure
    ):
        self.pevm = pevm
        self.map = _map
        self.overview = overview
        self.figure = figure

    def with_pevm(self, pevm: PeriodicEventManager) -> "Context":
        ctx = copy(self)
        ctx.pevm = pevm
        return ctx

    def with_overview(self, overview: Overview) -> "Context":
        ctx = copy(self)
        ctx.overview = overview
        return ctx
