"""Classes relate to achievements"""

import time
import scrap_engine as se
from pokete_general_use_fns import std_loop, liner
from .ui_elements import BetterChooseBox, Box
from .color import Color


class Achievement:
    """The Achievement class that groups identifier, title and description
    of an possible Achiement
    ARGS:
        identifier: Identifier ("first_poke")
        title: Title ("First Pokete")
        desc: Description ("Catch your first Pokete")"""

    def __init__(self, identifier, title, desc):
        self.identifier = identifier
        self.title = title
        self.desc = desc


class Achievements:
    """Manages Achiements
    ARGS:
        logging: logging module
        notifier: Notifier object"""

    def __init__(self, logging, notifier):
        self.logging = logging
        self.notifier = notifier
        self.achievements = []
        self.achieved = []

    def set_achieved(self, achieved):
        """Sets the achieved Achievements
        ARGS:
            achieved: List of identifiers of the achived Achievements"""
        self.achieved = achieved

    def add(self, identifier, title, desc):
        """Generates an Achiement
        See Achievement"""
        self.achievements.append(Achievement(identifier, title, desc))

    def achieve(self, identifier):
        """Checks and achives an Achievement
        ARGS:
            identifier: The Achievements identifier"""
        if identifier not in self.achieved:
            ach = [i for i in self.achievements
                    if i.identifier == identifier][0]
            self.notifier.notify(ach.title, "Achiement unlocked!", ach.desc)
            self.achieved.append(identifier)
            self.logging.info("[Achiements] Unlocked %s", identifier)


class AchBox(Box):
    """Box with info about an Achievement
    ARGS:
        ach: The Achievement
        achiements: Achievements object"""

    def __init__(self, ach, achievements):
        self.label = se.Text("Achieved: ", state="float")\
                   + se.Text("Yes" if ach.identifier
                                in achievements.achieved
                             else "No",
                             esccode=Color.thicc
                             + (Color.green
                                    if ach.identifier
                                        in achievements.achieved
                                else Color.grey), state="float")\
                   + se.Text("\n" + liner(ach.desc, 30), state="float")
        super().__init__(len(self.label.text.split("\n")) + 2,
                         sorted(len(i)
                             for i in self.label.text.split("\n"))[-1] + 4,
                         name=ach.title, info="q:close")
        self.add_ob(self.label, 2, 1)


class AchievementOverview(BetterChooseBox):
    """Overview for Achievements
    ARGS:
        achievements: Achievements object"""

    def __init__(self, achievements):
        self.achievements = achievements
        super().__init__(4, [se.Text(" ")], name="Achievements")

    def __call__(self, _ev, _map):
        """Input loop
        ARGS:
            _ev: Event object
            _map: se.Map to show this on"""
        self.set_items(4, [se.Text(i.title,
                                   esccode=Color.thicc + Color.green
                                    if i.identifier
                                        in self.achievements.achieved
                                    else "", state="float")
                           for i in self.achievements.achievements])
        self.map = _map
        with self:
            while True:
                if _ev.get() in ["'w'", "'s'", "'a'", "'d'"]:
                    self.input(_ev.get())
                    _ev.clear()
                elif _ev.get() in ["'q'", "Key.esc"]:
                    _ev.clear()
                    break
                elif _ev.get() == "Key.enter":
                    _ev.clear()
                    ach = self.achievements.achievements[
                            self.get_item(*self.index).ind]
                    with AchBox(ach, self.achievements).center_add(_map):
                        while True:
                            if _ev.get() in ["'q'", "Key.esc"]:
                                _ev.clear()
                                break
                            std_loop(_ev)
                            time.sleep(0.05)
                std_loop(_ev)
                time.sleep(0.05)
                self.map.show()
