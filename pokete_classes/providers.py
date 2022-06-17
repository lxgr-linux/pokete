import random

class Provider:
    """Provider can hold and manage Poketes
    ARGS:
        pokes: The Poketes the Provider holds"""

    def __init__(self, pokes):
        self.pokes = pokes
        self.play_index = 0

    @property
    def curr(self):
        """Returns the currently used Pokete"""
        return self.pokes[self.play_index]

    def index_conf(self):
        """Sets index correctly"""
        self.play_index = next(
            i for i, poke in enumerate(self.pokes) if poke.hp > 0
        )

    def get_attack(self, fightmap, enem):
        """Returns the choosen attack:
        ARGS:
            fightmap: fightmap object
            anem: The enemy Provider"""
        raise NotImplementedError

class NatureProvider(Provider):
    """The Natures Provider
    ARGS:
        poke: One Pokete"""
    def __init__(self, poke):
        super().__init__([poke])

    def get_attack(self, fightmap, enem):
        """Returns the choosen attack:
        ARGS:
            fightmap: fightmap object
            anem: The enemy Provider"""
        return random.choices(
            self.curr.attack_obs,
            weights=[
                i.ap for i in self.curr.attack_obs
            ]
        )[0]


class ProtoFigure(Provider):
    """Class Figure inherits from to avoid injecting the Figure class
    into fight"""
    pass

