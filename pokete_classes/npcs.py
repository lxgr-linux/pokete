"""Contains all classes needed to generate NPCs"""

import time
import logging
import random
import scrap_engine as se
from pokete_classes.general import heal
import pokete_classes.fightmap as fm
from pokete_classes.hotkeys import ACTION_UP_DOWN, Action, get_action
import pokete_classes.movemap as mvp
from .providers import Provider
from .loops import std_loop
from .input import ask_bool
from .inv_items import invitems
from .settings import settings
from .ui_elements import ChooseBox
from .general import check_walk_back
from release import SPEED_OF_TIME


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
    fig = None
    npcactions = None
    registry = {}

    @classmethod
    def set_vars(cls, fig, npcactions):
        """Sets all variables needed by NPCs
        ARGS:
            fig: Figure object
            npcactions: NPCActions class"""
        cls.fig = fig
        cls.npcactions = npcactions

    @classmethod
    def get(cls, name):
        """Gets a NPC from the registry
        ARGS:
            name: The NPCs name"""
        return cls.registry[name]

    def __init__(self, name, texts, fn=None, chat=None, side_trigger=True):
        super().__init__(0, 0)
        self.name = name
        self.texts = texts
        self.__fn = fn
        if chat is None:
            self.q_a = {}
        else:
            self.q_a = chat
        self.main_ob = se.Object("a")
        if side_trigger:
            for i, j in zip([-1, 1, 0, 0], [0, 0, 1, -1]):
                self.add_ob(NPCTrigger(self), i, j)
        self.add_ob(self.main_ob, 0, 0)
        NPC.registry[self.name] = self

    def text(self, text):
        """Movemap.text wrapper
        ARGS:
            text: Text that should be printed"""
        mvp.movemap.text(self.x, self.y, text)

    def exclamate(self):
        """Shows the exclamation on top of a NPC"""
        exclamation = se.Object("!")
        try:
            exclamation.add(mvp.movemap, self.x - mvp.movemap.x,
                            self.y - 1 - mvp.movemap.y)
        except se.CoordinateError:
            pass
        mvp.movemap.show()
        time.sleep(SPEED_OF_TIME * 1)
        exclamation.remove()

    def action(self):
        """Interaction with the NPC triggered by NPCTrigger.action"""
        if self.used and settings("save_trainers").val:
            return
        logging.info("[NPC][%s] Interaction", self.name)
        mvp.movemap.full_show()
        time.sleep(SPEED_OF_TIME * 0.7)
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
            mvp.movemap.full_show()
            time.sleep(SPEED_OF_TIME * 0.2)
        return True

    def give(self, name, item):
        """Method that gifts an item to the player
        ARGS:
            name: The displayed name of the npc
            item: Item name"""
        item = getattr(invitems, item)
        self.set_used()
        if ask_bool(mvp.movemap, f"{name} gifted you a '{item.pretty_name}'. \
Do you want to accept it?"):
            self.fig.give_item(item.name)

    @property
    def used(self):
        """Indicates whether or not the NPC has been used"""
        return self.name in self.fig.used_npcs

    def set_used(self):
        """Sets the NPC as used"""
        self.fig.used_npcs.append(self.name)

    def unset_used(self):
        """Sets the NPC as unused"""
        if self.used:
            self.fig.used_npcs.pop(self.fig.used_npcs.index(self.name))

    def chat(self):
        """Starts a question-answer chat"""
        q_a = self.q_a
        if q_a == {}:
            return
        while True:
            self.text(q_a["q"])
            while get_action() == None:
                std_loop()
            if q_a["a"] == {}:
                break
            keys = list(q_a["a"].keys())
            c_b = ChooseBox(len(keys) + 2,
                            sorted(len(i) for i in keys)[-1] + 6,
                            name="Answer",
                            c_obs=[se.Text(i, state="float")
                                     for i in keys])
            c_b.frame.corners[0].rechar("^")
            mvp.movemap.assure_distance(self.fig.x, self.fig.y,
                                        c_b.width + 2, c_b.height + 2)
            with c_b.add(mvp.movemap, self.fig.x - mvp.movemap.x,
                         self.fig.y - mvp.movemap.y + 1):
                while True:
                    action = get_action()
                    if action.triggers(*ACTION_UP_DOWN):
                        c_b.input(action)
                        mvp.movemap.show()
                    elif action.triggers(Action.ACCEPT):
                        key = keys[c_b.index.index]
                        break
                    std_loop()
            q_a = q_a["a"][key]


class Trainer(NPC, Provider):
    """Trainer class to fight against"""

    def __init__(self, pokes, name, gender, texts, lose_texts,
                 win_texts):
        NPC.__init__(self, name, texts, side_trigger=False)
        Provider.__init__(self, pokes)
        # attributes
        self.gender = gender
        self.lose_texts = lose_texts
        self.win_texts = win_texts

    def get_attack(self, fightmap, enem):
        return random.choices(
            self.curr.attack_obs,
            weights=[
                i.ap * (
                    1.5 if enem.curr.type.name in i.type.effective
                    else 0.5 if enem.curr.type.name in i.type.ineffective
                    else 1
                )
                for i in self.curr.attack_obs
            ]
        )[0]

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
        self.pokes = [p for p in self.pokes if p.hp > 0]
        if self.pokes and (not self.used
                                 or not settings("save_trainers").val) \
                and self.check_walk(self.fig.x, self.fig.y):
            mvp.movemap.full_show()
            time.sleep(SPEED_OF_TIME * 0.7)
            self.exclamate()
            self.walk_point(self.fig.x, self.fig.y)
            if any(poke.hp > 0 for poke in self.fig.pokes[:6]):
                self.text(self.texts)
                winner = fm.fightmap.fight(
                    [self.fig, self]
                )
                is_winner = (winner == self)
                self.text({True: self.lose_texts,
                           False: self.win_texts + ["Here's $20!"]}
                          [is_winner])
                heal(self) if is_winner else None
                if not is_winner:
                    self.fig.add_money(20)
                    self.set_used()
                logging.info("[NPC][%s] %s against player", self.name,
                             'Lost' if not is_winner else 'Won')
            self.walk_point(o_x, o_y + (1 if o_y > self.y else -1))
            check_walk_back(self.fig)
