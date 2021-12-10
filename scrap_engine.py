#!/usr/bin/env python3
"""
Ascii game engine for the terminal.

The main data structures are Map and Object.
Maps are objects, Object objects can be added to and then can be shown on
the screen.

ObjectGroup and their daughters can be used to automate generating, adding,
removing etc. for a list of objects in their defined manner.

States:
    Possible states an object can have are 'solid' and 'float'.
    If an objects state is 'solid' no other object can be set over it,
    so the other objects .set() method will return 1.
    If an objects state is 'float' other objects can be set over them,
    so their .set() methods will return 0.

arg_proto:
    arg_proto is an dictionary that is given to an object by
    the programmer or an object_group(circle, frame, etc.) via the ob_args
    argument.
    This can be used to store various extra values and is especially useful
    when using daughter classes of Object that needs extra values.

This software is licensed under the GPL3
You should have gotten an copy of the GPL3 license alongside this software
Feel free to contribute what ever you want to this engine
You can contribute here: https://github.com/lxgr-linux/scrap_engine
"""

__author__ = "lxgr <lxgr@protonmail.com>"
__version__ = "0.3.3"

import math
import os
import threading
import functools

MAXCACHE_LINE = 512
MAXCACHE_FRAME = 64

try:
    screen_width, screen_height = os.get_terminal_size()
except OSError:
    screen_width, screen_height = 100, 100


class CoordinateError(Exception):
    """
    An Error that is thrown, when an object is added to a non-existing
    part of a map.
    """

    def __init__(self, obj, _map, x, y):
        self.ob = obj
        self.x = x
        self.y = y
        self.map = _map
        super().__init__(f"The {obj}s coordinate ({x}|{y}) is \
not in {self.map.width - 1}x{self.map.height - 1}")


class Map:
    """
    The map, objects can be added to.
    """

    def __init__(self, height=screen_height - 1, width=screen_width,
                 background="#", dynfps=True):
        self.height = height
        self.width = width
        self.dynfps = dynfps
        self.background = background
        self.map = [[self.background for _ in range(width)]
                    for _ in range(height)]
        self.obmap = [[[] for _ in range(width)] for _ in range(height)]
        self.obs = []
        self.out_old = ""

    def blur_in(self, blurmap, esccode="\033[37m"):
        """
        Sets another maps content as its background.
        """
        for h in range(self.height):
            for w in range(self.width):
                if blurmap.map[h][w] != " ":
                    self.map[h][w] = (esccode +
                                      blurmap.map[h][w].replace("\033[0m", "")[-1] +
                                      "\033[0m")
                else:
                    self.map[h][w] = " "
        for obj in self.obs:
            obj.redraw()

    def show(self, init=False):
        """
        Prints the maps content.
        """
        _map = (tuple(arr) for arr in self.map)
        out = self.__show_map(self.height, self.__show_line, _map)
        if self.out_old != out or not self.dynfps or init:
            print(out + "\n\u001b[1000D", end="")
            self.out_old = out

    @staticmethod
    @functools.lru_cache(MAXCACHE_FRAME)
    def __show_map(height, show_line, _map):
        out = f"\r\u001b[{height}A"
        for arr in _map:
            out += show_line(arr)
        return out

    @staticmethod
    @functools.lru_cache(MAXCACHE_LINE)
    def __show_line(arr):
        out_line = ""
        for char in arr:
            out_line += char
        return out_line

    def resize(self, height, width, background="#"):
        """
        Resizes the map to a certain size.
        """
        self.background = background
        self.map = [[self.background for _ in range(width)]
                    for _ in range(height)]
        self.obmap = [[[] for _ in range(width
                                         if width > self.width else self.width)]
                      for _ in range(height
                                     if height > self.height else self.height)]
        self.width = width
        self.height = height
        for obj in self.obs:
            if obj.y < height and obj.x < width:
                self.obmap[obj.y][obj.x].append(obj)
                obj.redraw()


