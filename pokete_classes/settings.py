"""Contains classes and objects related to settings"""

class Setting:
    """Setting class grouping a name and a value
    ARGS:
        name: The settings name
        val: The settings value"""

    def __init__(self, name, val):
        self.val = val
        self.name = name


class Settings:
    """Contains all possible settings"""

    def __init__(self):
        self.settings = []
        self.keywords = ["autosave", "animations", "save_trainers", "load_mods"]

    def from_dict(self, src):
        """Setts the settings from a dict
        ARGS:
            src: The Dict"""
        for i in src:
            self.settings.append(Setting(i, src[i]))
        for i in self.keywords:
            if i not in [i.name for i in self.settings]:
                self.settings.append(Setting(i, True))

    def __call__(self, name):
        """Gets a Setting object
        ARGS:
            name: The Settings name
        RETURNS:
            Setting object"""
        return [i for i in self.settings if i.name == name][0]

    def to_dict(self):
        """Returns a dict of all current settings"""
        return {i.name: i.val for i in self.settings}


settings = Settings()
