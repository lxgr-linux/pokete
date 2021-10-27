"""This file contains most of the user interface
elements used in Pokete"""

import scrap_engine as se


class BoxIndex(se.Object):
    """Index that can be used in ChooseBox"""

    def __init__(self):
        super().__init__("*", state="float")
        self.index = 0


class StdFrame(se.Frame):
    """Standardized frame"""

    def __init__(self, height, width):
        super().__init__(width=width, height=height,
                         corner_chars=["┌", "┐", "└", "┘"],
                         horizontal_chars=["─", "─"],
                         vertical_chars=["│", "│"], state="float")


class StdFrame2(se.Frame):
    """Standardized frame"""

    def __init__(self, height, width, state="solid"):
        super().__init__(width=width, height=height,
                         corner_chars=["_", "_", "|", "|"],
                         horizontal_chars=["_", "_"], state=state)


class Box(se.Box):
    """Box to show content in"""

    def __init__(self, height, width, name="", info=""):
        super().__init__(height, width)
        self.frame = StdFrame(height, width)
        self.inner = se.Square(char=" ", width=width - 2, height=height - 2,
                               state="float")
        self.name_label = se.Text(name, state="float")
        self.info_label = se.Text(info, state="float")
        # adding
        self.add_ob(self.frame, 0, 0)
        self.add_ob(self.inner, 1, 1)
        self.add_ob(self.name_label, 2, 0)
        self.add_ob(self.info_label, 2, self.height - 1)

    def center_add(self, _map):
        """Adds the box to the maps center"""
        self.add(_map, round((_map.width - self.width) / 2),
                 round((_map.height - self.height) / 2))
        return self

    def resize(self, height, width):
        """Resizes the box to a certain size"""
        super().resize(height, width)
        self.inner.resize(width - 2, height - 2)
        self.frame.resize(height, width)
        self.set_ob(self.info_label, 2, self.height - 1)

    def add(self, _map, x, y):
        """Adds the box to a map"""
        super().add(_map, x, y)
        return self

    def __enter__(self):
        """Enter dunder for context management"""
        self.map.show()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        """Exit dunder for context management"""
        self.remove()
        self.map.show()


class ChooseBox(Box):
    """Box that contains items you can choose from"""

    def __init__(self, height, width, name="", info="", index_x=2, c_obs=None):
        super().__init__(height, width, name, info)
        self.index_x = index_x
        self.index = BoxIndex()
        if c_obs is not None:
            self.add_c_obs(c_obs)
        else:
            self.c_obs = []
        # adding
        self.add_ob(self.index, self.index_x, 1)

    def input(self, _ev):
        """Moves the cursor in the box"""
        if {"'s'": self.index.index + 1 < len(self.c_obs),
                "'w'": self.index.index - 1 >= 0}[_ev]:
            self.index.index += {"'s'": 1, "'w'": -1}[_ev]
        else:
            self.index.index = {"'s'": 0, "'w'": len(self.c_obs) - 1}[_ev]
        self.set_index()

    def set_index(self, index=None):
        """Sets the cursors index"""
        if index is not None:
            self.index.index = index
        self.set_ob(self.index, self.index.rx, self.c_obs[self.index.index].ry)

    def add_c_obs(self, _list):
        """Adds the c_obs (the objects that can be chosen from) to the box"""
        self.c_obs = _list
        for y, obj in enumerate(self.c_obs):
            self.add_ob(obj, self.index_x * 2, 1 + y)

    def remove_c_obs(self):
        """Removes the c_obs"""
        for obj in self.c_obs:
            self.rem_ob(obj)
        self.c_obs = []


class InfoBox(Box):
    """Box to display basic text information in"""

    def __init__(self, text, name="", _map=None):
        height = len(text.split("\n")) + 2
        width = sorted([len(i) for i in text.split("\n")])[-1] + 4
        super().__init__(height, width, name=name)
        self.text = se.Text(text)
        self.add_ob(self.text, 2, 1)
        self.map = _map

    def __enter__(self):  # Contextmanagement is fucking awesome!
        """Enter dunder for contextmanagement"""
        self.center_add(self.map)
        self.map.show()
        return self


class InputBox(InfoBox):
    """Box that promps the user to input a text"""

    def __init__(self, infotext, introtext, text, max_len, _map=None):
        height = len(infotext.split("\n")) + 3
        width = sorted([len(i) for i in infotext.split("\n")]
                        + [len(introtext) + 1 + max_len])[-1] + 4
        super(self.__class__.__bases__[0], self).__init__(height, width)
        self.map = _map
        self.infotext = se.Text(infotext)
        self.introtext = se.Text(introtext)
        self.text = se.Text(text)
        self.add_ob(self.infotext, 2, 1)
        self.add_ob(self.introtext, 2, len(infotext.split("\n")) + 1)
        self.add_ob(self.text, self.introtext.rx + len(introtext) + 1,
                    self.introtext.ry)


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
