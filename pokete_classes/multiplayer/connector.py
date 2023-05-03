import socket
import json

import release
from pokete_classes.input import ask_text, ask_ok

END_SECTION = b"<END>"


class Connector:
    def __init__(self):
        self.host = ""
        self.port = ""
        self.user_name = ""
        self.connection = None
        self.map = None
        self.overview = None

    def __call__(self, _map, overview):
        self.map = _map
        self.set_host_port()
        self.ask_user_name()
        self.establish_connection()
        self.handshake()

    def set_host_port(self):
        unified_host_port = ""
        while unified_host_port == "":
            unified_host_port = ask_text(
                self.map,
                "Please enter the servers host you want to connect to.",
                "Host:",
                self.host + ":" + self.port if self.host else "",
                "Host",
                20,
                self.overview
            )
        splid = unified_host_port.split(":")
        if len(splid) == 1:
            self.port = 9988
        else:
            self.port = splid[1]
        self.host = splid[0]

    def ask_user_name(self, reask=False):
        self.user_name = ask_text(
            self.map,
            ("That username isn't awailable right now\n" if reask else "") +
            "Please enter the username you want to use on the server",
            "Username:",
            self.user_name,
            "Username",
            20,
            self.overview
        )

    def establish_connection(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.connection.connect((self.host, self.port))
        except Exception as excpt:
            ask_ok(
                self.map,
                f"An error occured connecting to {self.host}:{self.port} :\n"
                f"{excpt}",
                self.overview
            )
            
    def handshake(self):
        self.connection.sendall(
            str.encode(
                json.dumps(
                    {
                        "Type": 1,
                        "Body": {
                            "UserName": self.user_name,
                            "Version": release.VERSION
                        }
                    }
                )
            )
        )
        if (d := self.receive_data())["Type"] == 2:
            self.ask_user_name(True)
            self.establish_connection()
            self.handshake()
        elif d["Type"] == 3:
            ask_ok(
                self.map,
                f"Version mismatch: {d['Body']}",
                self.overview
            )
            
    def receive_data(self):
        data = self.connection.recv(1048576)
        while data[-len(END_SECTION):] != END_SECTION:
            data += self.connection.recv(1048576)
        return json.loads(data[:-len(END_SECTION)])

    def ensure_closure(self):
        if self.connection:
            self.connection.close()


connector = Connector()
