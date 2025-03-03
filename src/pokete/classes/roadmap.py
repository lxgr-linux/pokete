"""Contains all classes relevant to show the roadmap"""

import scrap_engine as se

from pokete.base.input import ACTION_DIRECTIONS, Action, ActionList, get_action
from pokete.base.color import Color
from pokete.base.ui.elements import Box, InfoBox
from pokete.base.context import Context
from pokete.base.periodic_event_manager import PeriodicEvent
from pokete.base import loops
import pokete.classes.ob_maps as obmp
from pokete.classes.asset_service.service import asset_service
from pokete.classes.classes import PlayMap
from pokete.util import liner


class RoadMapException(Exception):
    """Exception thrown when a PlayMap has no corresponding MapStation"""

    def __init__(self, _map):
        self.map = _map
        text = f"{_map} {_map.name} has no mapstation"
        super().__init__(text)


class StationObject(se.Text):

    def __init__(self, text, color):
        super().__init__(text, esccode=color, state="float")


class Decoration(StationObject):
    def __init__(self, text, color=""):
        super().__init__(text, getattr(Color, color, Color.lightgrey))


class Station(StationObject):
    """Selectable station for Roadmap
    ARGS:
        roadmap: RoadMap object
        associate: Main PlayMap name the station belongs to
        additionals: List of PlayMap names the station also belongs to
        desc: The associated description
        {w,a,s,d}_next: The next Station's name in a certain direction"""

    choosen = None
    obs = []

    def __init__(
        self,
        roadmap,
        associate,
        additionals,
        desc,
        text,
        color="",
        w_next="",
        a_next="",
        s_next="",
        d_next="",
    ):
        self.desc = desc
        self.roadmap = roadmap
        self.color = getattr(Color, color, "\033[1;37m")
        self.base_color = self.color
        self.base_text = text
        self.associates: list[PlayMap] = [associate] + [obmp.ob_maps[i] for i in
                                                        additionals]
        if self.associates[0]:
            self.name = self.associates[0].pretty_name
        super().__init__(text, self.color)
        self.w_next = w_next
        self.a_next = a_next
        self.s_next = s_next
        self.d_next = d_next
        Station.obs.append(self)

    def choose(self, figure):
        """Chooses and hightlights the station"""
        Station.choosen = self
        self.roadmap.rechar_info(
            self.name if self.has_been_visited(figure) else "???")

    def unchoose(self):
        """Unchooses the station"""
        self.un_blink()

    def blink(self):
        self.rechar(self.text, Color.red + Color.thicc)

    def un_blink(self):
        self.rechar(self.text, self.color)

    def next(self, inp: ActionList, figure):
        """Chooses the next station in a certain direction
        ARGS:
            inp: Action Enum"""
        for action in inp:
            if action in ACTION_DIRECTIONS:
                inp = action
                break
        inp = {
            Action.UP: "w",
            Action.DOWN: "s",
            Action.LEFT: "a",
            Action.RIGHT: "d",
        }[inp]
        if (n_e := getattr(self, inp + "_next")) not in ["", None]:
            self.unchoose()
            getattr(self.roadmap, n_e).choose(figure)

    def has_been_visited(self, figure):
        """Returns if the stations map has been visited before"""
        return self.associates[0].name in figure.visited_maps

    def is_city(self):
        """Returns if the station is a city"""
        return "pokecenter" in \
            asset_service.get_assets().obmaps[self.associates[0].name].hard_obs

    def hide_if_visited(self, figure, choose=False):
        self.text = self.base_text
        if not self.has_been_visited(figure):
            self.color = Color.white
            for ch in ["A", "P", "$", "C", "#"]:
                self.text = self.text.replace(ch, " ")
        elif choose:
            if self.is_city():
                self.color = self.base_color
            else:
                self.color = Color.white
        else:
            self.color = self.base_color
        self.rechar(self.text, self.color)


