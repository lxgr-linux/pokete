from ...input import ask_ok


def handle_version_mismatch(context: Connector, body, client):
    ask_ok(context.map, f"Version mismatch: {body}", context.overview)
