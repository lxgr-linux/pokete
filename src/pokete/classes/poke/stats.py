"""Contains classes nedded for pokete stats"""

from datetime import datetime
import scrap_engine as se

from pokete.base.context import Context
from pokete.base.input import Action
from pokete.base.ui.elements import LabelBox
from pokete.base import loops
from ..multiplayer.msg.poke import StatsDict


class Stats:
    """Holds a poketes statistics data
    ARGS:
        poke_name: The poketes name
        ownership_date: The date of ownership
        caught_with: The balls name the pokete got caught with
        evolved_date: The date the pokete evolved at
        total_battles: The number of battles played with a pokete
        lost_battles: The number of battles the pokete lost
        win_battles: The number of battles the pokete won
        earned_xp: The xp the pokete collected while in possession
        run_away: The number of battles the pokete ran away from"""

    def __init__(self, poke_name, ownership_date, caught_with=None,
                 evolved_date=None, total_battles=0, lost_battles=0,
                 win_battles=0, earned_xp=0, run_away=0):
        self.ownership_date = ownership_date
        self.evolved_date = evolved_date
        self.total_battles = total_battles
        self.lost_battles = lost_battles
        self.win_battles = win_battles
        self.earned_xp = earned_xp
        self.poke_name = poke_name
        self.caught_with = caught_with
        self.run_away = run_away

    def add_battle(self, win=False):
        """Adds a battle to the statistics
        ARGS:
            win: Whether or not the battle was won"""
        if win:
            self.win_battles += 1
        else:
            self.lost_battles += 1
        self.total_battles += 1

    def set_evolved_date(self, evolved_date):
        """Sets the date the pokete evolve at
        ARGS:
            evolved_date: The date"""
        self.evolved_date = evolved_date

    def add_xp(self, _xp):
        """Adds xp to the statistics
        ARGS:
            _xp: Number of xp"""
        self.earned_xp += _xp

    def set_run_away_battle(self):
        """Sets a battle that was aborted"""
        self.run_away += 1
        self.total_battles += 1

    def dict(self) -> StatsDict:
        """RETURNS:
            A dict containing information to reconstruct the object"""
        ownership_date = None if self.ownership_date is None else \
            self.ownership_date.isoformat()
        evolved_date = None if self.evolved_date is None else \
            self.evolved_date.isoformat()
        return {"ownership_date": ownership_date,
                "evolved_date": evolved_date,
                "total_battles": self.total_battles,
                "lost_battles": self.lost_battles,
                "win_battles": self.win_battles,
                "earned_xp": self.earned_xp,
                "caught_with": self.caught_with,
                "run_away": self.run_away}

    @classmethod
    def from_dict(cls, _dict: StatsDict, poke_name):
        """Assembles a PokeStats from _dict"""
        ownership_date = None if _dict.get("ownership_date", None) is None \
            else datetime.fromisoformat(_dict.get("ownership_date"))
        evolved_date = None if _dict.get("evolved_date", None) is None else \
            datetime.fromisoformat(_dict.get("evolved_date"))
        return cls(poke_name, ownership_date,
                   _dict.get("caught_with", None), evolved_date,
                   _dict.get("total_battles", 0),
                   _dict.get("lost_battles", 0), _dict.get("win_battles", 0),
                   _dict.get("earned_xp", 0), _dict.get("run_away", 0))


class StatsInfoBox(LabelBox):
    """Box to show statistics about caught Poketes
    ARGS:
        poke_stats: PokeStats object"""

    def __init__(self, poke_stats: Stats):
        not_available = "N/A"
        if poke_stats.ownership_date is None:
            ownership_date = not_available
        else:
            ownership_date = poke_stats.ownership_date.strftime('%x %X')

        if poke_stats.evolved_date is None:
            evolve_date = not_available
        else:
            evolve_date = poke_stats.evolved_date.strftime('%x %X')

        if poke_stats.caught_with is None:
            caught_with = not_available
        else:
            caught_with = poke_stats.caught_with

        text = (
            se.Text(f"\nOwnership date: {ownership_date}", state="float")
            + se.Text(f"\nCaught with: {caught_with}", state="float")
            + se.Text(f"\nEvolved date: {evolve_date}", state="float")
            + se.Text(f"\nNumber of total battles: {poke_stats.total_battles}",
                      state="float")
            + se.Text(f"\nNumber of won battles: {poke_stats.win_battles}",
                      state="float")
            + se.Text(f"\nNumber of lost battles: {poke_stats.lost_battles}",
                      state="float")
            + se.Text(f"\nNumber of run away: {poke_stats.run_away}",
                      state="float")
            + se.Text(f"\nTotal XP earned: {poke_stats.earned_xp}\n",
                      state="float")
        )
        super().__init__(
            text, name=f"{poke_stats.poke_name} statistics",
            info=f"{Action.CANCEL.mapping}:close"
        )

    def __call__(self, ctx: Context):
        """Shows the box"""
        self.set_ctx(ctx)
        with self.center_add(self.map):
            loops.easy_exit(ctx.with_overview(self))
