package error

import "github.com/lxgr-linux/pokete/bs_rpc/msg"

const UserExistsType msg.Type = "pokete.error.user_exists"

type UserExists struct {
    msg.BaseMsg
}

func (u UserExists) GetType() msg.Type {
    return UserExistsType
}

func NewUserExists() UserExists {
    return UserExists{msg.BaseMsg{}}
}
