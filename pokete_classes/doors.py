"""Contains doors"""

import random
import scrap_engine as se
from pokete_classes import game, ob_maps as obmp


class CenterDoor(se.Object):
    """Door class for the map to enter centers and shops"""

    def action(self, ob):
        """Trigger
        ARGS:
            ob: The object triggering this action"""
        ob.remove()
        i = ob.map.name
        ob.add(ob.oldmap,
               ob.oldmap.dor.x
               if ob.map == obmp.ob_maps["centermap"]
               else ob.oldmap.shopdor.x,
               ob.oldmap.dor.y + 1
               if ob.map == obmp.ob_maps["centermap"]
               else ob.oldmap.shopdor.y + 1)
        ob.oldmap = obmp.ob_maps[i]
        game.game(ob.map)


class Door(se.Object):
    """Door class for the map to enter other maps"""

    def action(self, ob):
        """Trigger
        ARGS:
            ob: The object triggering this action"""
        ob.remove()
        i = ob.map.name
        ob.add(obmp.ob_maps[self.arg_proto["map"]], self.arg_proto["x"],
               self.arg_proto["y"])
        ob.oldmap = obmp.ob_maps[i]
        game.game(obmp.ob_maps[self.arg_proto["map"]])


class DoorToCenter(Door):
    """Door that leads to the Pokete center"""

    def __init__(self):
        super().__init__("#", state="float",
                         arg_proto={"map": "centermap",
                                    "x": int(
                                        obmp.ob_maps["centermap"].width / 2),
                                    "y": 7})

    def action(self, ob):
        """Triggers the door
        ARGS:
            ob: The object triggering this action"""
        ob.last_center_map = ob.map
        super().action(ob)


class DoorToShop(Door):
    """Door that leads to the shop"""

    def __init__(self):
        super().__init__("#", state="float",
                         arg_proto={"map": "shopmap",
                                    "x": int(obmp.ob_maps["shopmap"].width / 2),
                                    "y": 7})


class ChanceDoor(Door):
    """Same as door but with a chance"""

    def action(self, ob):
        """Trigger
        ARGS:
            ob: The object triggering this action"""
        if random.randint(0, self.arg_proto["chance"]) == 0:
            super().action(ob)


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
