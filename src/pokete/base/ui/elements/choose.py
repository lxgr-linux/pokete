import scrap_engine as se

from .box import Box
from pokete.base.input import ACTION_DIRECTIONS, ACTION_UP_DOWN, Action, \
    ActionList


class BoxIndex(se.Object):
    """Index that can be used in ChooseBox"""

    def __init__(self):
        super().__init__("*", state="float")
        self.index = 0


class ChooseBox(Box):
    """Box that contains items you can choose from
    ARGS:
        height: The boxes height
        width: The boxes width
        name: The boxes displayed name
        info: Info that will be displayed in the bottom left corner of the box
        index_x: The indexes x-coordinate
        c_obs: List of se.Texts that can be choosen from"""

    def __init__(
        self, height, width, name="", info="",
        index_x=2, c_obs=None, overview=None
    ):
        super().__init__(height, width, name, info, overview=overview)
        self.index_x = index_x
        self.index = BoxIndex()
        if c_obs is not None:
            self.add_c_obs(c_obs)
        else:
            self.c_obs = []
        # adding
        self.add_ob(self.index, self.index_x, 1)

    def input(self, input: ActionList):
        """Moves the cursor in the box
        ARGS:
             inp: Inputted action"""
        assert input.triggers(*ACTION_UP_DOWN)
        y_str = input.get_y_strength()
        if input.triggers(Action.UP):
            inp = Action.UP
        else:
            inp = Action.DOWN
        if {
            Action.DOWN: self.index.index + 1 < len(self.c_obs),
            Action.UP: self.index.index - 1 >= 0
        }[inp]:
            self.index.index += y_str
        else:
            self.index.index = {
                Action.DOWN: 0,
                Action.UP: len(self.c_obs) - 1,
            }[inp]
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

    def __init__(
        self, columns, labels: list[se.Text],
        name="", _map=None, overview=None
    ):
        self.nest_label_obs = []
        self.set_items(columns, labels, init=True)
        super().__init__(
            3 * len(self.nest_label_obs) + 2,
            sum(i.width for i in self.nest_label_obs[0]) + 2,
            name, f"{Action.CANCEL.mapping}:close",
            overview=overview
        )
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

    def input(self, input: ActionList):
        """Evaluates user input
        ARGS:
            inp: Inputted string"""
        assert input.triggers(*ACTION_DIRECTIONS)
        if input.triggers(Action.UP):
            inp = Action.UP
        elif input.triggers(Action.LEFT):
            inp = Action.LEFT
        elif input.triggers(Action.RIGHT):
            inp = Action.RIGHT
        else:
            inp = Action.DOWN
        _c = {
            Action.UP: (-1, 0),
            Action.DOWN: (1, 0),
            Action.LEFT: (0, -1),
            Action.RIGHT: (0, 1),
        }[inp]
        self.set_index((self.index[0] + _c[0])
                       % len([i for i in self.nest_label_obs if len(i) >
                              self.index[1]]),
                       (self.index[1] + _c[1])
                       % len(self.nest_label_obs[self.index[0]]))

    def set_items(self, columns, labels: list[se.Text], init=False):
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
        self.nest_label_obs = [
            label_obs[i * columns:(i + 1) * columns]
            for i in range(max(round(len(labels) / columns + 0.49), 1))
        ]
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
