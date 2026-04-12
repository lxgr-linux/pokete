"""Base class for objects that interact with the map"""

from pokete.base.context import Context


class MapInteract:
    """Base class for map-interactable objects"""

    ctx: Context

    @classmethod
    def set_ctx(cls, ctx: Context):
        """Set the context for all MapInteract instances"""
        cls.ctx = ctx


__all__ = ["MapInteract"]
