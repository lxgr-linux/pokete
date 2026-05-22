import random

from pokete.classes.asset_service.service import asset_service


class LearnAttack:
    @staticmethod
    def get_attack(poke):
        """Gets a learnable attack for a given pokete
        ARGS:
            poke: The pokete
        RETURNS:
            The attacks name, None if none is found"""
        attacks = asset_service.get_base_assets().attacks
        pool = [
            i
            for i, atc in attacks.items()
            if all(j in [i.name for i in poke.types] for j in atc.types)
            and atc.is_generic
        ]
        full_pool = [
            i
            for i in poke.inf.attacks + poke.inf.pool + pool
            if i not in poke.attacks and attacks[i].min_lvl <= poke.lvl()
        ]
        if len(full_pool) == 0:
            return None
        return random.choice(full_pool)
