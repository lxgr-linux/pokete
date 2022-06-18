"""This file contains most of the user interface
elements used in Pokete"""

import scrap_engine as se


class BoxIndex(se.Object):
    """Index that can be used in ChooseBox"""

    def __init__(self):
        super().__init__("*", state="float")
        self.index = 0


class StdFrame(se.Frame):
    """Standardized frame
    ARGS:
        height: The frames height
        width: The frames width"""

    def __init__(self, height, width):
        super().__init__(width=width, height=height,
                         corner_chars=["┌", "┐", "└", "┘"],
                         horizontal_chars=["─", "─"],
                         vertical_chars=["│", "│"], state="float")


class StdFrame2(se.Frame):
    """Standardized frame
    ARGS:
        height: The frames height
        width: The frames width"""

    def __init__(self, height, width, state="solid"):
        super().__init__(width=width, height=height,
                         corner_chars=["_", "_", "|", "|"],
                         horizontal_chars=["_", "_"], state=state)


class Box(se.Box):
    """Box to show content in
    ARGS:
        height: The boxes height
        width: The boxes width
        name: The boxes displayed name
        info: Info that will be displayed in the bottom left corner of the box"""

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
        """Adds the box to the maps center
        ARGS:
            _map: se.Map the box will be added to"""
        self.add(_map, round((_map.width - self.width) / 2),
                 round((_map.height - self.height) / 2))
        return self

    def resize(self, height, width):
        """Resizes the box to a certain size
        See se.Box.resize"""
        super().resize(height, width)
        self.inner.resize(width - 2, height - 2)
        self.frame.resize(height, width)
        self.set_ob(self.name_label, 2, 0)
        self.set_ob(self.info_label, 2, self.height - 1)

    def add(self, _map, x, y):
        """Adds the box to a map
        See se.Box.add"""
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
    """Box that contains items you can choose from
    ARGS:
        height: The boxes height
        width: The boxes width
        name: The boxes displayed name
        info: Info that will be displayed in the bottom left corner of the box
        index_x: The indexes x-coordinate
        c_obs: List of se.Texts that can be choosen from"""

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

    def input(self, inp):
        """Moves the cursor in the box
        ARGS:
             inp: Inputted char"""
        if {"'s'": self.index.index + 1 < len(self.c_obs),
                "'w'": self.index.index - 1 >= 0}[inp]:
            self.index.index += {"'s'": 1, "'w'": -1}[inp]
        else:
            self.index.index = {"'s'": 0, "'w'": len(self.c_obs) - 1}[inp]
        self.set_index()

    def set_index(self, index=None):
        """Sets the cursors index
        ARGS:
            index: The new index, if None the old index will be used"""
        if index is not None:
            self.index.index = index
        self.set_ob(self.index, self.index.rx, self.c_obs[self.index.index].ry)

    def add_c_obs(self, _list):
        """Adds the c_obs (the objects that can be chosen from) to the box
        ARGS:
            _list: List of se.Texts"""
        self.c_obs = _list
        for _y, obj in enumerate(self.c_obs):
            self.add_ob(obj, self.index_x * 2, 1 + _y)

    def remove_c_obs(self):
        """Removes the c_obs"""
        for obj in self.c_obs:
            self.rem_ob(obj)
        self.c_obs = []


class BetterChooserItem(Box):
    """Item for Better Choosebox
    ARGS:
        height: The boxes height
        width: The boxes width
        text: The boxes displayed text
        ind: The bpxes index"""

    def __init__(self, height, width, text, ind):
        super().__init__(height, width)
        self.ind = ind
        self.label = text
        self.add_ob(self.label, 2, 1)

    def choose(self):
        """Rechars the frame to be highlighted"""
        self.frame.rechar(corner_chars=["┏", "┓", "┗", "┛"],
                          horizontal_chars=["━", "━"],
                          vertical_chars=["┃", "┃"])

    def unchoose(self):
        """Rechars the frame to be not highlighted"""
        self.frame.rechar(corner_chars=["┌", "┐", "└", "┘"],
                          horizontal_chars=["─", "─"],
                          vertical_chars=["│", "│"])


