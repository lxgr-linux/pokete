"""Classes related to achievements"""

import datetime
import logging

import scrap_engine as se

from pokete.base import loops
from pokete.base.change import change_ctx
from pokete.base.color import Color
from pokete.base.context import Context
from pokete.base.ui.elements.labels import CloseLabel
from pokete.base.ui.notify import notifier
from pokete.base.ui.views.better_choose_box import BetterChooseBoxView
from pokete.base.ui.views.boxes import LabelBoxView
from pokete.util import liner


class Achievement:
    """The Achievement class that groups identifier, title and description
    of a possible Achievement
    ARGS:
        identifier: Identifier ("first_poke")
        title: Title ("First Pokete")
        desc: Description ("Catch your first Pokete")"""

    def __init__(self, identifier: str, title: str, desc: str) -> None:
        self.identifier = identifier
        self.title = title
        self.desc = desc


class Achievements:
    """Manages Achievements"""

    log = logging.getLogger("Achievements")

    def __init__(self) -> None:
        self.achievements: list[Achievement] = []
        self.achieved: list[tuple[str, str]] = []

    def set_achieved(self, achieved: list[tuple[str, str]]) -> None:
        """Sets the achieved Achievements
        ARGS:
            achieved: List of identifiers of the achieved Achievements"""
        self.achieved = achieved

    def add(self, identifier: str, title: str, desc: str) -> None:
        """Generates an Achievement

        See ``Achievement`` for argument info"""
        self.achievements.append(Achievement(identifier, title, desc))

    def achieve(self, identifier: str) -> None:
        """Checks and achieves an Achievement
        ARGS:
            identifier: The Achievements identifier"""
        if not self.is_achieved(identifier):
            ach = next(i for i in self.achievements if i.identifier == identifier)
            notifier.notify(ach.title, "Achievement unlocked!", ach.desc)
            self.achieved.append((identifier, str(datetime.date.today())))
            self.log.info("[Achievements] Unlocked %s", identifier)

    def is_achieved(self, identifier: str) -> bool:
        """Whether or not an identifier is achieved
        ARGS:
            identifier: The Achievements identifier
        RETURNS:
            bool"""
        return identifier in [i[0] for i in self.achieved]


class AchBox(LabelBoxView):
    """Box with info about an Achievement
    ARGS:
        ach: The Achievement
        achievements: Achievement's object"""

    def __init__(self, ach: Achievement, ach_ob: Achievements) -> None:
        is_ach = ach_ob.is_achieved(ach.identifier)
        date = (
            next(i[-1] for i in ach_ob.achieved if i[0] == ach.identifier)
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
            + (se.Text("\nAt: " + date, state="float") if is_ach else se.Text(""))
            + se.Text("\n" + liner(ach.desc, 30), state="float")
        )
        super().__init__(
            label,
            name=ach.title,
            info=[CloseLabel()],
        )


class AchievementOverview(BetterChooseBoxView):
    """Overview for Achievements"""

    def __init__(self) -> None:
        super().__init__(
            3,
            3,
            [se.Text(" ")],
            name="Achievements",
        )

    def __call__(self, ctx: Context) -> None:
        self.set_elems(
            3,
            3,
            [
                se.Text(
                    i.title,
                    esccode=(
                        Color.thicc + Color.green
                        if achievements.is_achieved(i.identifier)
                        else ""
                    ),
                    state="float",
                )
                for i in achievements.achievements
            ],
        )
        return super().__call__(ctx)

    def choose(self, ctx: Context, idx: int) -> None:
        ach = achievements.achievements[idx]
        with AchBox(
            ach,
            achievements,
        ).center_add(ctx.map) as achbox:
            achbox.set_ctx(ctx)
            ctx = change_ctx(ctx, achbox)
            loops.easy_exit(ctx)


achievements = Achievements()
