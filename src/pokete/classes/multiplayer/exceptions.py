class UserPresentException(Exception):
    def __init__(self) -> None:
        super().__init__("user present")


class VersionMismatchException(Exception):
    def __init__(self, version) -> None:
        self.version = version
        super().__init__("version mismatch")


class InvalidPokeException(Exception):
    def __init__(self, msg) -> None:
        self.msg = msg
        super().__init__(msg)


class ConnectionException(Exception):
    def __init__(self, e: Exception) -> None:
        super().__init__("failed to connect", e)
