import pokete.bs_rpc as bs_rpc
from pokete.classes.model.fight_decision import FightDecisionData

FIGHT_DECISION_TYPE = "pokete.fight.fightDecision"


class FightDecision(bs_rpc.Body):
    def __init__(self, data: FightDecisionData):
        super().__init__(FIGHT_DECISION_TYPE, data)
