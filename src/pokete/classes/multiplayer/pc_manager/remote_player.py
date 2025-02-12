import scrap_engine as se

from pokete.base.color import Color
from ...interactions import Interactor, MultiTextChooseBox
from ...landscape import MapInteract


class RemotePlayer(se.Object, MapInteract, Interactor):
    """A remote player
    ARGS:
        name: The players name"""

    def __init__(self, name):
        super().__init__("a", "float")
        self.name = name
        self.name_tag = NameTag(name)
        self.interaction_choose_box = MultiTextChooseBox(
            ["fight", "cancel"],
            "Interact")

    def add(self, _map, x, y):
        """Adds the player remoteplayer to the map
        ARGS:
            _map: The map to add to
            x: X-coordinate
            y: Y-coordinate"""
        super().add(_map, x, y)
        self.add_name_tag()

    def remove(self):
        """Removes the player"""
        super().remove()
        self.name_tag.remove()

    def add_name_tag(self):
        """Add a nametag to the players position"""
        self.name_tag.add_to_movemap(self.map, self.x, self.y)

    def readd_name_tag(self):
        """Readds the nametag"""
        self.name_tag.remove()
        self.add_name_tag()


class NameTag(se.Box, MapInteract):
    """Nametag that shows the RemotePlayers name
    ARGS:
        name: The remote players name"""

    def __init__(self, name):
        super().__init__(2, len(name))
        self.pointer = se.Text("v", "float", esccode=Color.thicc)
        self.tag = (
            se.Text("[", "float", esccode=Color.thicc)
            + se.Text(name, "float", esccode=Color.green)
            + se.Text("]", "float", esccode=Color.thicc)
        )
        self.add_ob(self.tag, 0, 0)
        self.add_ob(self.pointer, round(self.width / 2), 1)

    def add_to_movemap(self, player_map, x, y):
        """Adds the nametag to movemap
        ARGS:
            player_map: The map the remte player is on
            x: The X-coordinate
            y: The Y-coordinate"""
        if player_map == self.ctx.figure.map:
            self.add(
                self.ctx.map,
                x - self.ctx.map.x - round(self.width / 2),
                y - self.ctx.map.y - 2,
            )

    def add(self, _map, x, y):
        """
        Adds the box to a certain coordinate on a certain map.
        """
        self.x = x
        self.y = y
        self.map = _map
        for obj in self.obs:
            if (
                _map.width > obj.rx + self.x >= 0
                and _map.height > obj.ry + self.y >= 0
            ):  # Avoid crashing, when out of view
                obj.add(self.map, obj.rx + self.x, obj.ry + self.y)
        self.added = True
