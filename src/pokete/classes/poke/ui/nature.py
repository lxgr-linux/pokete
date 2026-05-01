import scrap_engine as se

from pokete.base import loops
from pokete.base.change import change_ctx
from pokete.base.color import Color
from pokete.base.context import Context
from pokete.base.ui.elements.labels import CloseLabel
from pokete.base.ui.views.boxes import LabelBoxView
from pokete.util import liner


class NatureInfo(LabelBoxView):
    """Box to show information in Detail
    ARGS:
        p_n: PoketeNature object"""

    def __init__(self, p_n):
        atc = self.get_amount(p_n.nature.atc)
        defense = self.get_amount(p_n.nature.defense)
        init = self.get_amount(p_n.nature.initiative)
        text = (
            se.Text(f"Nature: {'very ' if p_n.grade == 2 else ''}")
            + se.Text(p_n.nature.name, esccode=Color.thicc + p_n.nature.esccode)
            + se.Text(
                liner(
                    f"\n\n That means it has {atc} attack, \
{defense} defense and {init} initiative points compared to normal Poketes \
of its kind.",
                    40,
                    pre="",
                )
            )
        )
        super().__init__(text, name="Nature", info=[CloseLabel()])

    @staticmethod
    def get_amount(val):
        """Gets the amount denominator for a value"""
        if val == 1:
            return "the same"
        if val < 1:
            return "less"
        return "more"

    def __call__(self, ctx: Context):
        """Shows the box"""
        self.set_ctx(ctx)
        ctx = change_ctx(ctx, self)
        with self.center_add(self.map):
            loops.easy_exit(ctx)
