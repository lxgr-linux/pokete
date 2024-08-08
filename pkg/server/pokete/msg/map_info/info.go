package map_info

import (
	"github.com/lxgr-linux/pokete/bs_rpc/msg"
	"github.com/lxgr-linux/pokete/server/context"
	"github.com/lxgr-linux/pokete/server/pokete/user"
	"github.com/lxgr-linux/pokete/server/resources"
)

const InfoType msg.Type = "pokete.map.info"

type Info struct {
	msg.BaseMsg
	Assets       Assets        `json:"assets"`
	Position     user.Position `json:"position"`
	Users        []user.User   `json:"users"`
	GreetingText string        `json:"greeting_text"`
}

type Assets struct {
	Obmaps      resources.Obmaps         `json:"obmaps"`
	Maps        resources.Maps           `json:"maps"`
	NPCs        resources.NPCs           `json:"npcs"`
	Trainers    resources.Trainers       `json:"trainers"`
	Stations    resources.MapStations    `json:"stations"`
	Decorations resources.MapDecorations `json:"decorations"`
}

func (i Info) GetType() msg.Type {
	return InfoType
}

func NewInfo(
	resources2 *resources.Resources,
	position user.Position,
	users context.Users,
	greetingtext string,
) Info {
	return Info{
		msg.BaseMsg{},
		Assets{
			resources2.GetObmaps(),
			resources2.GetMaps(),
			resources2.GetNPCs(),
			resources2.GetTrainers(),
			resources2.GetMapStations(),
			resources2.GetMapDecorations(),
		},
		position,
		users.GetAllUsers(),
		greetingtext,
	}
}
