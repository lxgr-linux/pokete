"""Contains the NewDetail class - a Box-based detail view for Pokete"""

from typing import Optional, override

import scrap_engine as se

from pokete.base import loops
from pokete.base.change import change_ctx
from pokete.base.color import Color
from pokete.base.context import Context
from pokete.base.input import Action, get_action
from pokete.base.input.mouse import MouseEvent
from pokete.base.mouse import MouseInteractor
from pokete.base.single_event import SingleEvent, single_event_periodic_event
from pokete.base.tss import tss
from pokete.base.ui import Overview
from pokete.base.ui.elements import ChooseBox
from pokete.base.ui.elements.box import Box
from pokete.base.ui.elements.labels import CloseLabel, GenericActionLabel
from pokete.classes.poke import Poke
from pokete.classes.poke.nature import NatureInfo
from pokete.classes.single_events import TeleportationSingleEvent
from pokete.util import liner

from .poke.stats import StatsInfoBox


class NewDetail(Box, MouseInteractor):
    """Shows details about a Pokete in a Box (no own map)
    ARGS:
        height: Height of the box
        width: Width of the box
        overview: Optional overview for the box"""

    def __init__(
        self,
        overview: Optional[Overview] = None,
    ):
        super().__init__(
            *self.new_size(),
            name="Details",
            overview=overview,
            info=[
                CloseLabel(),
                GenericActionLabel(Action.NATURE_INFO, "Nature"),
                GenericActionLabel(Action.STATS_INFO, "Statistics"),
                GenericActionLabel(Action.ABILITIES_INFO, "Use ability"),
            ],
        )
        self.name_attacks = se.Text("Attacks", esccode=Color.thicc, state="float")
        self.attack_defense = se.Text("Attack:   Defense:", state="float")
        self.world_actions_label = se.Text("Abilities:", state="float")
        self.type_label = se.Text("Type:", state="float")
        self.initiative_label = se.Text("Initiative:", state="float")
        self.desc_label = se.Text("", "float")
        self.line_sep1 = se.Square("-", self.width - 2, 1, state="float")
        self.line_sep2 = se.Square("-", self.width - 2, 1, state="float")
        self.line_middle = se.Square("|", 1, 9, state="float")
        # adding elements to box
        self.add_ob(self.name_attacks, 2, 6)
        self.add_ob(self.attack_defense, 14, 5)
        self.add_ob(self.world_actions_label, 24, 4)
        self.add_ob(self.type_label, 37, 5)
        self.add_ob(self.initiative_label, 49, 5)
        self.add_ob(self.line_sep1, 1, 6)
        self.add_ob(self.line_sep2, 1, 11)
        self.add_ob(self.line_middle, round(self.width / 2), 7)
        self.add_ob(self.desc_label, 34, 2)
        self.poke = None

    def new_size(self) -> tuple[int, int]:
        return 17, max(tss.width - 10, 40)

    @override
    def get_interaction_areas(self) -> list[se.Area]:
        return []

    @override
    def interact(self, ctx: Context, area_idx: int, event: MouseEvent): ...

    @override
    def get_partial_interactors(self) -> list["MouseInteractor"]:
        return [
            label for label in self.info_labels if isinstance(label, MouseInteractor)
        ]

    def __rechar_desc_label(self):
        self.desc_label.rechar(liner(self.poke.desc, self.width - 34))

    def resize_view(self):
        """Manages recursive view resizing"""
        if self.poke is None:
            return
        self.remove()
        self.resize(*self.new_size())
        self.overview.resize_view()
        self.__rechar_desc_label()
        self.line_sep1.resize(self.width - 2, 1)
        self.line_sep2.resize(self.width - 2, 1)
        self.add_attack_labels()
        self.add_ob(self.line_middle, round(self.width / 2), 7)
        self.center_add(self.map)

    def add_attack_labels(self):
        """Adds the attack labels to map"""
        for atc, _x, _y in zip(
            self.poke.attack_obs,
            [
                1,
                round(self.width / 2) + 1,
                1,
                round(self.width / 2) + 1,
            ],
            [7, 7, 12, 12],
        ):
            atc.temp_i = 0
            atc.temp_j = -30
            atc.label_desc.rechar(atc.desc[: int(self.width / 2 - 1)])
            atc.label_ap.rechar(f"AP:{atc.ap}/{atc.max_ap}")
            for label, __x, __y in zip(
                [
                    atc.label_name,
                    atc.label_factor,
                    atc.label_type,
                    atc.label_ap,
                    atc.label_desc,
                ],
                [0, 0, 11, 0, 0],
                [0, 1, 1, 2, 3],
            ):
                self.add_ob(label, _x + __x, _y + __y)

    def enq_single_action(self, ret_action: str):
        """Enqueues a single event action"""
        event: Optional[SingleEvent] = None
        match ret_action:
            case "teleport":
                event = TeleportationSingleEvent(self.poke)
            case None, _:
                return
        if event is not None:
            single_event_periodic_event.add(event)

    def cleanup(self):
        """Cleans up Pokete info from the box"""
        for obj in [
            self.poke.text_name,
            self.poke.ico,
            self.poke.text_lvl,
            self.poke.text_hp,
            self.poke.tril,
            self.poke.trir,
            self.poke.hp_bar,
            self.poke.text_xp,
            self.poke.text_type,
        ]:
            self.rem_ob(obj)
            if obj.added:
                obj.remove()
        for eff in self.poke.effects:
            eff.cleanup()
        for atc in self.poke.attack_obs:
            for obj in [
                atc.label_name,
                atc.label_factor,
                atc.label_ap,
                atc.label_desc,
                atc.label_type,
            ]:
                self.rem_ob(obj)
                if obj.added:
                    obj.remove()
            if hasattr(atc, "temp_i"):  # TODO: Check this out
                del atc.temp_i
            if hasattr(atc, "temp_j"):
                del atc.temp_j

    def __call__(self, ctx: Context, poke: Poke, abb: bool = True) -> Optional[str]:
        """Shows details
        ARGS:
            ctx: Context object
            poke: Poke object whose details are given
            abb: Bool whether or not the ability option is shown
        RETURNS:
            None (used for interaction within the box)"""
        self.poke = poke
        self.set_ctx(ctx)
        ctx = change_ctx(ctx, self)

        with self.center_add(self.map):
            # Add poke info to box
            self.__rechar_desc_label()
            self.add_ob(self.poke.text_name, 14, 1)
            if self.poke.identifier != "__fallback__":
                for obj, __x, __y in zip(
                    [
                        self.poke.ico,
                        self.poke.text_lvl,
                        self.poke.text_hp,
                        self.poke.tril,
                        self.poke.trir,
                        self.poke.hp_bar,
                        self.poke.text_xp,
                    ],
                    [2, 14, 14, 20, 29, 21, 14],
                    [1, 2, 3, 3, 3, 3, 4],
                ):
                    self.add_ob(obj, __x, __y)
                for eff in self.poke.effects:
                    eff.add_label()

            do_exit = False
            abb_obs = [i for i in self.poke.attack_obs if i.world_action != ""]
            if abb_obs != [] and abb:
                self.world_actions_label.rechar(
                    "Abilities:" + " ".join([i.name for i in abb_obs])
                )
                # self.ability_label.add(self.map, self.x + 35, self.y + self.height - 2)
            else:
                self.world_actions_label.rechar("")
                # if self.ability_label.added:
                #    self.ability_label.remove()

            self.attack_defense.rechar(
                f"Attack:{self.poke.atc}\
{(4 - len(str(self.poke.atc))) * ' '}Defense:{self.poke.defense}"
            )
            self.initiative_label.rechar(f"Initiative:{self.poke.initiative}")
            self.add_ob(self.poke.text_type, 42, 5)
            self.add_attack_labels()
            self.map.show(init=True)

            while True:
                if do_exit:
                    self.cleanup()
                    return None
                action, _ = get_action()
                if action.triggers(Action.DECK, Action.CANCEL):
                    self.cleanup()
                    return None
                if action.triggers(Action.NATURE_INFO):
                    NatureInfo(poke.nature)(ctx)
                    ctx = change_ctx(ctx, self)
                elif action.triggers(Action.STATS_INFO):
                    StatsInfoBox(poke.poke_stats)(ctx)
                    ctx = change_ctx(ctx, self)
                elif action.triggers(Action.ABILITIES_INFO):
                    if abb_obs != [] and abb:
                        with ChooseBox(
                            len(abb_obs) + 2,
                            25,
                            name="Abilities",
                            c_obs=[se.Text(i.name) for i in abb_obs],
                            overview=self,
                        ).center_add(self.map) as box:
                            while True:
                                action, _ = get_action()
                                if action.triggers(Action.UP, Action.DOWN):
                                    box.input(action)
                                    self.map.show()
                                elif action.triggers(Action.ACCEPT):
                                    self.enq_single_action(
                                        abb_obs[box.index.index].world_action,
                                    )
                                    do_exit = True
                                    break
                                elif action.triggers(Action.CANCEL):
                                    break
                                loops.std(ctx.with_overview(box))
                # This section generates the Text effect for attack labels
                for atc in self.poke.attack_obs:
                    if len(atc.desc) > int((self.width - 3) / 2 - 1):
                        if atc.temp_j == 5:
                            atc.temp_i += 1
                            atc.temp_j = 0
                            if (
                                atc.temp_i
                                == len(atc.desc) - int(self.width / 2 - 1) + 10
                            ):
                                atc.temp_i = 0
                                atc.temp_j = -30
                            atc.label_desc.rechar(
                                atc.desc[
                                    atc.temp_i : int(self.width / 2 - 1) + atc.temp_i
                                ]
                            )
                        else:
                            atc.temp_j += 1
                loops.std(ctx)
