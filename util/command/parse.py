def parse(args) -> tuple[list[str], dict[str, list[str]]]:
    if len(args) == 1:
        return [], {}
    options: list[str] = []
    flags: dict[str, list[str]] = {}
    idx = 0
    for arg in args[1:]:
        if arg.startswith("--"):
            break
        idx += 1
        options.append(arg)
    __index_flags(0, args[1 + idx:], "", flags)

    return options, flags


def __index_flags(
    idx: int, arr: list[str], flag: str,
    flags: dict[str, list[str]]
):
    if idx == len(arr):
        return
    if arr[idx].startswith("--"):
        flag = arr[idx]
        flags[flag] = flags.get(flag, [])
    else:
        flags[flag].append(arr[idx])
    __index_flags(idx + 1, arr, flag, flags)
