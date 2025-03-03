import random
from typing import Generator

import pokete.bs_rpc as bs_rpc
from pokete.base.context import Context
from pokete.classes.fight.fight_decision import FightDecision
from pokete.classes.fight.fightmap.fightmap import FightMap
from pokete.classes.fight.providers import Provider
from pokete.classes.multiplayer.msg import fight


class FigureWrapperProvider(Provider):
    def __init__(self,
        figure,
        outgoing: bs_rpc.ResponseWriter,
        incomming: Generator[bs_rpc.Body, None, None],
    ):
        self.outgoing = outgoing
        self.incomming = incomming
        self.figure = figure
        super().__init__(figure.pokes, figure.escapable, figure.xp_multiplier, figure.inv)

    @property
    def caught_pokes(self):
        return self.figure.caught_pokes

    @property
    def map(self):
        return self.figure.map

    def remove_item(self, name:str):
        self.figure.remove_item(name)

    def greet(self, fightmap: FightMap):
        return super().greet(fightmap)

    def get_decision(self, ctx: Context, fightmap: FightMap, enem
    ) -> FightDecision:
        result = self.figure.get_decision(ctx, fightmap, enem)
        self.outgoing(fight.FightDecision(result.to_dict()))

        resp = next(self.incomming)
        match resp.type:
            case fight.SEED_TYPE:
                seed: fight.SeedData = resp.data
                random.seed(seed["seed"])
            case _:
                assert False, resp.type

        return result

    def handle_defeat(self, ctx: Context, fightmap, winner):
        self.figure.handle_defeat(ctx, fightmap, winner)
