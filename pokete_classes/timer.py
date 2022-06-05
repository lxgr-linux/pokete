"""Contains Classes to manage in-game time"""

import logging
import time as time_mod
import scrap_engine as se
from .event import _ev
from .ui_elements import Box
from .loops import std_loop

time = None
clock = None

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

    def emit_input(self):
        """Sets the last input time to the current time"""
        self.last_input = self.time

    @property
    def normalized(self):
        """Returns normalized time"""
        return self.time % (24*60)


class Clock(Box):
    """Clock class to display the current time
    ARGS:
        time: Time object"""

    def __init__(self, time):
        self.time = time
        super().__init__(9, 28, "Clock", "q:close")

    def __call__(self, _map):
        """Shows the clock
        ARGS:
            _map: The map to show on"""
        d_p = True
        letter_obs = self.draw_letters(d_p)
        raw_time = self.time.time
        with self.center_add(_map):
            while True:
                if _ev.get() in ["'q'", "Key.esc"]:
                    _ev.clear()
                    break
                if self.time.time == raw_time + 1:
                    d_p = not d_p
                    letter_obs = self.draw_letters(d_p, letter_obs)
                    raw_time = self.time.time
                self.map.show()
                std_loop()
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
        logging.info(ftime)
        letter_obs = [se.Text(letters[int(letter)]) for letter in ftime]
        letter_obs.insert(2, se.Text(DOUBLE_POINT if d_p else ""))
        _x = 2
        for obj in letter_obs:
            self.add_ob(obj, _x, 2)
            _x += 5
        return letter_obs


def time_threat():
    """Manages the time counting"""
    while True:
        time_mod.sleep(1)
        if time.time < time.last_input + 120:
            time.time += 1
