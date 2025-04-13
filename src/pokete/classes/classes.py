"""Contains just some small classes"""

from typing import Optional
import scrap_engine as se
import pokete.base.game_map as gm
from pokete.base.periodic_event_manager import PeriodicEvent
from pokete.classes.asset_service.resources import PokeArgs
from .weather import Weather


class PlayMap(gm.GameMap):
    """Map the actual player moves on and contains buildings etc
    ARGS:
        height: The maps height
        width: The maps width
        trainers: List of Trainers on the map
        name: Name of the map ("playmap1" etc)
        pretty_name: Pretty name of the map ("Route 1" etc)
        poke_args: Dict containing information for Poketes found in meadows
        w_poke_args: Same as above but with water
        extra_actions: Function executed every frame"""

    def __init__(self, height=se.screen_height - 1, width=se.screen_width,
                 trainers=None, name="", pretty_name="",
                 poke_args: Optional[PokeArgs] = None,
                 w_poke_args: Optional[PokeArgs] = None,
                 extra_actions: list[PeriodicEvent] | None = None, weather=None,
                 song="03 Chibi Ninja.mp3"):
        super().__init__(height, width, name=name)
        self.song = song
        self.trainers = trainers
        self.pretty_name = pretty_name
        self.poke_args = poke_args
        self.w_poke_args = w_poke_args
        self.registry = {}
        if self.trainers is None:
            self.trainers = []
        self.__extra_actions = extra_actions
        self.weather = None
        if weather is not None:
            self.weather = Weather(weather)

    def register_obj(self, name, obj):
        """Adds an object to the registry
        ARGS:
            name: Name in registry
            obj: Object"""
        self.registry[name] = obj

    def get_obj(self, name):
        """Gets and object from the registry
        ARGS:
            name: Name in registry"""
        return self.registry.get(name, None)

    def extra_actions(self) -> list[PeriodicEvent]:
        """Executes the extra action"""
        if self.__extra_actions is not None:
            return self.__extra_actions
        return []


class OutP(se.Text):
    """Output label to better organize output"""

    def outp(self, text):
        """Rechar and show wrapper
        ARGS:
            text: String that's printed out"""
        self.rechar(text)
        self.map.full_show()

    def append(self, *args):
        """Appends another se.Text to the outp
        ARGS:
            args: se.Texts that will be appended"""
        for i in args:
            self += i
        self.map.full_show()


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
