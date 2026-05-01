import scrap_engine as se

from pokete.base import loops
from pokete.base.change import change_ctx
from pokete.base.context import Context
from pokete.base.ui.elements.labels import CloseLabel
from pokete.base.ui.views.boxes import LabelBoxView
from pokete.classes.poke.poke import Stats


class StatsInfoBox(LabelBoxView):
    """Box to show statistics about caught Poketes
    ARGS:
        poke_stats: PokeStats object"""

    def __init__(self, poke_stats: Stats):
        not_available = "N/A"
        if poke_stats.ownership_date is None:
            ownership_date = not_available
        else:
            ownership_date = poke_stats.ownership_date.strftime("%x %X")

        if poke_stats.evolved_date is None:
            evolve_date = not_available
        else:
            evolve_date = poke_stats.evolved_date.strftime("%x %X")

        if poke_stats.caught_with is None:
            caught_with = not_available
        else:
            caught_with = poke_stats.caught_with

        text = (
            se.Text(f"\nOwnership date: {ownership_date}", state="float")
            + se.Text(f"\nCaught with: {caught_with}", state="float")
            + se.Text(f"\nEvolved date: {evolve_date}", state="float")
            + se.Text(
                f"\nNumber of total battles: {poke_stats.total_battles}",
                state="float",
            )
            + se.Text(
                f"\nNumber of won battles: {poke_stats.win_battles}",
                state="float",
            )
            + se.Text(
                f"\nNumber of lost battles: {poke_stats.lost_battles}",
                state="float",
            )
            + se.Text(f"\nNumber of run away: {poke_stats.run_away}", state="float")
            + se.Text(f"\nTotal XP earned: {poke_stats.earned_xp}\n", state="float")
        )
        super().__init__(
            text,
            name=f"{poke_stats.poke_name} statistics",
            info=[CloseLabel()],
        )

    def __call__(self, ctx: Context):
        """Shows the box"""
        self.set_ctx(ctx)
        ctx = change_ctx(ctx, self)
        with self.center_add(self.map):
            loops.easy_exit(ctx)
