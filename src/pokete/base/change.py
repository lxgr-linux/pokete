from pokete.base.context import Context
from pokete.base.mouse import MouseInteractor, mouse_interaction_manager
from pokete.base.ui.overview import Overview


def change_ctx(ctx: Context, overview: Overview) -> Context:
    ctx = ctx.with_overview(overview)
    if isinstance(overview, MouseInteractor):
        mouse_interaction_manager.attach([overview])
    else:
        mouse_interaction_manager.attach([])
    return ctx
