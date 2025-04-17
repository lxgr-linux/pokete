from pokete.classes.fight.fight import Fight


class RemoteFight(Fight):
    def __init__(self, starting: bool):
        self.starting = starting
        super().__init__()

    def initial_player_index(self):
        return 0 if self.starting else 1
