import random

class Provider:
    def __init__(self, pokes):
        self.pokes = pokes
        self.play_index = 0

    @property
    def curr(self):
        return self.pokes[self.play_index]

    def get_attack(self, fightmap, enem):
        raise NotImplementedError

class NatureProvider(Provider):
    def __init__(self, poke):
        super().__init__([poke])

    def get_attack(self, fightmap, enem):
        return random.choices(
            self.curr.attack_obs,
            weights=[
                i.ap for i in self.curr.attack_obs
            ]
        )[0]


class ProtoFigure(Provider):
    pass

