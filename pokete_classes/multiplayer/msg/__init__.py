import bs_rpc
from . import position, error, map_info, fight
from .handshake import Handshake


def get_registry():
    reg = bs_rpc.Registry()

    reg.register(Handshake)
    reg.register(position.Update)
    reg.register(position.SubscribePosition)
    reg.register(error.UserExists)
    reg.register(error.VersionMismatch)
    reg.register(error.PositionUnplausible)
    reg.register(position.Remove)
    reg.register(map_info.Info)
    reg.register(error.InvalidPoke)
    reg.register(fight.Request)
    reg.register(fight.Response)
    reg.register(error.UserDoesntExist)

    return reg
