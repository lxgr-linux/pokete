from typing import TypedDict
import bs_rpc

SEED_TYPE = "pokete.fight.seed"


class SeedData(TypedDict):
    seed: int


class Seed(bs_rpc.Body):
    def __init__(self, data: SeedData):
        super().__init__(SEED_TYPE, data)
