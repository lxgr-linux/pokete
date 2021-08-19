import scrap_engine as se
import os
from pokete_classes.ui_elements import *


class Color:
    reset = "\033[0m"
    thicc = "\033[1m"
    underlined = "\033[4m"
    grey = "\033[1;30m"
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    lightblue = "\033[1;34m"
    blue = "\033[34m"
    purple = "\033[1;35m"
    cyan = "\033[1;36m"
    lightgrey = "\033[37m"
    white = "\033[1;37m"


class NoColor(Color):
    grey = ""
    red = ""
    green = ""
    yellow = ""
    lightblue = ""
    blue = ""
    purple = ""
    cyan = ""
    lightgrey = ""
    white = ""


class PlayMap(se.Map):
    def __init__(self, height=se.height-1, width=se.width, trainers=None, name="",
                pretty_name="", poke_args=None, extra_actions=None):
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
        if self.__extra_actions is not None:
            self.__extra_actions()


class PokeType():
    def __init__(self, name, effective, ineffective, color):
        self.name = name
        self.effective = effective
        self.ineffective = ineffective
        self.color = "" if color is None else eval(color)


class InvItem:
    def __init__(self, name, pretty_name, desc, price, fn=None):
        self.name = name
        self.pretty_name = pretty_name
        self.desc = desc
        self.price = price
        self.fn = fn


class Settings():
    def __init__(self, autosave=True, animations=True, save_trainers=True, colors=True):
        self.keywords = ["autosave", "animations", "save_trainers", "colors"]
        for key in self.keywords:
            exec(f"self.{key} = {key}")

    def dict(self):
        return {i: eval("self."+i, {"self": self,}) for i in self.keywords}


class OutP(se.Text):
    def outp(self, text):
        self.rechar(text)
        self.map.show()

    def append(self, *args):
        for i in args:
            self += i
        self.map.show()


class ResizeScreen():
    def __init__(self):
        width, height = os.get_terminal_size()
        self.map = se.Map(background=" ")
        self.warning_label = se.Text("Minimum windowsize is 70x20")
        self.size_label = se.Text(f"{width}x{height}")
        self.frame = StdFrame(height-1, width)
        self.warning_label.add(self.map, int(width/2)-13, int(height/2)-1)
        self.size_label.add(self.map, 1, 0)
        self.frame.add(self.map, 0, 0)

    def __call__(self):
        width, height = os.get_terminal_size()
        while width < 70 or height < 20:
            width, height = os.get_terminal_size()
            self.warning_label.set(1, 1)
            self.frame.remove()
            self.map.resize(height-1, width, " ")
            self.warning_label.set(int(width/2)-13, int((height-1)/2)-1)
            self.size_label.rechar(f"{width}x{height}")
            self.frame = StdFrame(height-1, width)
            self.frame.add(self.map, 0, 0)
            self.map.show()
        return width, height


class LoadingScreen():
    def __init__(self, ver):
        width, height = os.get_terminal_size()
        self.map = se.Map(background=" ", width=width, height=height-1)
        se.Text(r""" _____      _        _
|  __ \    | |      | |
| |__) |__ | | _____| |_ ___
|  ___/ _ \| |/ / _ \ __/ _ \
| |  | (_) |   <  __/ ||  __/
|_|   \___/|_|\_\___|\__\___|""", state="float").add(self.map,
                int(self.map.width/2)-15, int(self.map.height/2)-4)
        se.Text(f"v{ver}", state="float").add(self.map,
                int(self.map.width/2)-15, int(self.map.height/2)+2)

    def __call__(self):
        self.map.show()


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
