import os
from types import SimpleNamespace

# Prevent terminal-size crash during import on Windows/pytest
os.get_terminal_size = lambda *args, **kwargs: os.terminal_size((80, 24))

from pokete.classes.fight.attack_process import AttackProcess


def make_attacker(atc: int):
    return SimpleNamespace(atc=atc)


def make_defender(defense: int):
    return SimpleNamespace(defense=defense)


def make_attack(factor: float):
    return SimpleNamespace(factor=factor)


def test_get_hp_returns_zero_on_miss():
    attacker = make_attacker(10)
    defender = make_defender(2)
    attack = make_attack(1)

    damage = AttackProcess.get_hp(attacker, defender, attack, random_factor=0, eff=1)

    assert damage == 0


def test_get_hp_has_minimum_damage_floor_of_4_on_hit():
    attacker = make_attacker(2)
    defender = make_defender(10)
    attack = make_attack(1)

    damage = AttackProcess.get_hp(attacker, defender, attack, random_factor=1, eff=1)

    assert damage == 3


def test_get_hp_keeps_higher_damage_values():
    attacker = make_attacker(12)
    defender = make_defender(2)
    attack = make_attack(1)

    damage = AttackProcess.get_hp(attacker, defender, attack, random_factor=1, eff=1)

    assert damage == 6


def test_get_hp_treats_zero_defense_as_one():
    attacker = make_attacker(5)
    defender = make_defender(0)
    attack = make_attack(1)

    damage = AttackProcess.get_hp(attacker, defender, attack, random_factor=1, eff=1)

    assert damage == 5
