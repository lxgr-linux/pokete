import scrap_engine as se


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
                pretty_name="", poke_args=None, extra_actions=None, dynfps=True):
        super().__init__(height=height, width=width, background=" ", dynfps=dynfps)
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


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
