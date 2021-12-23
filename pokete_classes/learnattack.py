"""Contains the LearnAttack class"""

import time
import random
import scrap_engine as se
from pokete_general_use_fns import std_loop, liner
from .input import ask_bool, ask_ok
from .ui_elements import ChooseBox, Box
from .detail import Detail
from .color import Color
from .attack import Attack


class AttackInfo(Box):
    def __init__(self, attack, p_d, _map):
        obj = Attack(attack, p_d)
        desc_label = se.Text(liner(obj.desc, 40))
        super().__init__(4 + len(desc_label.text.split("\n")),
                         sorted(len(i) for i in
                            desc_label.text.split("\n")
                            + [obj.label_type.text,
                               obj.label_factor.text])[-1] + 4, obj.name,
                         "q:close")
        self.map = _map
        self.add_ob(obj.label_type, 2, 1)
        self.add_ob(obj.label_factor, 2, 2)
        self.add_ob(desc_label, 2, 3)

    def __enter__(self):  # Contextmanagement is fucking awesome!
        """Enter dunder for contextmanagement"""
        self.center_add(self.map)
        self.map.show()
        return self


class LearnAttack:
    """Lets a Pokete learn a new attack"""

    def __init__(self, poke, _map):
        self.map = _map
        self.poke = poke
        self.box = ChooseBox(6, 25, name="Attacks", info="1: Details")

    def __call__(self, _ev, p_d, attack=None):
        """Starts the learning process"""
        attacks = p_d.attacks
        if attack is None:
            pool = [i for i in attacks
                    if all(j in [i.name for i in self.poke.types]
                           for j in attacks[i]["types"])
                    and attacks[i]["is_generic"]]
            full_pool = [i for i in self.poke.inf["attacks"] +
                         self.poke.inf["pool"] + pool
                         if i not in self.poke.attacks
                         and attacks[i]["min_lvl"] <= self.poke.lvl()]
            if len(full_pool) == 0:
                return False
            new_attack = random.choice(full_pool)
        else:
            new_attack = attack
        if ask_bool(_ev, self.map,
                    f"{self.poke.name} wants to learn \
{attacks[new_attack]['name']}!"):
            if len(self.poke.attac_obs) != len(self.poke.attacks):
                self.poke.attacks[-1] = new_attack
            elif len(self.poke.attacks) < 4:
                self.poke.attacks.append(new_attack)
            else:
                self.box.add_c_obs([se.Text(f"{i + 1}: {j.name}", state=float)
                                    for i, j in enumerate(self.poke.attac_obs)])
                with self.box.center_add(self.map):
                    while True:
                        if _ev.get() in ["'s'", "'w'"]:
                            self.box.input(_ev.get())
                            self.map.show()
                            _ev.clear()
                        elif _ev.get() == "Key.enter":
                            self.poke.attacks[self.box.index.index] = new_attack
                            _ev.clear()
                            ask_ok(_ev, self.map,
                                   f"{self.poke.name} learned \
{attacks[new_attack]['name']}!")
                            _ev.clear()
                            break
                        elif _ev.get() == "'1'":
                            _ev.clear()
                            Detail(self.map.height, self.map.width)\
                                  (_ev, self.poke, False)
                            self.map.show(init=True)
                        elif _ev.get() in ["Key.esc", "'q'"]:
                            _ev.clear()
                            return False
                        std_loop(_ev)
                        time.sleep(0.05)
                self.box.remove_c_obs()
            self.poke.set_vars()
            return True
        return False

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
