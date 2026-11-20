"""Contains all moves a Pokete can fulfill"""

import random
import time
from abc import ABC, abstractmethod
from typing import override

import scrap_engine as se

from pokete.base.color import Color
from pokete.classes.poke.ui import PokeLabels
from pokete.release import SPEED_OF_TIME


# Helper functions for animations - no duplication, pure functions
def _impact(player_labels: PokeLabels, enem_labels: PokeLabels):
    """Brief flash effect on enemy when attack lands"""
    if enem_labels.poke == player_labels.poke:
        return
    enem_ico = enem_labels.ico
    flash_chars = ["*", "X", "*"]
    flash = se.Text(flash_chars[0], esccode=Color.thicc + Color.yellow)
    flash.add(
        enem_ico.map,
        *(
            (enem_ico.x, enem_ico.y + enem_ico.height)
            if player_labels.poke.player
            else (
                enem_ico.x + enem_ico.width,
                enem_ico.y,
            )
        ),
    )
    for char in flash_chars:
        flash.rechar(char, esccode=Color.thicc + Color.yellow)
        enem_ico.map.show()
        time.sleep(SPEED_OF_TIME * 0.1)
    flash.remove()
    enem_ico.map.show()


def _throw(
    player_labels: PokeLabels,
    enem_labels: PokeLabels,
    txt: str = "#",
    factor: float = 1.0,
    num: int = 1,
    trail: bool = True,
):
    """Throw move with trail effect
    ARGS:
        player_labels: Labels of attacking pokemon
        enem_labels: Labels of defending pokemon
        txt: The char that moves across the screen
        factor: Scalar to stretch the vector
        num: The number of chars thrown
        trail: Whether to show a fading trail behind projectile"""
    if enem_labels.poke == player_labels.poke:
        return
    line = se.Line(
        " ",
        (
            enem_labels.ico.x
            - player_labels.ico.x
            + (-11 if player_labels.poke.player else 11)
        ),
        enem_labels.ico.y - player_labels.ico.y,
        l_type="crippled",
    )
    line.resize(line.cx * factor, line.cy * factor)
    line.add(
        player_labels.ico.map,
        player_labels.ico.x + (11 if player_labels.poke.player else -1),
        player_labels.ico.y + 1,
    )
    player_labels.ico.map.show()
    trail_char = Color.white + "." + Color.reset
    trail_len = 3 if trail else 0
    for i in range(len(line.obs) + num * 5 - 1):
        for j in range(0, num * 5, 5):
            if len(line.obs) > i - j >= 0:
                line.obs[i - j].rechar(txt)
            # Trail effect: show fading dots behind projectile
            if trail:
                for t in range(1, trail_len + 1):
                    trail_idx = i - j - t
                    if 0 <= trail_idx < len(line.obs):
                        line.obs[trail_idx].rechar(trail_char)
            # Clear old trail
            clear_idx = i - j - trail_len - 1 if trail else i - j - 1
            if len(line.obs) > clear_idx >= 0:
                line.obs[clear_idx].rechar(line.char)
        time.sleep(SPEED_OF_TIME * 0.05)
        player_labels.ico.map.show()
    line.remove()
    del line


def _shine(player_labels: PokeLabels, ico: str):
    """Shine animation with custom icon"""
    shines = [se.Object(ico) for _ in range(4)]
    for i, _x, _y in zip(
        shines,
        [
            player_labels.ico.x - 1,
            player_labels.ico.x + 11,
            player_labels.ico.x - 1,
            player_labels.ico.x + 11,
        ],
        [
            player_labels.ico.y,
            player_labels.ico.y,
            player_labels.ico.y + 3,
            player_labels.ico.y + 3,
        ],
    ):
        i.add(player_labels.ico.map, _x, _y)
        player_labels.ico.map.show()
        time.sleep(SPEED_OF_TIME * 0.2)
    time.sleep(SPEED_OF_TIME * 0.2)
    for i in shines:
        i.remove()
    player_labels.ico.map.show()


class Move(ABC):
    """Abstract base class for all pokete moves"""

    @abstractmethod
    def move(self, player_labels: PokeLabels, enem_labels: PokeLabels) -> None: ...


class AttackMove(Move):
    """Attack move - quick strike with knockback animation"""

    @override
    def move(self, player_labels: PokeLabels, enem_labels: PokeLabels) -> None:
        for i, j, _t in zip([3, -3], [2, -2], [0.3, 0]):
            player_labels.ico.move(
                i if player_labels.poke.player else -i,
                -j if player_labels.poke.player else j,
            )
            player_labels.ico.map.show()
            time.sleep(SPEED_OF_TIME * _t)
        _impact(player_labels, enem_labels)


class PoundMove(Move):
    """Pound move - vertical bobbing motion"""

    @override
    def move(self, player_labels: PokeLabels, enem_labels: PokeLabels) -> None:
        for i in [-1, 1]:
            player_labels.ico.move(0, i)
            player_labels.ico.map.show()
            time.sleep(SPEED_OF_TIME * 0.3)
        _impact(player_labels, enem_labels)