class RoadMap:
    """Map you can see and navigate maps on"""

    def __init__(self):
        stations = asset_service.get_assets().stations
        decorations = asset_service.get_assets().decorations
        self.box = Box(
            17, 61, "Roadmap", f"{Action.CANCEL.mapping}:close",
        )
        self.rose = se.Text("""   N
   ▲
W ◀ ▶ E
   ▼
   S""", state="float")
        self.legend = se.Text("""│ Legend:
│ P-Pokecenter
│ $-Shop
│ C-PoketeCare
│ A-Arena
└──────────────""", state="float")
        self.info_label = se.Text("", state="float")
        self.box.add_ob(self.info_label, self.box.width - 2, 0)
        self.box.add_ob(self.rose, 53, 11)
        self.box.add_ob(self.legend, 45, 1)
        for sta, d in decorations.items():
            obj = Decoration(d.gen.text, d.gen.color)
            self.box.add_ob(obj, d.add.x, d.add.y)
            setattr(self, sta, obj)

        for sta, d in stations.items():
            obj = Station(self, obmp.ob_maps[sta], **d.gen.to_dict())
            self.box.add_ob(obj, d.add.x, d.add.y)
            setattr(self, sta, obj)

    @property
    def sta(self) -> Station:
        """Gives choosen station"""
        return Station.choosen

    def rechar_info(self, name):
        """Changes info label
        ARGS:
            name: String displayed"""
        self.info_label.remove()
        self.box.rem_ob(self.info_label)
        self.info_label.rechar(name)
        self.box.add_ob(self.info_label, self.box.width - 2 - len(name), 0)

    def __call__(self, ctx: Context, choose=False):
        """Shows the roadmap
        ARGS:
            choose: Bool whether or not this is done to choose a city"""
        for i in Station.obs:
            i.hide_if_visited(ctx.figure, choose)
        [
            i
            for i in Station.obs
            if (
                   ctx.figure.map
                   if ctx.figure.map
                      not in [obmp.ob_maps[i] for i in ("shopmap", "centermap")]
                   else ctx.figure.oldmap
               )
               in i.associates
        ][0].choose(ctx.figure)
        self.box.overview = ctx.overview
        blinker = BlinkerEvent(self.sta)
        ctx = ctx.with_pevm(ctx.pevm.with_events([blinker])).with_overview(
            self.box)
        with self.box.center_add(ctx.map):
            while True:
                action = get_action()
                if action.triggers(*ACTION_DIRECTIONS):
                    self.sta.next(action, ctx.figure)
                elif action.triggers(Action.MAP, Action.CANCEL):
                    break
                elif (
                    action.triggers(Action.ACCEPT)
                    and choose
                    and self.sta.has_been_visited(ctx.figure)
                    and self.sta.is_city()
                ):
                    return self.sta.associates[0]
                elif (
                    action.triggers(Action.ACCEPT)
                    and not choose
                    and self.sta.has_been_visited(ctx.figure)
                ):
                    p_list = ", ".join(
                        set(
                            asset_service.get_base_assets().pokes[j].name
                            for i in self.sta.associates
                            for j in [
                                *(
                                    [] if i.poke_args is None else i.poke_args.pokes),
                                *(
                                    [] if i.w_poke_args is None else i.w_poke_args.pokes)
                            ]
                        )
                    )
                    with InfoBox(
                        liner(
                            self.sta.desc
                            + "\n\n Here you can find: "
                            + (p_list if p_list != "" else "Nothing"),
                            30,
                        ),
                        self.sta.name,
                        ctx=ctx,
                    ) as box:
                        blinker.box = box
                        loops.easy_exit(ctx=ctx.with_overview(box))
                        blinker.box = None
                blinker.station = self.sta
                loops.std(ctx=ctx.with_overview(self.box))
                ctx.map.full_show()
        self.sta.unchoose()

    # @staticmethod
    # TODO: Add to assetloading validation
    # def check_maps():
    #    """Checks for PlayMaps not having a corresponding MapStation"""
    #    all_road_maps = ["centermap", "shopmap"]
    #    for i, _dict in p_data.stations.items():
    #        all_road_maps.append(i)
    #        all_road_maps += _dict["gen"]["additionals"]
    #
    #   for _, _map in obmp.ob_maps.items():
    #        if _map.name not in all_road_maps:
    #            raise RoadMapException(_map)


roadmap: RoadMap | None = None


class BlinkerEvent(PeriodicEvent):
    def __init__(self, station: Station):
        self.station = station
        self.blink = False
        self.box: Box | None = None

    def tick(self, tick: int):
        if tick % 10 == 0:
            if self.blink:
                self.station.blink()
            else:
                self.station.un_blink()
            self.blink = not self.blink
            if self.box:
                self.box.set(self.box.x, self.box.y)


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
