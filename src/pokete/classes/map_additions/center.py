import random
import time

import scrap_engine as se

from pokete.base.input import _ev
from pokete.classes import deck
from pokete.classes import movemap as mvp
from pokete.classes.classes import PlayMap
from pokete.classes.doors import CenterDoor
from pokete.classes.interactions.multi_text_choose_box import MultiTextChooseBox
from pokete.classes.inv import buy
from pokete.classes.landscape import MapInteract
from pokete.release import SPEED_OF_TIME

CUDDLE_MESSAGES = [
    "{name} nuzzles against you affectionately!",
    "{name} nuzzles against you lovingly!",
    "{name} nuzzles against you happily!",
    "{name} purrs contentedly in your arms!",
    "{name} looks up at you with adoring eyes!",
    "{name} snuggles closer to you!",
]


class CenterMap(PlayMap):
    """Contains all relevant objects for centermap
    ARGS:
        _he: The maps height
        _wi: The maps width"""

    def __init__(self, _he, _wi):
        super().__init__(
            _he,
            _wi,
            name="centermap",
            pretty_name="Pokete-Center",
            song="Map.mp3",
        )
        self.inner = se.Text(
            """ ________________
 |______________|
 |     |a |     |
 |     ¯ ¯¯     |
 |              |
 |______  ______|
 |_____|  |_____|""",
            ignore=" ",
        )

        self.interact = CenterInteract("¯", state="float")
        self.dor_back1 = CenterDoor(" ", state="float")
        self.dor_back2 = CenterDoor(" ", state="float")
        # self.trader = NPC("trader",
        #                  ["I'm a trader.",
        #                   "Here you can trade one of your Poketes for \
        # one from another trainer."],
        #                         "swap_poke")
        # adding
        self.dor_back1.add(self, int(self.width / 2), 8)
        self.dor_back2.add(self, int(self.width / 2) + 1, 8)
        self.inner.add(self, int(self.width / 2) - 8, 1)
        self.interact.add(self, int(self.width / 2), 4)
        # self.trader.add(self, int(self.width / 2) - 6, 3)


class ShopMap(PlayMap):
    """Contains all relevant objects for shopmap
    ARGS:
        _he: The maps height
        _wi: The maps width"""

    def __init__(self, _he, _wi):
        super().__init__(
            _he, _wi, name="shopmap", pretty_name="Pokete-Shop", song="Map.mp3"
        )
        self.inner = se.Text(
            """ __________________
 |________________|
 |      |a |      |
 |      ¯ ¯¯      |
 |                |
 |_______  _______|
 |______|  |______|""",
            ignore=" ",
        )
        self.interact = ShopInteract("¯", state="float")
        self.dor_back1 = CenterDoor(" ", state="float")
        self.dor_back2 = CenterDoor(" ", state="float")
        # adding
        self.dor_back1.add(self, int(self.width / 2), 8)
        self.dor_back2.add(self, int(self.width / 2) + 1, 8)
        self.inner.add(self, int(self.width / 2) - 9, 1)
        self.interact.add(self, int(self.width / 2), 4)


class CenterInteract(se.Object, MapInteract):
    """Triggers a conversation in the Pokete center"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menu = MultiTextChooseBox(
            [
                "See your full deck",
                "Heal all your Poketes",
                "Cuddle with the Poketes",
                "Quit",
            ],
            "Select",
        )

    def __normalize_pokes(self, ob):
        while "__fallback__" in [p.identifier for p in ob.pokes]:
            ob.pokes.pop([p.identifier for p in ob.pokes].index("__fallback__"))

    def action(self, ob):
        """Triggers the interaction in the Pokete center
        ARGS:
            ob: The object triggering this action"""
        _ev.clear()
        mvp.movemap.full_show()
        mvp.movemap.text(
            self.ctx,
            mvp.movemap.bmap.inner.x - mvp.movemap.x + 8,
            3,
            [
                "Welcome to the Pokete-Center",
                "What do you want to do?",
            ],
        )

        match self.menu(self.ctx)[0]:
            case 0:
                self.__normalize_pokes(ob)
                ob.balls_label_rechar()
                deck.deck(self.ctx, len(ob.pokes))
            case 1:
                ob.heal()
                time.sleep(SPEED_OF_TIME * 0.5)
                mvp.movemap.text(
                    self.ctx,
                    mvp.movemap.bmap.inner.x - mvp.movemap.x + 8,
                    3,
                    ["...", "Your Poketes are now healed!"],
                )
            case 2:
                self.__normalize_pokes(ob)
                if ob.pokes:
                    selected_idx = deck.deck(
                        self.ctx,
                        len(ob.pokes),
                        label="Choose a Pokete to cuddle",
                        in_fight=True,
                    )
                    if selected_idx is not None:
                        poke = ob.pokes[selected_idx]
                        message = random.choice(CUDDLE_MESSAGES).format(
                            name=poke.name
                        )
                        mvp.movemap.text(
                            self.ctx,
                            mvp.movemap.bmap.inner.x - mvp.movemap.x + 8,
                            3,
                            ["...", message],
                        )
                else:
                    mvp.movemap.text(
                        self.ctx,
                        mvp.movemap.bmap.inner.x - mvp.movemap.x + 8,
                        3,
                        ["You don't have any Poketes to cuddle with!"],
                    )
        mvp.movemap.full_show(init=True)


class ShopInteract(se.Object, MapInteract):
    """Triggers an conversation in the shop"""

    def action(self, ob):
        """Triggers an interaction in the shop
        ARGS:
            ob: The object triggering this action"""
        _ev.clear()
        mvp.movemap.full_show()
        mvp.movemap.text(
            self.ctx,
            mvp.movemap.bmap.inner.x - mvp.movemap.x + 9,
            3,
            ["Welcome to the Pokete-Shop", "Wanna buy something?"],
        )
        buy(self.ctx)
        mvp.movemap.full_show(init=True)
        mvp.movemap.text(
            self.ctx,
            mvp.movemap.bmap.inner.x - mvp.movemap.x + 9,
            3,
            ["Have a great day!"],
        )
