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
    Obmaps       resources.Obmaps   `json:"obmaps"`
    Maps         resources.Maps     `json:"maps"`
    NPCs         resources.NPCs     `json:"npcs"`
    Trainers     resources.Trainers `json:"trainers"`
    MapStations  resources.Stations `json:"map_stations"`
    Position     user.Position      `json:"position"`
    Users        []user.User        `json:"users"`
    GreetingText string             `json:"greeting_text"`
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
        resources2.GetObmaps(),
        resources2.GetMaps(),
        resources2.GetNPCs(),
        resources2.GetTrainers(),
        resources2.GetStations(),
        position,
        users.GetAllUsers(),
        greetingtext,
    }
}
