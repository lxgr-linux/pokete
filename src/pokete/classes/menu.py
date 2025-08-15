import sys
import time
from typing import Never, Optional

import scrap_engine as se

from pokete.base.context import Context
from pokete.base.input.hotkeys import ActionList
from pokete.base.input_loops import text_input
from pokete.base.ui.elements import InfoBox
from pokete.base.ui.notify import notifier
from pokete.base.ui.views.choose_box import ChooseBoxView
from pokete.release import SPEED_OF_TIME

from .achievements import AchievementOverview
from .audio import audio
from .mods import ModInfo
from .save import save
from .settings import Slider, VisSetting, settings
from .side_loops import About


class Menu(ChooseBoxView):
    def __init__(self):
        super().__init__(50, 35, "Menu")
        self.playername_input = TextInputBox("Playername:", 17)
        self.represent_char_input = TextInputBox("Char:", 1)
        self.mods_label = se.Text("Mods", state="float")
        self.ach_label = se.Text("Achievements", state="float")
        self.about_label = se.Text("About", state="float")
        self.save_label = se.Text("Save", state="float")
        self.exit_label = se.Text("Exit", state="float")
        self.elems = [
            self.playername_input,
            self.represent_char_input,
            VisSetting("Autosave", "autosave", {True: "On", False: "Off"}),
            VisSetting("Animations", "animations", {True: "On", False: "Off"}),
            VisSetting(
                "Save trainers", "save_trainers", {True: "On", False: "Off"}
            ),
            VisSetting("Audio", "audio", {True: "On", False: "Off"}),
            Slider("Volume", "volume"),
            VisSetting("Load mods", "load_mods", {True: "On", False: "Off"}),
            self.mods_label,
            self.ach_label,
            self.about_label,
            self.save_label,
            self.exit_label,
        ]

    def handle_extra_actions(self, ctx: Context, action: ActionList) -> bool:
        i = self.c_obs[self.index.index]
        volume_before = settings("volume").val
        if (strength := action.get_x_strength()) != 0:
            if isinstance(i, Slider):
                i.change(strength)
        if volume_before != settings("volume").val:
            audio.play(ctx.figure.map.song)
        return False

    def choose(self, ctx: Context, idx: int) -> Optional[Never]:
        i = self.c_obs[self.index.index]
        audio_before = settings("audio").val
        if i == self.playername_input:
            ctx.figure.name = self.playername_input(ctx)
            self.map.name_label_rechar(ctx.figure.name)
        elif i == self.represent_char_input:
            inp = self.represent_char_input(ctx)
            # excludes bad unicode:
            if len(inp.encode("utf-8")) != 1 and inp not in [
                "ä",
                "ö",
                "ü",
                "ß",
            ]:
                inp = "a"
                self.represent_char_input.set_value(inp)
                notifier.notify(
                    "Error",
                    "Bad character",
                    "The chosen character has to be a \
valid single-space character!",
                )
            ctx.figure.rechar(inp)
        elif i == self.mods_label:
            ModInfo()(ctx)
        elif i == self.save_label:
            # When will python3.10 come out?
            with InfoBox(
                "Saving....",
                info="",
                ctx=ctx,
            ):
                # Shows a box displaying "Saving...." while saving
                save(ctx.figure)
                time.sleep(SPEED_OF_TIME * 1.5)
        elif i == self.exit_label:
            save(ctx.figure)
            sys.exit()
        elif i == self.about_label:
            About()(ctx)
        elif i == self.ach_label:
            AchievementOverview()(ctx)
        elif isinstance(i, VisSetting):
            i.change()
        if audio_before != settings("audio").val:
            audio.play(ctx.figure.map.song)

    def __call__(self, ctx: Context):
        """Opens the dex"""
        self.resize(ctx.map.height - 3, 35)
        self.playername_input.set_value(ctx.figure.name)
        self.represent_char_input.set_value(ctx.figure.char)
        self.add_elems()
        with self.add(ctx.map, ctx.map.width - self.width, 0):
            return super().__call__(ctx)


class TextInputBox(se.Box):
    def __init__(self, label: str, max_len: int):
        super().__init__(1, len(label) + 1 + max_len)
        self.max_len = max_len
        self.label = se.Text(label, state="float")
        self.value = se.Text("", state="float")
        self.add_ob(self.label, 0, 0)
        self.add_ob(self.value, len(label) + 1, 0)

    def __call__(self, ctx: Context) -> str:
        return text_input(
            ctx,
            self.value,
            self.value.text,
            self.max_len + 1,
            self.max_len,
        )

    def set_value(self, value: str):
        self.value.rechar(value)
