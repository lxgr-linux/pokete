class UserPresentException(Exception):
    def __init__(self) -> None:
        super().__init__("user present")


class VersionMismatchException(Exception):
    def __init__(self, version: str) -> None:
        self.version = version
        super().__init__("version mismatch")


class InvalidPokeException(Exception):
    def __init__(self, msg: str) -> None:
        self.msg = msg
        super().__init__(msg)


class ConnectionException(Exception):
    def __init__(self, e: Exception) -> None:
        super().__init__("failed to connect", e)


class UnexpectedResponseException(Exception):
    def __init__(self, resp: object) -> None:
        self.resp = resp
        super().__init__(f"unexpected response: {resp!r}")
