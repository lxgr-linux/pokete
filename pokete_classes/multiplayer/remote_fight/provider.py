import logging
import bs_rpc
from pokete_classes.attack import Attack
from pokete_classes.context import Context
from pokete_classes.fight.attack_result import AttackResult
from pokete_classes.multiplayer.msg import player
from pokete_classes.poke.poke import Poke
from ...fight import Provider

class RemoteProvider(Provider):
    def __init__(self, name: str,
        outgoing: bs_rpc.ResponseWriter,
        incomming: bs_rpc.ChannelGenerator,
        com_service
    ):
        p: player.User = com_service.get_player(name)
        self.outgoing = outgoing
        self.incomming = incomming

        super().__init__(
            [Poke(
                poke["name"], _xp=poke["xp"], _hp=poke["hp"], _ap=poke["ap"], _attacks=poke["attacks"], _effects=poke["effects"], player=False, shiny=poke["shiny"], nature=poke["nature"], stats=poke["stats"]
            ) for poke in p["pokes"]], False, 4)

    def greet(self, fightmap):
        return

    def get_attack(
        self, ctx: Context, fightmap: "FightMap", enem
    ) -> AttackResult:
        return None

    def handle_defeat(self, ctx: Context, fightmap, winner):
        return
