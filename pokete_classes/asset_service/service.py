import logging

import pokete_data as p_data
from .asset_types.assets import Assets, BaseAssets


class AssetSerice:
    def __init__(self):
        self.__assets: Assets | None = None
        self.__base_assets: BaseAssets | None = None
        self.load_base_assets_from_p_data()

    def load_assets(self, assets: Assets):
        self.__assets = assets

    def __load_base_assets(self, base_assets: BaseAssets):
        self.__base_assets = base_assets

    def load_assets_from_p_data(self):
        if self.__assets is not None:
            logging.warning("[AssetService]: Assets already loaded")
        self.load_assets({
            "trainers": p_data.trainers,
            "npcs": p_data.npcs,
            "obmaps": p_data.map_data,
            "stations": p_data.stations,
            "decorations": p_data.decorations,
            "maps": p_data.maps,
        })

    def load_base_assets_from_p_data(self):
        self.__load_base_assets({
            "items": p_data.items,
            "pokes": p_data.pokes,
            "natures": p_data.natures,
            "weathers": p_data.weathers,
            "types": p_data.types,
            "achievements": p_data.achievements
        })

    def get_assets(self) -> Assets | None:
        return self.__assets

    def get_base_assets(self) -> BaseAssets:
        return self.__base_assets


asset_service: AssetSerice = AssetSerice()
