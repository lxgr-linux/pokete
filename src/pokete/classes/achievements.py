"""Classes related to achievements"""

import datetime
import logging
from typing import Never, Optional

import scrap_engine as se

from pokete.base import loops
from pokete.base.color import Color
from pokete.base.context import Context
from pokete.base.input import Action
from pokete.base.ui.elements import LabelBox
from pokete.base.ui.notify import notifier
from pokete.base.ui.views.better_choose_box import BetterChooseBoxView
from pokete.util import liner


class Achievement:
    """The Achievement class that groups identifier, title and description
    of a possible Achievement
    ARGS:
        identifier: Identifier ("first_poke")
        title: Title ("First Pokete")
        desc: Description ("Catch your first Pokete")"""

    def __init__(self, identifier, title, desc):
        self.identifier = identifier
        self.title = title
        self.desc = desc


class Achievements:
    """Manages Achievements"""

    def __init__(self):
        self.achievements = []
        self.achieved = []

    def set_achieved(self, achieved):
        """Sets the achieved Achievements
        ARGS:
            achieved: List of identifiers of the achieved Achievements"""
        self.achieved = achieved

    def add(self, identifier, title, desc):
        """Generates an Achievement

        See ``Achievement`` for argument info"""
        self.achievements.append(Achievement(identifier, title, desc))

    def achieve(self, identifier):
        """Checks and achieves an Achievement
        ARGS:
            identifier: The Achievements identifier"""
        if not self.is_achieved(identifier):
            ach = [i for i in self.achievements if i.identifier == identifier][
                0
            ]
            notifier.notify(ach.title, "Achievement unlocked!", ach.desc)
            self.achieved.append((identifier, str(datetime.date.today())))
            logging.info("[Achievements] Unlocked %s", identifier)

    def is_achieved(self, identifier):
        """Whether or not an identifier is achieved
        ARGS:
            identifier: The Achievements identifier
        RETURNS:
            bool"""
        return identifier in [i[0] for i in self.achieved]


class AchBox(LabelBox):
    """Box with info about an Achievement
    ARGS:
        ach: The Achievement
        achievements: Achievement's object"""

    def __init__(self, ctx: Context, ach, ach_ob):
        is_ach = ach_ob.is_achieved(ach.identifier)
        date = (
            [i[-1] for i in ach_ob.achieved if i[0] == ach.identifier][0]
            if is_ach
            else ""
        )
        label = (
            se.Text("Achieved: ", state="float")
            + se.Text(
                "Yes" if is_ach else "No",
                esccode=Color.thicc + (Color.green if is_ach else Color.grey),
                state="float",
            )
            + (
                se.Text("\nAt: " + date, state="float")
                if is_ach
                else se.Text("")
            )
            + se.Text("\n" + liner(ach.desc, 30), state="float")
        )
        super().__init__(
            label,
            name=ach.title,
            info=f"{Action.CANCEL.mapping}:close",
            ctx=ctx,
        )


class AchievementOverview(BetterChooseBoxView):
    """Overview for Achievements"""

    def __init__(self):
        super().__init__(
            3,
            [se.Text(" ")],
            name="Achievements",
        )

    def __call__(self, ctx: Context) -> Optional[Never]:
        self.set_items(
            3,
            [
                se.Text(
                    i.title,
                    esccode=Color.thicc + Color.green
                    if achievements.is_achieved(i.identifier)
                    else "",
                    state="float",
                )
                for i in achievements.achievements
            ],
        )
        return super().__call__(ctx)

    def choose(self, ctx: Context, idx: int) -> Optional[Never]:
        ach = achievements.achievements[idx]
        with AchBox(
            ctx.with_overview(self),
            ach,
            achievements,
        ).center_add(ctx.map) as achbox:
            loops.easy_exit(ctx.with_overview(achbox))


achievements = Achievements()
