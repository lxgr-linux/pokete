from typing import TypedDict

from pokete import bs_rpc

INVALID_POKE_TYPE = "pokete.error.invalid_poke"


class InvalidPokeData(TypedDict):
    error: str


class InvalidPoke(bs_rpc.Body):
    def __init__(self, data: InvalidPokeData) -> None:
        super().__init__(INVALID_POKE_TYPE, data)