class Submap(Map):
    """
    Behaves just like a map, but it self contains a part of another map.
    """

    def __init__(self, bmap, x, y, height=screen_height - 1,
                 width=screen_width, dynfps=True):
        super().__init__(height, width, dynfps=dynfps)
        del self.background
        self.y = y
        self.x = x
        self.bmap = bmap
        self.remap()

    def remap(self):
        """
        Updates the map (rereads the map, the submap contains a part from)
        """
        self.map = self.__full_bg(self.bmap.background, self.width, self.height)
        self.map = self.__map_to_parent(self.height, self.width, self.y, self.x,
                                        (tuple(line) for line in self.map),
                                        (tuple(line) for line in self.bmap.map))
        for obj in self.obs:
            obj.redraw()

    @staticmethod
    @functools.lru_cache()
    def __map_to_parent(height, width, _y, _x, parent, child):
        parent = [list(line) for line in parent]
        child = [list(line) for line in child]
        for sy, y in zip(range(0, height),
                         range(_y, _y + height)):
            for sx, x in zip(range(0, width),
                             range(_x, _x + width)):
                try:
                    parent[sy][sx] = child[y][x]
                except IndexError:
                    continue
        return parent

    @staticmethod
    @functools.lru_cache(1)
    def __full_bg(background, width, height):
        return [[background for _ in range(width)]
                for _ in range(height)]

    def set(self, x, y):
        """
        Changes the coordinates on the map, the submap is at.
        """
        if x < 0 or y < 0:
            return 1
        self.x = x
        self.y = y
        self.remap()
        return 0

    def full_show(self, init=False):
        """
        Combines remap() and show().
        """
        self.remap()
        self.show(init)


class AddableObject:
    """
    The parent class of any object that can be added to a Map.
    """

    def __init__(self, state=None):
        self.x = None
        self.y = None
        # Those are the relativ coordinated used, when grouped
        self.rx = None
        self.ry = None
        self.added = False
        self.group = None
        self.state = state
        self.map = None


class Object(AddableObject):
    """
    An object, containing a character, that can be added to a map.
    """

    def __init__(self, char, state="solid", arg_proto=None):
        if arg_proto is None:
            arg_proto = {}
        super().__init__(state)
        self.char = char
        self.arg_proto = arg_proto
        self.backup = None

    def add(self, _map, x, y):
        """
        Adds the object to a certain coordinate on a certain map.
        """
        if not 0 <= x < _map.width or not 0 <= y < _map.height:
            raise CoordinateError(self, _map, x, y)
        if len(lis := _map.obmap[y][x]) != 0 and lis[-1].state == "solid":
            return 1
        self.backup = _map.map[y][x]
        self.x = x
        self.y = y
        _map.map[y][x] = self.char
        _map.obmap[y][x].append(self)
        _map.obs.append(self)
        self.map = _map
        self.added = True
        return 0

    def set(self, x, y):
        """
        Sets the object to a certain coordinate.
        """
        if not self.added:
            return 1
        elif x > self.map.width - 1:
            self.bump_right()
            return 1
        elif x < 0:
            self.bump_left()
            return 1
        elif y > self.map.height - 1:
            self.bump_bottom()
            return 1
        elif y < 0:
            self.bump_top()
            return 1
        elif self.x > self.map.width - 1 or self.y > self.map.height - 1:
            self.pull_ob()
            return 1
        for obj in self.map.obmap[y][x]:
            if obj.state == "solid":
                self.bump(obj, self.x - x, self.y - y)
                return 1
        self.__backup_setter()
        self.map.obmap[y][x].append(self)
        self.backup = self.map.map[y][x]
        self.x = x
        self.y = y
        self.map.map[y][x] = self.char
        for obj in self.map.obmap[y][x]:
            if obj.state == "float":
                obj.action(self)
        return 0

    def redraw(self):
        """
        Redraws the object on the map.
        """
        if not self.added:
            return 1
        self.backup = self.map.map[self.y][self.x]
        self.map.map[self.y][self.x] = self.char
        return 0

    def __backup_setter(self):
        if (len(self.map.obmap[self.y][self.x])
                > self.map.obmap[self.y][self.x].index(self) + 1):
            self.map.obmap[self.y][self.x][self.map.obmap[self.y][self.x].index(self) + 1].backup = self.backup
        else:
            self.map.map[self.y][self.x] = self.backup
        del self.map.obmap[self.y][self.x][self.map.obmap[self.y][self.x].index(self)]

    def action(self, ob):
        """
        This is triggered when another object is set over this one.
        """
        return

    def bump(self, ob, x, y):
        """
        This is triggered, when this object is tried to be set onto another
        solid object.
        """
        return

    def bump_right(self):
        """
        Same as bump, but is triggered when hitting the right side of the map.
        """
        return

    def bump_left(self):
        """
        Same as bump, but is triggered when hitting the left side of the map.
        """
        return

    def bump_top(self):
        """
        Same as bump, but is triggered when hitting the top side of the map.
        """
        return

    def bump_bottom(self):
        """
        Same as bump, but is triggered when hitting the bottom side of the map.
        """
        return

    def pull_ob(self):
        """
        This is triggered, when trying to set an object from a non existing
        spot on the map to an existing one.
        This is just usefull when resizing maps with objects out of the
        new size.
        """
        return

    def rechar(self, char):
        """
        Changes the objects character.
        """
        self.char = char
        if not self.added:
            return 1
        self.map.map[self.y][self.x] = self.backup
        self.redraw()
        return 0

    def remove(self):
        """
        Removes the object from the map.
        """
        if not self.added:
            return 1
        self.added = False
        self.__backup_setter()
        del self.map.obs[self.map.obs.index(self)]
        return 0

    def set_state(self, state):
        """
        Chnanges the objects state ('float' or 'solid')
        """
        self.state = state


