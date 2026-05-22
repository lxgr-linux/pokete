"""Type and PokeType class"""

from typing import Optional

from pokete.base.color import Color
from pokete.classes.asset_service.service import asset_service


class Types:
    """Class to organize PokeTypese"""

    def __init__(self):
        for i, typ in asset_service.get_base_assets().types.items():
            setattr(self, i, PokeType(i, typ.effective, typ.ineffective, typ.color))
        for i in asset_service.get_base_assets().sub_types:
            setattr(self, i, PokeSubType(i))


class PokeType:
    """Type for Poketes and attacks
    ARGS:
        name: The types name
        effective: List of type names the type is effective against
        ineffective: List of type names the type is ineffectice against
        color: Color string"""

    def __init__(
        self,
        name: str,
        effective: list[str],
        ineffective: list[str],
        color: list[Optional[str]],
    ):
        self.name = name
        self.effective = effective
        self.ineffective = ineffective
        self.color = "" if color is None else "".join(getattr(Color, i) for i in color)


class PokeSubType(PokeType):
    """Subtype class to better organize generic attacks
    ARGS:
        name: The types name"""

    def __init__(self, name):
        super().__init__(name, [], [], None)


types = Types()

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
