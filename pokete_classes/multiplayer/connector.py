"""Contains class retaed to cennecting to a server"""

import socket
import json
import logging
import threading

import bs_rpc
import release

from pokete_classes import ob_maps as obmp, roadmap
from pokete_classes.generate import gen_maps, gen_obs
from pokete_classes.input import ask_text, ask_ok
from pokete_classes.multiplayer import msg
from pokete_classes.multiplayer.pc_manager import pc_manager
from pokete_general_use_fns import liner


class Connector:
    """Managers server connection"""

    def __init__(self):
        self.host = ""
        self.port = ""
        self.user_name = ""
        self.connection = None
        self.map = None
        self.overview = None
        self.figure = None
        self.saved_pos = ()
        self.bs_rpc_client: bs_rpc.Client = None
        self.reg = msg.get_registry()

    def __call__(self, _map, overview):
        """Starts ui to connect to server
        ARGS:
            _map: Map to show this on
            overview: Overview for resizing"""
        self.map = _map
        conn_succ = False
        while not conn_succ:
            self.set_host_port()
            self.ask_user_name()
            conn_succ = self.establish_connection()
        self.handshake()

    def set_host_port(self):
        """Asks the user for host and port to conenct to"""
        unified_host_port = ""
        while unified_host_port == "":
            unified_host_port = ask_text(
                self.map,
                "Please enter the servers host you want to connect to.",
                "Host:",
                f"{self.host}:{self.port}" if self.host else "",
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
            self.user_name,
            "Username",
            20,
            self.overview,
        )

    def establish_connection(self):
        """Actually connects to the server"""
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.connection.connect((self.host, self.port))
            self.bs_rpc_client = bs_rpc.Client(connector, self.reg)

            listen = threading.Thread(
                target=lambda: self.bs_rpc_client.listen(self),
                daemon=True)

            listen.start()
            return True
        except Exception as excpt:
            ask_ok(
                self.map,
                f"An error occured connecting to {self.host}:{self.port} :\n"
                f"{excpt}",
                self.overview,
            )
            return False

    def send_pos_update(self, _map, x, y):
        """Sends a position update to the server
        ARGS:
            _map: Name of the map the player is on
            x: X-coordinate
            y: Y-coordinate"""
        self.send(
            {
                "Type": 0,
                "Body": {
                    "Map": _map,
                    "X": x,
                    "Y": y,
                },
            }
        )
        self.bs_rpc_client.__send(msg.)

    def handshake(self):
        """Sends and handles the handshake with the server"""
        self.bs_rpc_client.__send(msg.TYPE_HANDSHAKE, {
            "UserName": self.user_name,
            "Version": release.VERSION,
        })

    def ensure_closure(self):
        """Makes sure the connection is closed"""
        if self.connection:
            self.connection.close()

    def set_args(self, figure):
        """Sets arguments
        ARGS:
            figure: Figure instance"""
        self.figure = figure


connector = Connector()
