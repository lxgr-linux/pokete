import scrap_engine as se

from pokete.base.change import change_ctx
from pokete.classes.landscape import MapInteract


class NPCTrigger(se.Object):
    """Object on the map, that triggers a npc
    ARGS:
        npc: The NPC it belongs to"""

    def __init__(self, npc: MapInteract):
        super().__init__(" ", state="float")
        self.npc = npc

    def action(self, ob):
        """Action triggers the NPCs action"""
        self.npc.action()
        change_ctx(self.npc.ctx, self.npc.ctx.overview)
