from typing import TypedDict


class Item(TypedDict):
    pretty_name: str
    desc: str
    price: int
    fn: str | None


Items = dict[str, Item]
