import scrap_engine as se

import pokete.data as p_data
from pokete.classes.doors import Door, ChanceDoor
from .. import ob_maps as obmp
from ..landscape import HighGrass
from ..settings import settings


def map_additions(figure):
    """Applies additions to the maps
    ARGS:
        figure: Figure instance"""

    # cave_1
    _map = obmp.ob_maps["cave_1"]
    _map.inner = se.Text("""##########################################
##        ################################
#         ################################
#         ######################        ##
#                    ###########   #######
#         #########  ###########   #######
#         #########  ###########   #######
###################  ###########   #######
##############                     #######
##############                     #######
##############  ##########################
##############  ##########################
########        ##########################
#######  ###    ##########################
#######  ###    ##########################
#######         ##########################
##############  ##########################
##############  ##########################
##############  ##########################
##############  ##########################""", ignore="#",
                         ob_class=HighGrass,
                         ob_args=_map.poke_args,
                         state="float")
    # adding
    _map.inner.add(_map, 0, 0)

    # playmap_4
    _map = obmp.ob_maps["playmap_4"]
    _map.dor_playmap_5 = ChanceDoor("~", state="float",
                                    arg_proto={"chance": 6,
                                               "map": "playmap_5",
                                               "x": 17, "y": 16})
    # adding
    _map.dor_playmap_5.add(_map, 56, 1)

    # playmap_5
    _map = obmp.ob_maps["playmap_5"]
    _map.inner = se.Square(" ", 11, 11, state="float", ob_class=HighGrass,
                           ob_args=_map.poke_args)
    # adding
    _map.inner.add(_map, 26, 1)

    # playmap_7
    _map = obmp.ob_maps["playmap_7"]
    _map.inner = se.Text("""##############################
#########        #############
#########        #############
#########        #############
#########        #############
#########               ######
##   ####     ####      ######
#    ####     ####     #######
#             ################
#    ####     ################
#########     ################
#########     ################
#########                   ##
#########     ################
#########     ################
#########     ################
#########             ########
###################   ########
####################  ########
##############################""", ignore="#", ob_class=HighGrass,
                         ob_args=_map.poke_args, state="float")
    for ob in (
        _map.get_obj("inner_walls").obs + [i.main_ob for i in _map.trainers] +
        [_map.get_obj(i) for i in p_data.map_data["playmap_7"]["balls"]
         if "playmap_7." + i not in figure.used_npcs
            or not settings("save_trainers").val]):
        ob.bchar = ob.char
        ob.rechar(" ")
    # adding
    _map.inner.add(_map, 0, 0)

    # playmap_9
    _map = obmp.ob_maps["playmap_9"]
    _map.inner = se.Text("""
#########################
#########################
###       #  #         ##
#         ####          #
#                       #
##                      #
#               #########
############ ############
#########################""", ignore="#", ob_class=HighGrass,
                         ob_args=_map.poke_args, state="float")
    # adding
    _map.inner.add(_map, 2, 1)

    # playmap_19
    _map = obmp.ob_maps["playmap_19"]
    _map.inner = se.Text("""                         ####
                         #  #   ############
                         #  #   #          #
                         #  #   #          #
        ##############   #  #####          #
        ##           #   #                 #
        #            #   #  #####          #
        #            #####  #   #          #
        #                   #   #         ##
        #            #####  #   ############
        ##############   #  #
                         #  #
         #################  ####################
         #                                    ##
     #####                                     #
     #                                         #
     #                        #######          #
     #                        #     #          #
     ######## #################     ######  ####
            # #                          #  #
            # #                          #  #
            # #                          #  #
            # #                          #  #
            # #                          #  #
            # #                   ########  #
            # #                  ##         #
            # #                   ###########
            # #
            # #
            ###""", ignore="#", ob_class=HighGrass,
                         ob_args=_map.poke_args, state="float")
    # adding
    _map.inner.add(_map, 0, 0)

    # playmap_21
    _map = obmp.ob_maps["playmap_21"]
    _map.dor_playmap_19 = Door("_", state="float",
                               arg_proto={"map": "playmap_19",
                                          "x": 26, "y": 1})
    # adding
    _map.dor_playmap_19.add(_map, 5, 26)
