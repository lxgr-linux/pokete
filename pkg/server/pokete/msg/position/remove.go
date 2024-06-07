package position

import "github.com/lxgr-linux/pokete/bs_rpc/msg"

const RemoveType msg.Type = "pokete.position.remove"

type Remove struct {
    msg.BaseMsg
    UserName string `json:"user_name"`
}

func (r Remove) GetType() msg.Type {
    return RemoveType
}

func NewRemove(userName string) Remove {
    return Remove{msg.BaseMsg{}, userName}
}
