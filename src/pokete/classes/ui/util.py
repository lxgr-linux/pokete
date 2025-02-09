"""Contains pokete.util functions for ObjectGroups"""

import scrap_engine as se


def get_nested(group: se.ObjectGroup):
    """RETURNS the raw objects an ObjectGroup contains
    ARGS:
        group: The given ObjectGroup"""
    obs = []
    for obj in group.obs:
        if isinstance(obj, se.ObjectGroup):
            obs += get_nested(obj)
        else:
            obs.append(obj)
    return obs
