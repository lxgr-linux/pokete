import os
import scrap_engine as se
from pokete_classes.ui_elements import StdFrame


class PlayMap(se.Map):
    """Map the actual player moves on and contains buildings etc"""

    def __init__(self, height=se.screen_height - 1, width=se.screen_width,
                 trainers=None, name="", pretty_name="", poke_args=None,
                 extra_actions=None):
        super().__init__(height=height, width=width, background=" ")
        self.trainers = trainers
        self.name = name
        self.pretty_name = pretty_name
        self.poke_args = poke_args
        if self.trainers is None:
            self.trainers = []
        if self.poke_args is None:
            self.poke_args = {}
        self.__extra_actions = extra_actions

    def extra_actions(self):
        """Executes the extra action"""
        if self.__extra_actions is not None:
            self.__extra_actions()


class Settings():
    """Contains all possible settings"""

    def __init__(self, autosave=True, animations=True, save_trainers=True,
                 colors=True):
        self.keywords = ["autosave", "animations", "save_trainers"]
        self.autosave = autosave
        self.animations = animations
        self.save_trainers = save_trainers

    def dict(self):
        """Returns a dict of all current settings"""
        return {i: getattr(self, i) for i in self.keywords}


class OutP(se.Text):
    """Output label to better organize output"""

    def outp(self, text):
        """Rechar and show wrapper"""
        self.rechar(text)
        self.map.show()

    def append(self, *args):
        """Appends another se.Text to the outp"""
        for i in args:
            self += i
        self.map.show()


class ResizeScreen():
    """Screen thats shown when the screen is resized"""

    def __init__(self):
        width, height = os.get_terminal_size()
        self.map = se.Map(background=" ")
        self.warning_label = se.Text("Minimum windowsize is 70x20")
        self.size_label = se.Text(f"{width}x{height}")
        self.frame = StdFrame(height - 1, width)
        self.warning_label.add(self.map, int(width / 2) - 13, int(height / 2) - 1)
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
            self.warning_label.set(int(width / 2) - 13, int((height - 1) / 2) - 1)
            self.size_label.rechar(f"{width}x{height}")
            self.frame.resize(height - 1, width)
            self.frame.add(self.map, 0, 0)
            self.map.show()
        return width, height


class LoadingScreen():
    """Loading screen that's shown at game's start"""

    def __init__(self, ver, codename):
        width, height = os.get_terminal_size()
        self.map = se.Map(background=" ", width=width, height=height - 1)
        se.Text(r""" _____      _        _
|  __ \    | |      | |
| |__) |__ | | _____| |_ ___
|  ___/ _ \| |/ / _ \ __/ _ \
| |  | (_) |   <  __/ ||  __/
|_|   \___/|_|\_\___|\__\___|""", state="float").add(self.map,
                                                     int(self.map.width / 2) - 15, int(self.map.height / 2) - 4)
        se.Text(f"v{ver}", state="float").add(self.map,
                                              int(self.map.width / 2) - 15, int(self.map.height / 2) + 2)
        se.Text(codename, state="float").add(self.map,
                                             int(self.map.width / 2) + 14 - len(codename),
                                             int(self.map.height / 2) + 2)

    def __call__(self):
        """Shows the loading screen"""
        self.map.show()


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
