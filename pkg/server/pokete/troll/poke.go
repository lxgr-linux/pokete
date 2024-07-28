package troll

import (
	"fmt"
	"github.com/lxgr-linux/pokete/server/pokete/fight"
	"github.com/lxgr-linux/pokete/server/resources"
)

func CheckPokes(protos resources.Pokes, pokes []fight.Poke) error {
	for _, poke := range pokes {
		err := CheckPoke(protos, poke)
		if err != nil {
			return fmt.Errorf("check failed for poke %s: %w", poke.Name, err)
		}
	}
	return nil
}

func CheckPoke(pokes resources.Pokes, poke fight.Poke) error {
	proto, ok := pokes[poke.Name]
	if !ok {
		return fmt.Errorf("poke %s not found", poke.Name)
	}

	if proto.Hp < poke.Hp {
		return fmt.Errorf("invalid hp")
	}

	return nil
}
