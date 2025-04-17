import logging
from copy import copy


class Inventory:
    __inv: dict[str, int]

    def __init__(self, inv: dict[str, int]):
        self.__inv = inv

    def give_item(self, item:str, amount:int=1):
        """Gives an item to the player"""
        assert amount > 0, "Amounts have to be positive!"
        self.__inv[item] = self.__inv.get(item, 0) + amount
        logging.info("[Figure] %d %s(s) given", amount, item)

    def has_item(self, item:str):
        """Checks if an item is already present
        ARGS:
            item: Generic item name
        RETURNS:
            If the player has this item"""
        return item in self.__inv and self.__inv[item] > 0

    def get_inv(self):
        return copy(self.__inv)

    def remove_item(self, item:str, amount:int=1):
        """Removes a certain amount of an item from the inv
        ARGS:
            item: Generic item name
            amount: Amount of items beeing removed"""
        assert amount > 0, "Amounts have to be positive!"
        assert item in self.__inv, f"Item {item} is not in the inventory!"
        assert self.__inv[item] - amount >= 0, f"There are not enought {item}s \
in the inventory!"
        self.__inv[item] -= amount
        logging.info("[Figure] %d %s(s) removed", amount, item)
