from copy import copy

from .movemap import Movemap
from .game import PeriodicEventManager
from .ui import Overview


class Context:
    def __init__(
        self, pevm: PeriodicEventManager, _map: Movemap,
        overview: Overview, figure
    ):
        self.pevm = pevm
        self.map = _map
        self.overview = overview
        self.figure = figure

    def with_overview(self, overview: Overview) -> "Context":
        ctx = copy(self)
        ctx.overview = overview
        return ctx
