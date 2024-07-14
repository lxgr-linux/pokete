import scrap_engine as se

from util import liner
from .items import LearnDisc, invitems
from .. import loops, deck
from .box import InvBox
from ..input import Action, get_action, _ev
from ..learnattack import LearnAttack
from ..types import types
from ..poke import upgrade_by_one_lvl
from ..ui import ask_bool, ask_ok
from ..ui.elements import ChooseBox


class Inv:
    """Inventory to see and manage items in
    ARGS:
        _map: se.Map this will be shown on"""

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
        self.map.resize_view()
        self.box.resize(self.map.height - 3, 35)
        self.box.add(self.map, self.map.width - self.box.width, 0)
        self.map.full_show()

    def set_money(self, figure):
        self.money_label.rechar(f"${figure.get_money()}")
        self.box.set_ob(self.money_label,
                        self.box.width - 2 - len(self.money_label.text), 0)

    def __call__(self, _map, pevm, figure):
        """Opens the inventory"""
        self.map = _map
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
                                    self.map,
                                    "Do you want to upgrade one of "
                                    "your Poketes by a level?",
                                    self
                                ):
                                    ex_cond = True
                                    while ex_cond:
                                        index = deck.deck(
                                            self.map, 6, label="Your deck",
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
                                    upgrade_by_one_lvl(poke, figure, self.map)
                                    items = self.rem_item(figure, obj.name,
                                                          items)
                                    ask_ok(
                                        self.map,
                                        f"{poke.name} reached level "
                                        f"{poke.lvl()}!",
                                        self
                                    )
                            elif isinstance(obj, LearnDisc):
                                if ask_bool(
                                    self.map,
                                    f"Do you want to teach "
                                    f"'{obj.attack_dict['name']}'?",
                                    self
                                ):
                                    ex_cond = True
                                    while ex_cond:
                                        index = deck.deck(
                                            self.map, 6, label="Your deck",
                                            in_fight=True
                                        )
                                        if index is None:
                                            ex_cond = False
                                            self.map.show(init=True)
                                            break
                                        poke = figure.pokes[index]
                                        if getattr(types,
                                                   obj.attack_dict['types'][0]) \
                                            in poke.types:
                                            break
                                        ex_cond = ask_bool(
                                            self.map,
                                            "You can't teach "
                                            f"'{obj.attack_dict['name']}' to "
                                            f"'{poke.name}'! \n"
                                            "Do you want to continue?",
                                            self
                                        )
                                    if not ex_cond:
                                        break
                                    if LearnAttack(poke, self.map, self) \
                                            (obj.attack_name):
                                        items = self.rem_item(figure, obj.name,
                                                              items)
                                        if len(items) == 0:
                                            break
                            break
                        loops.std(pevm=pevm, box=self.box2)
                        self.map.full_show()
                elif action.triggers(Action.REMOVE):
                    if ask_bool(
                        self.map,
                        "Do you really want to throw "
                        f"{items[self.box.index.index].pretty_name} away?",
                        self
                    ):
                        items = self.rem_item(
                            figure, items[self.box.index.index].name,
                            items
                        )
                        if len(items) == 0:
                            break
                loops.std(pevm=pevm, box=self)
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
