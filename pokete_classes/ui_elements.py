import scrap_engine as se

class BoxIndex(se.Object):
    def __init__(self):
        super().__init__("*", state="float")
        self.index = 0


class StdFrame(se.Frame):
    def __init__(self, height, width, corner_chars=None, horizontal_chars=None,
            vertical_chars=None, state=None, ob_class=None, ob_args=None):
        super().__init__(width=width, height=height,
                        corner_chars=["┌", "┐", "└", "┘"],
                        horizontal_chars=["─", "─"],
                        vertical_chars=["│", "│"], state="float")


class StdFrame2(se.Frame):
    def __init__(self, height, width, state="solid"):
        super().__init__(width=width, height=height,
                        corner_chars=["_", "_", "|", "|"],
                        horizontal_chars=["_", "_"], state=state)
 

class Box(se.Box):
    def __init__(self, height, width, name="", info=""):
        super().__init__(height, width)
        self.frame = StdFrame(height, width)
        self.inner = se.Square(char=" ", width=width-2, height=height-2,
                                state="float")
        self.name_label = se.Text(name, state="float")
        self.info_label = se.Text(info, state="float")
        # adding
        self.add_ob(self.frame, 0, 0)
        self.add_ob(self.inner, 1, 1)
        self.add_ob(self.name_label, 2, 0)
        self.add_ob(self.info_label, 2, self.height-1)

    def center_add(self, map):
        self.add(map, round((map.width-self.width)/2),
                round((map.height-self.height)/2))
        return self

    def resize(self, height, width):
        super().resize(height, width)
        self.inner.resize(width-2, height-2)
        self.frame.resize(height, width)
        self.set_ob(self.info_label, 2, self.height-1)

    def add(self, map, x, y):
        super().add(map, x, y)
        return self

    def __enter__(self):
        self.map.show()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.remove()
        self.map.show()


class ChooseBox(Box):
    def __init__(self, height, width, name="", info="", index_x=2, c_obs=[]):
        super().__init__(height, width, name, info)
        self.index_x = index_x
        self.index = BoxIndex()
        if c_obs != []:
            self.add_c_obs(c_obs)
        else:
            self.c_obs = []
        # adding
        self.add_ob(self.index, self.index_x, 1)

    def input(self, ev):
        if {"'s'": self.index.index+1 < len(self.c_obs),
            "'w'": self.index.index-1 >= 0}[ev]:
            self.index.index += {"'s'": 1, "'w'": -1}[ev]
        else:
            self.index.index = {"'s'": 0, "'w'": len(self.c_obs)-1}[ev]
        self.set_index()

    def set_index(self, index=None):
        if index is not None:
            self.index.index = index
        self.set_ob(self.index, self.index.rx, self.c_obs[self.index.index].ry)

    def add_c_obs(self, list):
        self.c_obs = list
        for y, ob in enumerate(self.c_obs):
            self.add_ob(ob, self.index_x*2, 1+y)

    def remove_c_obs(self):
        for ob in self.c_obs:
            self.rem_ob(ob)
        self.c_obs = []


class InfoBox(Box):
    def __init__(self, text, map=None):
        height = len(text.split("\n"))+2
        width = sorted([len(i) for i in text.split("\n")])[-1]+4
        super().__init__(height, width)
        self.text = se.Text(text)
        self.add_ob(self.text, 2, 1)
        self.map = map

    def __enter__(self):  # Contextmanagement is fucking awesome!
        self.center_add(self.map)
        self.map.show()
        return self


class InputBox(InfoBox):
    def __init__(self, infotext, introtext, text, max_len, map=None):
        height = len(infotext.split("\n"))+3
        width = sorted([len(i) for i in infotext.split("\n")]+[len(introtext)+1+max_len])[-1]+4
        super(InfoBox, self).__init__(height, width)
        self.map = map
        self.infotext = se.Text(infotext)
        self.introtext = se.Text(introtext)
        self.text = se.Text(text)
        self.add_ob(self.infotext, 2, 1)
        self.add_ob(self.introtext, 2, len(infotext.split("\n"))+1)
        self.add_ob(self.text, self.introtext.rx+len(introtext)+1,
                    self.introtext.ry)


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
