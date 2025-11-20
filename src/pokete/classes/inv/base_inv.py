import scrap_engine as se

from pokete.base.ui.views.choose_box import ChooseBoxView

from .box import InvBox


class BaseInv(ChooseBoxView):
    def __init__(self, name: str, info=""):
        super().__init__(50, 35, name, info)
        self.invbox = InvBox(overview=self)
        self.money_label = se.Text("$0")

        # adding
        self.add_ob(
            self.money_label, self.width - 2 - len(self.money_label.text), 0
        )

    def new_size(self) -> tuple[int, int]:
        return self.map.height - 3, 35

    def set_money(self, figure):
        self.money_label.rechar(f"${figure.get_money()}")
        self.set_ob(
            self.money_label, self.width - 2 - len(self.money_label.text), 0
        )
