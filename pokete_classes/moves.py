import time
import scrap_engine as se
from .color import Color

class Moves:
    """This class contains all attack moves"""

    def __init__(self, poke):
        self.poke = poke

    def attack(self):
        """Attack move"""
        for i, j, t in zip([3, -3], [2, -2], [0.3, 0]):
            self.poke.ico.move(i if self.poke.player
                               else -i, -j if self.poke.player else j)
            self.poke.ico.map.show()
            time.sleep(t)

    def pound(self):
        """Pound move"""
        for i in [-1, 1]:
            self.poke.ico.move(0, i)
            self.poke.ico.map.show()
            time.sleep(0.3)

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
        time.sleep(1)
        line.remove()
        del line

    def throw(self, txt="#"):
        """Throw move"""
        if self.poke.enem == self.poke:
            return
        line = se.Line(" ",
                       (self.poke.enem.ico.x
                        - self.poke.ico.x
                        + (-11 if self.poke.player else 11)),
                       self.poke.enem.ico.y - self.poke.ico.y,
                       l_type="crippled")
        line.add(self.poke.ico.map,
                 self.poke.ico.x + (11 if self.poke.player else -1),
                 self.poke.ico.y + 1)
        self.poke.ico.map.show()
        for i in range(len(line.obs)):
            line.obs[i].rechar(txt)
            if i != 0:
                line.obs[i - 1].rechar(line.char)
            time.sleep(0.05)
            self.poke.ico.map.show()
        line.remove()
        del line

    def fireball(self):
        """Fireball move"""
        self.throw(txt=Color.thicc + Color.red + "*" + Color.reset)

    def shine(self, ico=Color.thicc + Color.green + "*" + Color.reset):
        """Shine Move"""
        shines = [se.Object(ico) for _ in range(4)]
        for i, x, y in zip(shines, [self.poke.ico.x - 1, self.poke.ico.x + 11,
                                    self.poke.ico.x - 1, self.poke.ico.x + 11],
                           [self.poke.ico.y, self.poke.ico.y,
                            self.poke.ico.y + 3, self.poke.ico.y + 3]):
            i.add(self.poke.ico.map, x, y)
            self.poke.ico.map.show()
            time.sleep(0.2)
        time.sleep(0.2)
        for i in shines:
            i.remove()
        self.poke.ico.map.show()

    def downgrade(self):
        """Downgrade move"""
        self.poke.enem.moves.shine(ico=Color.thicc + Color.red + "-"
                                       + Color.reset)


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
