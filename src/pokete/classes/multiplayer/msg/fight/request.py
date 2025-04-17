from typing import TypedDict

import pokete.bs_rpc as bs_rpc
from pokete.classes.multiplayer.remote_fight import MainThreatFightEvent
from pokete.base.single_event import single_event_periodic_event
from ...pc_manager import pc_manager
from .reponse import Response

REQUEST_TYPE = "pokete.fight.request"


class RequestData(TypedDict):
    name: str


class Request(bs_rpc.Body):
    def __init__(self, data: RequestData):
        super().__init__(REQUEST_TYPE, data)

    def call_for_response(self, context):
        name = self.data["name"]
        rmtpl = pc_manager.get(name)
        event = MainThreatFightEvent(name)
        single_event_periodic_event.add(event)
        accept = event.wait_accepted()
        return Response({"accept": accept})
