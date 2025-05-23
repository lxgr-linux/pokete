# DO NOT EDIT!
# This code was auto generated by the `protoc-gen-pokete-resources-python` plugin,
# part of the pokete project, by <lxgr@protonmail.com>
from typing import TypedDict


class PokeArgsDict(TypedDict):
    pokes: list[str]
    minlvl: int
    maxlvl: int


class PokeArgs:
    def __init__(
        self,
        pokes: list[str],
        minlvl: int,
        maxlvl: int
    ):
        self.pokes: list[str] = pokes
        self.minlvl: int = minlvl
        self.maxlvl: int = maxlvl

    @classmethod
    def from_dict(cls, _d: PokeArgsDict | None) -> "PokeArgs | None":
        if _d is None:
            return None
        return cls(
            pokes=_d["pokes"],
            minlvl=_d["minlvl"],
            maxlvl=_d["maxlvl"],
        )

    @staticmethod
    def validate(_d: PokeArgsDict) -> bool:
        return all([
            "pokes" in _d and all(type(i) is str for i in _d["pokes"]),
            "minlvl" in _d and type(_d["minlvl"]) is int,
            "maxlvl" in _d and type(_d["maxlvl"]) is int,
        ])

    def to_dict(self) -> PokeArgsDict:
        ret: PokeArgsDict = {}
        
        ret["pokes"] = self.pokes
        ret["minlvl"] = self.minlvl
        ret["maxlvl"] = self.maxlvl

        return ret


class MapDict(TypedDict):
    height: int
    width: int
    song: str
    pretty_name: str
    extra_actions: str | None
    poke_args: "PokeArgsDict | None"
    w_poke_args: "PokeArgsDict | None"
    weather: str | None


class Map:
    def __init__(
        self,
        height: int,
        width: int,
        song: str,
        pretty_name: str,
        extra_actions: str | None,
        poke_args: "PokeArgs | None",
        w_poke_args: "PokeArgs | None",
        weather: str | None
    ):
        self.height: int = height
        self.width: int = width
        self.song: str = song
        self.pretty_name: str = pretty_name
        self.extra_actions: str | None = extra_actions
        self.poke_args: "PokeArgs | None" = poke_args
        self.w_poke_args: "PokeArgs | None" = w_poke_args
        self.weather: str | None = weather

    @classmethod
    def from_dict(cls, _d: MapDict | None) -> "Map | None":
        if _d is None:
            return None
        return cls(
            height=_d["height"],
            width=_d["width"],
            song=_d["song"],
            pretty_name=_d["pretty_name"],
            extra_actions=_d.get("extra_actions", None),
            poke_args=PokeArgs.from_dict(_d.get("poke_args", None)),
            w_poke_args=PokeArgs.from_dict(_d.get("w_poke_args", None)),
            weather=_d.get("weather", None),
        )

    @staticmethod
    def validate(_d: MapDict) -> bool:
        return all([
            "height" in _d and type(_d["height"]) is int,
            "width" in _d and type(_d["width"]) is int,
            "song" in _d and type(_d["song"]) is str,
            "pretty_name" in _d and type(_d["pretty_name"]) is str,
            type(_d.get("extra_actions", None)) is str or _d.get("extra_actions", None) is None,
            True if _d.get("poke_args", None) is None else PokeArgs.validate(_d.get("poke_args", None)),
            True if _d.get("w_poke_args", None) is None else PokeArgs.validate(_d.get("w_poke_args", None)),
            type(_d.get("weather", None)) is str or _d.get("weather", None) is None,
        ])

    def to_dict(self) -> MapDict:
        ret: MapDict = {}
        
        ret["height"] = self.height
        ret["width"] = self.width
        ret["song"] = self.song
        ret["pretty_name"] = self.pretty_name
        if self.extra_actions is not None:
            ret["extra_actions"] = self.extra_actions
        if self.poke_args is not None:
            ret["poke_args"] = PokeArgs.to_dict(self.poke_args)
        if self.w_poke_args is not None:
            ret["w_poke_args"] = PokeArgs.to_dict(self.w_poke_args)
        if self.weather is not None:
            ret["weather"] = self.weather

        return ret
