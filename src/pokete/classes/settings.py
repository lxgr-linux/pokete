"""Contains classes and objects related to settings"""

import logging

import scrap_engine as se

from pokete.base import loops
from pokete.base.change import change_ctx
from pokete.base.color import Color
from pokete.base.context import Context
from pokete.base.input.hotkeys import Action, get_action
from pokete.base.input.mouse import MouseEvent, MouseEventType
from pokete.base.mouse import MouseInteractor, mouse_interaction_manager
from pokete.base.ui.input import TextInput
from pokete.base.ui.overview import Overview


class Setting:
    """Setting class grouping a name and a value
    ARGS:
        name: The settings name
        val: The settings value"""

    def __init__(self, name: str, val) -> None:
        self.val = val
        self.name = name


class SliderCursor(se.Text):
    """Wrapper for se.Text to ensure stuff actually works"""

    def move(self, x: int = 0, y: int = 0) -> None:
        """
        Moves all objects in the group by a certain vector.
        """
        for obj in self.obs:
            obj.remove()
        for obj in self.obs:
            if self.added:
                obj.add(self.map, obj.x + x, obj.y + y)


class Slider(se.Box, Overview, MouseInteractor):
    """Slider component for menu
    ARGS:
        text: The text to show
        setting: The associated settings name"""

    def __init__(self, text: str, setting: str) -> None:
        super().__init__(1, 1)
        self.overview: Overview
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

    def add(self, _map, x: int, y: int) -> None:
        """Add wrapper, see se.Box.add"""
        super().add(_map, x, y)
        self.set_top_redraw(self.left)
        self.set_top_redraw(self.right)

    def set_slider(self, x: int) -> None:
        """Sets the slider to a certain position
        ARGS:
            x: The position"""
        self.set_ob(self.slider, self.left.rx + x, 0)
        self.set_top_redraw(self.left)
        self.set_top_redraw(self.right)

    @staticmethod
    def set_top_redraw(obj: se.Object) -> None:
        """Makes sure object is and will be redrawn
        ARGS:
            obj: The object"""
        if obj.added:
            obj.map.obs.pop(obj.map.obs.index(obj))
            obj.map.obs.append(obj)
            obj.redraw()

    def set_slider_from_setting(self) -> None:
        """Sets the sliders position from the given setting"""
        self.set_slider(round(self.boundary * self.setting.val / 100))

    @property
    def offset(self) -> None:
        """The sliders current position"""
        return self.slider.rx - self.left.rx

    def resize_view(self) -> None:
        return self.overview.resize_view()

    def __set_setting(self) -> None:
        self.setting.val = round(100 * self.offset / self.boundary)

    def get_interaction_areas(self) -> list[se.Area]:
        return [e.get_area() for e in self.line.obs]

    def interact(self, ctx: Context, area_idx: int, event: MouseEvent) -> None:
        if area_idx >= 0:
            if event.type == MouseEventType.LEFT:
                if event.pressed:
                    self.set_slider(area_idx)
                    self.__set_setting()
            elif event.type == MouseEventType.DRAG_LEFT:
                self.set_slider(area_idx)
                self.__set_setting()

    def change(self, ctx: Context) -> None:
        """Changes the current position by a value
        ARGS:
            val: The value"""
        self.overview = ctx.overview
        ctx = change_ctx(ctx, self)
        while True:
            action, _ = get_action()
            if (strength := action.get_x_strength()) != 0 and (
                0 <= (self.offset + strength) <= self.boundary
            ):
                self.set_slider(self.offset + strength)
                self.__set_setting()
            if action.triggers(Action.ACCEPT, Action.CANCEL):
                return
            loops.std(ctx)


class VisSetting(se.Text):
    """The setting label for the menu
    ARGS:
        text: The text displayed / the settings name
        setting: The settings name the setting belongs to (load_mods)
        options: Dict containing all options ({True: "On", False: "Off"})"""

    logger = logging.getLogger("VisSetting")

    def __init__(self, text: str, setting: str, options: dict | None = None) -> None:
        if options is None:
            options = {}
        self.options = options
        self.name = text
        self.setting = settings(setting)
        self.index = list(options).index(self.setting.val)
        super().__init__(text + ": " + self.options[self.setting.val], state="float")

    def change(self, ctx: Context) -> None:
        """Change the setting"""
        self.index = (self.index + 1) % len(self.options)
        self.setting.val = list(self.options)[self.index]
        self.rechar(self.name + ": " + self.options[self.setting.val])
        self.logger.info("[Setting][%s] set to %s", self.setting.name, self.setting.val)


class Settings:
    """Contains all possible settings"""

    def __init__(self) -> None:
        self.keywords = {
            "autosave": True,
            "animations": True,
            "save_trainers": True,
            "load_mods": False,
            "audio": True,
            "volume": 50,
        }
        self.settings = [Setting(name, val) for name, val in self.keywords.items()]

    def from_dict(self, src: dict) -> None:
        """Sets the settings from a dict
        ARGS:
            src: The Dict"""
        self.settings = []
        for name, val in src.items():
            self.settings.append(Setting(name, val))
        for i in self.keywords:
            if i not in [j.name for j in self.settings]:
                self.settings.append(Setting(i, self.keywords[i]))

    def __call__(self, name: str) -> Setting:
        """Gets a Setting object
        ARGS:
            name: The Settings name
        RETURNS:
            Setting object"""
        return next(i for i in self.settings if i.name == name)

    def to_dict(self) -> dict:
        """Returns a dict of all current settings"""
        return {i.name: i.val for i in self.settings}


class TextInputBox(se.Box):
    logger = logging.getLogger("TextInputBox")

    def __init__(self, label: str, max_len: int) -> None:
        super().__init__(1, len(label) + 1 + max_len)
        self.max_len = max_len
        self.label = se.Text(label, state="float")
        self.value = se.Text("", state="float")
        self.add_ob(self.label, 0, 0)
        self.add_ob(self.value, len(label) + 1, 0)
        self.__input = TextInput(self.value, self.max_len + 1, self.max_len)

    def __call__(self, ctx: Context) -> str | None:
        mouse_interaction_manager.attach([self.__input])
        return self.__input(ctx)

    def set_value(self, value: str) -> None:
        self.value.rechar(value)


settings = Settings()
