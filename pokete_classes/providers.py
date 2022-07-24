import random
import time
from .input import ask_bool

class Provider:
    """Provider can hold and manage Poketes
    ARGS:
        pokes: The Poketes the Provider holds"""

    def __init__(self, pokes, escapable):
        self.pokes = pokes
        self.escapable = escapable
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

    def greet(self, fightmap):
        """Outputs a greeting text at the fights start:
        ARGS:
            fightmap: fightmap object"""
        raise NotImplementedError

    def handle_defeat(self, fightmap, winner):
        """Function caleld when the providers current Pokete dies
        ARGS:
            fightmap: fightmap object
            winner: the defeating provider"""
        raise NotImplementedError


class NatureProvider(Provider):
    """The Natures Provider
    ARGS:
        poke: One Pokete"""
    def __init__(self, poke):
        super().__init__([poke], True)

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

    def greet(self, fightmap):
        """Outputs a greeting text at the fights start:
        ARGS:
            fightmap: fightmap object"""
        fightmap.outp.outp(f"A wild {self.curr.name} appeared!")

    def handle_defeat(self, fightmap, winner):
        """Function caleld when the providers current Pokete dies
        ARGS:
            fightmap: fightmap object
            winner: the defeating provider"""
        return False


class ProtoFigure(Provider):
    """Class Figure inherits from to avoid injecting the Figure class
    into fight"""

    def greet(self, fightmap):
        """Outputs a greeting text at the fights start:
        ARGS:
            fightmap: fightmap object"""
        return

    def get_attack(self, fightmap, enem):
        """Returns the choosen attack:
        ARGS:
            fightmap: fightmap object
            anem: The enemy Provider"""
        return fightmap.get_figure_attack(self, enem)

    def handle_defeat(self, fightmap, winner):
        """Function caleld when the providers current Pokete dies
        ARGS:
            fightmap: fightmap object
            winner: the defeating provider"""
        if winner.escapable:
            if ask_bool(fightmap, "Do you want to choose another Pokete?"):
                success = fightmap.choose_poke(self)
                if not success:
                    return False
        else:
            time.sleep(2)
            fightmap.choose_poke(self, False)
        return True


