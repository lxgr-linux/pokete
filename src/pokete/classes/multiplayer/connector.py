"""Contains class retaed to cennecting to a server"""

from pokete import release
from pokete.util import liner
from pokete.base.context import Context
from pokete.base.input_loops import ask_ok, ask_text
from .communication import com_service, ConnectionException
from .exceptions import UserPresentException, VersionMismatchException, \
    InvalidPokeException
from .host_port import HostPort, HostPortParseException


DEFAULT_PORT = 9988


class Connector:
    """Managers server connection"""

    def __init__(self):
        self.host_port: HostPort = HostPort("localhost")
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
        while True:
            try:
                self.host_port = HostPort.parse(ask_text(
                    ctx,
                    "Please enter the servers host you want to connect to.",
                    "Host:",
                    str(self.host_port),
                    "Host",
                    40,
                ))
            except HostPortParseException as e:
                ask_ok(ctx, f"Error: {e}")
                continue
            break

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
            com_service.connect(
                self.host_port.host,
                self.host_port.port if self.host_port.port is not None else DEFAULT_PORT
            )
        except ConnectionException as excpt:
            ask_ok(
                ctx,
                f"An error occured connecting to {self.host_port} :\n"
                f"{excpt}",
            )
            return False
        return True


connector = Connector()
