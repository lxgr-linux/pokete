import scrap_engine as se

from pokete_classes import ob_maps as obmp, movemap as mvp
from pokete_classes.color import Color


class RemotePlayer(se.Object):
    def __init__(self, name):
        super().__init__("a", "float")
        self.name_tag = NameTag(name)

    def add(self, _map, x, y):
        super().add(_map, x, y)
        self.add_name_tag()

    def remove(self):
        super().remove()
        self.name_tag.remove()

    def add_name_tag(self):
        self.name_tag.add_to_movemap(self.map, self.x, self.y)

    def readd_name_tag(self):
        self.name_tag.remove()
        self.add_name_tag()


class NameTag(se.Box):
    fig = None

    @classmethod
    def set_args(cls, fig):
        cls.fig = fig

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
        if player_map == self.fig.map:
            self.add(
                mvp.movemap,
                x - mvp.movemap.x - round(self.width / 2),
                y - mvp.movemap.y - 2,
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


class PCManager:
    def __init__(self):
        self.reg = {}

    def set(self, name, _map, x, y):
        if name not in self.reg:
            self.reg[name] = RemotePlayer(name)
        self.reg[name].remove()
        self.reg[name].add(obmp.ob_maps[_map], x, y)

    def remove(self, name):
        self.reg[name].remove()
        del self.reg[name]

    def movemap_move(self):
        for _, rmtpl in self.reg.items():
            rmtpl.readd_name_tag()


pc_manager = PCManager()
