import random
from typing import Generator

import pokete.bs_rpc as bs_rpc
from pokete.base.context import Context
from pokete.classes.fight.fight_decision import FightDecision
from pokete.classes.fight.fightmap.fightmap import FightMap
from pokete.classes.multiplayer.msg import player, fight
from pokete.classes.poke.poke import Poke
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
            ) for poke in self.player["pokes"]], False, 4, self.player["items"])

    def greet(self, fightmap: FightMap):
        fightmap.outp.outp(f"Fight started with {self.name}, good luck!")

    def get_decision(
        self, ctx: Context, fightmap: FightMap, enem
    ) -> FightDecision:
        resp = next(self.incomming)
        match resp.type:
            case fight.SEED_TYPE:
                seed: fight.SeedData = resp.data
                random.seed(seed["seed"])
            case _:
                assert False, resp.type

        resp = next(self.incomming)
        match resp.type:
            case fight.FIGHT_DECISION_TYPE:
                data: fight.FightDecisionData = resp.data
                return FightDecision.from_dict(data, self.curr, self.player)
            case _:
                assert False

    def handle_defeat(self, ctx: Context, fightmap, winner):
        return
