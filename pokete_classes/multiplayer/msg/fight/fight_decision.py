from typing import TypedDict

import bs_rpc

FIGHT_DECISION_TYPE = "pokete.fight.fightDecision"


class FightDecisionData(TypedDict):
    result: int
    attack: str | None
    item: str | None


class FightDecision(bs_rpc.Body):
    def __init__(self, data: FightDecisionData):
        super().__init__(FIGHT_DECISION_TYPE, data)
