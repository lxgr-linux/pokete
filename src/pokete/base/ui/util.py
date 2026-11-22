"""Contains pokete.util functions for ObjectGroups"""

import scrap_engine as se


def get_nested(
    group: se.ObjectGroup,
) -> tuple[list[se.Object], list[tuple[int, int]]]:
    """RETURNS the raw objects an ObjectGroup contains
    ARGS:
        group: The given ObjectGroup"""
    obs: list[se.Object] = []
    coords: list[tuple[int, int]] = []
    for obj in group.obs:
        if isinstance(obj, se.ObjectGroup):
            ret_obs, ret_coords = get_nested(obj)
            obs += ret_obs
            coords += [(c[0] + obj.rx, c[1] + obj.ry) for c in ret_coords]
        else:
            obs.append(obj)
            coords.append((obj.rx, obj.ry))
    return obs, coords
