package positon

import (
    "github.com/lxgr-linux/pokete/server/bs_rpc/msg"
    "github.com/lxgr-linux/pokete/server/pokete/user"
)

const PositionUpdateType msg.Type = "pokete.position.update"

type Update struct {
    msg.BaseMsg
    user.User
}

func (u Update) GetType() msg.Type {
    return PositionUpdateType
}

func NewUpdate(user user.User) Update {
    return Update{msg.BaseMsg{}, user}
}
