import scrap_engine as se
from pokete_general_use_fns import liner
from .ui_elements import Box
from .color import Color


class Notification(Box):
    def __init__(self, title, name, desc):
        self.title = title
        self.desc = desc
        self.label = se.Text(title + "\n", esccode=Color.thicc, state="float")\
                   + se.Text(liner(desc, 30), state="float")
        super().__init__(len(self.label.text.split("\n")) + 2,
                         sorted(len(i)
                             for i in self.label.text.split("\n"))[-1] + 4,
                         name)
        self.add_ob(self.label, 2, 1)

    def corner_add(self, _map):
        self.add(_map, _map.width - self.width, 0)

    def shift(self):
        self.x += 1
        for i in self.frame.corners + [k for j in self.frame.horizontals
                 + self.frame.verticals + [self.inner, self.name_label,
                     self.info_label, self.label] for k in j.obs]:
            if i.x == self.map.width - 1:
                i.remove()
            else:
                i.set(i.x + 1, i.y)


class Notifier:
    def __init__(self, _map, logging):
        self.map = _map
        self.logging = logging
        self.wait = []
        self.notified = False
        self.notification = None
        self.counter = -1

    def notify(self, title, name, desc):
        noti = Notification(title, name, desc)
        if self.notified:
            self.wait.append(noti)
        else:
            self.__notify(noti)

    def __notify(self, noti):
        self.notification = noti
        self.notification.corner_add(self.map)
        self.counter = 100
        self.notified = True

    def denotify(self):
        self.counter = -1

    def next(self):
        if self.counter > 0:
            self.counter -= 1
        elif self.counter == 0:
            self.denotify()
        elif self.counter == -1 and self.notified:
            self.notification.shift()
            if self.notification.x == self.map.width - 1:
                self.notification.remove()
                self.notified = False
                if len(self.wait) != 0:
                    self.__notify(self.wait.pop(0))