class BetterChooseBox(Box):
    """Better Choosebox using a tile layout
    ARGS:
        columns: Number of columns
        labels: List of se.Texts
        name: The boxes displayed name
        _map: The map it will be shown on"""

    def __init__(self, columns, labels: [se.Text], name="", _map=None):
        self.nest_label_obs = []
        self.set_items(columns, labels, init=True)
        super().__init__(3 * len(self.nest_label_obs) + 2,
                         sum(i.width for i in self.nest_label_obs[0]) + 2,
                         name, "q:close")
        self.map = _map
        self.__add_obs()
        self.index = (0, 0)
        self.get_item(*self.index).choose()

    def set_index(self, _y, _x):
        """Sets index and chooses item
        ARGS:
            _y: Y-Coordinate in the box
            _x: X-Coordinate in the box"""
        self.get_item(*self.index).unchoose()
        self.index = (_y, _x)
        self.get_item(*self.index).choose()

    def get_item(self, _y, _x):
        """Gives a chosen element
        ARGS:
            _y: Y-Coordinate in the box
            _x: X-Coordinate in the box
        RETURNS:
            The BetterChooseBoxItem at the coordinate"""
        return self.nest_label_obs[_y][_x]

    def input(self, inp):
        """Evaluates user input
        ARGS:
            inp: Inputted string"""
        _c = {"'w'": (-1, 0),
              "'s'": (1, 0),
              "'a'": (0, -1),
              "'d'": (0, 1)}[inp]
        self.set_index((self.index[0] + _c[0])
                            % len([i for i in self.nest_label_obs if len(i) >
                                self.index[1]]),
                       (self.index[1] + _c[1])
                            % len(self.nest_label_obs[self.index[0]]))

    def set_items(self, columns, labels: [se.Text], init=False):
        """Sets the items shown in the box
        ARGS:
            columns: Number of columns
            labels: List of se.Texts that will be shown on the items
            init: Whether or not the box is initiated"""
        for i in self.nest_label_obs:
            for obj in i:
                self.rem_ob(obj)
        box_width = sorted(len(i.text) for i in labels)[-1]
        label_obs = [BetterChooserItem(3, box_width + 4, label, i)
                     for i, label in enumerate(labels)]
        self.nest_label_obs = [label_obs[i * columns:(i + 1) * columns]
                               for i in range(int(len(labels) / columns) + 1)]
        if not init:
            self.resize(3 * len(self.nest_label_obs) + 2,
                        sum(i.width for i in self.nest_label_obs[0]) + 2)
            self.__add_obs()
            try:
                self.set_index(*self.index)
            except IndexError:
                self.index = (0, 0)
                self.get_item(*self.index).choose()

    def __add_obs(self):
        """Adds items to the box"""
        for i, arr in enumerate(self.nest_label_obs):
            for j, obj in enumerate(arr):
                self.add_ob(obj, 1 + j * obj.width, 1 + i * obj.height)

    def __enter__(self):
        """Enter dunder for context management"""
        self.center_add(self.map)
        self.map.show()
        return self


class LabelBox(Box):
    """A Box just containing one label
    ARGS:
        label: The se.Text label
        name: The boxes displayed name
        info: Info that will be displayed in the bottom left corner of the box"""

    def __init__(self, label, name="", info=""):
        self.label = label
        super().__init__(label.height + 2, label.width + 4, name, info)
        self.add_ob(label, 2, 1)


class InfoBox(LabelBox):
    """Box to display basic text information in
    ARGS:
        text: String displayed
        name: The boxes displayed name
        info: Info that will be displayed in the bottom left corner of the box
        _map: The se.Map this will be shown on"""

    def __init__(self, text, name="", info="q:close", _map=None):
        super().__init__(se.Text(text), name=name, info=info)
        self.map = _map

    def __enter__(self):  # Contextmanagement is fucking awesome!
        """Enter dunder for contextmanagement"""
        self.center_add(self.map)
        self.map.show()
        return self


class InputBox(InfoBox):
    """Box that promps the user to input a text
    ARGS:
        _map: The map the input box should be shown on
        infotext: The information text about the input
        introtext: The text that introduces the text field
        text: The default text in the text field
        name: The boxes desplayed name
        max_len: Max length of the text"""

    def __init__(self, infotext, introtext, text, max_len, name="", _map=None):
        height = len(infotext.split("\n")) + 3
        width = sorted([len(i) for i in infotext.split("\n")]
                        + [len(introtext) + 1 + max_len])[-1] + 4
        super(LabelBox, self).__init__(height, width, name)
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
