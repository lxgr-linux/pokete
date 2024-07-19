"""Contains all classes needed to generate NPCs"""

import time
import logging
import random
import scrap_engine as se
from release import SPEED_OF_TIME
from .context import Context
from .fight import Fight, Provider
from .input import ACTION_UP_DOWN, Action, get_action
from .input_loops import ask_bool
from .inv import invitems
from .ui.elements import ChooseBox
from .general import check_walk_back
from . import movemap as mvp, loops, settings


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
    ctx: Context = None
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

    def __init__(self, name, texts, _fn=None, chat=None, side_trigger=True):
        super().__init__(0, 0)
        self.name = name
        self.texts = texts
        self.__fn = _fn
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
        mvp.movemap.text(self.ctx, self.x, self.y, text)

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
        if self.used and settings.settings("save_trainers").val:
            return
        logging.info("[NPC][%s] Interaction", self.name)
        mvp.movemap.full_show()
        time.sleep(SPEED_OF_TIME * 0.7)
        self.exclamate()
        self.text(self.texts)
        self.func()

    def func(self):
        """The function that's executed after the interaction"""
        if self.__fn is not None:
            getattr(self.npcactions, self.__fn)(self)

    def check_walk(self, _x, _y):
        """Checks whether the NPC can walk to a point or not
        ARGS:
            _x: X-coordinate
            _y: Y-coordinate
        RETURNS:
            bool: Whether or not the walk is possible"""
        vec = se.Line(" ", _x - self.x, _y - self.y)
        ret = not any([any(j.state == "solid"
                           for j in
                           self.map.obmap[i.ry + self.y][i.rx + self.x])
                       for i in vec.obs][1:])
        logging.info("[NPC][%s] %s walk check to (%d|%d)",
                     self.name, 'Succeeded' if ret else 'Failed', _x, _y)
        return ret

    def walk_point(self, _x, _y):
        """Walks the NPC tp a certain point
        ARGS:
            _x: X-coordinate
            _y: Y-coordinate
        RETURNS:
            bool: Whether or not the walk succeeded"""
        o_x = self.x
        o_y = self.y
        vec = se.Line(" ", _x - o_x, _y - o_y)
        if not self.check_walk(_x, _y):
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
        if ask_bool(self.ctx, f"{name} gifted you a '{item.pretty_name}'. \
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
            while get_action() is None:
                loops.std(mvp.movemap)
                mvp.movemap.show()
            if q_a["a"] == {}:
                break
            q_a = q_a["a"][
                MultiTextChooseBox(
                    list(q_a["a"].keys())
                )(self.ctx)
            ]


class MultiTextChooseBox(ChooseBox):
    """ChooseBox wrapper for multitext conversations"""

    def __init__(self, keys):
        super().__init__(
            len(keys) + 2,
            sorted(len(i) for i in keys)[-1] + 6,
            name="Answer",
            c_obs=[se.Text(i, state="float") for i in keys],
        )
        self.fig = None
        self.keys = keys

    def resize_view(self):
        """Manages recursive view resizing"""
        self.remove()
        self.overview.resize_view()
        mvp.movemap.assure_distance(
            self.fig.x, self.fig.y,
            self.width + 2, self.height + 2
        )
        self.add(
            mvp.movemap,
            self.fig.x - mvp.movemap.x,
            self.fig.y - mvp.movemap.y + 1
        )

    def __call__(self, ctx: Context) -> int:
        self.set_ctx(ctx)
        self.fig = ctx.figure
        self.frame.corners[0].rechar("^")
        mvp.movemap.assure_distance(self.fig.x, self.fig.y,
                                    self.width + 2, self.height + 2)
        with self.add(ctx.map, self.fig.x - mvp.movemap.x,
                      self.fig.y - mvp.movemap.y + 1):
            while True:
                action = get_action()
                if action.triggers(*ACTION_UP_DOWN):
                    self.input(action)
                    mvp.movemap.full_show()
                elif action.triggers(Action.ACCEPT):
                    key = self.keys[self.index.index]
                    break
                loops.std(ctx.with_overview(self))
                mvp.movemap.full_show()
        return key


class Trainer(NPC, Provider):
    """Trainer class to fight against"""

    def __init__(self, pokes, name, gender, texts, lose_texts,
                 win_texts):
        NPC.__init__(self, name, texts, side_trigger=False)
        Provider.__init__(self, pokes, escapable=False, xp_multiplier=2)
        # attributes
        self.gender = gender
        self.lose_texts = lose_texts
        self.win_texts = win_texts
        self.trainer = True

    def get_attack(self, ctx: Context, fightmap, enem):
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
                           or not settings.settings("save_trainers").val) \
            and self.check_walk(self.fig.x, self.fig.y):
            mvp.movemap.full_show()
            time.sleep(SPEED_OF_TIME * 0.7)
            self.exclamate()
            self.walk_point(self.fig.x, self.fig.y)
            if any(poke.hp > 0 for poke in self.fig.pokes[:6]):
                self.text(self.texts)
                winner = Fight()(
                    self.ctx,
                    [self.fig, self]
                )
                is_winner = (winner == self)
                self.text({True: self.lose_texts,
                           False: self.win_texts + ["Here's $20!"]}
                          [is_winner])
                if is_winner:
                    self.heal()
                else:
                    self.fig.add_money(20)
                    self.set_used()
                logging.info("[NPC][%s] %s against player", self.name,
                             'Lost' if not is_winner else 'Won')
            self.walk_point(o_x, o_y + (1 if o_y > self.y else -1))
            check_walk_back(self.fig)

    def greet(self, fightmap):
        """Outputs a greeting text at the fights start:
        ARGS:
            fightmap: fightmap object"""
        fightmap.outp.outp(f"{self.name} started a fight!")
        time.sleep(SPEED_OF_TIME * 1)
        fightmap.outp.outp(
            f'{fightmap.outp.text}\n{self.gender} used {self.curr.name} '
            'against you!'
        )

    def handle_defeat(self, ctx: Context, fightmap, winner):
        """Function caleld when the providers current Pokete dies
        ARGS:
            fightmap: fightmap object
            winner: the defeating provider"""
        time.sleep(SPEED_OF_TIME * 1)
        ico = self.curr.ico
        fightmap.fast_change(
            [ico, fightmap.deadico1, fightmap.deadico2],
            ico
        )
        fightmap.deadico2.remove()
        fightmap.show()
        fightmap.clean_up(self)
        self.play_index += 1
        fightmap.__add_1(winner, self)
        ico = self.curr.ico
        fightmap.fast_change(
            [ico, fightmap.deadico2, fightmap.deadico1, ico],
            ico
        )
        fightmap.outp.outp(f"{self.name} used {self.curr.name}!")
        fightmap.show()
        time.sleep(SPEED_OF_TIME * 2)
        return True
