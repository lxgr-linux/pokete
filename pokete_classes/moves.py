"""Contains all moves a Pokete can fullfill"""

import time
import scrap_engine as se
from .color import Color
from release import SPEED_OF_TIME

class Moves:
    """This class contains all attack moves
    ARGS:
        poke: The Poke that does the moves"""

    def __init__(self, poke):
        self.poke = poke

    def attack(self):
        """Attack move"""
        for i, j, _t in zip([3, -3], [2, -2], [0.3, 0]):
            self.poke.ico.move(i if self.poke.player
                               else -i, -j if self.poke.player else j)
            self.poke.ico.map.show()
            time.sleep(SPEED_OF_TIME * _t)

    def pound(self):
        """Pound move"""
        for i in [-1, 1]:
            self.poke.ico.move(0, i)
            self.poke.ico.map.show()
            time.sleep(SPEED_OF_TIME * 0.3)

    def bomb(self):
        """Bomb move"""
        frames = [
            """

     o

""", """

    (o)

""", """

    ( )

""", r"""
   \   /
    ( )
   /   \
""", r"""
   \   /

   /   \
""", r"""
   \ - /
 (       )
   / - \
""", """
     -
 (       )
     -
""", """
'         '

.         .
"""
        ]
        _map = self.poke.ico.map
        text = se.Text("")
        text.add(_map, round((_map.width - 11)/2), round((_map.height - 9)/2))
        self.throw(Color.thicc + Color.blue + "o" + Color.reset, 0.5)
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
        line = se.Line(Color.thicc + Color.yellow + "-" + Color.reset,
                       (self.poke.enem.ico.x - self.poke.ico.x
                        + (-11 if self.poke.player else 11)),
                       self.poke.enem.ico.y - self.poke.ico.y,
                       l_type="crippled")
        line.add(self.poke.ico.map,
                 self.poke.ico.x + (11 if self.poke.player else -1),
                 self.poke.ico.y + 1)
        self.poke.ico.map.show()
        time.sleep(SPEED_OF_TIME * 1)
        line.remove()
        del line

    def throw(self, txt="#", factor=1., num=1):
        """Throw move
        ARGS:
            txt: The char that moves across the screen
            factor: Scalar to stretch the vector
            num: The number of chars thrown"""
        if self.poke.enem == self.poke:
            return
        line = se.Line(" ",
                       (self.poke.enem.ico.x
                        - self.poke.ico.x
                        + (-11 if self.poke.player else 11)),
                       self.poke.enem.ico.y - self.poke.ico.y,
                       l_type="crippled")
        line.resize(line.cx * factor, line.cy * factor)
        line.add(self.poke.ico.map,
                 self.poke.ico.x + (11 if self.poke.player else -1),
                 self.poke.ico.y + 1)
        self.poke.ico.map.show()
        for i in range(len(line.obs) + num*5 - 1):
            for j in range(0, num*5, 5):
                if len(line.obs) > i - j >= 0:
                    line.obs[i - j].rechar(txt)
                if len(line.obs) >= i - j > 0:
                    line.obs[i - j - 1].rechar(line.char)
            time.sleep(SPEED_OF_TIME * 0.05)
            self.poke.ico.map.show()
        line.remove()
        del line

    def gun(self):
        """Gun move"""
        self.throw(txt=Color.thicc + Color.blue + "o" + Color.reset, num=4)

    def fireball(self):
        """Fireball move"""
        self.throw(txt=Color.thicc + Color.red + "*" + Color.reset)

    def shine(self, ico=Color.thicc + Color.green + "*" + Color.reset):
        """Shine Move"""
        shines = [se.Object(ico) for _ in range(4)]
        for i, _x, _y in zip(shines,
                             [self.poke.ico.x - 1, self.poke.ico.x + 11,
                              self.poke.ico.x - 1, self.poke.ico.x + 11],
                             [self.poke.ico.y, self.poke.ico.y,
                              self.poke.ico.y + 3, self.poke.ico.y + 3]):
            i.add(self.poke.ico.map, _x, _y)
            self.poke.ico.map.show()
            time.sleep(SPEED_OF_TIME * 0.2)
        time.sleep(SPEED_OF_TIME * 0.2)
        for i in shines:
            i.remove()
        self.poke.ico.map.show()

    def downgrade(self):
        """Downgrade move"""
        self.poke.enem.moves.shine(ico=Color.thicc + Color.red + "-"
                                   + Color.reset)


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
