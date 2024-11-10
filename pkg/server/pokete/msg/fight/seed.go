package fight

import (
	"github.com/lxgr-linux/pokete/bs_rpc/msg"
)

const SeedType msg.Type = "pokete.fight.seed"

type Seed struct {
	msg.BaseMsg
	Seed uint32 `json:"seed"`
}

func (i Seed) GetType() msg.Type {
	return SeedType
}

func NewSeed(seed uint32) Seed {
	return Seed{msg.BaseMsg{}, seed}
}
