import sys
import time

import scrap_engine as se
from pokete.release import SPEED_OF_TIME
from pokete.base import loops
from pokete.base.context import Context
from pokete.base.input import get_action, Action, _ev
from pokete.base.input_loops import text_input
from pokete.base.ui import notifier, Overview
from pokete.base.ui.elements import ChooseBox, InfoBox
from .achievements import AchievementOverview
from .audio import audio
from .mods import ModInfo
from .save import save
from .settings import VisSetting, Slider, settings
from .side_loops import About


class Menu(Overview):
    """Menu to manage settings and other stuff in"""

    def __init__(self):
        self.map = None
        self.box = ChooseBox(50, 35, "Menu")
        self.playername_label = se.Text("Playername: ", state="float")
        self.represent_char_label = se.Text("Char: ", state="float")
        self.mods_label = se.Text("Mods", state="float")
        self.ach_label = se.Text("Achievements", state="float")
        self.about_label = se.Text("About", state="float")
        self.save_label = se.Text("Save", state="float")
        self.exit_label = se.Text("Exit", state="float")
        self.realname_label = se.Text("", state="float")
        self.char_label = se.Text("", state="float")
        self.box.add_c_obs([self.playername_label,
                            self.represent_char_label,
                            VisSetting("Autosave", "autosave",
                                       {True: "On", False: "Off"}),
                            VisSetting("Animations", "animations",
                                       {True: "On", False: "Off"}),
                            VisSetting("Save trainers", "save_trainers",
                                       {True: "On", False: "Off"}),
                            VisSetting("Audio", "audio",
                                       {True: "On", False: "Off"}),
                            Slider("Volume", "volume"),
                            VisSetting("Load mods", "load_mods",
                                       {True: "On", False: "Off"}),
                            self.mods_label, self.ach_label,
                            self.about_label, self.save_label,
                            self.exit_label])
        # adding
        self.box.add_ob(self.realname_label,
                        self.playername_label.rx + self.playername_label.width,
                        self.playername_label.ry)
        self.box.add_ob(self.char_label,
                        self.represent_char_label.rx
                        + self.represent_char_label.width,
                        self.represent_char_label.ry)

    def resize_view(self):
        """Manages recursive view resizing"""
        self.box.remove()
        self.box.overview.resize_view()
        self.box.resize(self.map.height - 3, 35)
        self.box.add(self.map, self.map.width - self.box.width, 0)

    def __call__(self, ctx: Context):
        """Opens the menu"""
        self.map = ctx.map
        figure = ctx.figure
        self.box.set_ctx(ctx)

        self.box.resize(self.map.height - 3, 35)
        self.realname_label.rechar(figure.name)
        self.char_label.rechar(figure.char)
        audio_before = settings("audio").val
        volume_before = settings("volume").val
        with self.box.add(self.map, self.map.width - self.box.width, 0):
            _ev.clear()
            while True:
                action = get_action()
                i = self.box.c_obs[self.box.index.index]
                if (strength := action.get_x_strength()) != 0:
                    if isinstance(i, Slider):
                        i.change(strength)
                elif action.triggers(Action.ACCEPT):
                    # Fuck python for not having case statements - lxgr
                    #     but it does lmao - Magnus
                    if i == self.playername_label:
                        figure.name = text_input(
                            ctx.with_overview(self),
                            self.realname_label,
                            figure.name, 18, 17
                        )
                        self.map.name_label_rechar(figure.name)
                    elif i == self.represent_char_label:
                        inp = text_input(
                            ctx.with_overview(self),
                            self.char_label,
                            figure.char, 18, 1
                        )
                        # excludes bad unicode:
                        if (
                            len(inp.encode("utf-8")) != 1
                            and inp not in ["ä", "ö", "ü", "ß"]
                        ):
                            inp = "a"
                            self.char_label.rechar(inp)
                            notifier.notify("Error", "Bad character",
                                            "The chosen character has to be a \
valid single-space character!")
                        figure.rechar(inp)
                    elif i == self.mods_label:
                        ModInfo()(ctx.with_overview(self))
                    elif i == self.save_label:
                        # When will python3.10 come out?
                        with InfoBox("Saving....", info="",
                                     ctx=ctx.with_overview(self.box)):
                            # Shows a box displaying "Saving...." while saving
                            save(figure)
                            time.sleep(SPEED_OF_TIME * 1.5)
                    elif i == self.exit_label:
                        save(figure)
                        sys.exit()
                    elif i == self.about_label:
                        About()(ctx.with_overview(self))
                    elif i == self.ach_label:
                        AchievementOverview()(ctx.with_overview(self))
                    elif isinstance(i, VisSetting):
                        i.change()
                if (
                    audio_before != settings("audio").val
                    or volume_before != settings("volume").val
                ):
                    audio.switch(figure.map.song)
                    audio_before = settings("audio").val
                    volume_before = settings("volume").val
                elif action.triggers(Action.UP, Action.DOWN):
                    self.box.input(action)
                elif action.triggers(Action.CANCEL, Action.MENU):
                    break
                loops.std(ctx.with_overview(self))
                self.map.full_show()