class BombMove(Move):
    """Bomb move - explosion animation"""

    @override
    def move(self, player_labels: PokeLabels, enem_labels: PokeLabels) -> None:
        frames = [
            """

     o

""",
            """

    (o)

""",
            """

    ( )

""",
            r"""
   \   /
    ( )
   /   \
""",
            r"""
   \   /

   /   \
""",
            r"""
   \ - /
 (       )
   / - \
""",
            """
     -
 (       )
     -
""",
            """
'         '

.         .
""",
        ]
        _map = player_labels.ico.map
        text = se.Text("")
        text.add(_map, round((_map.width - 11) / 2), round((_map.height - 9) / 2))
        _throw(
            player_labels,
            enem_labels,
            txt=Color.thicc + Color.blue + "o" + Color.reset,
            factor=0.5,
        )
        for i in frames:
            text.rechar(i)
            player_labels.ico.map.show()
            time.sleep(SPEED_OF_TIME * 0.03)
        time.sleep(SPEED_OF_TIME * 0.03)
        text.remove()


class ArchMove(Move):
    """Arch move - arcing projectile"""

    @override
    def move(self, player_labels: PokeLabels, enem_labels: PokeLabels) -> None:
        if enem_labels.poke == player_labels.poke:
            return
        line = se.Line(
            Color.thicc + Color.yellow + "-" + Color.reset,
            (
                enem_labels.ico.x
                - player_labels.ico.x
                + (-11 if player_labels.poke.player else 11)
            ),
            enem_labels.ico.y - player_labels.ico.y,
            l_type="crippled",
        )
        line.add(
            player_labels.ico.map,
            player_labels.ico.x + (11 if player_labels.poke.player else -1),
            player_labels.ico.y + 1,
        )
        player_labels.ico.map.show()
        time.sleep(SPEED_OF_TIME * 1)
        line.remove()
        del line


class ThrowMove(Move):
    """Throw move - projectile with impact"""

    @override
    def move(self, player_labels: PokeLabels, enem_labels: PokeLabels) -> None:
        _throw(player_labels, enem_labels)
        _impact(player_labels, enem_labels)


class GunMove(Move):
    """Gun move - rapid-fire projectiles"""

    @override
    def move(self, player_labels: PokeLabels, enem_labels: PokeLabels) -> None:
        _throw(
            player_labels,
            enem_labels,
            txt=Color.thicc + Color.blue + "o" + Color.reset,
            num=4,
        )
        _impact(player_labels, enem_labels)


class FireballMove(Move):
    """Fireball move - fiery projectile"""

    @override
    def move(self, player_labels: PokeLabels, enem_labels: PokeLabels) -> None:
        _throw(
            player_labels, enem_labels, txt=Color.thicc + Color.red + "*" + Color.reset
        )
        _impact(player_labels, enem_labels)


class ShineMove(Move):
    """Shine move - glowing stars around pokemon"""

    @override
    def move(self, player_labels: PokeLabels, enem_labels: PokeLabels) -> None:
        _shine(player_labels, ico=Color.thicc + Color.green + "*" + Color.reset)


class DowngradeMove(Move):
    """Downgrade move - red shine effect on enemy"""

    @override
    def move(self, player_labels: PokeLabels, enem_labels: PokeLabels) -> None:
        _shine(enem_labels, ico=Color.thicc + Color.red + "-" + Color.reset)


class SmellMove(Move):
    """Smell move - wavy shine effect"""

    @override
    def move(self, player_labels: PokeLabels, enem_labels: PokeLabels) -> None:
        _shine(player_labels, ico=Color.thicc + Color.peach + "~" + Color.reset)


class RainMove(Move):
    """Rain move - cloud with falling raindrops"""

    @override
    def move(self, player_labels: PokeLabels, enem_labels: PokeLabels) -> None:
        drops = []
        _map = player_labels.ico.map
        cloud = se.Text("""  _____
 (  )  )_
(____)___)""")

        cloud.add(
            _map,
            round(_map.width / 2) - 5,
            round(_map.frame_big.height / 2) - 1,
        )
        _map.show()
        for i in range(50):
            if i >= 5:
                drops.pop(random.choice(range(len(drops)))).remove()
            rain = se.Text("\\", esccode=Color.blue)
            rain.add(
                _map,
                random.choice(range(9)) + cloud.x + 1,
                random.choice(range(2)) + cloud.y + 3,
            )
            _map.show()
            time.sleep(SPEED_OF_TIME * 0.05)
            drops.append(rain)
        cloud.remove()
        for drop in drops:
            drop.remove()
        _map.show()


moves = {
    "attack": AttackMove(),
    "pound": PoundMove(),
    "bomb": BombMove(),
    "arch": ArchMove(),
    "throw": ThrowMove(),
    "gun": GunMove(),
    "fireball": FireballMove(),
    "shine": ShineMove(),
    "downgrade": DowngradeMove(),
    "smell": SmellMove(),
    "rain": RainMove(),
}


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
