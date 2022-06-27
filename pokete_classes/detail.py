"""Contains classes needed for the detail-view of a Pokete"""

import logging
import scrap_engine as se
import pokete_classes.game_map as gm
from pokete_classes.hotkeys import Action, get_action
from .loops import std_loop
from .event import _ev
from .ui_elements import StdFrame2, ChooseBox
from .color import Color


class Informer:
    """Supplies methods for Deck and Detail"""

    @staticmethod
    def add(poke, figure, _map, _x, _y, in_deck=True):
        """Adds a Pokete's info to the deck
        ARGS:
            poke: Poke object
            figure: Figure object
            _map: se.Map object the information is added to
            _x: X-coordinate the info is added to
            _y: Y-coordinate
            in_deck: bool whether or not the info is added to the deck"""
        poke.text_name.add(_map, _x + 12, _y + 0)
        if poke.identifier != "__fallback__":
            for obj, __x, __y in zip([poke.ico, poke.text_lvl, poke.text_hp,
                                      poke.tril, poke.trir, poke.hp_bar,
                                      poke.text_xp],
                                     [0, 12, 12, 18, 27, 19, 12],
                                     [0, 1, 2, 2, 2, 2, 3]):
                obj.add(_map, _x + __x, _y + __y)
            if in_deck and figure.pokes.index(poke) < 6:
                poke.pball_small.add(_map, round(_map.width / 2) - 1
                                           if figure.pokes.index(poke) % 2 == 0
                                           else _map.width - 2, _y)
            for eff in poke.effects:
                eff.add_label()

    @staticmethod
    def remove(poke):
        """Removes a Pokete from the deck
        ARGS:
            poke: Poke object that should be removed"""
        for obj in [poke.ico, poke.text_name, poke.text_lvl, poke.text_hp,
                    poke.tril, poke.trir, poke.hp_bar, poke.text_xp,
                    poke.pball_small]:
            obj.remove()
        for eff in poke.effects:
            eff.cleanup()


