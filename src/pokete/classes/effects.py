"""Contains everything related to Effects"""

import logging
import random
import time
from typing import override

import scrap_engine as se

from pokete.base.color import Color
from pokete.base.game_map import GameMapWithOutp
from pokete.classes.i import IEffect, IPoke
from pokete.classes.poke.ui import PokeLabels
from pokete.release import SPEED_OF_TIME


class Effect(IEffect):
    """An effect that can be given to a Pokete and that effects the Pokete
    during fights
    ARGS:
        name: The effects displayed name (paralysed etc)
        rem_chance: The chance the effect gets removed
        catch_chance: The number with which the catch chance of the Poke is
            increased
        text: The text shown near the Pokes name ("(Bur)")
        str_esccode: The color of said label,
        obj: The Poke the effect is added to
        exclude: A list of type names that the effect can't be added to
    CLASS VARS:
        desc: The effects description
        c_name: The class' simplified name
        color: The color of effect"""

    desc = ""
    c_name = ""
    color = ""
    log = logging.getLogger("Effect")

    def __init__(
        self,
        name: str,
        rem_chance: int,
        catch_chance: int,
        text: str,
        str_esccode: str = "",
        exclude: list[str] | None = None,
    ) -> None:
        self.name = name
        self.text = text
        self.rem_chance = rem_chance
        self.catch_chance = catch_chance
        self.str_esccode = str_esccode
        if exclude is not None:
            self.exclude = exclude
        else:
            self.exclude = []

    @override
    def __repr__(self) -> None:
        return f"{type(self).__name__}"

    def effect(
        self,
        poke: IPoke,
        fightmap: GameMapWithOutp,
        poke_labels: PokeLabels,  # pyright: ignore[reportUnusedParameter]
    ) -> bool:
        """The action that's executed every attack round"""
        fightmap.outp.outp(f"{poke.ext_name} is still ")
        fightmap.outp.append(
            se.Text(self.name, esccode=self.str_esccode, state="float"),
            se.Text(" and can't attack!", state="float"),
        )
        time.sleep(SPEED_OF_TIME * 0.5)
        return True

    @classmethod
    def ret_md(cls) -> None:
        """Returns a descriptive markdown string"""
        return f"""
### {cls.c_name.capitalize()}
{cls.desc}
"""


class EffectParalyzation(Effect):
    """Effect see desc"""

    desc = "Paralyses the enemy and stops it from attacking. \
This is reverted randomly."
    c_name = "paralyzation"
    color = Color.thicc + Color.yellow

    def __init__(self) -> None:
        super().__init__("paralyzed", 3, 2, "(Par)", self.color)


class EffectSleep(Effect):
    """Effect see desc"""

    desc = "Makes the enemy fall asleep and stops it from attacking. \
This is reverted randomly."
    c_name = "sleep"
    color = Color.white

    def __init__(self) -> None:
        super().__init__("sleeping", 4, 3, "(Sle)", self.color)


class EffectBurning(Effect):
    """Effect see desc"""

    desc = "Sets the enemy on fire and damages them with 2 HP every round. \
This is reverted randomly."
    c_name = "burning"
    color = Color.thicc + Color.red

    def __init__(self) -> None:
        super().__init__(
            "burning", 3, 0, "(Bur)", self.color, exclude=["fire", "water"]
        )
        self.hurt_text = "burned it self!"
        self.damage = 2

    @override
    def effect(
        self, poke: IPoke, fightmap: GameMapWithOutp, poke_labels: PokeLabels
    ) -> bool:
        fightmap.outp.outp(f"{poke.ext_name} is still ")
        fightmap.outp.append(
            se.Text(self.name, esccode=self.str_esccode, state="float"),
            se.Text("!", state="float"),
        )
        fightmap.show()
        time.sleep(SPEED_OF_TIME * 1)
        for _ in range(random.randint(1, 3)):
            oldhp = poke.hp
            poke.hp = max(poke.hp - self.damage, 0)
            poke_labels.hp_bar.update(oldhp, poke.hp)
            fightmap.outp.outp(f"{poke.ext_name} {self.hurt_text}")
            time.sleep(SPEED_OF_TIME * 0.5)
        return False


class EffectPoison(EffectBurning):
    """Effect see desc"""

    desc = "Poisons the enemy and damages the enemy with 1 HP every round.\
 This is reverted randomly."
    c_name = "poison"
    color = Color.purple

    def __init__(self) -> None:
        super(EffectBurning, self).__init__("poisoned", 4, 2, "(Poi)", self.color)
        self.hurt_text = "got damaged through poison!"
        self.damage = 1


class EffectConfusion(Effect):
    """Effect see desc"""

    desc = "Makes the enemy hurt it self. This is reverted randomly."
    c_name = "confusion"
    color = Color.lightblue

    def __init__(self) -> None:
        super().__init__("confused", 3, 2, "(Con)", self.color, exclude=["undead"])

    @override
    def effect(
        self, poke: IPoke, fightmap: GameMapWithOutp, poke_labels: PokeLabels
    ) -> bool:
        fightmap.outp.outp(f"{poke.ext_name} is still ")
        fightmap.outp.append(
            se.Text(self.name, esccode=self.str_esccode, state="float"),
            se.Text("!", state="float"),
        )
        time.sleep(SPEED_OF_TIME * 0.5)
        return False


class EffectFreezing(Effect):
    """Effect see desc"""

    desc = "Freezes the enemy and stops it from attacking. \
This is reverted randomly."
    c_name = "freezing"
    color = Color.cyan

    def __init__(self) -> None:
        super().__init__("frozen", 3, 3, "(Fro)", self.color, exclude=["ice", "fire"])


effect_list = [
    EffectParalyzation,
    EffectSleep,
    EffectBurning,
    EffectPoison,
    EffectConfusion,
    EffectFreezing,
]


def _build_effects() -> dict[str, type[Effect]]:
    """Build the effects dictionary from effect_list"""
    return {effect_class.c_name: effect_class for effect_class in effect_list}


effects: dict[str, type[Effect]] = _build_effects()

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
