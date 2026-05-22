from pokete.base.context import Context
from pokete.classes.poke.poke import Poke

from .evomap import EvoMap
from .learnattack import learn_attack


def upgrade_by_one_lvl(ctx: Context, poke: Poke):
    """Upgrades a Pokete by exactly one level, this will only be used by treats
    ARGS:
        poke: The pokete, that will be upgraded"""
    poke.add_xp((poke.lvl() + 1) ** 2 - 1 - ((poke.lvl()) ** 2 - 1))
    poke.set_vars()
    learn_attack(poke, ctx)
    evomap = EvoMap(ctx.map.height, ctx.map.width)
    evomap(ctx, poke)
