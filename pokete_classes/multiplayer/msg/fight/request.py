import threading
from typing import TypedDict

import bs_rpc
from ....input_loops import ask_bool
from ...remote_fight import remote_fight
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
        accept = ask_bool(
            rmtpl.ctx,
            f"'{name}' wants to start a fight with you"
        )
        if accept:
            threading.Thread(target=remote_fight.start, args=(rmtpl.ctx, ), daemon=True).start()
        return Response({"accept": accept})
