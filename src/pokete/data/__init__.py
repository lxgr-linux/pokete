"""This provides p_data. Never ever import this except for in pokete.py since
   p_data can be manipulated by mods and therefore should be injected and not
   imported

   I know all this is very awfull...

   ...not so awfull anymore, since I introduced code generation
"""

from .poketes import *
from .attacks import *
from .map_data import *
from .types import *
from .items import *
from .trainers import *
from .npcs import *
from .mapstations import *
from .maps import *
from .achievements import *
from .weather import *
from .natures import *

# from .npc_actions import *

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
