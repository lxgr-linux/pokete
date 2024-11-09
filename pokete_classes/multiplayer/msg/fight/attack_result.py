from typing import TypedDict

import bs_rpc

ATTACK_RESULT_TYPE = "pokete.fight.attackResult"


class AttackResultData(TypedDict):
    result: int
    attack: str | None
    item: str | None


class AttackResult(bs_rpc.Body):
    def __init__(self, data: AttackResultData):
        super().__init__(ATTACK_RESULT_TYPE, data)
