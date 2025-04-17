import yaml

FILE = "assets/AppImageBuilder.yml"


def write_appimage(tag: str):
    with open(FILE, 'r') as f:
        content = yaml.safe_load(f)

    content["AppDir"]["app_info"]["version"] = tag.lstrip("v")

    with open(FILE, 'w') as f:
        yaml.dump(content, f)
