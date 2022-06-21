"""Contains all classes relevant to show the roadmap"""

import scrap_engine as se
from pokete_classes.hotkeys import ACTION_DIRECTIONS, Action, ActionList, get_action
import pokete_data as p_data
import pokete_classes.ob_maps as obmp
from pokete_general_use_fns import liner
from .loops import std_loop, easy_exit_loop
from .color import Color
from .ui_elements import Box, InfoBox


class RoadMapException(Exception):
    """Exception thrown when a PlayMap has no corresponding MapStation"""

    def __init__(self, _map):
        self.map = _map
        text = f"{_map} {_map.name} has no mapstation"
        super().__init__(text)


class Station(se.Square):
    """Selectable station for Roadmap
    ARGS:
        roadmap: RoadMap object
        associate: Main PlayMap name the station belongs to
        additionals: List of PlayMap names the station also belongs to
        width: The Station's width
        height: The Station's height
        desc: The associated description
        char: Displayed char
        {w,a,s,d}_next: The next Station's name in a certain direction"""
    choosen = None
    obs = []

    def __init__(self, roadmap, associate, additionals, width, height, desc,
                 char="#", w_next="", a_next="", s_next="", d_next=""):
        self.desc = desc
        self.roadmap = roadmap
        self.org_char = char
        self.associates = [associate] + [obmp.ob_maps[i] for i in additionals]
        self.color = ""
        self.name = self.associates[0].pretty_name
        super().__init__(char, width, height, state="float")
        self.w_next = w_next
        self.a_next = a_next
        self.s_next = s_next
        self.d_next = d_next
        Station.obs.append(self)

    def choose(self):
        """Chooses and hightlights the station"""
        self.rechar(Color.red + Color.thicc + self.org_char + Color.reset)
        Station.choosen = self
        self.roadmap.rechar_info(self.name if self.has_been_visited() else "???")

    def unchoose(self):
        """Unchooses the station"""
        self.rechar(self.color + self.org_char + Color.reset)

    def next(self, inp: ActionList):
        """Chooses the next station in a certain direction
        ARGS:
            inp: Action Enum"""
        for action in inp:
            if action in (ACTION_DIRECTIONS):
                inp = action
                break
        inp = {
            Action.UP: 'w',
            Action.DOWN: 's',
            Action.LEFT: 'a',
            Action.RIGHT: 'd',
        }[inp]
        if (n_e := getattr(self, inp + "_next")) != "":
            self.unchoose()
            getattr(self.roadmap, n_e).choose()

    def has_been_visited(self):
        """Returns if the stations map has been visited before"""
        return self.associates[0].name in self.roadmap.fig.visited_maps

    def is_city(self):
        """Returns if the station is a city"""
        return "pokecenter"\
            in p_data.map_data[self.associates[0].name]["hard_obs"]

    def set_color(self, choose=False):
        """Marks a station as visited
        ARGS:
            choose: Bool whether or not this done when choosing a city"""
        if self.has_been_visited() and (self.is_city() if choose else True):
            self.color = Color.yellow
        else:
            self.color = ""
        self.unchoose()


class RoadMap:
    """Map you can see and navigate maps on
    ARGS:
        fig: Figure object"""

    def __init__(self, fig):
        self.fig = fig
        self.box = Box(11, 40, "Roadmap", "q:close")
        self.info_label = se.Text("", state="float")
        self.box.add_ob(self.info_label, self.box.width-2, 0)
        for sta, _dict in p_data.stations.items():
            obj = Station(self, obmp.ob_maps[sta], **_dict['gen'])
            self.box.add_ob(obj, **_dict['add'])
            setattr(self, sta, obj)

    @property
    def sta(self):
        """Gives choosen station"""
        return Station.choosen

    def rechar_info(self, name):
        """Changes info label
        ARGS:
            name: String displayed"""
        self.info_label.remove()
        self.box.rem_ob(self.info_label)
        self.info_label.rechar(name)
        self.box.add_ob(self.info_label, self.box.width-2-len(name), 0)

    def __call__(self, _map, choose=False):
        """Shows the roadmap
        ARGS:
            _map: se.Map this is shown on
            choose: Bool whether or not this is done to choose a city"""
        for i in Station.obs:
            i.set_color(choose)
        [i for i in Station.obs
         if (self.fig.map
             if self.fig.map not in [obmp.ob_maps[i] for i in
                                            ["shopmap", "centermap"]]
             else self.fig.oldmap)
         in i.associates][0].choose()
        with self.box.center_add(_map):
            while True:
                action = get_action()
                if action.triggers(*ACTION_DIRECTIONS):
                    self.sta.next(action)
                elif action.triggers(*[Action.ACT_3, Action.CANCEL]):
                    break
                elif (action == Action.ACCEPT and choose
                      and self.sta.has_been_visited()
                      and self.sta.is_city()):
                    return self.sta.associates[0]
                elif (action == Action.ACCEPT and not choose
                      and self.sta.has_been_visited()):
                    p_list = ", ".join(set(p_data.pokes[j]["name"]
                                       for i in self.sta.associates
                                           for j in
                                           i.poke_args.get("pokes", [])
                                           + i.w_poke_args.get("pokes", [])))
                    with InfoBox(liner(self.sta.desc
                                       + "\n\n Here you can find: " +
                                       (p_list if p_list != "" else "Nothing"),
                                       30), self.sta.name, _map=_map):
                        easy_exit_loop()
                std_loop()
                _map.show()
        self.sta.unchoose()

    @staticmethod
    def check_maps():
        """Checks for PlayMaps not having a corresponding MapStation"""
        all_road_maps = ["centermap", "shopmap"]
        for i, _dict in p_data.stations.items():
            all_road_maps.append(i)
            all_road_maps += _dict['gen']['additionals']

        for _, _map in obmp.ob_maps.items():
            if _map.name not in all_road_maps:
                raise RoadMapException(_map)


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
