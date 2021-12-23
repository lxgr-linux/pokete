"""Contains all classes relevant to show the roadmap"""
import time
import scrap_engine as se
from pokete_general_use_fns import std_loop, liner
from .color import Color
from .ui_elements import Box, InfoBox


class Station(se.Square):
    """Selectable station for Roadmap"""
    choosen = None
    obs = []

    def __init__(self, roadmap, associate, additionals, width, height, desc,
                 char="#", w_next="", a_next="", s_next="", d_next=""):
        self.desc = desc
        self.roadmap = roadmap
        self.org_char = char
        self.associates = [associate] + [roadmap.ob_maps[i] for i in additionals]
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

    def next(self, _ev):
        """Chooses the next station in a certain direction"""
        _ev = _ev.strip("'")
        if (n_e := getattr(self, _ev + "_next")) != "":
            self.unchoose()
            getattr(self.roadmap, n_e).choose()

    def has_been_visited(self):
        """Returns if the stations map has been visited before"""
        return self.associates[0].name in self.roadmap.fig.visited_maps

    def is_city(self):
        """Returns if the station is a city"""
        return "pokecenter"\
            in self.roadmap.p_d.map_data[self.associates[0].name]["hard_obs"]

    def set_color(self, choose=False):
        """Marks a station as visited"""
        if self.has_been_visited() and (self.is_city() if choose else True):
            self.color = Color.yellow
        else:
            self.color = ""
        self.unchoose()


class RoadMap:
    """Map you can see and navigate maps on"""

    def __init__(self, p_d, ob_maps, fig):
        self.ob_maps = ob_maps
        self.p_d = p_d
        self.fig = fig
        self.box = Box(11, 40, "Roadmap", "q:close")
        self.info_label = se.Text("", state="float")
        self.box.add_ob(self.info_label, self.box.width-2, 0)
        for sta in p_d.stations:
            obj = Station(self, ob_maps[sta], **p_d.stations[sta]['gen'])
            self.box.add_ob(obj, **p_d.stations[sta]['add'])
            setattr(self, sta, obj)

    @property
    def sta(self):
        """Gives choosen station"""
        return Station.choosen

    def rechar_info(self, name):
        """Changes info label"""
        self.box.set_ob(self.info_label, self.box.width-2-len(name), 0)
        self.info_label.rechar(name)

    def __call__(self, _ev, _map, choose=False):
        """Shows the roadmap"""
        _ev.clear()
        for i in Station.obs:
            i.set_color(choose)
        [i for i in Station.obs
         if (self.fig.map
             if self.fig.map not in [self.ob_maps[i] for i in
                                            ["shopmap", "centermap"]]
             else self.fig.oldmap)
         in i.associates][0].choose()
        with self.box.center_add(_map):
            while True:
                if _ev.get() in ["'w'", "'a'", "'s'", "'d'"]:
                    self.sta.next(_ev.get())
                    _ev.clear()
                elif _ev.get() in ["'3'", "Key.esc", "'q'"]:
                    _ev.clear()
                    break
                elif (_ev.get() == "Key.enter" and choose
                      and self.sta.has_been_visited()
                      and self.sta.is_city()):
                    return self.sta.associates[0]
                elif (_ev.get() == "Key.enter" and not choose
                      and self.sta.has_been_visited()):
                    _ev.clear()
                    p_list = ", ".join(set(self.p_d.pokes[j]["name"]
                                       for i in self.sta.associates
                                           for j in
                                           i.poke_args.get("pokes", [])
                                           + i.w_poke_args.get("pokes", [])))
                    with InfoBox(liner(self.sta.desc
                                       + "\n\n Here you can find: " +
                                       (p_list if p_list != "" else "Nothing"),
                                       30), self.sta.name, _map=_map):
                        while True:
                            if _ev.get() in ["Key.esc", "'q'"]:
                                _ev.clear()
                                break
                            std_loop(_ev)
                            time.sleep(0.05)
                std_loop(_ev)
                time.sleep(0.05)
                _map.show()
        self.sta.unchoose()

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")

