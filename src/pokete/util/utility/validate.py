from pokete.classes.asset_service.service import asset_service


def validate(ex: str, options: list[str],
             flags: dict[str, list[str]]):
    asset_service.load_base_assets_from_p_data()
    asset_service.load_assets_from_p_data()
