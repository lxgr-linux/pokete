import importlib.util
import os
import sys
import unittest
from pathlib import Path
from types import ModuleType, SimpleNamespace

# Prevent terminal-size crash during import on Windows
os.get_terminal_size = lambda *args, **kwargs: os.terminal_size((80, 24))


def stub_module(name: str, **attrs):
    mod = ModuleType(name)
    for key, value in attrs.items():
        setattr(mod, key, value)
    sys.modules[name] = mod
    return mod


# Stub the package structure needed for attack_process.py
pokete_pkg = stub_module("pokete")
pokete_pkg.__path__ = []

classes_pkg = stub_module("pokete.classes")
classes_pkg.__path__ = []

fight_pkg = stub_module("pokete.classes.fight")
fight_pkg.__path__ = []

# Stub imported dependencies that get_hp does not actually need
stub_module("pokete.classes.attack", Attack=type("Attack", (), {}))
stub_module("pokete.release", SPEED_OF_TIME=1)
stub_module("pokete.classes.fight.providers", Provider=type("Provider", (), {}))
stub_module("pokete.classes.fight.fightmap", FightMap=type("FightMap", (), {}))
stub_module("pokete.classes.attack_actions", AttackActions=type("AttackActions", (), {}))
stub_module(
    "pokete.classes.effects",
    effects=SimpleNamespace(confusion=type("confusion", (), {})),
)
stub_module("pokete.classes.poke", Poke=type("Poke", (), {}))

# Load only the attack_process.py module directly
attack_process_path = Path("src/pokete/classes/fight/attack_process.py").resolve()
spec = importlib.util.spec_from_file_location(
    "pokete.classes.fight.attack_process",
    attack_process_path,
)
attack_process_module = importlib.util.module_from_spec(spec)
sys.modules["pokete.classes.fight.attack_process"] = attack_process_module
spec.loader.exec_module(attack_process_module)

AttackProcess = attack_process_module.AttackProcess


def make_attacker(atc: int):
    return SimpleNamespace(atc=atc)


def make_defender(defense: int):
    return SimpleNamespace(defense=defense)


def make_attack(factor: float):
    return SimpleNamespace(factor=factor)


class TestAttackProcess(unittest.TestCase):
    def test_get_hp_returns_zero_on_miss(self):
        attacker = make_attacker(10)
        defender = make_defender(2)
        attack = make_attack(1)

        damage = AttackProcess.get_hp(
            attacker, defender, attack, random_factor=0, eff=1
        )

        self.assertEqual(damage, 0)

    def test_get_hp_has_minimum_damage_floor_of_4_on_hit(self):
        attacker = make_attacker(2)
        defender = make_defender(10)
        attack = make_attack(1)

        damage = AttackProcess.get_hp(
            attacker, defender, attack, random_factor=1, eff=1
        )

        self.assertEqual(damage, 4)

    def test_get_hp_keeps_higher_damage_values(self):
        attacker = make_attacker(12)
        defender = make_defender(2)
        attack = make_attack(1)

        damage = AttackProcess.get_hp(
            attacker, defender, attack, random_factor=1, eff=1
        )

        self.assertEqual(damage, 6)

    def test_get_hp_treats_zero_defense_as_one(self):
        attacker = make_attacker(5)
        defender = make_defender(0)
        attack = make_attack(1)

        damage = AttackProcess.get_hp(
            attacker, defender, attack, random_factor=1, eff=1
        )

        self.assertEqual(damage, 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)