"""Contains class retaed to cennecting to a server"""

import release

from util import liner
from .communication import com_service, ConnectionException
from .exceptions import UserPresentException, VersionMismatchException, \
    InvalidPokeException
from ..context import Context
from ..input_loops import ask_ok, ask_text


class Connector:
    """Managers server connection"""

    def __init__(self):
        self.host = ""
        self.port = ""
        self.user_name = ""
        self.saved_pos = ()

    def __call__(self, ctx: Context):
        """Starts ui to connect to server"""
        conn_succ = False
        while not conn_succ:
            self.set_host_port(ctx)
            self.ask_user_name(ctx)
            conn_succ = self.establish_connection(ctx)
        self.handshake(ctx)

    def handshake(self, ctx: Context):
        try:
            greeting_text = com_service.handshake(ctx, self.user_name,
                                                  release.VERSION)
            ask_ok(ctx, liner(greeting_text, ctx.map.width - 4))
        except UserPresentException:
            self.ask_user_name(ctx, True)
            self.establish_connection(ctx)
            self.handshake(ctx)
        except VersionMismatchException as e:
            ask_ok(ctx, f"Version mismatch: {e.version}")
        except InvalidPokeException as e:
            ask_ok(ctx, f"Invalid Poke: {e.msg}")

    def set_host_port(self, ctx: Context):
        """Asks the user for host and port to conenct to"""
        unified_host_port = ""
        while unified_host_port == "":
            unified_host_port = ask_text(
                ctx,
                "Please enter the servers host you want to connect to.",
                "Host:",
                f"{self.host}:{self.port}" if self.host else "localhost",
                "Host",
                20,
            )
        splid = unified_host_port.split(":")
        if len(splid) == 1:
            self.port = 9988
        else:
            self.port = int(splid[1])
        self.host = splid[0]

    def ask_user_name(self, ctx: Context, reask=False):
        """Asks the user for username
        ARGS:
            reask: Boolean whether or not this is asked again"""
        self.user_name = ctx.figure.name
        self.user_name = ask_text(
            ctx,
            ("That username isn't awailable right now\n" if reask else "")
            + "Please enter the username you want to use on the server",
            "Username:",
            self.user_name,
            "Username",
            20,
        )

    def establish_connection(self, ctx):
        """Actually connects to the server"""
        try:
            com_service.connect(self.host, self.port)
        except ConnectionException as excpt:
            ask_ok(
                ctx,
                f"An error occured connecting to {self.host}:{self.port} :\n"
                f"{excpt}",
            )
            return False
        return True


connector = Connector()
