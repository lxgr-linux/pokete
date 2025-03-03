"""Contains some small loops"""

import os
import scrap_engine as se
import pokete.base.game_map as gm
from pokete import release
from pokete.base.context import Context
from pokete.base.ui.elements import InfoBox
from pokete.base import loops
from pokete.util import liner


class LoopBox:
    """Provides an loops.easy_exit call function
    ARGS:
        box: The box to display"""

    def __init__(self, box):
        self.box = box

    def __call__(self, ctx: Context):
        """Shows the about text"""
        self.box.set_ctx(ctx)
        with self.box:
            loops.easy_exit(ctx=ctx.with_overview(self.box))


class About(LoopBox):
    """The about text, that can be triggered in the menu"""

    def __init__(self):
        super().__init__(
            InfoBox(
                liner(
                    f"""Pokete v{release.VERSION} -- {release.CODENAME}
by  lxgr-linux <lxgr@protonmail.com>

This  software is licensed under the GPL3, you should have gotten a \
copy of the GPL3 license alongside this software.
Feel  free to contribute what ever you want to this game, \
new Pokete contributions are especially welcome.
For  this see the comments in the definations area.
You  can contribute here: https://github.com/lxgr-linux/pokete""",
                    60, pre=""
                ),
                name="About",
            )
        )


class Help(LoopBox):
    """Helptext that can be displayed by pressing '?'"""

    def __init__(self):
        super().__init__(
            InfoBox(
                """Controls:
'w':up, 'a':left,
's':down, 'd':right,
'e':menu

When walking into the high grass (';') you may get attacked
by wild Poketes, those can be killed or weakened and caught.
NPCs will talk to you when walking up to them.
For more information about how to play this game, check out
https://git.io/JRRqe""",
                name="Help",
            )
        )


class LoadingScreen:
    """Loading screen that's shown at game's start"""

    def __init__(self):
        width, height = os.get_terminal_size()
        self.map = gm.GameMap(width=width, height=height - 1)
        se.Text(r""" _____      _        _
|  __ \    | |      | |
| |__) |__ | | _____| |_ ___
|  ___/ _ \| |/ / _ \ __/ _ \
| |  | (_) |   <  __/ ||  __/
|_|   \___/|_|\_\___|\__\___|""", state="float") \
            .add(self.map, int(self.map.width / 2) - 15,
                 int(self.map.height / 2) - 4)
        se.Text(f"v{release.VERSION}", state="float").add(self.map,
                                                          int(self.map.width / 2) - 15,
                                                          int(self.map.height / 2) + 2)
        se.Text(release.CODENAME, state="float").add(self.map,
                                                     int(self.map.width / 2) + 14
                                                     - len(release.CODENAME),
                                                     int(self.map.height / 2) + 2)

    def __call__(self):
        """Shows the loading screen"""
        self.map.show()


loading_screen = LoadingScreen()

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
