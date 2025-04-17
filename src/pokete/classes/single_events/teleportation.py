from pokete.base.context import Context
from pokete.base.single_event import SingleEvent
from pokete.classes import animations, roadmap
from pokete.classes.doors import Door
from pokete.classes.settings import settings
from pokete.classes.asset_service.service import asset_service

class TeleportationSingleEvent(SingleEvent):
    def __init__(self, poke):
        self.poke = poke

    def run(self, ctx:Context):
        # TODO: This is horrible, remove the te
        if (obj := roadmap.roadmap(ctx, choose=True)) is None:
            return
        if settings("animations").val:
            animations.transition(ctx.map, self.poke)
        cen_d = asset_service.get_assets().obmaps[obj.name].hard_obs["pokecenter"]
        Door("", state="float", arg_proto={
            "map": obj.name,
            "x": cen_d.x + 5,
            "y": cen_d.y + 6
        }).action(ctx.figure)