class ObjectGroup(AddableObject):
    """
    A datatype used to group objects together and do things with them
    simultaniuously.
    """

    def __init__(self, obs, state=None):
        super().__init__(state)
        self.obs = obs
        for obj in obs:
            obj.group = self

    def add_ob(self, obj):
        """
        Adds and object to the group.
        """
        self.obs.append(obj)
        obj.group = self

    def add_obs(self, obs):
        """
        Adds a list of objects to th group.
        """
        for obj in obs:
            self.add_ob(obj)

    def rem_ob(self, obj):
        """
        Removes an object from the group.
        """
        if obj in self.obs:
            obj.group = None
            self.obs.pop(self.obs.index(obj))
            return 0
        return 1

    def move(self, x=0, y=0):
        """
        Moves all objects in the group by a certain vector.
        """
        for obj in self.obs:
            obj.remove()
        for obj in self.obs:
            obj.add(self.map, obj.x + x, obj.y + y)

    def remove(self):
        """
        Removes all objects from their maps.
        """
        for obj in self.obs:
            obj.remove()

    def set(self, x, y):
        """
        Sets the group to a certain coordinate.
        !!! Just use this with inherited classes !!!
        """
        self.move(x - self.x, y - self.y)
        self.x = x
        self.y = y

    def set_state(self, state):
        """
        Sets all objects states to a certain state.
        """
        self.state = state
        for obj in self.obs:
            obj.set_state(state)


class Text(ObjectGroup):
    """
    A datatype containing a string, that can be added to a map.
    Different Texts can be added together with the '+' operator.
    """

    def __init__(self, text, state="solid", esccode="", ob_class=Object,
                 ob_args=None, ignore=""):
        super().__init__([], state)
        if ob_args is None:
            ob_args = {}
        self.ob_class = ob_class
        self.text = text
        self.esccode = esccode
        self.ignore = ignore
        self.ob_args = ob_args
        self.__texter(text)

    def __add__(self, other):
        self.text += other.text
        self.obs += other.obs
        if self.added:
            self.remove()
            self.add(self.map, self.x, self.y)
        return self

    def __texter(self, text):
        for txt in text.split("\n"):
            for char in txt:
                if self.esccode != "":
                    char = self.esccode + char + "\033[0m"
                self.obs.append(self.ob_class(char, self.state,
                                              arg_proto=self.ob_args))
        for obj in self.obs:
            obj.group = self

    def add(self, _map, x, y):
        """
        Adds the text to a certain coordinate on a certain map.
        """
        self.added = True
        self.map = _map
        self.x = x
        self.y = y
        count = 0
        for l, text in enumerate(self.text.split("\n")):
            for i, obj in enumerate(self.obs[count:count + len(text)]):
                if obj.char != self.ignore:
                    obj.add(self.map, x + i, y + l)
            count += len(text)

    def remove(self):
        """
        Removes the text from the map.
        """
        self.added = False
        for obj in self.obs:
            obj.remove()

    def rechar(self, text, esccode=""):
        """
        Changes the string contained in the text.
        """
        self.esccode = esccode
        if self.added:
            for obj in self.obs:
                obj.remove()
        self.obs = []
        self.__texter(text)
        self.text = text
        if self.added:
            self.add(self.map, self.x, self.y)


