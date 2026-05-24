import scrap_engine as se

from pokete.base.color import Color
from pokete.classes.poke.poke import Poke
from pokete.classes.poke.ui.health_bar import HealthBarWrapper


class PokeLabels:
    def __init__(self, poke: Poke):
        # Labels
        self.hp_bar: HealthBarWrapper = HealthBarWrapper(poke)
        self.hp_bar.make(poke.hp)
        self.ico = se.Box(4, 11)
        for ico in poke.inf.ico:
            esccode = str.join("", [getattr(Color, i) for i in ico.esc])
            self.ico.add_ob(
                se.Text(
                    ico.txt,
                    state="float",
                    esccode=esccode,
                    ignore=f"{esccode} {Color.reset}",
                ),
                0,
                0,
            )
        self.text_lvl = se.Text(f"Lvl:{poke.lvl()}", state="float")
        self.text_name = se.Text(
            (poke.name.upper() if poke.shiny else poke.name),
            esccode=Color.underlined + poke.type.color,
            state="float",
        )
        self.text_xp = se.Text(
            f"XP:{poke.xp - (poke.lvl() ** 2 - 1)}/\
{((poke.lvl() + 1) ** 2 - 1) - (poke.lvl() ** 2 - 1)}",
            state="float",
        )
        self.text_type = se.Text(
            poke.type.name.capitalize(), state="float", esccode=poke.type.color
        )
