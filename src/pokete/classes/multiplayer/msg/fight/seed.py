from typing import TypedDict

from pokete import bs_rpc

SEED_TYPE = "pokete.fight.seed"


class SeedData(TypedDict):
    seed: int


class Seed(bs_rpc.Body):
    def __init__(self, data: SeedData) -> None:
        super().__init__(SEED_TYPE, data)
