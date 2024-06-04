from typing import TypedDict

import bs_rpc


class VersionMismatchData(TypedDict):
    version: str


class VersionMismatch(bs_rpc.Body):
    def __init__(self, data: VersionMismatchData):
        super().__init__("pokete.error.version_mismatch", data)
