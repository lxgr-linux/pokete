"""Contains the Pokete dex that gives information about all Poketes"""

from typing import Never, Optional

import scrap_engine as se

from pokete.base import loops
from pokete.base.color import Color
from pokete.base.context import Context
from pokete.base.input import Action
from pokete.base.ui.elements import Box
from pokete.base.ui.views.choose_box import ChooseBoxView
from pokete.util import liner

from .asset_service.service import asset_service
from .poke import Poke, PokeNature


class DetailBox(Box):
    def __init__(self):
        super().__init__(16, 35)
        self.detail_info = se.Text("", state="float")
        self.detail_desc = se.Text("", state="float")
        self.add_ob(self.detail_info, 16, 1)
        self.add_ob(self.detail_desc, 3, 8)

    def __call__(self, ctx: Context, poke_name: str):
        poke = Poke(poke_name, 0)
        poke.nature = PokeNature.dummy()
        poke.set_vars()
        active = {
            True: ("Night", Color.thicc + Color.blue),
            False: ("Day", Color.thicc + Color.yellow),
            None: ("Always", ""),
        }[poke.night_active]
        desc_text = liner(
            poke.desc.text.replace("\n", " ")
            + (
                f"""\n\n Evolves into {
                    asset_service.get_base_assets().pokes[poke.evolve_poke].name
                    if poke.evolve_poke in ctx.figure.caught_pokes
                    else "???"
                }."""
                if poke.evolve_lvl != 0
                else ""
            ),
            29,
        )
        self.resize(10 + len(desc_text.split("\n")), 35)
        self.name_label.rechar(poke.name)
        self.add_ob(poke.ico, 3, 2)
        self.detail_desc.rechar(desc_text)
        self.detail_info.rechar("Type: ")
        self.detail_info += (
            se.Text(poke.type.name.capitalize(), esccode=poke.type.color)
            + se.Text(f"""
HP: {poke.hp}
Attack: {poke.atc}
Defense: {poke.defense}
Initiative: {poke.initiative}
Active: """)
            + se.Text(active[0], esccode=active[1])
        )

        self.set_ctx(ctx)
        with self.center_add(self.map):
            loops.easy_exit(ctx.with_overview(self))
        self.rem_ob(poke.ico)


class PokeDex(ChooseBoxView):
    def __init__(self):
        super().__init__(
            50, 35, "Poketedex", info=f"{Action.CANCEL.mapping}:close"
        )
        self.detail_box = DetailBox()
        pokes = asset_service.get_base_assets().pokes
        self.p_dict = {
            i[1]: i[-1]
            for i in sorted(
                [(pokes[j].types[0], j, pokes[j]) for j in list(pokes)[1:]]
            )
        }

    def choose(self, ctx: Context, idx: int) -> Optional[Never]:
        if "???" not in self.c_obs[self.index.index].text:
            self.detail_box(
                ctx.with_overview(self),
                list(self.p_dict)[idx],
            )

    def __call__(self, ctx: Context):
        """Opens the dex"""
        self.resize(ctx.map.height - 3, 35)
        self.elems = [
            se.Text(
                f"{i + 1} \
{self.p_dict[poke].name if poke in ctx.figure.caught_pokes else '???'}",
                state="float",
            )
            for i, poke in enumerate(self.p_dict)
        ]
        self.add_elems()
        with self.add(ctx.map, ctx.map.width - self.width, 0):
            return super().__call__(ctx)
