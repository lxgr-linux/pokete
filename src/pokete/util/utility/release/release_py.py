def write_release_py(tag: str):
    with open("release.py", "r") as f:
        content = f.readlines()

    for idx, line in enumerate(content):
        if line.startswith('VERSION = "'):
            content[idx] = f'VERSION = "{tag.lstrip("v")}"\n'
            break

    with open("release.py", "w") as f:
        f.writelines(content)
