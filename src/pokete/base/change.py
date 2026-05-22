from typing import TypeVar

from pokete.base.context import Context
from pokete.base.mouse import MouseInteractor, mouse_interaction_manager
from pokete.base.ui.overview import Overview

T = TypeVar("T")


def change_ctx(ctx: Context[T], overview: Overview) -> Context[T]:
    ctx = ctx.with_overview(overview)
    if isinstance(overview, MouseInteractor):
        mouse_interaction_manager.attach([overview])
    else:
        mouse_interaction_manager.attach([])
    return ctx
