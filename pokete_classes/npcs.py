"""Contains all classes needed to generate NPCs"""

import time
import scrap_engine as se
from .input import ask_bool


class NPCTrigger(se.Object):
    """Object on the map, that triggers a npc"""

    def __init__(self, npc):
        super().__init__(" ", state="float")
        self.npc = npc

    def action(self, ob):
        """Action triggers the NPCs action"""
        self.npc.action()


class NPC(se.Box):
    """An NPC to talk to"""
    mvmp = None
    fig = None
    _ev = None
    invitems = None
    used_ncps = None
    settings = None
    npcactions = None

    @classmethod
    def set_vars(cls, mvmp, fig, _ev, invitems, used_npcs,
                 settings, npcactions):
        """Sets all variables needed by NPCs"""
        cls.mvmp = mvmp
        cls.fig = fig
        cls._ev = _ev
        cls.invitems = invitems
        cls.used_npcs = used_npcs
        cls.settings = settings
        cls.npcactions = npcactions

    def __init__(self, name, texts, fn=None):
        super().__init__(0, 0)
        self.will = True
        self.name = name
        self.texts = texts
        self.__fn = fn
        for i, j in zip([-1, 1, 0, 0], [0, 0, 1, -1]):
            self.add_ob(NPCTrigger(self), i, j)
        self.add_ob(se.Object("a"), 0, 0)

    def text(self, text):
        """Movemap.text wrapper"""
        self.mvmp.text(self.x, self.y, text, self._ev)

    def exclamate(self):
        """Shows the exclamation on top of a NPC"""
        exclamation = se.Object("!")
        try:
            exclamation.add(self.mvmp, self.x - self.mvmp.x, self.y - 1 - self.mvmp.y)
        except se.CoordinateError:
            pass
        self.mvmp.show()
        time.sleep(1)
        exclamation.remove()

    def action(self):
        """Interaction with the NPC triggered by NPCTrigger.action"""
        if not self.will or (self.name in self.used_npcs and self.settings.save_trainers):
            return
        self.mvmp.full_show()
        time.sleep(0.7)
        self.exclamate()
        self.text(self.texts)
        self.fn()

    def fn(self):
        """The function that's executed after the interaction"""
        if self.__fn is not None:
            getattr(self.npcactions, self.__fn)(self)

    def walk_point(self, x, y):
        """Walks the NPC tp a certain point"""
        o_x = self.x
        o_y = self.y
        vec = se.Line(" ", x - o_x, y - o_y)
        if any([any(j.state == "solid"
                for j in self.map.obmap[i.ry + o_y][i.rx + o_x])
                    for i in vec.obs][1:]):
            return False
        for i in vec.obs:
            self.set(i.rx + o_x, i.ry + o_y)
            time.sleep(0.2)
            self.mvmp.full_show()
        return True

    def give(self, name, item):
        """Method thats gifts an item to the player"""
        item = getattr(self.invitems, item)
        self.will = False
        self.used_npcs.append(self.name)
        if ask_bool(self._ev, self.mvmp,
                    f"{name} gifted you a '{item.pretty_name}'. \
Do you want to accept it?"):
            self.fig.give_item(item.name)

