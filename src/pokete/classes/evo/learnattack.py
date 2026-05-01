"""Contains the LearnAttack class"""

from typing import Optional, override

import scrap_engine as se

from pokete.base import loops
from pokete.base.context import Context
from pokete.base.input import Action
from pokete.base.input.hotkeys import ActionList
from pokete.base.input_loops import ask_bool, ask_ok
from pokete.base.ui.elements import Box
from pokete.base.ui.elements.labels import CloseLabel
from pokete.base.ui.views.choose_box import ChooseBoxView
from pokete.classes.asset_service.service import asset_service
from pokete.classes.attack import Attack
from pokete.classes.detail import Detail
from pokete.classes.poke.poke import Poke
from pokete.classes.poke.poke.learnattack import LearnAttack
from pokete.util import liner


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
                len(i)
                for i in desc_label.text.split("\n")
                + [atc.label_type.text, atc.label_factor.text]
            )[-1]
            + 4,
            atc.name,
            [CloseLabel()],
        )
        self.add_ob(atc.label_type, 2, 1)
        self.add_ob(atc.label_factor, 2, 2)
        self.add_ob(se.Text(f"AP:{atc.max_ap}"), 2, 3)
        self.add_ob(desc_label, 2, 4)

    def __enter__(self):
        """Enter dunder for context management"""
        self.center_add(self.map)
        self.map.show()
        return self


class LearnAttackBox(ChooseBoxView[int]):
    """Lets a Pokete learn a new attack by choosing which attack to replace

    This is used when the Pokete already knows 4 attacks and needs to choose
    which one to replace with the new attack.
    """

    def __init__(self):
        super().__init__(6, 25, "Attacks")
        self.poke: Optional[Poke] = None
        self.new_attack: Optional[str] = None

    @override
    def new_size(self) -> tuple[int, int]:
        return 6, 25

    @override
    def choose(self, ctx: Context, idx: int) -> Optional[int]:
        """Return the index of the selected attack to replace"""
        return idx

    @override
    def handle_extra_actions(self, ctx: Context, action: ActionList) -> bool:
        """Handle extra actions like Details and Info"""
        if action.triggers(Action.DECK):
            Detail()(ctx.with_overview(self), self.poke, False)
            ctx.map.show(init=True)
            return False
        elif action.triggers(Action.INFO):
            if self.new_attack:
                with AttackInfo(self.new_attack).set_ctx(
                    ctx.with_overview(self)
                ) as box:
                    loops.easy_exit(ctx.with_overview(box))
            ctx.map.show(init=True)
            return False
        return False

    def show_attack_replacement(
        self, ctx: Context, poke: Poke, new_attack: str
    ) -> bool:
        """Show the attack replacement dialog

        ARGS:
            ctx: Context object
            poke: The Poke that will learn the attack
            new_attack: The attack name to learn

        RETURNS:
            bool: Whether an attack was replaced
        """
        self.poke = poke
        self.new_attack = new_attack
        attacks = asset_service.get_base_assets().attacks

        # Set up the list of current attacks
        self.elems = [
            se.Text(f"{i + 1}: {j.name}", state="float")
            for i, j in enumerate(poke.attack_obs)
        ]
        self.add_elems()

        with self.add(ctx.map, ctx.map.width - self.width, 0):
            idx = super().__call__(ctx)

        if idx is not None:
            # Replace the selected attack
            poke.attacks[idx] = new_attack
            poke.attack_obs[idx] = Attack(new_attack, idx + 1)
            ask_ok(
                ctx,
                f"{poke.name} learned {attacks[new_attack].name}!",
            )
            return True
        return False


class LearnAttackManager(LearnAttack):
    """Manages the attack learning process for a Pokete

    Handles automatic attack selection and uses LearnAttackBox when
    the Pokete needs to choose which attack to replace.
    """

    def __init__(self, poke: Poke):
        self.poke = poke
        self.learn_box = LearnAttackBox()

    def __call__(self, ctx: Context, attack: Optional[str] = None) -> bool:
        """Starts the learning process

        ARGS:
            ctx: Context object
            attack: The attack's name that should be learned, if None a fitting
                    attack will be chosen randomly

        RETURNS:
            bool: Whether or not the attack was learned
        """
        attacks = asset_service.get_base_assets().attacks

        # Get the attack to learn
        if attack is None:
            if (new_attack := self.get_attack(self.poke)) is None:
                return False
        else:
            new_attack = attack

        # Ask if the Pokete should learn the attack
        if ask_bool(
            ctx,
            f"{self.poke.name} wants to learn {attacks[new_attack].name}!",
        ):
            # If Pokete has less than 4 attacks, just add it
            if len(self.poke.attacks) < 4:
                self.poke.attacks.append(new_attack)
                self.poke.attack_obs.append(Attack(new_attack, len(self.poke.attacks)))
                return True
            else:
                # Otherwise, use the LearnAttackBox to choose which to replace
                return self.learn_box.show_attack_replacement(
                    ctx, self.poke, new_attack
                )
        return False


def learn_attack(poke: Poke, ctx: Context):
    """Checks if a new attack can be learned and then teaches it to the poke"""
    if poke.lvl() % 5 == 0:
        LearnAttackManager(poke)(ctx)
