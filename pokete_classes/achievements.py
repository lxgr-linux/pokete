"""Classes relate to achievements"""


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
