"""Contains the LearnAttack class"""

import random
import scrap_engine as se

from pokete.util import liner
from pokete.base.context import Context
from pokete.base.input import Action, get_action
from pokete.base.input_loops import ask_bool, ask_ok
from pokete.base.ui.elements import ChooseBox, Box
from pokete.base import loops
from .asset_service.service import asset_service
from .attack import Attack
from . import detail


class AttackInfo(Box):
    """Gives information about a certain attack
    ARGS:
        attack: The attack's name"""

    def __init__(self, attack):
        atc = Attack(attack)
        desc_label = se.Text(liner(atc.desc, 40))
        super().__init__(
            5 + len(desc_label.text.split("\n")),
            sorted(
                len(i) for i in
                desc_label.text.split("\n")
                + [
                    atc.label_type.text,
                    atc.label_factor.text
                ]
            )[-1] + 4, atc.name, f"{Action.CANCEL.mapping}:close")
        self.add_ob(atc.label_type, 2, 1)
        self.add_ob(atc.label_factor, 2, 2)
        self.add_ob(se.Text(f"AP:{atc.max_ap}"), 2, 3)
        self.add_ob(desc_label, 2, 4)

    def __enter__(self):
        """Enter dunder for context management"""
        self.center_add(self.map)
        self.map.show()
        return self


class LearnAttack:
    """Lets a Pokete learn a new attack
    ARGS:
        poke: The Poke that should learn an attack"""

    def __init__(self, poke):
        self.poke = poke
        self.box = ChooseBox(
            6, 25, name="Attacks",
            info=f"{Action.DECK.mapping}:Details, {Action.INFO.mapping}:Info",
        )

    @staticmethod
    def get_attack(poke):
        """Gets a learnable attack for a given pokete
        ARGS:
            poke: The pokete
        RETURNS:
            The attacks name, None if none is found"""
        attacks = asset_service.get_base_assets().attacks
        pool = [i for i, atc in attacks.items()
                if all(j in [i.name for i in poke.types]
                       for j in atc.types)
                and atc.is_generic]
        full_pool = [i for i in poke.inf.attacks +
                     poke.inf.pool + pool
                     if i not in poke.attacks
                     and attacks[i].min_lvl <= poke.lvl()]
        if len(full_pool) == 0:
            return None
        return random.choice(full_pool)

    def __call__(self, ctx: Context, attack=None):
        """Starts the learning process
        ARGS:
            attack: The attack's name that should be learned, if None a fitting
                    attack will be chosen randomly
        RETURNS:
            bool: Whether or not the attack was learned"""
        attacks = asset_service.get_base_assets().attacks
        self.box.set_ctx(ctx)
        if attack is None:
            if (new_attack := self.get_attack(self.poke)) is None:
                return False
        else:
            new_attack = attack
        if ask_bool(
            ctx,
            f"{self.poke.name} wants to learn "
            f"{attacks[new_attack].name}!",
        ):
            if len(self.poke.attacks) < 4:
                self.poke.attacks.append(new_attack)
                self.poke.attack_obs.append(
                    Attack(
                        new_attack,
                        len(self.poke.attacks)
                    )
                )
            else:
                self.box.add_c_obs(
                    [se.Text(f"{i + 1}: {j.name}", state="float")
                     for i, j in enumerate(self.poke.attack_obs)]
                )
                with self.box.center_add(ctx.map):
                    while True:
                        action = get_action()
                        if action.triggers(Action.UP, Action.DOWN):
                            self.box.input(action)
                            ctx.map.show()
                        elif action.triggers(Action.ACCEPT):
                            i = self.box.index.index
                            self.poke.attacks[i] = new_attack
                            self.poke.attack_obs[i] = Attack(new_attack, i + 1)
                            ask_ok(
                                ctx.with_overview(self.box),
                                f"{self.poke.name} learned "
                                f"{attacks[new_attack].name}!",
                            )
                            break
                        elif action.triggers(Action.DECK):
                            detail.detail(ctx.with_overview(self.box),
                                          self.poke, False)
                            ctx.map.show(init=True)
                        elif action.triggers(Action.INFO):
                            with AttackInfo(
                                new_attack
                            ).set_ctx(ctx.with_overview(self.box)) as box:
                                loops.easy_exit(ctx.with_overview(box))
                        elif action.triggers(Action.CANCEL):
                            return False
                        loops.std(ctx.with_overview(self.box))
                self.box.remove_c_obs()
            return True
        return False
