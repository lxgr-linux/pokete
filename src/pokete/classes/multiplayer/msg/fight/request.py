import threading
from typing import TypedDict

import pokete.bs_rpc as bs_rpc
from pokete.classes.multiplayer.remote_fight import main_thread_fight_attacher
from ....input_loops import ask_bool
from ...remote_fight import remote_fight_controller
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
        accept = main_thread_fight_attacher.set_ready(name).listen()
        return Response({"accept": accept})