class Square(ObjectGroup):
    """
    A rectangle, that can be added to a map.
    """

    def __init__(self, char, width, height, state="solid", ob_class=Object,
                 ob_args=None, threads=False):
        super().__init__([], state)
        if ob_args is None:
            ob_args = {}
        self.ob_class = ob_class
        self.width = width
        self.height = height
        self.char = char
        self.exits = []
        self.ob_args = ob_args
        self.threads = threads
        self.__create()

    def __create(self):
        for _ in range(self.height):
            if self.threads:
                threading.Thread(target=self.__one_line_create,
                                 daemon=True).start()
            else:
                self.__one_line_create()

    def __one_line_create(self):
        for _ in range(self.width):
            self.obs.append(self.ob_class(self.char, self.state,
                                          arg_proto=self.ob_args))

    def __one_line_add(self, j):
        for i, obj in enumerate(self.obs[j * self.width: (j + 1) * self.width]):
            self.exits.append(obj.add(self.map, self.x + i, self.y + j))

    def add(self, _map, x, y):
        """
        Adds the square to a certain coordinate on a certain map.
        """
        self.x = x
        self.y = y
        self.map = _map
        for i in range(self.height):
            if self.threads:
                threading.Thread(target=self.__one_line_add, args=(i,),
                                 daemon=True).start()
            else:
                self.__one_line_add(i)
        self.added = True
        if 1 in self.exits:
            return 1
        return 0

    def remove(self):
        """
        Removes the square from the map.
        """
        self.added = False
        for obj in self.obs:
            obj.remove()

    def rechar(self, char):
        """
        Changes the chars the Square is filled with.
        """
        for obj in self.obs:
            obj.rechar(char)

    def resize(self, width, height):
        """
        Resizes the rectangle to a certain size.
        """
        self.width = width
        self.height = height
        if added := self.added:
            self.remove()
        self.obs = []
        self.__create()
        if added:
            self.add(self.map, self.x, self.y)


class Frame(ObjectGroup):
    """
    A Frame made of ascii charactes:

    +----+
    |    |
    |    |
    +----*

    That can be added to map.
    """

    def __init__(self, height, width, corner_chars=None,
                 horizontal_chars=None, vertical_chars=None,
                 state="solid", ob_class=Object, ob_args=None):
        super().__init__([], state)
        if ob_args is None:
            ob_args = {}
        if vertical_chars is None:
            vertical_chars = ["|", "|"]
        if horizontal_chars is None:
            horizontal_chars = ["-", "-"]
        if corner_chars is None:
            corner_chars = ["+", "+", "+", "+"]
        self.height = height
        self.width = width
        self.ob_class = ob_class
        self.ob_args = ob_args
        self.corner_chars = corner_chars
        self.horizontal_chars = horizontal_chars
        self.vertical_chars = vertical_chars
        self.__gen_obs()

    def __gen_obs(self):
        self.corners = [self.ob_class(i, arg_proto=self.ob_args,
                                      state=self.state)
                        for i, j in zip(self.corner_chars, range(4))]
        self.horizontals = [Square(char=i, width=self.width - 2, height=1,
                                   state=self.state, ob_class=Object,
                                   ob_args={})
                            for i, j in zip(self.horizontal_chars, range(2))]
        self.verticals = [Square(char=i, width=1, height=self.height - 2,
                                 state=self.state, ob_class=Object, ob_args={})
                          for i, j in zip(self.vertical_chars, range(2))]

    def __add_obs(self):
        for obj, rx, ry in zip(self.corners, [0, self.width - 1, 0, self.width - 1],
                               [0, 0, self.height - 1, self.height - 1]):
            obj.add(self.map, self.x + rx, self.y + ry)
        for obj, rx, ry in zip(self.horizontals, [1, 1], [0, self.height - 1]):
            obj.add(self.map, self.x + rx, self.y + ry)
        for obj, rx, ry in zip(self.verticals, [0, self.width - 1], [1, 1]):
            obj.add(self.map, self.x + rx, self.y + ry)

    def add(self, _map, x, y):
        """
        Adds the frame to a certain coordinate on a certain map.
        """
        self.x = x
        self.y = y
        self.map = _map
        self.__add_obs()
        self.added = True

    def set(self, x, y):
        """
        Sets the frame to a certain coordinate.
        """
        self.x = x
        self.y = y
        for obj in self.corners + self.horizontals + self.verticals:
            obj.remove()
        self.__add_obs()

    def rechar(self, corner_chars=None, horizontal_chars=None,
               vertical_chars=None):
        """
        Rechars the frame.
        """
        if corner_chars is not None:
            self.corner_chars = corner_chars
        if horizontal_chars is not None:
            self.horizontal_chars = horizontal_chars
        if vertical_chars is not None:
            self.vertical_chars = vertical_chars

        for obj, _c in zip(self.corners, self.corner_chars):
            obj.rechar(_c)
        for obj, _c in zip(self.horizontals, self.horizontal_chars):
            obj.rechar(_c)
        for obj, _c in zip(self.verticals, self.vertical_chars):
            obj.rechar(_c)

    def remove(self):
        """
        Removes the frame from the map.
        """
        for obj in self.corners + self.horizontals + self.verticals:
            obj.remove()
        self.added = False

    def resize(self, height, width):
        """
        Changes the frames size.
        """
        self.height = height
        self.width = width
        if added := self.added:
            self.remove()
        self.__gen_obs()
        if added:
            self.add(self.map, self.x, self.y)


