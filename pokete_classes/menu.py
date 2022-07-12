import scrap_engine as se
from . import movemap as mvp
from .ui_elements import ChooseBox, InfoBox
from .mods import ModInfo
from .settings import VisSetting
from .hotkeys import get_action, Action
from .loops import std_loop
from .input import text_input
from .language import HARDCODED_LANGUAGE_NAMES
from .achievements import AchievementOverview


class Menu:
    """Menu to manage settings and other stuff in
    ARGS:
        _map: se.Map this will be shown on"""

    def __init__(self, _map):
        self.map = _map
        self.box = ChooseBox(_map.height - 3, 35, "Menu")
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
                            VisSetting("Load mods", "load_mods",
                                       {True: "On", False: "Off"}),
                            VisSetting("Language", "language",
                                       HARDCODED_LANGUAGE_NAMES),
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

    def __call__(self, pevm, figure, mods, about):
        """Opens the menu"""
        self.realname_label.rechar(figure.name)
        self.char_label.rechar(figure.char)
        with self.box.add(self.map, self.map.width - self.box.width, 0):
            while True:
                action = get_action()
                if action.triggers(Action.ACCEPT):
                    # Fuck python for not having case statements - lxgr
                    #     but it does lmao - Magnus
                    if (i := self.box.c_obs[self.box.index.index]) ==\
                            self.playername_label:
                        figure.name = text_input(self.realname_label, self.map,
                                                 figure.name, 18, 17)
                        self.map.name_label_rechar(figure.name)
                    elif i == self.represent_char_label:
                        inp = text_input(self.char_label, self.map,
                                         figure.char, 18, 1)
                        # excludes bad unicode:
                        if len(inp.encode("utf-8")) != 1:
                            inp = "a"
                            notifier.notify("Error", "Bad character",
                                            "The chosen character has to be a \
valid single-space character!")
                        figure.rechar(inp)
                    elif i == self.mods_label:
                        ModInfo(mvp.movemap, mods.mod_info)()
                    elif i == self.save_label:
                        # When will python3.10 come out?
                        with InfoBox("Saving....", info="", _map=self.map):
                            # Shows a box displaying "Saving...." while saving
                            save()
                            time.sleep(SPEED_OF_TIME * 1.5)
                    elif i == self.exit_label:
                        save()
                        exit()
                    elif i == self.about_label:
                        about()
                    elif i == self.ach_label:
                        AchievementOverview()(mvp.movemap)
                    else:
                        i.change()
                elif action.triggers(Action.UP, Action.DOWN):
                    self.box.input(action)
                elif action.triggers(Action.CANCEL, Action.MENU):
                    break
                std_loop(pevm=pevm)
                self.map.full_show()


menu = None
