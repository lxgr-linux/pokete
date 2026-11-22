from typing import TypedDict

from pokete import bs_rpc

STARTER_TYPE = "pokete.fight.starter"


class StarterData(TypedDict):
    name: str


class Starter(bs_rpc.Body):
    def __init__(self, data: StarterData) -> None:
        super().__init__(STARTER_TYPE, data)
