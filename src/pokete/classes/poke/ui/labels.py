import scrap_engine as se

from pokete.base.color import Color
from pokete.classes.i import IPoke
from pokete.classes.poke.ui.health_bar import HealthBarWrapper


class PokeLabels:
    def __init__(self, poke: IPoke) -> None:
        # Labels
        self.hp_bar: HealthBarWrapper = HealthBarWrapper(poke)
        self.hp_bar.make(poke.hp)
        self.effects = EffectsLabel(poke)
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


class EffectsLabel(se.Text[se.Object]):
    def __init__(self, poke: IPoke) -> None:
        super().__init__("", state="float")
        self.poke = poke
        self.update()

    def update(self) -> None:
        was_added = self.added
        if self.added:
            self.remove()
        self.rechar("")
        for eff in self.poke.effects:
            self += se.Text(eff.text + " ", state="float", esccode=eff.str_esccode)
        if was_added:
            _ = self.add(self.map, self.x, self.y, failsafe=True)
