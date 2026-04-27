"""This provides p_data. Never ever import this except for in pokete.py since
p_data can be manipulated by mods and therefore should be injected and not
imported

I know all this is very awful...

...not so awful anymore, since I introduced code generation
"""

from .achievements import *  # noqa: F403
from .attacks import *  # noqa: F403
from .items import *  # noqa: F403
from .map_data import *  # noqa: F403
from .maps import *  # noqa: F403
from .mapstations import *  # noqa: F403
from .natures import *  # noqa: F403
from .npcs import *  # noqa: F403
from .poketes import *  # noqa: F403
from .trainers import *  # noqa: F403
from .types import *  # noqa: F403
from .weather import *  # noqa: F403

# from .npc_actions import *

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
