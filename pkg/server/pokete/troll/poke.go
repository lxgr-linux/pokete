package troll

import (
	"fmt"
	"github.com/lxgr-linux/pokete/resources/base"
	"github.com/lxgr-linux/pokete/server/pokete/fight"
)

func CheckPokes(protos map[string]base.Poke, pokes []fight.Poke) error {
	for _, poke := range pokes {
		err := CheckPoke(protos, poke)
		if err != nil {
			return fmt.Errorf("check failed for poke %s: %w", poke.Name, err)
		}
	}
	return nil
}

func CheckPoke(pokes map[string]base.Poke, poke fight.Poke) error {
	proto, ok := pokes[poke.Name]
	if !ok {
		return fmt.Errorf("poke %s not found", poke.Name)
	}

	if proto.Hp < poke.Hp {
		return fmt.Errorf("invalid hp")
	}

	return nil
}
