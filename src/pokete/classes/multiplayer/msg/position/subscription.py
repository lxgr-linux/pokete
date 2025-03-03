import logging
import pokete.bs_rpc as bs_rpc
from pokete.bs_rpc.msg import ResponseWriter
from pokete.classes.multiplayer.msg.position.update import Update

SUBSCRIBE_POSITION_TYPE = "pokete.position.subscribe"


class SubscribePosition(bs_rpc.Body):
    def __init__(self, data):
        super().__init__(SUBSCRIBE_POSITION_TYPE, {})

    def call_for_responses(self, context, response_writer: ResponseWriter) -> None:
        gen = context.position_channel_generator()
        for coords in gen():
            response_writer(Update({
                "name": "",
                "position": {
                    "map": coords[0],
                    "x": coords[1],
                    "y": coords[2],
                },
            }))
