"""Manages remote players"""
import logging

from .remote_player import RemotePlayer
from ..interactions import movemap_deco
from ... import ob_maps as obmp
from ...multiplayer.msg.position.update import User


class PCManager:
    """Manages remote players"""

    def __init__(self):
        self.reg: dict[str, RemotePlayer] = {}
        self.waiting_users: list[User] = []

    def set(self, name, _map, x, y):
        """Stets a remote player to a certain position
        ARGS:
            name: The players name
            _map: The maps name to add them to
            x: X-coordniate
            y: Y-ccordniate"""
        if name not in self.reg:
            self.reg[name] = RemotePlayer(name)
        self.reg[name].remove()
        self.reg[name].add(obmp.ob_maps[_map], x, y)
        self.check_interactable(self.reg[name].ctx.figure)

    def set_waiting_users(self):
        for user in self.waiting_users:
            pc_manager.set(
                user["name"],
                user["position"]["map"],
                user["position"]["x"],
                user["position"]["y"],
            )

    def remove(self, name):
        """Removes a remote player
        ARGS:
            name: The Players name"""
        pc = self.reg.get(name, None)
        if pc is None:
            logging.warning(
                "[PCManager] Trying to remove player with name `%s`, "
                "but is not present",
                name)
            return
        pc.remove()
        del self.reg[name]

    def movemap_move(self):
        """Handles the movemap moving"""
        for _, rmtpl in self.reg.items():
            rmtpl.readd_name_tag()

    def check_interactable(self, figure):
        for _, rmtpl in self.reg.items():
            if (
                rmtpl.map == figure.map and
                (figure.x - 2 <= rmtpl.x <= figure.x + 2) and
                (figure.y - 2 <= rmtpl.y <= figure.y + 2)
            ):
                movemap_deco.set_active()
                return
        movemap_deco.set_inactive()


pc_manager = PCManager()
