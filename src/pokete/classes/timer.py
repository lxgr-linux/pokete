"""Contains Classes to manage in-game time"""

import time as time_mod

import scrap_engine as se

from pokete.base import loops
from pokete.base.change import change_ctx
from pokete.base.context import Context
from pokete.base.input import Action, get_action
from pokete.base.input.mouse import MouseEvent
from pokete.base.mouse import MouseInteractor
from pokete.base.ui.elements import Box
from pokete.base.ui.elements.labels import CloseLabel
from pokete.release import SPEED_OF_TIME

letters = [
    """ ##
#  #
#  #
#  #
 ##""",
    """  #
 ##
  #
  #
 ###""",
    """ ##
#  #
  #
 #
####""",
    """ ##
#  #
  #
#  #
 ##""",
    """  #
 ##
####
  #
  #""",
    """####
#
###
   #
###""",
    """  #
 #
###
#  #
 ##""",
    """####
   #
  #
 #
#""",
    """ ##
#  #
 ##
#  #
 ##""",
    """ ##
#  #
 ###
  #
 #""",
]

DOUBLE_POINT = """
 ##

 ##"""


class Time:
    """Timer class to keep track of in-game time
    ARGS:
        init_time: The initial time used for the timer"""

    def __init__(self, init_time=0):
        self.time = init_time  # time in in-game minutes
        self.last_input = init_time

    def formatted(self):
        """Returns the in-game time in a formatted manner"""
        _t = self.normalized
        hours = int(_t / 60)
        minutes = _t % 60
        return f"{hours:02}:{minutes:02}"

    def set(self, t):
        self.time = t
        self.last_input = t

    def emit_input(self):
        """Sets the last input time to the current time"""
        self.last_input = self.time

    @property
    def normalized(self):
        """Returns normalized time"""
        return self.time % (24 * 60)


time = Time()


class Clock(Box, MouseInteractor):
    """Clock class to display the current time
    ARGS:
        time_ob: Time object"""

    def __init__(self, time_ob):
        self.time = time_ob
        super().__init__(
            9,
            28,
            "Clock",
            [CloseLabel()],
        )

    def interact(self, ctx: Context, area_idx: int, event: MouseEvent): ...

    def get_interaction_areas(self) -> list[se.Area]:
        return []

    def get_partial_interactors(self) -> list["MouseInteractor"]:
        return [i for i in self.info_labels if isinstance(i, MouseInteractor)]

    def __call__(self, ctx: Context):
        """Shows the clock"""
        self.set_ctx(ctx)
        ctx = change_ctx(ctx, self)
        d_p = True
        letter_obs = self.draw_letters(d_p)
        raw_time = self.time.time
        with self.center_add(self.map):
            while True:
                if get_action()[0].triggers(*(Action.CANCEL, Action.CLOCK)):
                    break
                if self.time.time == raw_time + 1:
                    d_p = not d_p
                    letter_obs = self.draw_letters(d_p, letter_obs)
                    raw_time = self.time.time
                loops.std(ctx)
            self.__rem_obs(letter_obs)

    def __rem_obs(self, letter_obs):
        """Removed all letters from the clock
        ARGS:
            letter_obs: The list of letters"""
        for obj in letter_obs:
            obj.remove()
            self.rem_ob(obj)

    def draw_letters(self, d_p=True, letter_obs=None):
        """Method to draw the letters on the clock
        ARGS:
            d_p: Whether or not the DOUBLE_POINT should be shown
            letter_obs: The letter objects of the former intervall"""
        if letter_obs is None:
            letter_obs = []
        self.__rem_obs(letter_obs)
        ftime = self.time.formatted().replace(":", "")
        letter_obs = [se.Text(letters[int(letter)]) for letter in ftime]
        letter_obs.insert(2, se.Text(DOUBLE_POINT if d_p else ""))
        _x = 2
        for obj in letter_obs:
            self.add_ob(obj, _x, 2)
            _x += 5
        return letter_obs


clock = Clock(time)


def time_threat():
    """Manages the time counting"""
    while True:
        time_mod.sleep(SPEED_OF_TIME * 1)
        if time.time < time.last_input + 120:
            time.time += 1
