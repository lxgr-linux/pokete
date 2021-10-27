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
                 colors=True, load_mods=False):
        self.keywords = ["autosave", "animations",
                         "save_trainers", "load_mods"]
        self.autosave = autosave
        self.animations = animations
        self.save_trainers = save_trainers
        self.load_mods = load_mods

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


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
