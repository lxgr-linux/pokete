"""Contains classes and objects related to settings"""

import logging
import scrap_engine as se


class Setting:
    """Setting class grouping a name and a value
    ARGS:
        name: The settings name
        val: The settings value"""

    def __init__(self, name, val):
        self.val = val
        self.name = name


class VisSetting(se.Text):
    """The setting label for the menu
    ARGS:
        text: The text displayed / the settings name
        setting: The settings name the setting belongs to (load_mods)
        options: Dict containing all options ({True: "On", False: "Off"})"""

    def __init__(self, text, setting, options=None):
        if options is None:
            options = {}
        self.options = options
        self.name = text
        self.setting = settings(setting)
        self.index = list(options).index(self.setting.val)
        super().__init__(text + ": " + self.options[self.setting.val],
                         state="float")

    def change(self):
        """Change the setting"""
        self.index = (self.index + 1) % len(self.options)
        self.setting.val = list(self.options)[self.index]
        self.rechar(self.name + ": " + self.options[self.setting.val])
        logging.info("[Setting][%s] set to %s", self.setting.name,
                     self.setting.val)


class Settings:
    """Contains all possible settings"""

    def __init__(self):
        self.keywords = {
            "autosave": True,
            "animations": True,
            "save_trainers": True,
            "load_mods": False,
            "audio": True,
            "volume": 100,
        }
        self.settings = [
            Setting(name, val) for nam, val in self.keywords.items()
        ]

    def from_dict(self, src):
        """Sets the settings from a dict
        ARGS:
            src: The Dict"""
        self.settings = []
        for name, val in src.items():
            self.settings.append(Setting(name, val))
        for i in self.keywords:
            if i not in [j.name for j in self.settings]:
                self.settings.append(Setting(i, self.keywords[i]))

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
