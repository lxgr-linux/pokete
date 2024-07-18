"""Contains class retaed to cennecting to a server"""

import release

from util import liner
from .communication import com_service, ConnectionException
from .exceptions import UserPresentException, VersionMismatchException, \
    InvalidPokeException
from ..context import Context
from ..ui import ask_ok, ask_text


class Connector:
    """Managers server connection"""

    def __init__(self):
        self.host = ""
        self.port = ""
        self.user_name = ""
        self.map = None
        self.overview = None
        self.figure = None
        self.saved_pos = ()

    def __call__(self, ctx: Context):
        """Starts ui to connect to server"""
        self.map = ctx.map
        self.overview = ctx.overview
        conn_succ = False
        while not conn_succ:
            self.set_host_port()
            self.ask_user_name()
            conn_succ = self.establish_connection()
        self.handshake()

    def handshake(self):
        try:
            greeting_text = com_service.handshake(self, self.user_name,
                                                  release.VERSION)
            ask_ok(
                self.map,
                liner(greeting_text, self.map.width - 4),
                self.overview
            )
        except UserPresentException:
            self.ask_user_name(True)
            self.establish_connection()
            self.handshake()
        except VersionMismatchException as e:
            ask_ok(self.map, f"Version mismatch: {e.version}", self.overview)
        except InvalidPokeException as e:
            ask_ok(self.map, f"Invalid Poke: {e.msg}", self.overview)

    def set_host_port(self):
        """Asks the user for host and port to conenct to"""
        unified_host_port = ""
        while unified_host_port == "":
            unified_host_port = ask_text(
                self.map,
                "Please enter the servers host you want to connect to.",
                "Host:",
                f"{self.host}:{self.port}" if self.host else "localhost",
                "Host",
                20,
                self.overview,
            )
        splid = unified_host_port.split(":")
        if len(splid) == 1:
            self.port = 9988
        else:
            self.port = int(splid[1])
        self.host = splid[0]

    def ask_user_name(self, reask=False):
        """Asks the user for username
        ARGS:
            reask: Boolean whether or not this is asked again"""
        self.user_name = ask_text(
            self.map,
            ("That username isn't awailable right now\n" if reask else "")
            + "Please enter the username you want to use on the server",
            "Username:",
            self.user_name if self.user_name else "lxgr",
            "Username",
            20,
            self.overview,
        )

    def establish_connection(self):
        """Actually connects to the server"""
        try:
            com_service.connect(self.host, self.port)
        except ConnectionException as excpt:
            ask_ok(
                self.map,
                f"An error occured connecting to {self.host}:{self.port} :\n"
                f"{excpt}",
                self.overview,
            )
            return False
        return True

    def set_args(self, figure):
        """Sets arguments
        ARGS:
            figure: Figure instance"""
        self.figure = figure


connector = Connector()
