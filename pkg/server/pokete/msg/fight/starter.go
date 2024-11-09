package fight

import (
	"github.com/lxgr-linux/pokete/bs_rpc/msg"
)

const StarterType msg.Type = "pokete.fight.starter"

type Starter struct {
	msg.BaseMsg
	Name string `json:"name"`
}

func (s Starter) GetType() msg.Type {
	return StarterType
}

func NewStarter(name string) Starter {
	return Starter{msg.BaseMsg{}, name}
}
