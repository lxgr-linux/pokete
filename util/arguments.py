def parse(args) -> tuple[str, list[str], dict[str, list[str]]]:
    if len(args) == 0:
        return "", [], {}
    options: list[str] = []
    flags: dict[str, list[str]] = {}
    idx = 0
    for arg in args[2:]:
        if arg.startswith("--"):
            break
        idx += 1
        options.append(arg)
    __index_flags(0, args[2 + idx:], "", flags)

    return args[1], options, flags


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
