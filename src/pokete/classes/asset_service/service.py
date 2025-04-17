import logging

from pokete.classes.items import InvItem, LearnDisc
import pokete.data as p_data
from .resources import Assets, BaseAssets, AssetsDict, BaseAssetsDict


Items = dict[str, InvItem]


class ValidationException(Exception):
    def __init__(self):
        super().__init__("Failed to validate data")


class AssetSerice:
    def __init__(self):
        self.__assets: Assets | None = None
        self.__base_assets: BaseAssets | None = None
        self.__items: Items = {}
        self.load_base_assets_from_p_data()

    def load_assets(self, assets: AssetsDict):
        if not Assets.validate(assets):
            raise ValidationException

        self.__assets = Assets.from_dict(assets)

    def __load_base_assets(self, base_assets: BaseAssetsDict):
        if not BaseAssets.validate(base_assets):
            raise ValidationException
        self.__base_assets = BaseAssets.from_dict(base_assets)
        assert self.__base_assets is not None
        self.__items = {**{
            name: InvItem(
                name, item.pretty_name,
                item.desc, item.price, item.fn
            )
            for name, item in self.__base_assets.items.items()
        }, **{
            (
                disc:=LearnDisc(i, self.__base_assets.attacks[i])
            ).name: disc
            for i in ["flying","bubble_bomb", "the_old_roots_hit"]
        }}

    def get_items(self) -> Items:
        return self.__items

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
            "attacks": p_data.attacks,
            "natures": p_data.natures,
            "weathers": p_data.weathers,
            "types": p_data.types,
            "sub_types": p_data.sub_types,
            "achievements": p_data.achievements
        })

    def get_assets(self) -> Assets:
        return self.__assets

    def get_base_assets(self) -> BaseAssets:
        return self.__base_assets


asset_service: AssetSerice = AssetSerice()
