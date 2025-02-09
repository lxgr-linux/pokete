import pokete.bs_rpc as bs_rpc
from . import position, error, map_info, fight, player
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
    reg.register(fight.FightDecision)
    reg.register(fight.Fight)
    reg.register(player.Player)
    reg.register(player.Get)
    reg.register(fight.Starter)
    reg.register(fight.Seed)

    return reg
