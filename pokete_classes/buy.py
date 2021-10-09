import time
import scrap_engine as se
from pokete_classes.ui_elements import Box, ChooseBox
from pokete_general_use_fns import std_loop, liner


class Buy:
    """Menu to buy items in, is triggered in shop"""

    def __init__(self, figure, Inv, _map):
        self.box = ChooseBox(_map.height - 3, 35, "Shop")
        self.box2 = Box(7, 21)
        self.fig = figure
        self.map = _map
        self.items = [Inv.poketeball, Inv.superball, Inv.healing_potion,
                      Inv.super_potion, Inv.ap_potion]
        self.box.add_c_obs([se.Text(f"{obj.pretty_name} : {obj.price}$")
                            for obj in self.items])
        self.money_label = se.Text(f"{figure.get_money()}$")
        self.desc_label = se.Text(" ")
        # adding
        self.box.add_ob(self.money_label,
                        self.box.width - 2 - len(self.money_label.text), 0)
        self.box2.add_ob(self.desc_label, 1, 1)

    def __call__(self, ev):
        """Opens the buy menu"""
        ev.clear()
        with self.box.add(self.map, self.map.width - 35, 0):
            self.box2.add(self.map, self.box.x - 19, 3)
            self.rechar()
            self.map.show()
            while True:
                if ev.get() in ["'s'", "'w'"]:
                    self.box.input(ev.get())
                    self.rechar()
                    ev.clear()
                elif ev.get() in ["Key.esc", "'q'"]:
                    break
                elif ev.get() == "Key.enter":
                    obj = self.items[self.box.index.index]
                    if self.fig.get_money() - obj.price >= 0:
                        self.fig.add_money(-obj.price)
                        self.fig.give_item(obj.name)
                    ev.clear()
                std_loop(ev)
                time.sleep(0.05)
                self.map.show()
        self.box2.remove()

    def rechar(self):
        """Rechars the detail text"""
        obj = self.items[self.box.index.index]
        self.box2.name_label.rechar(obj.pretty_name)
        self.desc_label.rechar(liner(obj.desc, 19))


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
