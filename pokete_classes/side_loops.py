"""Contains some small loops"""

import os
import scrap_engine as se
import pokete_classes.game_map as gm
from pokete_general_use_fns import liner
from .loops import easy_exit_loop
from .ui_elements import InfoBox, StdFrame


class About:
    """The about text, that can be triggered in the menu
    ARGS:
        ver: Version
        cname: Codename
        _map: se.Map this will be displayed on"""

    def __init__(self, ver, cname, _map):
        self.box = InfoBox(liner(f"""Pokete v{ver} -- {cname}
by  lxgr-linux <lxgr@protonmail.com>

This  software is licensed under the GPL3, you should have gotten a copy of the GPL3 license alongside this software.
Feel  free to contribute what ever you want to this game, new Pokete contributions are especially welcome.
For  this see the comments in the definations area.
You  can contribute here: https://github.com/lxgr-linux/pokete""",
                                 60, pre=""), name="About", _map=_map)

    def __call__(self):
        """Shows the about text"""
        with self.box:
            easy_exit_loop()


class Help(About):
    """Helptext that can be displayed by pressing '?'
    ARGS:
        _map: se.Map this will be displayed on"""

    def __init__(self, _map):
        self.map = _map
        self.box = InfoBox("""Controls:
'w':up, 'a':left,
's':down, 'd':right,
'e':menu

When walking into the high grass (';') you may get attacked
by wild Poketes, those can be killed or weakened and caught.
NPCs will talk to you when walking up to them.
For more information about how to play this game, check out
https://git.io/JRRqe""", name="Help", _map=self.map)


class ResizeScreen():
    """Screen thats shown when the screen is resized"""

    def __init__(self):
        width, height = os.get_terminal_size()
        self.map = gm.GameMap(height, width)
        self.warning_label = se.Text("Minimum windowsize is 70x20")
        self.size_label = se.Text(f"{width}x{height}")
        self.frame = StdFrame(height - 1, width)
        self.warning_label.add(self.map, int(width / 2) - 13,
                               int(height / 2) - 1)
        self.size_label.add(self.map, 1, 0)
        self.frame.add(self.map, 0, 0)

    def __call__(self):
        """Shows the map"""
        width, height = os.get_terminal_size()
        while width < 70 or height < 20:
            width, height = os.get_terminal_size()
            self.warning_label.set(1, 1)
            self.frame.remove()
            self.map.resize(height - 1, width, " ")
            self.warning_label.set(int(width / 2) - 13,
                                   int((height - 1) / 2) - 1)
            self.size_label.rechar(f"{width}x{height}")
            self.frame.resize(height - 1, width)
            self.frame.add(self.map, 0, 0)
            self.map.show()
        return width, height


class LoadingScreen():
    """Loading screen that's shown at game's start
    ARGS:
        ver: Version
        codename: Codename"""

    def __init__(self, ver, codename):
        width, height = os.get_terminal_size()
        self.map = gm.GameMap(width=width, height=height - 1)
        se.Text(r""" _____      _        _
|  __ \    | |      | |
| |__) |__ | | _____| |_ ___
|  ___/ _ \| |/ / _ \ __/ _ \
| |  | (_) |   <  __/ ||  __/
|_|   \___/|_|\_\___|\__\___|""", state="float")\
            .add(self.map, int(self.map.width / 2) - 15,
                 int(self.map.height / 2) - 4)
        se.Text(f"v{ver}", state="float").add(self.map,
                                              int(self.map.width / 2) - 15,
                                              int(self.map.height / 2) + 2)
        se.Text(codename, state="float").add(self.map,
                                             int(self.map.width / 2) + 14
                                             - len(codename),
                                             int(self.map.height / 2) + 2)

    def __call__(self):
        """Shows the loading screen"""
        self.map.show()


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
