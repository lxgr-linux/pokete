from pokete_classes.multiplayer.connector import Connector


def handle_user_already_present(context: Connector, body, client):
    context.ask_user_name(True)
    context.establish_connection()
    context.handshake()
