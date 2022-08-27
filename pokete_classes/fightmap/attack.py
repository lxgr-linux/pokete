"""Contains stuff related to fight attack choosing"""

import scrap_engine as se
from pokete_general_use_fns import liner
from ..hotkeys import ACTION_UP_DOWN, Action, get_action
from ..ui_elements import ChooseBox, LabelBox
from ..loops import std_loop


class AttackBox(se.Box):
    """Box containing attack choose and info box
    ARGS:
        overview: Overview"""

    def __init__(self, overview):
        super().__init__(0, 0)
        self.overview = overview
        self.box = ChooseBox(
            6, 25, "Attacks",
            f"{Action.INFO.mapping}:Info", index_x=1
        )
        self.atk_box = LabelBox(se.Text(""), "Attack Info")
        self.add_ob(self.box, 0, 0)
        self.atk_box_added = False

    def rechar_atk_box(self, attack_obs):
        """Rechars the attack info box
        ARGS:
            attack_obs: The current attack obs"""
        self.atk_box.label.rechar(
            liner(attack_obs[self.box.index.index].desc, 37)
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

    def __call__(self, _map, attack_obs):
        """Inputloop for attack options
        ARGS:
            _map: Map to add to
            attack_obs: A list of Attack objects that belong to a Poke"""
        with self.add(_map, 1, _map.height - 7):
            self.rechar_atk_box(attack_obs)
            self.map.show()
            while True:#158
                action = get_action()
                if action.triggers(*ACTION_UP_DOWN):
                    self.box.input(action)
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
                std_loop(False, box=self)
        return attack
