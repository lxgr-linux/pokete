import logging
import socket

import pokete.bs_rpc as bs_rpc
from pokete.base.exception_propagation import PropagatingThread
from pokete.base.context import Context
from pokete.classes.asset_service.service import asset_service
from pokete.classes.multiplayer import msg
from pokete.classes.multiplayer.exceptions import ConnectionException, \
    VersionMismatchException, UserPresentException, InvalidPokeException
from pokete.classes.multiplayer.msg import player, position, error, map_info, fight
from pokete.classes.multiplayer.msg.position.update import UpdateDict
from pokete.classes.multiplayer.pc_manager import pc_manager


class CommunicationService:
    def __init__(self):
        self.client: bs_rpc.Client
        self.saved_pos = ()
        self.__positions_channel = bs_rpc.Channel[tuple[str, int, int]]()

    def position_channel_generator(self):
        return bs_rpc.ChannelGenerator(self.__positions_channel)

    def __subscribe_position_updates(self):
        gen = self.client.call_for_responses(
            position.SubscribePosition({})
        )

        for body in gen():
            match body.get_type():
                case position.UPDATE_TYPE:
                    update_data: UpdateDict = body.data
                    pc_manager.set(
                        update_data["name"],
                        update_data["position"]["map"],
                        update_data["position"]["x"],
                        update_data["position"]["y"],
                    )
                case position.REMOVE_TYPE:
                    pos_data: position.RemoveData = body.data
                    pc_manager.remove(pos_data["user_name"])

    """def __send_position_update(self, coords: tuple[str, int, int]):
        resp = self.client.call_for_response(
            position.Update({
                "name": "",
                "position": {
                    "map": coords[0],
                    "x": coords[1],
                    "y": coords[2],
                },
            }))
        # Handle Err here
        """

    """def __send_position_updates(self):
        gen = bs_rpc.ChannelGenerator(self.__positions_channel, None)
        for coords in gen():
            threading.Thread(
                target=self.__send_position_update,
                args=(coords, ),
                daemon=True
            ).start()
    """

    def __call__(self):
        PropagatingThread(
            target=self.__subscribe_position_updates,
            daemon=True
        ).start()
        #threading.Thread(
        #    target=self.__send_position_updates,
        #    daemon=True
        #).start()

    def connect(self, host: str, port: int):
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
        PropagatingThread(
            target=listener,
            daemon=True
        ).start()

    def handshake(
        self, ctx: Context, user_name,
        version
    ):  # Here Context usage outside of the UI context
        """Sends and handles the handshake with the server"""
        resp = self.client.call_for_response(
            msg.Handshake({
                "user": {
                    "name": user_name,
                    "pokes": [p.dict() for p in ctx.figure.pokes],
                    "items": ctx.figure.inv,
                    "client": None,
                    "position": {"map": "", "x":0, "y": 0}  # Null position
                },
                "version": version,
            }))
        match resp.get_type():
            case error.VERSION_MISMATCH_TYPE:
                raise VersionMismatchException(resp.data["version"])
            case error.USER_EXISTS_TYPE:
                raise UserPresentException()
            case error.INVALID_POKE_TYPE:
                err_data: error.InvalidPokeData = resp.data
                raise InvalidPokeException(err_data["error"])
            case map_info.INFO_TYPE:
                data: map_info.InfoData = resp.data
                asset_service.load_assets(data["assets"])
                pos = data["position"]
                self.saved_pos = (
                    ctx.figure.map_name,
                    ctx.figure.oldmap_name,
                    ctx.figure.last_center_map_name,
                    ctx.figure.x,
                    ctx.figure.y,
                )
                # don't ask
                ctx.figure.map_name = pos["map"]
                ctx.figure.x = pos["x"]
                ctx.figure.y = pos["y"]
                pc_manager.waiting_users = data["users"]
                return data["greeting_text"]
            case _:
                assert False, resp.get_type()

    def request_fight(self, name: str) -> bool | None:
        resp = self.client.call_for_response(fight.Request({"name": name}))
        match resp.type:
            case fight.RESPONSE_TYPE:
                return resp.data["accept"]
            case _:
                return None

    def join_fight(self, fight_id: int) -> bs_rpc.ChannelGenerator:
        return self.client.call_for_responses(fight.Fight({"fight_id": fight_id}))

    def pos_update(self, _map:str, x:int, y:int):
        """Sends a position update to the server
        ARGS:
            _map: Name of the map the player is on
            x: X-coordinate
            y: Y-coordinate"""
        self.__positions_channel.push((_map, x, y))

    def get_player(self, name) -> player.User:
        resp = self.client.call_for_response(
            player.Get({"name": name})
        )
        logging.info(resp)
        match resp.get_type():
            case player.PLAYER_TYPE:
                data: player.PlayerData = resp.data
                return data["user"]
            case _:
                raise Exception(resp)


com_service: CommunicationService = CommunicationService()
