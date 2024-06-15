class UserPresentException(Exception):
    def __init__(self):
        super().__init__("user present")


class VersionMismatchException(Exception):
    def __init__(self, version):
        self.version = version
        super().__init__("version mismatch")


class ConnectionException(Exception):
    def __init__(self, e: Exception):
        super().__init__("failed to connect", e)
