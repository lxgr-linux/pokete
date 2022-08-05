"""Contains the Pokete dex that gives information about all Poketes"""

import scrap_engine as se
from pokete_classes.hotkeys import Action, ACTION_UP_DOWN, get_action
import pokete_data as p_data
import pokete_classes.movemap as mvp
from pokete_general_use_fns import liner
from .loops import std_loop, easy_exit_loop
from .language import lang
from .poke import Poke
from .color import Color
from .nature import PokeNature
from .ui_elements import ChooseBox, Box


class Dex:
    """The Pokete dex that shows stats about all Poketes ever caught
    ARGS:
        figure: Figure object"""

    def __init__(self, figure):
        self.box = ChooseBox(mvp.movemap.height - 3, 35, lang.str("ui.dex.title"),
                             info=f"{Action.CANCEL.mapping}:close")
        self.detail_box = Box(16, 35)
        self.figure = figure
        self.idx = 0
        self.obs = []
        self.detail_info = se.Text("", state="float")
        self.detail_desc = se.Text("", state="float")
        self.detail_box.add_ob(self.detail_info, 16, 1)
        self.detail_box.add_ob(self.detail_desc, 3, 8)

    def add_c_obs(self):
        """Adds c_obs to box"""
        self.box.add_c_obs(self.obs[self.idx * (self.box.height - 2):
                                    (self.idx + 1) * (self.box.height - 2)])

    def rem_c_obs(self):
        """Removes c_obs to box"""
        for c_ob in self.box.c_obs:
            c_ob.remove()
        self.box.remove_c_obs()

    def detail(self, poke):
        """Shows details about the Pokete
        ARGS:
            poke: Pokes identifier"""
        poke = Poke(poke, 0)
        poke.nature = PokeNature.dummy()
        poke.set_vars()
        active = {
            True: (lang.str("dialog.time.night"), Color.thicc + Color.blue),
            False: (lang.str("dialog.time.day"), Color.thicc + Color.yellow),
            None: (lang.str("dialog.time.always"), "")
        }[poke.night_active]
        desc_text = liner(poke.desc.text.replace("\n", " ") +
                          (f"""\n\n Evolves into {
                              p_data.pokes[poke.evolve_poke]['name'] if
                              poke.evolve_poke in
                              self.figure.caught_pokes else '???'
                                                }."""
                           if poke.evolve_lvl != 0 else ""), 29)
        self.detail_box.resize(10 + len(desc_text.split("\n")), 35)
        self.detail_box.name_label.rechar(poke.name)
        self.detail_box.add_ob(poke.ico, 3, 2)
        self.detail_desc.rechar(desc_text)
        self.detail_info.rechar(f"{lang.str('dialog.attack.type')}: ")
        self.detail_info += se.Text(poke.type.name.capitalize(),
                                    esccode=poke.type.color) + se.Text(f"""
{lang.str('dialog.attack.hp')}: {poke.hp}
{lang.str('ui.details.attack')}: {poke.atc}
{lang.str('ui.details.defense')}: {poke.defense}
{lang.str('ui.details.initiative')}: {poke.initiative}
{lang.str('ui.dialog.active')}: """) + se.Text(active[0], esccode=active[1])

        with self.detail_box.center_add(mvp.movemap):
            easy_exit_loop()
        self.detail_box.rem_ob(poke.ico)

    def __call__(self):
        """Opens the dex"""
        pokes = p_data.pokes
        self.idx = 0
        p_dict = {i[1]: i[-1] for i in
                  sorted([(pokes[j]["types"][0], j, pokes[j])
                          for j in list(pokes)[1:]])}
        self.obs = [se.Text(f"{i + 1} \
{lang.str(p_dict[poke]['name']) if poke in self.figure.caught_pokes else '???'}",
                    state="float")
                    for i, poke in enumerate(p_dict)]
        self.add_c_obs()
        with self.box.add(mvp.movemap, mvp.movemap.width - self.box.width, 0):
            while True:
                action = get_action()
                for event, idx, n_idx, add, idx_2 in zip(
                    [Action.DOWN, Action.UP],
                    [len(self.box.c_obs) - 1, 0],
                    [0, self.box.height - 3],
                    [1, -1],
                    [-1, 0],
                ):
                    if action.triggers(event) and self.box.index.index == idx:
                        if self.box.c_obs[self.box.index.index]\
                                    != self.obs[idx_2]:
                            self.rem_c_obs()
                            self.idx += add
                            self.add_c_obs()
                            self.box.set_index(n_idx)
                        action = get_action()
                if action.triggers(Action.ACCEPT):
                    if "???" not in self.box.c_obs[self.box.index.index].text:
                        self.detail(list(p_dict)[self.idx
                                                 * (self.box.height - 2)
                                                 + self.box.index.index])
                elif action.triggers(*ACTION_UP_DOWN):
                    self.box.input(action)
                elif action.triggers(Action.CANCEL, Action.POKEDEX):
                    break
                std_loop()
                mvp.movemap.show()
            self.rem_c_obs()
