from typing import TypedDict

from pokete import bs_rpc

VERSION_MISMATCH_TYPE = "pokete.error.version_mismatch"


class VersionMismatchData(TypedDict):
    version: str


class VersionMismatch(bs_rpc.Body):
    def __init__(self, data: VersionMismatchData) -> None:
        super().__init__(VERSION_MISMATCH_TYPE, data)
