import threading
import socket

import bs_rpc
from pokete_classes.generate import gen_maps, gen_obs
from pokete_classes.multiplayer import msg
from pokete_classes.multiplayer.exceptions import ConnectionException, \
    VersionMismatchException, UserPresentException
from pokete_classes.multiplayer.msg import position, error, map_info
from pokete_classes.multiplayer.msg.position.update import User
from pokete_classes.multiplayer.pc_manager import pc_manager
from pokete_classes import ob_maps as obmp, roadmap


class CommunicationService:
    def __init__(self):
        self.client: bs_rpc.Client | None = None

    def __subscribe_position_updates(self):
        gen = self.client.call_for_responses(
            position.SubscribePosition({})
        )

        for body in gen():
            match body.get_type():
                case position.UPDATE_TYPE:
                    data: User = body.data
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

    def connect(self, host: str, port: str):
        con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            con.connect((host, port))
        except Exception as e:
            raise ConnectionException(e)

        def listener():
            try:
                self.client.listen(self)
            finally:
                con.close()

        self.client = bs_rpc.Client(con, msg.get_registry())
        threading.Thread(
            target=listener,
            daemon=True
        ).start()

    def handshake(self, context, user_name, version):
        """Sends and handles the handshake with the server"""
        resp = self.client.call_for_response(
            msg.Handshake({
                "user_name": user_name,
                "version": version
            }))
        match resp.get_type():
            case error.VERSION_MISMATCH_TYPE:
                raise VersionMismatchException(resp.data["version"])
            case error.USER_EXISTS_TYPE:
                raise UserPresentException()
            case map_info.INFO_TYPE:
                data: map_info.InfoData = resp.data
                obmp.ob_maps = gen_maps(data["maps"], fix_center=True)
                gen_obs(
                    data["obmaps"],
                    data["npcs"],
                    data["trainers"],
                    context.figure,
                )
                roadmap.roadmap = roadmap.RoadMap(
                    context.figure,
                    data["map_stations"]
                )
                pos = data["position"]
                context.saved_pos = (
                    context.figure.map.name,
                    context.figure.oldmap.name,
                    context.figure.last_center_map.name,
                    context.figure.x,
                    context.figure.y,
                )
                context.figure.remove()
                context.figure.add(obmp.ob_maps[pos["map"]], pos["x"], pos["y"])
                for user in data["users"]:
                    pc_manager.set(
                        user["name"],
                        user["position"]["map"],
                        user["position"]["x"],
                        user["position"]["y"],
                    )
                return data["greeting_text"]

    def pos_update(self, _map, x, y):
        """Sends a position update to the server
        ARGS:
            _map: Name of the map the player is on
            x: X-coordinate
            y: Y-coordinate"""
        resp = self.client.call_for_response(
            position.Update({
                "name": "",
                "position": {
                    "map": _map,
                    "x": x,
                    "y": y,
                },
                "client": None
            }))


com_service: CommunicationService = CommunicationService()
