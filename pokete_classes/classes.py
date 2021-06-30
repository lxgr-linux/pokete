import scrap_engine as se

class Color:
    reset = "\033[0m"
    thicc = "\033[1m"
    underlined = "\033[4m"
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    lightblue = "\033[1;34m"
    blue = "\033[34m"


class PlayMap(se.Map):
    def __init__(self, height=se.height-1, width=se.width, background="#", trainers=[], name="", pretty_name="", poke_args={}, extra_actions=None, dynfps=True):
        super().__init__(height=height, width=width, background=background, dynfps=dynfps)
        for i in ["trainers", "name", "pretty_name", "poke_args"]:
            exec("self."+i+"="+i)
        self.__extra_actions = extra_actions

    def extra_actions(self):
        if self.__extra_actions != None:
            self.__extra_actions()


class PokeType():
    def __init__(self, name, effective, ineffective):
        self.name = name
        self.effective = effective
        self.ineffective = ineffective


class InvItem:
    def __init__(self, name, pretty_name, desc, price, fn=None):
        self.name = name
        self.pretty_name = pretty_name
        self.desc = desc
        self.price = price
        self.fn = fn


class Settings():
    def __init__(self, autosave=True, animations=True, save_trainers=True):
        self.keywords = ["autosave", "animations", "save_trainers"]
        for key in self.keywords:
            exec(f"self.{key} = {key}")

    def dict(self):
        return {i: eval("self."+i, {"self": self,}) for i in self.keywords}


class OutP(se.Text):
    def outp(self, text):
        self.rechar(text)
        self.map.show()


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
