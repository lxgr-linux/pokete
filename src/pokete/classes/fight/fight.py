import logging
import random
import time

from pokete.base.change import change_ctx
from pokete.base.context import Context
from pokete.base.exception_propagation import (
    exception_propagating_periodic_event,
)
from pokete.base.periodic_event_manager import PeriodicEventManager
from pokete.base.single_event import single_event_periodic_event
from pokete.base.tss import tss
from pokete.classes.fight.items.item import RoundContinuation
from pokete.classes.items.invitem import InvItem
from pokete.release import SPEED_OF_TIME

from ..attack import Attack
from ..audio import audio
from ..poke import EvoMap
from .attack_process import AttackProcess
from .fight_decision import Result
from .fightmap import FightMap
from .items import fight_items
from .providers import Provider


class Fight:
    def __init__(self):
        self.fightmap: FightMap = FightMap(tss.height - 1, tss.width)
        self.providers: list[Provider] = []
        self.attack_process = AttackProcess(self.fightmap)

    def initial_player_index(self):
        return self.providers.index(
            max(self.providers, key=lambda i: i.curr.initiative)
        )

    def __call__(self, ctx: Context, providers: list[Provider]):
        audio.play("xDeviruchi - Decisive Battle (Loop).mp3")
        self.providers = providers
        self.fightmap.set_overview(ctx.overview)
        self.fightmap.set_providers(providers)
        ctx = change_ctx(
            Context(
                PeriodicEventManager(
                    [
                        exception_propagating_periodic_event,
                        single_event_periodic_event,
                    ]
                ),
                self.fightmap,
                ctx.overview,
                ctx.figure,
            ),
            self.fightmap,
        )
        logging.info(
            "[Fight] Started between %s",
            "and ".join(
                f"{prov.curr.name} ({type(prov)}) lvl. {prov.curr.lvl()}"
                for prov in self.providers
            ),
        )
        for prov in self.providers:
            prov.index_conf()
        self.fightmap.add_providers(self.providers)

        index = self.initial_player_index()
        for prov in self.providers:
            i = prov.curr
            for j in i.effects:
                j.readd()
        while True:
            player: Provider = self.providers[index % 2]
            enem: Provider = self.providers[(index + 1) % 2]
            winner: Provider | None = None
            loser: Provider | None = None

            while True:
                attack_result = player.get_decision(ctx, self.fightmap, enem)
                match attack_result.result:
                    case Result.ATTACK:
                        attack: Attack = attack_result.attack_value
                        self.attack_process(
                            player.curr, enem.curr, attack, self.providers
                        )

                    case Result.RUN_AWAY:
                        if not enem.escapable:
                            logging.warning(
                                "[Fight]: Trying to run away from inescapbale fight"
                            )
                        else:
                            if random.randint(0, 100) < max(
                                5,
                                min(
                                    50
                                    - (
                                        player.curr.initiative
                                        - enem.curr.initiative
                                    ),
                                    95,
                                ),
                            ):
                                self.fightmap.failed_to_escape()
                            else:
                                audio.play(
                                    "xDeviruchi - Decisive Battle (End).mp3"
                                )
                                self.fightmap.ran_away(player, enem)
                                logging.info("[Fight] Ended, ran away")
                                player.curr.poke_stats.set_run_away_battle()
                                audio.play(ctx.figure.map.song)
                                return player
                    case Result.ITEM:
                        item: InvItem = attack_result.item_value
                        fight_item = fight_items.get(item.func, None)
                        if fight_item is None:
                            raise Exception(
                                f"fight_item doesnt exist {item.func}"
                            )
                        self.fightmap.show_item_used(player, item)
                        match fight_item.use(self.fightmap, player, enem):
                            case RoundContinuation.CONTINUE_ATTACK:
                                continue  # This is the sole reason for the while loop on top
                            case RoundContinuation.ENEMY_ATTACK:
                                break
                            case RoundContinuation.EXIT:
                                player.curr.poke_stats.add_battle(True)
                                logging.info("[Fight] Ended, fightitem")
                                time.sleep(SPEED_OF_TIME * 2)
                                audio.play(ctx.figure.map.song)
                                return player
                break

            time.sleep(SPEED_OF_TIME * 0.3)
            self.fightmap.show()
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
                    if not loser.handle_defeat(ctx, self.fightmap, winner):
                        break
                else:
                    break
            index += 1
        audio.play("xDeviruchi - Decisive Battle (End).mp3")

        xp = (
            sum(
                poke.lose_xp + max(0, poke.lvl() - winner.curr.lvl())
                for poke in loser.pokes
            )
            * loser.xp_multiplier
        )
        self.fightmap.declare_winner(winner, xp)

        winner.handle_win(ctx, loser)
        if winner.curr.player and winner.curr.add_xp(xp):
            self.fightmap.win_animation(winner)
            winner.curr.set_vars()
            winner.curr.learn_attack(ctx.with_overview(self.fightmap))
            evomap = EvoMap(self.fightmap.height, self.fightmap.width)
            evomap(ctx.with_overview(self.fightmap), winner.curr)

        if winner.curr.player:
            winner.curr.poke_stats.add_battle(True)
        else:
            loser.curr.poke_stats.add_battle(False)

        self.fightmap.death_animation(loser)
        self.fightmap.clean_up(winner)
        logging.info(
            "[Fight] Ended, %s(%s) won",
            winner.curr.name,
            "player" if winner.curr.player else "enemy",
        )
        audio.play(ctx.figure.map.song)
        return winner
