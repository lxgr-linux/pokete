package user

import (
	"github.com/lxgr-linux/pokete/bs_rpc"
	"github.com/lxgr-linux/pokete/server/pokete/fight"
)

type User struct {
	Name     string         `json:"name"`
	Position Position       `json:"position"`
	Client   *bs_rpc.Client `json:"client"` // TODO: Maybe remove
	Pokes    []fight.Poke   `json:"pokes"`
}
