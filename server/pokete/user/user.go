package user

import (
    "github.com/lxgr-linux/pokete/server/bs_rpc"
)

type User struct {
    Name     string
    Position Position
    Client   *bs_rpc.Client // TODO: Maybe remove
}
