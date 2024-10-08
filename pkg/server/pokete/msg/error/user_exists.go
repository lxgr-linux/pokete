package error

import "github.com/lxgr-linux/pokete/bs_rpc/msg"

const UserDoesntExistType msg.Type = "pokete.error.user_doesnt_exit"

type UserDoesntExist struct {
	msg.BaseMsg
}

func (u UserDoesntExist) GetType() msg.Type {
	return UserDoesntExistType
}

func NewUserDoesntExist() UserDoesntExist {
	return UserDoesntExist{msg.BaseMsg{}}
}
