"""Contains the AbilitiesChooseBox - a ChooseBoxView for selecting Pokete abilities"""

from typing import Optional, override

import scrap_engine as se

from pokete.base.context import Context
from pokete.base.ui.elements.labels import CloseLabel
from pokete.base.ui.views.choose_box import ChooseBoxView


class AbilitiesChooseBox(ChooseBoxView[str]):
    """A ChooseBoxView for selecting and using Pokete abilities

    Displays a list of abilities that have world_action set and allows
    the user to select and use them.
    """

    def __init__(self):
        super().__init__(10, 25, "Abilities", info=[CloseLabel()])
        self.abilities = []

    @override
    def new_size(self) -> tuple[int, int]:
        return len(self.elems) + 2, max(i.width for i in self.elems) + 6

    @override
    def choose(self, ctx: Context, idx: int) -> Optional[str]:
        """Return the world_action of the selected ability"""
        if idx < len(self.abilities):
            return self.abilities[idx].world_action
        return None

    def __call__(self, ctx: Context, abilities) -> Optional[str]:
        """Show abilities and let user select one

        ARGS:
            ctx: Context object
            abilities: List of ability objects with world_action attribute

        RETURNS:
            The world_action string of the selected ability, or None
        """
        self.abilities = abilities
        self.elems = [se.Text(i.name) for i in abilities]
        self.resize(*self.new_size())
        self.add_elems()

        with self.center_add(ctx.map):
            return super().__call__(ctx)
