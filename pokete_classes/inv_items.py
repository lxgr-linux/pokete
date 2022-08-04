"""All classes needed for Item management"""

import pokete_data as p_data


class Items:
    """Has all items as attributes"""

    def __init__(self):
        for item in p_data.items.items():
            _obj = InvItem(item[0], item[1]["pretty_name"],
                           item[1]["desc"],
                           item[1]["price"], item[1]["fn"])
            setattr(self, item[0], _obj)
        self.ld_bubble_bomb = LearnDisc("bubble_bomb")
        self.ld_flying = LearnDisc("flying")
        self.ld_the_old_roots_hit = LearnDisc("the_old_roots_hit")


class InvItem:
    """Item for the inventory
    ARGS:
        name: The item's generic name (healing_potion)
        pretty_name: The item's pretty name (Healing potion)
        desc: The item's description
        price: The item's price in the shop
        fn: The associated method name in FightItems"""

    def __init__(self, name, pretty_name, desc, price, _fn=None):
        self.name = name
        self.pretty_name = pretty_name
        self.desc = desc
        self.price = price
        self.func = _fn


class LearnDisc(InvItem):
    """Learning disc item to teach attacks to Poketes
    ARGS:
        attack_name: The name of the attack being taught"""

    def __init__(self, attack_name):
        self.attack_name = attack_name
        self.attack_dict = p_data.attacks[attack_name]
        pretty_name = f"LD-{self.attack_dict['name']}"
        name = f"ld_{attack_name}"
        desc = f"Teaches a Pokete the attack '{self.attack_dict['name']}'."
        super().__init__(name, pretty_name, desc, 0)


invitems = Items()

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
