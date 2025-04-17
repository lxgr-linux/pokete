import scrap_engine as se

from pokete.classes.classes import PlayMap
from pokete.classes.doors import ChanceDoor
from pokete.classes.landscape import HighGrass
from .customizer import MapCustomizer

class Cave1Customizer(MapCustomizer):
    def customize(self, _map: PlayMap):
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


class Playmap4Customizer(MapCustomizer):
    def customize(self, _map: PlayMap):
        _map.dor_playmap_5 = ChanceDoor("~", state="float",
                                        arg_proto={"chance": 6,
                                                   "map": "playmap_5",
                                                   "x": 17, "y": 16})
        # adding
        _map.dor_playmap_5.add(_map, 56, 1)


class Playmap5Customizer(MapCustomizer):
    def customize(self, _map: PlayMap):
        _map.inner = se.Square(" ", 11, 11, state="float", ob_class=HighGrass,
                               ob_args=_map.poke_args)
        # adding
        _map.inner.add(_map, 26, 1)


class Playmap7Customizer(MapCustomizer):
    def customize(self, _map: PlayMap):
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
        _map.inner.add(_map, 0, 0)


class Playmap9Customizer(MapCustomizer):
    def customize(self, _map: PlayMap):
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


class Playmap19Customizer(MapCustomizer):
    def customize(self, _map: PlayMap):
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


customizers: dict[str, MapCustomizer] = {
    "cave_1": Cave1Customizer(),
    "playmap_4": Playmap4Customizer(),
    "playmap_5": Playmap5Customizer(),
    "playmap_7": Playmap7Customizer(),
    "playmap_9": Playmap9Customizer(),
    "playmap_19": Playmap19Customizer(),
}
