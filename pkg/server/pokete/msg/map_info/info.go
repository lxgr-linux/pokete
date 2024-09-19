package map_info

import (
	"github.com/lxgr-linux/pokete/bs_rpc/msg"
	"github.com/lxgr-linux/pokete/resources"
	"github.com/lxgr-linux/pokete/server/context"
	"github.com/lxgr-linux/pokete/server/pokete/user"
)

const InfoType msg.Type = "pokete.map.info"

type Info struct {
	msg.BaseMsg
	Assets       resources.Assets `json:"assets"`
	Position     user.Position    `json:"position"`
	Users        []user.User      `json:"users"`
	GreetingText string           `json:"greeting_text"`
}

func (i Info) GetType() msg.Type {
	return InfoType
}

func NewInfo(
	assets resources.Assets,
	position user.Position,
	users context.Users,
	greetingtext string,
) Info {
	return Info{
		msg.BaseMsg{},
		assets,
		position,
		users.GetAllUsers(),
		greetingtext,
	}
}
