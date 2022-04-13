import logging
import scrap_engine as se
from .ui_elements import Box
from .loops import std_loop
from pokete_classes.event import _ev

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

double_point = """
 ##

 ##"""

class Time:
    def __init__(self, init_time=0):
        self.time = init_time  # time in ingame minutes
        self.last_input = init_time

    def formated(self):
        time = self.time % (24*60)
        hours = int(time / 60)
        minutes = time % 60
        return f"{hours:02}:{minutes:02}"

    def emit_input(self):
        self.last_input = self.time


class Clock(Box):
    def __init__(self, time):
        self.time = time
        super().__init__(9, 28, "Clock", "q:close")

    def __call__(self, _map):
        dp = True
        letter_obs = self.draw_letters(dp)
        raw_time = self.time.time
        with self.center_add(_map):
            while True:
                if _ev.get() in ["'q'", "Key.esc"]:
                    _ev.clear()
                    break
                if self.time.time == raw_time + 1:
                    dp = not dp
                    letter_obs = self.draw_letters(dp, letter_obs)
                    raw_time = self.time.time
                self.map.show()
                std_loop()
            for obj in letter_obs:
                obj.remove()
                self.rem_ob(obj)

    def draw_letters(self, dp=True, letter_obs=[]):
        for obj in letter_obs:
            obj.remove()
            self.rem_ob(obj)
        ftime = self.time.formated().replace(":", "")
        logging.info(ftime)
        letter_obs = [se.Text(letters[int(letter)]) for letter in ftime]
        letter_obs.insert(2, se.Text(double_point if dp else ""))
        _x = 2
        for obj in letter_obs:
            self.add_ob(obj, _x, 2)
            _x += 5
        return letter_obs


time = None
clock = None
