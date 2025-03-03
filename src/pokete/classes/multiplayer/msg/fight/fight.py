import threading
from typing import TypedDict

import pokete.bs_rpc as bs_rpc
from ...remote_fight import remote_fight_controller

FIGHT_TYPE = "pokete.fight.fight"


class FightData(TypedDict):
    fight_id: int


class Fight(bs_rpc.Body):
    def __init__(self, data: FightData):
        super().__init__(FIGHT_TYPE, data)

    def call_for_responses(self, context, response_writer):
        chan = context.join_fight(self.data["fight_id"])
        remote_fight_controller.ready(response_writer, chan, context)
        remote_fight_controller.end.wait()
