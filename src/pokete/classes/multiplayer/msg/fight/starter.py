from typing import TypedDict
import pokete.bs_rpc as bs_rpc

STARTER_TYPE = "pokete.fight.starter"


class StarterData(TypedDict):
    name: str


class Starter(bs_rpc.Body):
    def __init__(self, data: StarterData):
        super().__init__(STARTER_TYPE, data)
