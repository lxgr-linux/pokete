import scrap_engine as se

from pokete.util import liner
from pokete.base import loops
from pokete.base.context import Context
from pokete.base.input import Action, get_action, _ev
from pokete.base.input_loops import ask_bool, ask_ok
from pokete.base.ui import Overview
from pokete.base.ui.elements import ChooseBox
from .items import LearnDisc, invitems
from .box import InvBox
from .. import deck
from ..learnattack import LearnAttack
from ..types import types
from ..poke import upgrade_by_one_lvl


class Inv(Overview):
    """Inventory to see and manage items in"""

    def __init__(self):
        self.map = None
        self.box = ChooseBox(50, 35, "Inventory",
                             f"{Action.REMOVE.mapping}:remove")
        self.box2 = InvBox(7, 21, overview=self)
        self.money_label = se.Text("$0")
        self.desc_label = se.Text(" ")
        # adding
        self.box.add_ob(self.money_label,
                        self.box.width - 2 - len(self.money_label.text), 0)
        self.box2.add_ob(self.desc_label, 1, 1)

    def resize_view(self):
        """Manages recursive view resizing"""
        self.box.remove()
        self.box.overview.resize_view()
        self.box.resize(self.map.height - 3, 35)
        self.box.add(self.map, self.map.width - self.box.width, 0)
        self.map.full_show()

    def set_money(self, figure):
        self.money_label.rechar(f"${figure.get_money()}")
        self.box.set_ob(self.money_label,
                        self.box.width - 2 - len(self.money_label.text), 0)

    def __call__(self, ctx: Context):
        """Opens the inventory"""
        self.map = ctx.map
        self.box.overview = ctx.overview
        self.box.set_ctx(ctx)
        figure = ctx.figure
        _ev.clear()
        items = self.add(figure)
        self.box.resize(self.map.height - 3, 35)
        self.set_money(figure)
        with self.box.add(self.map, self.map.width - 35, 0):
            while True:
                action = get_action()
                if action.triggers(Action.UP, Action.DOWN):
                    self.box.input(action)
                elif action.triggers(Action.CANCEL):
                    break
                elif action.triggers(Action.ACCEPT):
                    obj = items[self.box.index.index]
                    self.box2.name_label.rechar(obj.pretty_name)
                    self.desc_label.rechar(liner(obj.desc, 19))
                    self.box2.add(self.map, self.box.x - 19, 3)
                    while True:
                        action = get_action()
                        if (
                            action.triggers(Action.CANCEL)
                            or action.triggers(Action.ACCEPT)
                        ):
                            self.box2.remove()
                            if obj.name == "treat":
                                if ask_bool(
                                    ctx.with_overview(self),
                                    "Do you want to upgrade one of "
                                    "your Poketes by a level?",
                                ):
                                    ex_cond = True
                                    while ex_cond:
                                        index = deck.deck(
                                            ctx.with_overview(self), 6,
                                            label="Your deck",
                                            in_fight=True
                                        )
                                        if index is None:
                                            ex_cond = False
                                            self.map.show(init=True)
                                            break
                                        poke = figure.pokes[index]
                                        break
                                    if not ex_cond:
                                        break
                                    upgrade_by_one_lvl(
                                        ctx.with_overview(self),
                                        poke
                                    )
                                    items = self.rem_item(figure, obj.name,
                                                          items)
                                    ask_ok(
                                        ctx.with_overview(self),
                                        f"{poke.name} reached level "
                                        f"{poke.lvl()}!",

                                    )
                            elif isinstance(obj, LearnDisc):
                                if ask_bool(
                                    ctx.with_overview(self),
                                    f"Do you want to teach "
                                    f"'{obj.attack['name']}'?",
                                ):
                                    ex_cond = True
                                    while ex_cond:
                                        index = deck.deck(
                                            ctx.with_overview(self), 6,
                                            label="Your deck",
                                            in_fight=True
                                        )
                                        if index is None:
                                            ex_cond = False
                                            self.map.show(init=True)
                                            break
                                        poke = figure.pokes[index]
                                        if getattr(types,
                                                   obj.attack['types'][0]) \
                                            in poke.types:
                                            break
                                        ex_cond = ask_bool(
                                            ctx.with_overview(self),
                                            "You can't teach "
                                            f"'{obj.attack['name']}' to "
                                            f"'{poke.name}'! \n"
                                            "Do you want to continue?",
                                        )
                                    if not ex_cond:
                                        break
                                    if LearnAttack(poke)(
                                        ctx.with_overview(self),
                                        obj.attack_name
                                    ):
                                        items = self.rem_item(figure, obj.name,
                                                              items)
                                        if len(items) == 0:
                                            break
                            break
                        loops.std(ctx=ctx.with_overview(self.box2))
                        self.map.full_show()
                elif action.triggers(Action.REMOVE):
                    if ask_bool(
                        ctx.with_overview(self),
                        "Do you really want to throw "
                        f"{items[self.box.index.index].pretty_name} away?"
                    ):
                        items = self.rem_item(
                            figure, items[self.box.index.index].name,
                            items
                        )
                        if len(items) == 0:
                            break
                loops.std(ctx=ctx.with_overview(self))
                self.map.full_show()
        self.box.remove_c_obs()

    def rem_item(self, figure, name, items):
        """Removes an item from the inv
        ARGS:
            name: Items name
            items: List of Items
        RETURNS:
            List of Items"""
        figure.remove_item(name)
        for obj in self.box.c_obs:
            obj.remove()
        self.box.remove_c_obs()
        items = self.add(figure)
        if not items:
            return items
        if self.box.index.index >= len(items):
            self.box.set_index(len(items) - 1)
        return items

    def add(self, figure):
        """Adds all items to the box
        RETURNS:
            List of Items"""
        items = [getattr(invitems, i) for i in figure.inv if figure.inv[i] > 0]
        self.box.add_c_obs(
            [
                se.Text(
                    f"{i.pretty_name}s : {figure.inv[i.name]}",
                    state="float"
                )
                for i in items
            ]
        )
        return items


inv = Inv()
