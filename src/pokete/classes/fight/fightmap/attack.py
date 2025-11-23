"""Contains stuff related to fight attack choosing"""

from typing import Optional, override

import scrap_engine as se

from pokete.base.context import Context
from pokete.base.input import Action
from pokete.base.input.hotkeys import ActionList
from pokete.base.mouse import MouseInteractor
from pokete.base.ui.elements import LabelBox
from pokete.base.ui.elements.labels import GenericActionLabel
from pokete.base.ui.views.choose_box import ChooseBoxView
from pokete.util import liner

from ... import effects
from ...attack import Attack


class AttackInfoBox(se.Box):
    def __init__(self):
        self.effects_dictionary = {e.c_name: e for e in effects.effect_list}
        self.effect_active = False
        self.effect_available = False
        self.attack_info = LabelBox(se.Text("", state="float"), "Attack Info")
        self.attack_info_label = GenericActionLabel(
            Action.SCREEN_SWITCH, "Attack Info"
        )
        self.effect_info_label = GenericActionLabel(
            Action.SCREEN_SWITCH, "Effect Info"
        )
        self.effect_info = LabelBox(
            se.Text("", state="float"),
            "Effect Info",
            info=[self.attack_info_label],
        )
        super().__init__(1, 1)

    def show_effect(self):
        if self.effect_available:
            self.effect_active = True
            self.rem_ob(self.attack_info)
            self.attack_info.remove()
            self.add_ob(self.effect_info, 0, 0)

    def unshow_effect(self):
        self.rem_ob(self.effect_info)
        self.effect_info.remove()
        self.add_ob(self.attack_info, 0, 0)
        self.effect_active = False

    def toggle(self):
        if self.effect_active:
            self.unshow_effect()
        else:
            self.show_effect()

    def set_attack(self, attack_ob: Attack):
        self.attack_info.label.rechar(liner(attack_ob.desc, 37))
        self.effect_available = attack_ob.effect is not None
        if self.effect_available:
            for label in self.attack_info.info_labels:
                self.attack_info.rem_ob(label)
                label.remove()
            self.attack_info.info_labels = [self.effect_info_label]
            self.attack_info.add_info_labels()
            self.effect_info.label.rechar(
                liner(self.effects_dictionary[attack_ob.effect].desc, 37),
                esccode=self.effects_dictionary[attack_ob.effect].color,
            )
            self.effect_info.resize(
                self.effect_info.label.height + 2,
                self.effect_info.label.width + 4,
            )
        else:
            for label in self.attack_info.info_labels:
                self.attack_info.rem_ob(label)
                label.remove()
            self.attack_info.info_labels = []
            self.unshow_effect()
        self.attack_info.resize(
            self.attack_info.label.height + 2, self.attack_info.label.width + 4
        )


class AttackBox(ChooseBoxView[Attack]):
    def __init__(self):
        self.attack_obs: list[Attack] = []
        self.attack_info_box = AttackInfoBox()
        super().__init__(
            6,
            25,
            "Attacks",
            [GenericActionLabel(Action.INFO, "Info")],
            index_x=1,
        )

    def toggle_atk_box(self):
        """Toggles the attack info box"""
        if not self.attack_info_box.added:
            self.add_ob(self.attack_info_box, 26, 0)
        else:
            self.rem_ob(self.attack_info_box)
            self.attack_info_box.remove()

    def get_partial_interactors(self) -> list[MouseInteractor]:
        return super().get_partial_interactors() + [
            label
            for label in (
                self.attack_info_box.attack_info.info_labels
                if not self.attack_info_box.effect_active
                else self.attack_info_box.effect_info.info_labels
            )
            if isinstance(label, MouseInteractor)
        ]

    @override
    def new_size(self) -> tuple[int, int]:
        return 6, 25

    @override
    def choose(self, ctx: Context, idx: int) -> Optional[Attack]:
        return self.attack_obs[idx]

    @override
    def resize_view(self):
        """Resizes the view"""
        self.remove()
        self.overview.resize_view()
        self.add(self.map, 1, self.map.height - 7)
        self.map.show()

    @override
    def on_index_change(self, area_idx: int):
        self.attack_info_box.set_attack(self.attack_obs[area_idx])

    def handle_extra_actions(self, ctx: Context, action: ActionList) -> bool:
        if action.triggers(Action.INFO):
            self.toggle_atk_box()
            self.map.show()
        elif action.triggers(Action.SCREEN_SWITCH):
            if self.attack_info_box.added:
                self.attack_info_box.toggle()
        return False

    def __call__(
        self, ctx: Context, attack_obs: list[Attack]
    ) -> Optional[Attack]:
        self.attack_obs = attack_obs
        self.elems = [atc.label for atc in attack_obs]
        self.add_elems()
        if self.index.index >= len(attack_obs):
            self.set_index(0)
        self.attack_info_box.set_attack(self.attack_obs[self.index.index])
        with self.add(ctx.map, 1, ctx.map.height - 7):
            return super().__call__(ctx)
