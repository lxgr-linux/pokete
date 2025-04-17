"""Contains stuff related to fight attack choosing"""

import scrap_engine as se

from pokete.util import liner
from pokete.base.context import Context
from pokete.base.input import ACTION_UP_DOWN, Action, get_action
from pokete.base.ui import Overview
from pokete.base.ui.elements import ChooseBox, LabelBox
from pokete.base import loops
from ... import effects
from ...attack import Attack


class AttackBox(se.Box, Overview):
    """Box containing attack choose and info box"""

    def __init__(self):
        super().__init__(0, 0)
        self.overview: Overview | None = None
        self.box = ChooseBox(
            6, 25, "Attacks",
            f"{Action.INFO.mapping}:Info", index_x=1
        )
        self.atk_box = LabelBox(se.Text(""), "Attack Info")
        self.add_ob(self.box, 0, 0)
        self.atk_box_added = False
        self.is_effect_info_box_active = False
        self.effects_dictionary = {e.c_name: e for e in effects.effect_list}
        self.effect_info_text = "Effect Info"
        self.attack_info_text = "Attack Info"

    def rechar_atk_box(self, attack_obs):
        """Rechars the attack info box
        ARGS:
            attack_obs: The current attack obs"""
        self.atk_box.name_label.rechar(self.attack_info_text)
        if attack_obs[self.box.index.index].effect is not None:
            self.atk_box.info_label.rechar(
                f"{Action.SCREEN_SWITCH.mapping}:{self.effect_info_text}")
        else:
            self.atk_box.info_label.rechar("")
        self.atk_box.label.rechar(
            liner(attack_obs[self.box.index.index].desc, 37)
        )
        self.atk_box.resize(
            self.atk_box.label.height + 2,
            self.atk_box.label.width + 4
        )

    def rechar_with_effect_info(self, attack_obs):
        """Rechars the attack info box with effect info
        ARGS:
            attack_obs: The current attack obs"""
        self.atk_box.name_label.rechar(self.effect_info_text)
        self.atk_box.info_label.rechar(
            f"{Action.SCREEN_SWITCH.mapping}:{self.attack_info_text}")
        current_attack = attack_obs[self.box.index.index]

        self.atk_box.label.rechar(
            liner(self.effects_dictionary[current_attack.effect].desc, 37),
            esccode=self.effects_dictionary[current_attack.effect].color
        )
        self.atk_box.resize(
            self.atk_box.label.height + 2,
            self.atk_box.label.width + 4
        )

    def toggle_atk_box(self):
        """Toggles the attack info box"""
        if not self.atk_box_added:
            self.add_ob(self.atk_box, 26, 0)
        else:
            self.rem_ob(self.atk_box)
            self.atk_box.remove()
        self.atk_box_added = not self.atk_box_added

    def resize_view(self):
        """Resizes the view"""
        self.remove()
        self.overview.resize_view()
        self.add(self.map, 1, self.map.height - 7)
        self.map.show()

    def add(self, _map, _x, _y):
        """Wrapper for add"""
        super().add(_map, _x, _y)
        return self

    def __enter__(self):
        """Enter dunder for context management"""
        self.map.show()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        """Exit dunder for context management"""
        self.remove()
        self.map.show()

    def __call__(self, ctx: Context, attack_obs: list[Attack]) -> Attack:
        """Inputloop for attack options
        ARGS:
            attack_obs: A list of Attack objects that belong to a Poke"""
        self.overview = ctx.overview
        with self.add(ctx.map, 1, ctx.map.height - 7):
            self.rechar_atk_box(attack_obs)
            self.map.show()
            while True:
                action = get_action()
                if action.triggers(*ACTION_UP_DOWN):
                    self.box.input(action)
                    self.is_effect_info_box_active = False
                    self.rechar_atk_box(attack_obs)
                    self.map.show()
                elif action.triggers(Action.ACCEPT) or (0 <= action.get_number()
                                                        < len(attack_obs)):
                    attack = attack_obs[
                        self.box.index.index if action.triggers(Action.ACCEPT)
                        else action.get_number()
                    ]
                    if attack.ap == 0:
                        continue
                    break
                elif action.triggers(Action.INFO):
                    self.toggle_atk_box()
                    self.map.show()
                    continue
                elif action.triggers(Action.CANCEL):
                    attack = ""
                    break
                elif action.triggers(Action.SCREEN_SWITCH):
                    selected_attack = attack_obs[self.box.index.index]
                    if self.atk_box_added and selected_attack.effect is not None:
                        self.is_effect_info_box_active = \
                            not self.is_effect_info_box_active
                        if self.is_effect_info_box_active:
                            self.rechar_with_effect_info(attack_obs)
                        else:
                            self.rechar_atk_box(attack_obs)
                    self.map.show()
                    continue
                loops.std(ctx.with_overview(self))
        return attack
