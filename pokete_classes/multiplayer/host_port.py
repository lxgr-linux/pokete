class HostPortParseException(Exception):
    pass


class HostPort:
    def __init__(self, host: str, port: int | None = None):
        self.host: str = host
        self.port: int | None = port

    @classmethod
    def parse(cls, s: str) -> "HostPort":
        splid = s.split(":")
        if len(splid) == 1:
            return cls(splid[0])
        elif len(splid) == 2:
            try:
                return cls(splid[0], int(splid[1]))
            except ValueError:
                HostPortParseException("Invalid port")
        else:
            raise HostPortParseException("Invalid format")

    def __str__(self):
        return f"{self.host}:{self.port}" if self.port is not None else self.host
