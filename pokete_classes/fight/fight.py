import logging
import random
import time

from pokete_data import achievements
from release import SPEED_OF_TIME
from .attack_result import Result
from .fight_items import FightItems
from .fightmap import FightMap
from .providers import Provider
from ..attack import Attack
from ..audio import audio
from ..inv_items import InvItem
from ..npcs import Trainer
from ..tss import tss
from .. import movemap as mvp


class Fight:
    def __init__(self):
        self.fightmap: FightMap = FightMap(tss.height - 1, tss.width)
        self.providers: list[Provider] = []
        self.fight_items = FightItems()

    def __call__(self, providers: list[Provider]):
        audio.switch("xDeviruchi - Decisive Battle (Loop).mp3")
        self.providers = providers
        logging.info(
            "[Fight] Started between %s",
            "and ".join(
                f"{prov.curr.name} ({type(prov)}) lvl. {prov.curr.lvl()}"
                for prov in self.providers
            )
        )
        for prov in self.providers:
            prov.index_conf()
        self.fightmap.add_providers(self.providers)

        index = self.providers.index(
            max(self.providers, key=lambda i: i.curr.initiative)
        )
        for prov in self.providers:
            i = prov.curr
            for j in i.effects:
                j.readd()
        while True:
            player: Provider = self.providers[index % 2]
            enem: Provider = self.providers[(index + 1) % 2]
            winner: Provider | None = None
            loser: Provider | None = None

            attack_result = player.get_attack(self.fightmap, enem)
            match attack_result.result:
                case Result.ATTACK:
                    attack: Attack = attack_result.attack
                    player.curr.attack(
                        attack, enem.curr, self.fightmap,
                        self.providers
                    )
                case Result.RUN_AWAY:
                    if enem.escapable:
                        logging.warning(
                            "[Fight]: Trying to run away from inescapbale fight")
                    else:
                        if (
                            random.randint(0, 100) < max(
                            5,
                            min(
                                50 - (
                                    player.curr.initiative - enem.curr.initiative
                                ),
                                95
                            )
                        )):
                            self.fightmap.failed_to_escape()
                        else:
                            audio.switch(
                                "xDeviruchi - Decisive Battle (End).mp3"
                            )
                            self.fightmap.ran_away(player, enem)
                            logging.info("[Fight] Ended, ran away")
                            player.curr.poke_stats.set_run_away_battle()
                            audio.switch(player.map.song)
                            return player
                case Result.ITEM:
                    item: InvItem = attack_result.item
                    fight_func = getattr(self.fight_items, item.func)
                    match fight_func(self.fightmap, player, enem):
                        # case 1:
                        #    continue  TODO:impl
                        case 2:
                            player.curr.poke_stats.add_battle(True)
                            logging.info("[Fight] Ended, fightitem")
                            time.sleep(SPEED_OF_TIME * 2)
                            audio.switch(player.map.song)
                            return player

            time.sleep(SPEED_OF_TIME * 0.3)
            self.show()
            time.sleep(SPEED_OF_TIME * 0.5)

            for i, prov in enumerate(self.providers):
                if prov.curr.hp <= 0:
                    loser = prov
                    winner = self.providers[(i + 1) % 2]
            if winner is not None:
                self.fightmap.show_death(loser)
            elif all(i.ap == 0 for i in player.curr.attack_obs):
                winner = self.providers[(index + 1) % 2]
                loser = player
                self.fightmap.show_used_all_attacks(player)
            if winner is not None:
                if any(p.hp > 0 for p in loser.pokes[:6]):
                    if not loser.handle_defeat(self, winner):
                        break
                else:
                    break
            index += 1
        audio.switch("xDeviruchi - Decisive Battle (End).mp3")

        xp = sum(
            poke.lose_xp + max(0, poke.lvl() - winner.curr.lvl())
            for poke in loser.pokes
        ) * loser.xp_multiplier
        self.fightmap.declare_winner(winner, xp)

        if winner.curr.player and isinstance(loser, Trainer):
            achievements.achieve("first_duel")
        if winner.curr.player and winner.curr.add_xp(xp):
            self.fightmap.win_animation(winner)
            winner.curr.set_vars()
            winner.curr.learn_attack(self, self)
            winner.curr.evolve(winner, self)

        if winner.curr.player:
            winner.curr.poke_stats.add_battle(True)
        else:
            loser.curr.poke_stats.add_battle(False)

        self.fightmap.death_animation(loser)
        mvp.movemap.balls_label_rechar(winner.pokes)
        logging.info(
            "[Fight] Ended, %s(%s) won",
            winner.curr.name, "player" if winner.curr.player else "enemy"
        )
        audio.switch(self.providers[0].map.song)
        return winner
