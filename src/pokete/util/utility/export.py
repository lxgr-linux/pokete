import json
from pathlib import Path

from pokete.classes.asset_service.service import asset_service
from pokete.util.command.command import Flag

DEFAULT_OUT_PATH = Path("base_data.json")

out_flag = Flag(["--out", "-o"], f"Output path, default '{DEFAULT_OUT_PATH}'")


def export_base_data(ex: str, options: list[str], flags: dict[str, list[str]]):
    out_path: Path = DEFAULT_OUT_PATH

    for flag, value in flags.items():
        if out_flag.is_flag(flag):
            out_path = Path(value[0])

    asset_service.load_base_assets_from_p_data()

    with open(out_path, "w") as file:
        json.dump(asset_service.get_base_assets().to_dict(), file, indent=2)
