import threading

import bs_rpc
from pokete_classes.multiplayer.msg import position
from pokete_classes.multiplayer.pc_manager import pc_manager


class ComService:
    def __init__(self, client: bs_rpc.Client):
        self.client = client

    def __subscribe_position_updates(self):
        gen = self.client.call_for_responses(
            position.SubscribePosition({})
        )

        for body in gen():
            match body.get_type():
                case position.UPDATE_TYPE:
                    data: position.UpdateData = body.data
                    pc_manager.set(
                        data["name"],
                        data["position"]["map"],
                        data["position"]["x"],
                        data["position"]["y"],
                    )
                case position.REMOVE_TYPE:
                    data: position.RemoveData = body.data
                    pc_manager.remove(data["user_name"])

    def __call__(self):
        threading.Thread(
            target=self.__subscribe_position_updates,
            daemon=True
        ).start()
