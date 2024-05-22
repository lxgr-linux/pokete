from pokete_classes.generate import gen_maps
from pokete_classes.multiplayer.connector import Connector
from pokete_classes import ob_maps as obmp, roadmap
from pokete_classes.generate import gen_maps, gen_obs
from pokete_general_use_fns import liner
from pokete_classes.input import ask_ok
from pokete_classes.multiplayer.pc_manager import pc_manager


def handle_map_data(context: Connector, body, client):
    obmp.ob_maps = gen_maps(body["Maps"], fix_center=True)
    gen_obs(
        body["Obmaps"],
        body["NPCs"],
        body["Trainers"],
        context.figure,
    )
    roadmap.roadmap = roadmap.RoadMap(
        context.figure,
        body["MapStations"]
    )
    pos = body["Position"]
    context.saved_pos = (
        context.figure.map.name,
        context.figure.oldmap.name,
        context.figure.last_center_map.name,
        context.figure.x,
        context.figure.y,
    )
    context.figure.remove()
    context.figure.add(obmp.ob_maps[pos["Map"]], pos["X"], pos["Y"])
    if body["GreetingText"]:
        ask_ok(
            context.map,
            liner(body["GreetingText"], context.map.width - 4)
        )
    if body["Users"]:
        for user in body["Users"]:
            pc_manager.set(
                user["Name"],
                user["Position"]["Map"],
                user["Position"]["X"],
                user["Position"]["Y"],
            )
