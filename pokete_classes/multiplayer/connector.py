import socket
import json
import logging

import release
from pokete_classes import ob_maps as obmp
from pokete_classes.generate import gen_maps, gen_obs
from pokete_classes.input import ask_text, ask_ok
from pokete_classes.multiplayer.pc_manager import pc_manager
from pokete_general_use_fns import liner

END_SECTION = b"<END>"


class Connector:
    def __init__(self):
        self.host = ""
        self.port = ""
        self.user_name = ""
        self.connection = None
        self.map = None
        self.overview = None
        self.figure = None
        self.saved_pos = ()

    def __call__(self, _map, overview):
        self.map = _map
        conn_succ = False
        while not conn_succ:
            self.set_host_port()
            self.ask_user_name()
            conn_succ = self.establish_connection()
        self.handshake()

    def set_host_port(self):
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
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.connection.connect((self.host, self.port))
            return True
        except Exception as excpt:
            ask_ok(
                self.map,
                f"An error occured connecting to {self.host}:{self.port} :\n"
                f"{excpt}",
                self.overview,
            )
            return False

    def send(self, data: dict):
        self.connection.sendall(
            str.encode(json.dumps(data)) + END_SECTION
        )

    def send_pos_update(self, _map, x, y):
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

    def handshake(self):
        self.send(
            {
                "Type": 1,
                "Body": {
                    "UserName": self.user_name,
                    "Version": release.VERSION,
                },
            }
        )
        if (d := self.receive_data())["Type"] == 2:
            self.ask_user_name(True)
            self.establish_connection()
            self.handshake()
        elif d["Type"] == 3:
            ask_ok(self.map, f"Version mismatch: {d['Body']}", self.overview)
        elif d["Type"] == 0:
            obmp.ob_maps = gen_maps(d["Body"]["Maps"])
            gen_obs(
                d["Body"]["Obmaps"],
                d["Body"]["NPCs"],
                d["Body"]["Trainers"],
                self.figure,
            )
            pos = d["Body"]["Position"]
            self.saved_pos = (
                self.figure.map.name,
                self.figure.oldmap.name,
                self.figure.x,
                self.figure.y,
            )
            self.figure.remove()
            self.figure.add(obmp.ob_maps[pos["Map"]], pos["X"], pos["Y"])
            if d["Body"]["GreetingText"]:
                ask_ok(
                    self.map,
                    liner(d["Body"]["GreetingText"], self.map.width - 4)
                )
            if d["Body"]["Users"]:
                for user in d["Body"]["Users"]:
                    pc_manager.set(
                        user["Name"],
                        user["Position"]["Map"],
                        user["Position"]["X"],
                        user["Position"]["Y"],
                    )

    def receive_data(self):
        data = self.connection.recv(1048576)
        while data[-len(END_SECTION):] != END_SECTION:
            data += self.connection.recv(1048576)
        ret = json.loads(data[: -len(END_SECTION)])
        logging.info("[Connector] Received data: %s", ret)
        return ret

    def ensure_closure(self):
        if self.connection:
            self.connection.close()

    def set_args(self, figure):
        self.figure = figure


connector = Connector()
