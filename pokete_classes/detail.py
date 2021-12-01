import scrap_engine as se
from pokete_general_use_fns import std_loop
from .ui_elements import StdFrame2


class Detail(Deck):
    """Shows details about a Pokete"""

    def __init__(self):
        self.map = se.Map(height - 1, width, " ")
        self.name_label = se.Text("Details", esccode=Color.thicc)
        self.name_attacks = se.Text("Attacks", esccode=Color.thicc)
        self.frame = StdFrame2(17, self.map.width, state="float")
        self.attack_defense = se.Text("Attack:   Defense:")
        self.world_actions_label = se.Text("Abilities:")
        self.type_label = se.Text("Type:")
        self.initiative_label = se.Text("Initiative:")
        self.exit_label = se.Text("1: Exit")
        self.ability_label = se.Text("2: Use ability")
        self.line_sep1 = se.Square("-", self.map.width - 2, 1, state="float")
        self.line_sep2 = se.Square("-", self.map.width - 2, 1, state="float")
        self.line_middle = se.Square("|", 1, 10, state="float")
        # adding
        self.name_label.add(self.map, 2, 0)
        self.name_attacks.add(self.map, 2, 6)
        self.attack_defense.add(self.map, 13, 5)
        self.world_actions_label.add(self.map, 24, 4)
        self.type_label.add(self.map, 36, 5)
        self.initiative_label.add(self.map, 49, 5)
        self.exit_label.add(self.map, 0, self.map.height - 1)
        self.ability_label.add(self.map, 9, self.map.height - 1)
        self.line_sep1.add(self.map, 1, 6)
        self.line_sep2.add(self.map, 1, 11)
        self.frame.add(self.map, 0, 0)
        self.line_middle.add(self.map, round(self.map.width / 2), 7)

    def __call__(self, poke, abb=True):
        """Shows details"""
        ret_action = None
        self.add(poke, self.map, 1, 1, False)
        abb_obs = [i for i in poke.attac_obs
                   if i.world_action != ""]
        if abb_obs != [] and abb:
            self.world_actions_label.rechar("Abilities:"
                                            + " ".join([i.name
                                                        for i in abb_obs]))
            self.ability_label.rechar("2: Use ability")
        else:
            self.world_actions_label.rechar("")
            self.ability_label.rechar("")
        self.attack_defense.rechar(f"Attack:{poke.atc}\
{(4 - len(str(poke.atc))) * ' '}Defense:{poke.defense}")
        self.initiative_label.rechar(f"Initiative:{poke.initiative}")
        for obj, x, y in zip([poke.desc, poke.text_type], [34, 41], [2, 5]):
            obj.add(self.map, x, y)
        for atc, x, y in zip(poke.attac_obs, [1,
                                              round(self.map.width / 2) + 1,
                                              1,
                                              round(self.map.width / 2) + 1],
                                             [7, 7, 12, 12]):
            atc.temp_i = 0
            atc.temp_j = -30
            atc.label_desc.rechar(atc.desc[:int(width / 2 - 1)])
            atc.label_ap.rechar(f"AP:{atc.ap}/{atc.max_ap}")
            for label, _x, _y in zip([atc.label_name, atc.label_factor,
                                      atc.label_type_1, atc.label_type_2,
                                      atc.label_ap, atc.label_desc],
                                     [0, 0, 11, 16, 0, 0], [0, 1, 1, 1, 2, 3]):
                label.add(self.map, x + _x, y + _y)
        self.map.show(init=True)
        while True:
            if ev.get() in ["'1'", "Key.esc", "'q'"]:
                ev.clear()
                self.remove(poke)
                for obj in [poke.desc, poke.text_type]:
                    obj.remove()
                for atc in poke.attac_obs:
                    for obj in [atc.label_name, atc.label_factor, atc.label_ap,
                                atc.label_desc, atc.label_type_1,
                                atc.label_type_2]:
                        obj.remove()
                    del atc.temp_i, atc.temp_j
                return ret_action
            elif ev.get() == "'2'" and abb_obs != [] and abb:
                with ChooseBox(len(abb_obs) + 2, 25, name="Abilities",
                               c_obs=[se.Text(i.name)
                                      for i in abb_obs]).center_add(self.map)\
                        as box:
                    while True:
                        if ev.get() in ["'s'", "'w'"]:
                            box.input(ev)
                            self.map.show()
                            ev.clear()
                        elif ev.get() == "Key.enter":
                            ret_action = abb_obs[box.index.index].world_action
                            ev.set("'q'")
                            break
                        elif ev.get() in ["Key.esc", "'q'"]:
                            ev.clear()
                            break
                        std_loop(ev)
                        time.sleep(0.05)
            std_loop(ev)
            # This section generates the Text effect for attack labels
            for atc in poke.attac_obs:
                if len(atc.desc) > int((width - 3) / 2 - 1):
                    if atc.temp_j == 5:
                        atc.temp_i += 1
                        atc.temp_j = 0
                        if atc.temp_i == len(atc.desc) - int(width / 2 - 1)\
                                                       + 10:
                            atc.temp_i = 0
                            atc.temp_j = -30
                        atc.label_desc.rechar(atc.desc[atc.temp_i:
                            int(width / 2 - 1) + atc.temp_i])
                    else:
                        atc.temp_j += 1
            time.sleep(0.05)
            self.map.show()
