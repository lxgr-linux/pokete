import logging
from typing import Generator
import bs_rpc
from pokete_classes.attack import Attack
from pokete_classes.context import Context
from pokete_classes.fight.attack_result import AttackResult
from pokete_classes.fight.fightmap.fightmap import FightMap
from pokete_classes.multiplayer.msg import player, fight
from pokete_classes.poke.poke import Poke
from ...fight import Provider

class RemoteProvider(Provider):
    def __init__(self, name: str,
        outgoing: bs_rpc.ResponseWriter,
        incomming: Generator[bs_rpc.Body, None, None],
        com_service
    ):
        self.player: player.User = com_service.get_player(name)
        self.outgoing = outgoing
        self.incomming = incomming
        self.name = name

        super().__init__(
            [Poke(
                poke["name"], _xp=poke["xp"], _hp=poke["hp"], _ap=poke["ap"], _attacks=poke["attacks"], _effects=poke["effects"], player=False, shiny=poke["shiny"], nature=poke["nature"], stats=poke["stats"]
            ) for poke in self.player["pokes"]], False, 4)

    def greet(self, fightmap: FightMap):
        fightmap.outp.outp(f"Fight started with {self.name}, good luck!")

    def get_attack(
        self, ctx: Context, fightmap: FightMap, enem
    ) -> AttackResult:
        logging.info("Waiting attack")
        resp = next(self.incomming)
        logging.info(resp)
        match resp.type:
            case fight.ATTACK_RESULT_TYPE:
                data: fight.AttackResultData = resp.data
                return AttackResult.from_dict(data, self.curr, self.player)
            case _:
                assert False

    def handle_defeat(self, ctx: Context, fightmap, winner):
        return
