"""Type and PokeType class"""


from pokete.base.color import Color
from pokete.classes.asset_service.service import asset_service


def _build_types() -> dict[str, "PokeType"]:
    """Build the types dictionary from base assets"""
    types_dict: dict[str, PokeType] = {}
    for i, typ in asset_service.get_base_assets().types.items():
        types_dict[i] = PokeType(i, typ.effective, typ.ineffective, typ.color)
    for i in asset_service.get_base_assets().sub_types:
        types_dict[i] = PokeSubType(i)
    return types_dict


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
        color: list[str | None] | None,
    ) -> None:
        self.name = name
        self.effective = effective
        self.ineffective = ineffective
        self.color = "" if color is None else "".join(getattr(Color, i) for i in color)


class PokeSubType(PokeType):
    """Subtype class to better organize generic attacks
    ARGS:
        name: The types name"""

    def __init__(self, name: str) -> None:
        super().__init__(name, [], [], None)


types: dict[str, PokeType] = _build_types()

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
