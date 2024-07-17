"""Contains stuff related to fight inventory"""

import scrap_engine as se

from ...inv import InvItem
from ...ui.elements import ChooseBox
from ...input import ACTION_UP_DOWN, Action, get_action
from ... import loops


class InvBox(ChooseBox):
    """Inventory box for fight"""

    def resize_view(self):
        """Resizes the view"""
        self.remove()
        self.overview.resize_view()
        self.resize(self.map.height - 3, 35)
        self.add(self.map, self.map.width - 35, 0)
        self.map.show()

    def __call__(self, _map, items: list[InvItem], inv) -> InvItem | None:
        """Inputloop for inv
        ARGS:
            _map: Map to add to
            items: List of InvItems that can be choosen from
            inv: The Figures inv"""
        self.add_c_obs([se.Text(f"{i.pretty_name}s : {inv[i.name]}")
                        for i in items])
        self.set_index(0)
        self.resize(_map.height - 3, 35)
        with self.add(_map, _map.width - 35, 0):
            while True:
                action = get_action()
                if action.triggers(*ACTION_UP_DOWN):
                    self.input(action)
                    _map.show()
                elif action.triggers(Action.CANCEL):
                    item = None
                    break
                elif action.triggers(Action.ACCEPT):
                    item = items[self.index.index]
                    break
                loops.std(False, box=self)
        self.remove_c_obs()
        return item
