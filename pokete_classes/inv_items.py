"""InvItem class and it's daughters"""


class InvItem:
    """Item for the inventory"""

    def __init__(self, name, pretty_name, desc, price, fn=None):
        self.name = name
        self.pretty_name = pretty_name
        self.desc = desc
        self.price = price
        self.fn = fn


class LearnDisc(InvItem):
    """Learning disc item to teach attacks to Poketes"""

    def __init__(self, attack_name, attacks):
        self.attack_name = attack_name
        self.attack_dict = attacks[attack_name]
        pretty_name = f"LD-{self.attack_dict['name']}"
        name = f"ld_{attack_name}"
        desc = f"Teaches a Pokete the attack '{self.attack_dict['name']}'."
        super().__init__(name, pretty_name, desc, 0)
