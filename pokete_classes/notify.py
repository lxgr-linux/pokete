"""Contains classes for notifications"""

import scrap_engine as se
from pokete_general_use_fns import liner
from .ui_elements import LabelBox
from .color import Color


class Notification(LabelBox):
    """Notification box
    ARGS:
        title: The bold title shown in the box
        name: The name displayed at the boxes top
        desc: The notifications description"""

    def __init__(self, title, name, desc):
        self.title = title
        self.desc = desc
        label = se.Text(title + "\n", esccode=Color.thicc, state="float")\
                + se.Text(liner(desc, 30), state="float")
        super().__init__(label, name)

    def corner_add(self, _map):
        """Adds the Notification to a map
        ARGS:
            _map: The se.Map to add this to"""
        self.add(_map, _map.width - self.width, 0)

    def shift(self):
        """Shifts the box to the right"""
        self.x += 1
        for i in self.frame.corners + [k for j in self.frame.horizontals
                                       + self.frame.verticals + [
                                           self.inner, self.name_label,
                                           self.info_label,
                                           self.label] for k in j.obs]:
            if i.x == self.map.width - 1:
                i.remove()
            else:
                i.set(i.x + 1, i.y)
        self.map.show()


class Notifier:
    """Class managing notifications"""

    def __init__(self):
        self.map = None
        self.wait = []
        self.notified = False
        self.notification = None
        self.counter = -1

    def set_vars(self, _map):
        """Sets map variable
        ARGS:
            _map: The se.Map the notifications will be shown on"""
        self.map = _map

    def notify(self, title, name, desc):
        """Initilizes a Notification and manages it
        ARGS:
            title: The bold title shown in the box
            name: The name displayed at the boxes top
            desc: The notifications description"""
        noti = Notification(title, name, desc)
        if self.notified:
            self.wait.append(noti)
        else:
            self.__notify(noti)

    def __notify(self, noti):
        """Shows a Notifications
        ARGS:
            noti: The Notification"""
        self.notification = noti
        self.notification.corner_add(self.map)
        self.counter = 100
        self.notified = True

    def next(self):
        """Manages counter, removes current and adds next notification"""
        if self.counter >= 0:
            self.counter -= 1
        elif self.counter == -1 and self.notified:
            self.notification.shift()
            if self.notification.x == self.map.width - 1:
                self.notification.remove()
                self.notified = False
                self.map.show()
                if len(self.wait) != 0:
                    self.__notify(self.wait.pop(0))


notifier = Notifier()
