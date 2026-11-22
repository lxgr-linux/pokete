from abc import ABC

from pokete.base.context import Context
from pokete.base.input import ActionList


class HasExtraActions(ABC):
    def handle_extra_actions(self, ctx: Context, action: ActionList) -> bool: ...
