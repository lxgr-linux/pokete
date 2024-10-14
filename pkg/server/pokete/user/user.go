package user

import (
	"github.com/lxgr-linux/pokete/bs_rpc"
	"github.com/lxgr-linux/pokete/server/pokete/poke"
)

type User struct {
	Name     string          `json:"name"`
	Position Position        `json:"position"`
	Client   *bs_rpc.Client  `json:"client"` // TODO: Maybe remove
	Pokes    []poke.Instance `json:"pokes"`
}
