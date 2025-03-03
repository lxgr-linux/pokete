"""Contains classes and objects related to settings"""

import logging
import scrap_engine as se

from pokete.base.color import Color


class Setting:
    """Setting class grouping a name and a value
    ARGS:
        name: The settings name
        val: The settings value"""

    def __init__(self, name, val):
        self.val = val
        self.name = name


class SliderCursor(se.Text):
    """Wrapper for se.Text to ensure stuff actually works"""

    def move(self, x=0, y=0):
        """
        Moves all objects in the group by a certain vector.
        """
        for obj in self.obs:
            obj.remove()
        for obj in self.obs:
            if self.added:
                obj.add(self.map, obj.x + x, obj.y + y)


class Slider(se.Box):
    """Slider component for menu
    ARGS:
        text: The text to show
        setting: The associated settings name"""

    def __init__(self, text, setting):
        super().__init__(0, 0)
        self.setting = settings(setting)
        self.text = se.Text(text + ":", state="float")
        self.slider = SliderCursor("<o>", state="float")
        self.left = se.Object("[", state="float")
        self.right = se.Object("]", state="float")
        self.line = (
            se.Text(6 * "#", esccode=Color.green, state="float")
            + se.Text(7 * "#", esccode=Color.yellow, state="float")
            + se.Text(6 * "#", esccode=Color.red, state="float")
        )
        self.boundary = self.line.width - 1
        self.add_ob(self.text, 0, 0)
        self.add_ob(self.left, self.text.width + 1, 0)
        self.add_ob(self.line, self.left.rx + 1, 0)
        self.add_ob(self.right, self.line.rx + self.line.width, 0)
        self.add_ob(self.slider, 0, 0)
        self.set_slider_from_setting()

    def add(self, _map, x, y):
        """Add wrapper, see se.Box.add"""
        super().add(_map, x, y)
        self.set_top_redraw(self.left)
        self.set_top_redraw(self.right)

    def set_slider(self, x):
        """Sets the slider to a certain position
        ARGS:
            x: The position"""
        self.set_ob(self.slider, self.left.rx + x, 0)
        self.set_top_redraw(self.left)
        self.set_top_redraw(self.right)

    @staticmethod
    def set_top_redraw(obj):
        """Makes sure object is and will be redrawn
        ARGS:
            obj: The object"""
        if obj.added:
            obj.map.obs.pop(obj.map.obs.index(obj))
            obj.map.obs.append(obj)
            obj.redraw()

    def set_slider_from_setting(self):
        """Sets the sliders position from the given setting"""
        self.set_slider(
            round(self.boundary * self.setting.val / 100)
        )

    @property
    def offset(self):
        """The sliders current position"""
        return self.slider.rx - self.left.rx

    def change(self, val):
        """Changes the current position by a value
        ARGS:
            val: The value"""
        if 0 <= (self.offset + val) <= self.boundary:
            self.set_slider(self.offset + val)
            self.setting.val = round(100 * self.offset / self.boundary)


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
            "volume": 50,
        }
        self.settings = [
            Setting(name, val) for name, val in self.keywords.items()
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
