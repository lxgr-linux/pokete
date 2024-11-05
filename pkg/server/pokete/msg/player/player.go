package player

import (
	"github.com/lxgr-linux/pokete/bs_rpc/msg"
	"github.com/lxgr-linux/pokete/server/pokete/user"
)

const PlayerType msg.Type = "pokete.player.player"

type Player struct {
	msg.BaseMsg
	User user.User `json:"user"`
}

func (p Player) GetType() msg.Type {
	return PlayerType
}

func NewPlayer(user user.User) Player {
	return Player{msg.BaseMsg{}, user}
}