class Box(ObjectGroup):
    """
    A datastucture used to group objects(groups) relative to a certain
    coordinate, that can be added to a map.
    """

    def __init__(self, height, width):
        super().__init__([], None)
        self.height = height
        self.width = width

    def add(self, _map, x, y):
        """
        Adds the box to a certain coordinate on a certain map.
        """
        self.x = x
        self.y = y
        self.map = _map
        for obj in self.obs:
            obj.add(self.map, obj.rx + self.x, obj.ry + self.y)
        self.added = True

    def add_ob(self, obj, x, y):
        """
        Adds an object(group) to a certain coordinate relative to the box.
        """
        self.obs.append(obj)
        obj.rx = x
        obj.ry = y
        if self.added:
            obj.add(self.map, obj.rx + self.x, obj.ry + self.y)

    def set_ob(self, obj, x, y):
        """
        Sets an object(group) to a certain coordinate relative to the box.
        """
        obj.rx = x
        obj.ry = y
        if self.added:
            obj.set(obj.rx + self.x, obj.ry + self.y)

    def remove(self):
        """
        Removes the box from the map.
        """
        for obj in self.obs:
            obj.remove()
        self.added = False

    def resize(self, height, width):
        """
        Resizes the box.
        """
        self.height = height
        self.width = width


class Circle(Box):
    """
    A circle, that can be added to a map.
    """

    def __init__(self, char, radius, state="solid", ob_class=Object,
                 ob_args=None):
        super().__init__(0, 0)
        if ob_args is None:
            ob_args = {}
        self.char = char
        self.ob_class = ob_class
        self.ob_args = ob_args
        self.state = state
        self.__gen(radius)

    def __gen(self, radius):
        self.radius = radius
        for i in range(-(int(radius) + 1), int(radius + 1) + 1):
            for j in range(-(int(radius) + 1), int(radius + 1) + 1):
                if math.sqrt(i ** 2 + j ** 2) <= radius:
                    self.add_ob(self.ob_class(self.char, state=self.state,
                                              arg_proto=self.ob_args), i, j)

    def rechar(self, char):
        """
        Changes the chars the circle is filled with.
        """
        self.char = char
        for obj in self.obs:
            obj.rechar(char)

    def resize(self, radius):
        """
        Resizes the circle.
        """
        if added := self.added:
            self.remove()
        self.obs = []
        self.__gen(radius)
        if added:
            self.add(self.map, self.x, self.y)


class Line(Box):
    """
    A line described by a vector, that cam be added to map.
    """

    def __init__(self, char, cx, cy, l_type="straight", state="solid",
                 ob_class=Object, ob_args=None):
        super().__init__(0, 0)
        if ob_args is None:
            ob_args = {}
        self.char = char
        self.ob_class = ob_class
        self.ob_args = ob_args
        self.state = state
        self.type = l_type
        self.__gen(cx, cy)

    def __gen(self, cx, cy):
        self.cx = cx
        self.cy = cy
        if cx ** 2 >= cy ** 2:
            for i in range(int(math.sqrt(cx ** 2))):
                i = int(cx / math.sqrt(cx ** 2) * i)
                j = {"straight": int, "crippled": round}[self.type](cy * i / cx)
                self.add_ob(self.ob_class(self.char, state=self.state,
                                          arg_proto={**self.ob_args, **{"x": i, "y": cy * i / cx}}),
                            i, j)
        else:
            for j in range(int(math.sqrt(cy ** 2))):
                j = int(cy / math.sqrt(cy ** 2) * j)
                i = {"straight": int, "crippled": round}[self.type](cx * j / cy)
                self.add_ob(self.ob_class(self.char, state=self.state,
                                          arg_proto={**self.ob_args, **{"x": cx * j / cy, "y": j}}),
                            i, j)

    def rechar(self, char):
        """
        Changes the chars the line is made from.
        """
        self.char = char
        for obj in self.obs:
            obj.rechar(char)

    def resize(self, cx, cy):
        """
        Resizes the line.
        """
        if added := self.added:
            self.remove()
        self.obs = []
        self.__gen(cx, cy)
        if added:
            self.add(self.map, self.x, self.y)
