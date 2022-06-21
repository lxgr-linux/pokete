"""Classes related to buing stuff"""

import scrap_engine as se
from pokete_classes.hotkeys import ACTION_UP_DOWN, Action, get_action
from pokete_general_use_fns import liner
from .loops import std_loop
from .ui_elements import Box, ChooseBox
from .inv_items import invitems


class Buy:
    """Menu to buy items in, is triggered in shop
    Args:
        figure: Figure object
        _map: The se.Map the menu is shown on"""

    def __init__(self, figure, _map):
        self.box = ChooseBox(_map.height - 3, 35, "Shop")
        self.box2 = Box(7, 21)
        self.fig = figure
        self.map = _map
        self.items = [invitems.poketeball, invitems.superball,
                      invitems.healing_potion,
                      invitems.super_potion, invitems.ap_potion]
        self.box.add_c_obs([se.Text(f"{obj.pretty_name} : {obj.price}$")
                            for obj in self.items])
        self.money_label = se.Text(f"{figure.get_money()}$")
        self.desc_label = se.Text(" ")
        # adding
        self.box.add_ob(self.money_label,
                        self.box.width - 2 - len(self.money_label.text), 0)
        self.box2.add_ob(self.desc_label, 1, 1)

    def __call__(self):
        """Opens the buy menu"""
        with self.box.add(self.map, self.map.width - 35, 0):
            self.box2.add(self.map, self.box.x - 19, 3)
            self.rechar()
            self.map.show()
            while True:
                action = get_action()
                if action.triggers(*ACTION_UP_DOWN):
                    self.box.input(action)
                    self.rechar()
                elif action.triggers(Action.CANCEL):
                    break
                elif action.triggers(Action.ACCEPT):
                    obj = self.items[self.box.index.index]
                    if self.fig.get_money() - obj.price >= 0:
                        self.fig.add_money(-obj.price)
                        self.fig.give_item(obj.name)
                std_loop()
                self.map.show()
        self.box2.remove()

    def rechar(self):
        """Rechars the detail text"""
        obj = self.items[self.box.index.index]
        self.box2.name_label.rechar(obj.pretty_name)
        self.desc_label.rechar(liner(obj.desc, 19))


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