class Detail(Informer):
    """Shows details about a Pokete
    ARGS:
        height: Height of the map
        width: Width of the map"""

    def __init__(self, height, width):
        self.map = gm.GameMap(height, width)
        self.name_label = se.Text("Details", esccode=Color.thicc)
        self.name_attacks = se.Text("Attacks", esccode=Color.thicc)
        self.frame = StdFrame2(17, self.map.width, state="float")
        self.attack_defense = se.Text("Attack:   Defense:")
        self.world_actions_label = se.Text("Abilities:")
        self.type_label = se.Text("Type:")
        self.initiative_label = se.Text("Initiative:")
        self.exit_label = se.Text(f"{Action.DECK.mapping}: Exit")
        self.nature_label = se.Text(f"{Action.NATURE_INFO.mapping}: Nature")
        self.ability_label = se.Text(f"{Action.ABILITIES}: Use ability")
        self.line_sep1 = se.Square("-", self.map.width - 2, 1, state="float")
        self.line_sep2 = se.Square("-", self.map.width - 2, 1, state="float")
        self.line_middle = se.Square("|", 1, 10, state="float")
        # adding
        self.name_label.add(self.map, 2, 0)
        self.name_attacks.add(self.map, 2, 6)
        self.attack_defense.add(self.map, 13, 5)
        self.world_actions_label.add(self.map, 24, 4)
        self.type_label.add(self.map, 36, 5)
        self.initiative_label.add(self.map, 49, 5)
        self.exit_label.add(self.map, 0, self.map.height - 1)
        self.nature_label.add(self.map, 9, self.map.height - 1)
        self.ability_label.add(self.map, 20, self.map.height - 1)
        self.line_sep1.add(self.map, 1, 6)
        self.line_sep2.add(self.map, 1, 11)
        self.frame.add(self.map, 0, 0)
        self.line_middle.add(self.map, round(self.map.width / 2), 7)

    def __call__(self, poke, abb=True):
        """Shows details
        ARGS:
            poke: Poke object whose details are given
            abb: Bool whether or not the ability option is shown"""
        ret_action = None
        self.add(poke, None, self.map, 1, 1, False)
        abb_obs = [i for i in poke.attack_obs
                   if i.world_action != ""]
        if abb_obs != [] and abb:
            self.world_actions_label.rechar("Abilities:"
                                            + " ".join([i.name
                                                        for i in abb_obs]))
            self.ability_label.rechar("3: Use ability")
        else:
            self.world_actions_label.rechar("")
            self.ability_label.rechar("")
        self.attack_defense.rechar(f"Attack:{poke.atc}\
{(4 - len(str(poke.atc))) * ' '}Defense:{poke.defense}")
        self.initiative_label.rechar(f"Initiative:{poke.initiative}")
        for obj, _x, _y in zip([poke.desc, poke.text_type], [34, 41], [2, 5]):
            obj.add(self.map, _x, _y)
        for atc, _x, _y in zip(poke.attack_obs, [1,
                                                round(self.map.width / 2) + 1,
                                                1,
                                                round(self.map.width / 2) + 1],
                               [7, 7, 12, 12]):
            atc.temp_i = 0
            atc.temp_j = -30
            atc.label_desc.rechar(atc.desc[:int(self.map.width / 2 - 1)])
            atc.label_ap.rechar(f"AP:{atc.ap}/{atc.max_ap}")
            for label, __x, __y in zip([atc.label_name, atc.label_factor,
                                        atc.label_type,
                                        atc.label_ap, atc.label_desc],
                                       [0, 0, 11, 0, 0],
                                       [0, 1, 1, 2, 3]):
                label.add(self.map, _x + __x, _y + __y)
        self.map.show(init=True)
        while True:
            action = get_action()
            if action.triggers(Action.DECK, Action.CANCEL):
                self.remove(poke)
                for obj in [poke.desc, poke.text_type]:
                    obj.remove()
                for atc in poke.attack_obs:
                    for obj in [atc.label_name, atc.label_factor, atc.label_ap,
                                atc.label_desc, atc.label_type]:
                        obj.remove()
                    del atc.temp_i, atc.temp_j
                logging.info("2"+repr(ret_action))
                return ret_action
            elif action.triggers(Action.NATURE_INFO):
                poke.nature.info(self.map)
            elif action.triggers(Action.ABILITIES):
                if abb_obs != [] and abb:
                    with ChooseBox(len(abb_obs) + 2, 25, name="Abilities",
                                   c_obs=[se.Text(i.name)
                                          for i in abb_obs]).center_add(self.map)\
                            as box:
                        while True:
                            action = get_action()
                            if action.triggers(Action.UP, Action.DOWN):
                                box.input(action)
                                self.map.show()
                            elif action.triggers(Action.ACCEPT):
                                ret_action = abb_obs[box.index.index].world_action
                                logging.info("1"+repr(ret_action))
                                _ev.set(Action.CANCEL.mapping)
                                break
                            elif action.triggers(Action.CANCEL):
                                break
                            std_loop(False)
            std_loop(False)
            # This section generates the Text effect for attack labels
            for atc in poke.attack_obs:
                if len(atc.desc) > int((self.map.width - 3) / 2 - 1):
                    if atc.temp_j == 5:
                        atc.temp_i += 1
                        atc.temp_j = 0
                        if atc.temp_i == len(atc.desc)\
                                          - int(self.map.width / 2 - 1)\
                                          + 10:
                            atc.temp_i = 0
                            atc.temp_j = -30
                        atc.label_desc.rechar(atc.desc[atc.temp_i:
                                                       int(self.map.width
                                                           / 2 - 1)
                                                       + atc.temp_i])
                    else:
                        atc.temp_j += 1
            self.map.show()


detail = None

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
