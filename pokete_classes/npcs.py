"""Contains all classes needed to generate NPCs"""

import time
import logging
import scrap_engine as se
from .input import ask_bool
from .inv_items import invitems
from .settings import settings


class NPCTrigger(se.Object):
    """Object on the map, that triggers a npc
    ARGS:
        npc: The NPC it belongs to"""

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
    npcactions = None
    check_walk_back = None

    @classmethod
    def set_vars(cls, mvmp, fig, _ev,
                 npcactions, check_walk_back):
        """Sets all variables needed by NPCs
        ARGS:
            mvmp: MoveMap object
            fig: Figure object
            _ev: Event object
            npcactions: NPCActions class
            check_walk_back: check_walk_back function"""
        cls.mvmp = mvmp
        cls.fig = fig
        cls._ev = _ev
        cls.npcactions = npcactions
        cls.check_walk_back = check_walk_back

    def __init__(self, name, texts, fn=None, side_trigger=True):
        super().__init__(0, 0)
        self.will = True
        self.name = name
        self.texts = texts
        self.__fn = fn
        self.main_ob = se.Object("a")
        if side_trigger:
            for i, j in zip([-1, 1, 0, 0], [0, 0, 1, -1]):
                self.add_ob(NPCTrigger(self), i, j)
        self.add_ob(self.main_ob, 0, 0)

    def text(self, text):
        """Movemap.text wrapper
        ARGS:
            text: Text that should be printed"""
        self.mvmp.text(self.x, self.y, text, self._ev)

    def exclamate(self):
        """Shows the exclamation on top of a NPC"""
        exclamation = se.Object("!")
        try:
            exclamation.add(self.mvmp, self.x - self.mvmp.x,
                            self.y - 1 - self.mvmp.y)
        except se.CoordinateError:
            pass
        self.mvmp.show()
        time.sleep(1)
        exclamation.remove()

    def action(self):
        """Interaction with the NPC triggered by NPCTrigger.action"""
        if not self.will or \
                (self.name in self.fig.used_npcs and
                        settings("save_trainers").val):
            return
        logging.info("[NPC][%s] Interaction", self.name)
        self.mvmp.full_show()
        time.sleep(0.7)
        self.exclamate()
        self.text(self.texts)
        self.fn()

    def fn(self):
        """The function that's executed after the interaction"""
        if self.__fn is not None:
            getattr(self.npcactions, self.__fn)(self)

    def check_walk(self, x, y):
        """Checks whether the NPC can walk to a point or not
        ARGS:
            x: X-coordinate
            y: Y-coordinate
        RETURNS:
            bool: Whether or not the walk is possible"""
        vec = se.Line(" ", x - self.x, y - self.y)
        ret = not any([any(j.state == "solid"
                           for j in
                            self.map.obmap[i.ry + self.y][i.rx + self.x])
                                for i in vec.obs][1:])
        logging.info("[NPC][%s] %s walk check to (%d|%d)",
                          self.name, 'Succeeded' if ret else 'Failed', x, y)
        return ret

    def walk_point(self, x, y):
        """Walks the NPC tp a certain point
        ARGS:
            x: X-coordinate
            y: Y-coordinate
        RETURNS:
            bool: Whether or not the walk succeeded"""
        o_x = self.x
        o_y = self.y
        vec = se.Line(" ", x - o_x, y - o_y)
        if not self.check_walk(x, y):
            return False
        for i in vec.obs:
            self.set(i.rx + o_x, i.ry + o_y)
            self.mvmp.full_show()
            time.sleep(0.2)
        return True

    def give(self, name, item):
        """Method that gifts an item to the player
        ARGS:
            name: The displayed name of the npc
            item: Item name"""
        item = getattr(invitems, item)
        self.will = False
        self.fig.used_npcs.append(self.name)
        if ask_bool(self._ev, self.mvmp,
                    f"{name} gifted you a '{item.pretty_name}'. \
Do you want to accept it?"):
            self.fig.give_item(item.name)


class Trainer(NPC):
    """Trainer class to fight against"""

    def __init__(self, poke, name, gender, texts, lose_texts,
                 win_texts, fight):
        super().__init__(name, texts, side_trigger=False)
        # attributes
        self.gender = gender
        self.poke = poke
        self.lose_texts = lose_texts
        self.win_texts = win_texts
        self.fight = fight

    def add(self, _map, x, y):
        """Add wrapper
        See se.Box.add"""
        line = se.Line(" ", 0, _map.height, state="float")
        for i, obj in enumerate(line.obs):
            line.obs[i] = NPCTrigger(self)
            line.obs[i].rx = obj.rx
            line.obs[i].ry = obj.ry
        line.add(_map, x, 0)
        super().add(_map, x, y)

    def action(self):
        """Interaction with the trainer"""
        o_x = self.x
        o_y = self.y
        if self.fig.has_item("shut_the_fuck_up_stone"):
            return
        if self.poke.hp > 0 and (self.name not in self.fig.used_npcs \
                                    or not settings("save_trainers").val) \
                and self.check_walk(self.fig.x, self.fig.y):
            self.mvmp.full_show()
            time.sleep(0.7)
            self.exclamate()
            self.walk_point(self.fig.x, self.fig.y)
            if any(poke.hp > 0 for poke in self.fig.pokes[:6]):
                self.text(self.texts)
                winner = self.fight([poke for poke in self.fig.pokes[:6]
                                    if poke.hp > 0][0],
                                    self.poke,
                                    info={"type": "duel", "player": self})
                self.text({True: self.lose_texts,
                           False: self.win_texts + [" < Here u go 20$"]}
                                [winner == self.poke])
                if winner != self.poke:
                    self.fig.add_money(20)
                    self.fig.used_npcs.append(self.name)
                logging.info("[NPC][%s] %s against player", self.name,
                                  'Lost' if  winner != self.poke else 'Won')
            self.walk_point(o_x, o_y + (1 if o_y > self.y else -1))
            self.check_walk_back()
