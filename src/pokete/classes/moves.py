"""Contains all moves a Pokete can fullfill"""

import random
import time

import scrap_engine as se

from pokete.base.color import Color
from pokete.release import SPEED_OF_TIME


class Moves:
    """This class contains all attack moves
    ARGS:
        poke: The Poke that does the moves"""

    def __init__(self, poke):
        self.poke = poke

    def attack(self):
        """Attack move"""
        for i, j, _t in zip([3, -3], [2, -2], [0.3, 0]):
            self.poke.ico.move(
                i if self.poke.player else -i, -j if self.poke.player else j
            )
            self.poke.ico.map.show()
            time.sleep(SPEED_OF_TIME * _t)
        self.impact()

    def impact(self):
        """Brief flash effect on enemy when attack lands"""
        if self.poke.enem == self.poke:
            return
        enem_ico = self.poke.enem.ico
        flash_chars = ["*", "X", "*"]
        flash = se.Text(flash_chars[0], esccode=Color.thicc + Color.yellow)
        flash.add(
            enem_ico.map,
            *(
                (enem_ico.x, enem_ico.y + enem_ico.height)
                if self.poke.player
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

    def pound(self):
        """Pound move"""
        for i in [-1, 1]:
            self.poke.ico.move(0, i)
            self.poke.ico.map.show()
            time.sleep(SPEED_OF_TIME * 0.3)
        self.impact()

    def bomb(self):
        """Bomb move"""
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
        _map = self.poke.ico.map
        text = se.Text("")
        text.add(
            _map, round((_map.width - 11) / 2), round((_map.height - 9) / 2)
        )
        self.__throw(Color.thicc + Color.blue + "o" + Color.reset, 0.5)
        for i in frames:
            text.rechar(i)
            self.poke.ico.map.show()
            time.sleep(SPEED_OF_TIME * 0.03)
        time.sleep(SPEED_OF_TIME * 0.03)
        text.remove()

    def arch(self):
        """Arch move"""
        if self.poke.enem == self:
            return
        line = se.Line(
            Color.thicc + Color.yellow + "-" + Color.reset,
            (
                self.poke.enem.ico.x
                - self.poke.ico.x
                + (-11 if self.poke.player else 11)
            ),
            self.poke.enem.ico.y - self.poke.ico.y,
            l_type="crippled",
        )
        line.add(
            self.poke.ico.map,
            self.poke.ico.x + (11 if self.poke.player else -1),
            self.poke.ico.y + 1,
        )
        self.poke.ico.map.show()
        time.sleep(SPEED_OF_TIME * 1)
        line.remove()
        del line

    def throw(self):
        self.__throw()
        self.impact()

    def __throw(self, txt="#", factor=1.0, num=1, trail=True):
        """Throw move with trail effect
        ARGS:
            txt: The char that moves across the screen
            factor: Scalar to stretch the vector
            num: The number of chars thrown
            trail: Whether to show a fading trail behind projectile"""
        if self.poke.enem == self.poke:
            return
        line = se.Line(
            " ",
            (
                self.poke.enem.ico.x
                - self.poke.ico.x
                + (-11 if self.poke.player else 11)
            ),
            self.poke.enem.ico.y - self.poke.ico.y,
            l_type="crippled",
        )
        line.resize(line.cx * factor, line.cy * factor)
        line.add(
            self.poke.ico.map,
            self.poke.ico.x + (11 if self.poke.player else -1),
            self.poke.ico.y + 1,
        )
        self.poke.ico.map.show()
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
            self.poke.ico.map.show()
        line.remove()
        del line

    def gun(self):
        """Gun move"""
        self.__throw(txt=Color.thicc + Color.blue + "o" + Color.reset, num=4)
        self.impact()

    def fireball(self):
        """Fireball move"""
        self.__throw(txt=Color.thicc + Color.red + "*" + Color.reset)
        self.impact()

    def shine(self, ico=Color.thicc + Color.green + "*" + Color.reset):
        """Shine Move"""
        shines = [se.Object(ico) for _ in range(4)]
        for i, _x, _y in zip(
            shines,
            [
                self.poke.ico.x - 1,
                self.poke.ico.x + 11,
                self.poke.ico.x - 1,
                self.poke.ico.x + 11,
            ],
            [
                self.poke.ico.y,
                self.poke.ico.y,
                self.poke.ico.y + 3,
                self.poke.ico.y + 3,
            ],
        ):
            i.add(self.poke.ico.map, _x, _y)
            self.poke.ico.map.show()
            time.sleep(SPEED_OF_TIME * 0.2)
        time.sleep(SPEED_OF_TIME * 0.2)
        for i in shines:
            i.remove()
        self.poke.ico.map.show()

    def downgrade(self):
        """Downgrade move"""
        self.poke.enem.moves.shine(
            ico=Color.thicc + Color.red + "-" + Color.reset
        )

    def smell(self):
        self.shine(ico=Color.thicc + Color.peach + "~" + Color.reset)

    def rain(self):
        """Rain animation"""
        drops = []
        _map = self.poke.ico.map
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


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
