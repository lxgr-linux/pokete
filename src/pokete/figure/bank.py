import logging



class Bank:
    logger = logging.getLogger("Bank")
    __money: int

    def __init__(self, money: int) -> None:
        self.__money = money

    def add_money(self, money: int) -> None:
        """Adds money
        ARGS:
            money: Amount of money being added"""
        self.set_money(self.__money + money)

    def get_money(self) -> None:
        """Getter for __money
        RETURNS:
            The current money"""
        return self.__money

    def set_money(self, money: int) -> None:
        """Sets the money to a certain value
        ARGS:
            money: New value"""
        assert money >= 0, "Money has to be positive."
        self.logger.info("[Figure] Money set to $%d from $%d", money, self.__money)
        self.__money = money
