"""Contains some stuff that's used in this module"""

import logging
from pokete.base.context import Context
from pokete.base.input_loops import ask_ok
from .doors import DoorToCenter


def check_walk_back(ctx: Context, self=None):
    """Check whether the figure has to be walked back to the last Poketecenter
       or not"""
    if all(i.hp <= 0 for i in ctx.figure.pokes[:6]):
        amount = round(ctx.figure.get_money() / 3)
        ctx.figure.add_money(-amount)
        ctx.figure.heal()
        ask_ok(ctx, f"""All your Poketes have died and you ran
back to the last Pokecenter you visited to heal them!
On the way there, ${amount} fell out of your pocket!""")
        ctx.figure.remove()
        ctx.figure.map = ctx.figure.last_center_map
        logging.info("[Figure] You lost all Poketes and ran away!")
        DoorToCenter().action(ctx.figure)
