"""Contains all classes needed to generate NPCs"""

import time
import logging
import random
import scrap_engine as se

from pokete.classes.asset_service.service import asset_service
from pokete.release import SPEED_OF_TIME
from pokete.base.context import Context
from pokete.base.input import get_action
from pokete.base.input_loops import ask_bool
from pokete.base import loops
from .npc_action import NPCInterface, NPCAction
from .npc_trigger import NPCTrigger
from .ui import UI
from ..asset_service.resources import Chat
from ..fight import Fight, Provider, FightDecision
from ..interactions import MultiTextChooseBox, Interactor
from ..settings import settings
from ..general import check_walk_back
from ..landscape import MapInteract


class NPC(se.Box, NPCInterface, MapInteract, Interactor):
    """An NPC to talk to"""
    npcactions: dict[str, NPCAction] = {}
    registry: dict[str, "NPC"] = {}

    @classmethod
    def set_vars(cls, npcactions: dict[str, NPCAction]):
        """Sets all variables needed by NPCs
        ARGS:
            npcactions: NPCActions class"""
        cls.npcactions = npcactions

    @classmethod
    def get(cls, name):
        """Gets a NPC from the registry
        ARGS:
            name: The NPCs name"""
        return cls.registry[name]

    def __init__(self, name, texts, _fn=None, chat: Chat | None = None,
                 side_trigger=True):
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

    def action(self):
        """Interaction with the NPC triggered by NPCTrigger.action"""
        if self.used and settings("save_trainers").val:
            return
        logging.info("[NPC][%s] Interaction", self.name)
        self.ctx.map.full_show()
        time.sleep(SPEED_OF_TIME * 0.7)
        self.exclamate()
        self.text(self.texts)
        self.func()

    def func(self):
        """The function that's executed after the interaction"""
        if self.__fn is not None:
            action = self.npcactions.get(self.__fn, None)
            if action is not None:
                action.act(self, UI(self))

    def give(self, name, item_name:str):
        """Method that gifts an item to the player
        ARGS:
            name: The displayed name of the npc
            item: Item name"""
        item = asset_service.get_items()[item_name]
        self.set_used()
        if ask_bool(self.ctx, f"{name} gifted you a '{item.pretty_name}'. \
Do you want to accept it?"):
            self.ctx.figure.give_item(item.name)

    @property
    def used(self):
        """Indicates whether or not the NPC has been used"""
        return self.name in self.ctx.figure.used_npcs

    def set_used(self):
        """Sets the NPC as used"""
        self.ctx.figure.used_npcs.append(self.name)

    def unset_used(self):
        """Sets the NPC as unused"""
        if self.used:
            self.ctx.figure.used_npcs.pop(
                self.ctx.figure.used_npcs.index(self.name))

    def chat(self):
        """Starts a question-answer chat"""
        q_a: Chat = self.q_a
        if q_a == {}:
            return
        while True:
            self.text(q_a.q)
            while get_action() is None:
                loops.std(self.ctx)
            if q_a.a == {}:
                break
            q_a = q_a.a[
                MultiTextChooseBox(
                    list(q_a.a.keys()), "Answer"
                )(self.ctx)
            ]


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

    def get_decision(self, ctx: Context, fightmap, enem) -> FightDecision:
        return FightDecision.attack(random.choices(
            self.curr.attack_obs,
            weights=[
                i.ap * (
                    1.5 if enem.curr.type.name in i.type.effective
                    else 0.5 if enem.curr.type.name in i.type.ineffective
                    else 1
                )
                for i in self.curr.attack_obs
            ]
        )[0])

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
        if self.ctx.figure.has_item("shut_the_fuck_up_stone"):
            return
        self.pokes = [p for p in self.pokes if p.hp > 0]
        if self.pokes and (not self.used
                           or not settings("save_trainers").val) \
            and self.check_walk(self.ctx.figure.x, self.ctx.figure.y):
            self.ctx.map.full_show()
            time.sleep(SPEED_OF_TIME * 0.7)
            self.exclamate()
            self.walk_point(self.ctx.figure.x, self.ctx.figure.y)
            if any(poke.hp > 0 for poke in self.ctx.figure.pokes[:6]):
                self.text(self.texts)
                winner = Fight()(
                    self.ctx,
                    [self.ctx.figure, self]
                )
                is_winner = (winner == self)
                self.text({True: self.lose_texts,
                           False: self.win_texts + ["Here's $20!"]}
                          [is_winner])
                if is_winner:
                    self.heal()
                else:
                    self.ctx.figure.add_money(20)
                    self.set_used()
                logging.info("[NPC][%s] %s against player", self.name,
                             'Lost' if not is_winner else 'Won')
            self.walk_point(o_x, o_y + (1 if o_y > self.y else -1))
            check_walk_back(self.ctx)

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
        """Function called when the providers current Pokete dies
        ARGS:
            fightmap: fightmap object
            winner: the defeating provider"""
        fightmap.death_animation(self)
        self.play_index += 1
        fightmap.add_enemy_after_choosing(winner, self)
        return True
