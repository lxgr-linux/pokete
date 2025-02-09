from typing import TypedDict

import pokete.bs_rpc as bs_rpc

VERSION_MISMATCH_TYPE = "pokete.error.version_mismatch"


class VersionMismatchData(TypedDict):
    version: str


class VersionMismatch(bs_rpc.Body):
    def __init__(self, data: VersionMismatchData):
        super().__init__(VERSION_MISMATCH_TYPE, data)
